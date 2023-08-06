"""
    Planning to make it a central place to run paradigm generation
"""
# import settings

from pathlib import Path
from typing import (Collection, Dict, Optional)

from .generation import default_paradigm_manager
from .manager import ParadigmManager
from .panes import Paradigm
from . import settings
import json

class PaneGenerator:
    def generate_pane(self, lemma: str, paradigm_type: str, specified_size: Optional[str] = None) -> Dict[str, any]:
        """
        Validate given parameters and set options (settings) and return serialized pane of the paradigm"""
        if (settings.is_setup_complete()):
            if paradigm_type is not None:
                paradigm = self._crete_paradigm(lemma, paradigm_type, specified_size)

                serialized_paradigm = self.serialize_paradigm(paradigm)

                return serialized_paradigm
            else:
                raise Exception("Paradigm layout specification is missing.")
        else:
            raise Exception("FST and Layouts resources are not configured correctly.")

    def _crete_paradigm(self, lemma: str, paradigm_type: str, specified_size: Optional[str] = None) -> Paradigm:
        """
        Create the paradigm as a built-in type and return.
        Check given optional size, and use default otherwise.
        """
        paradigm_manager = default_paradigm_manager()
        sizes = list(paradigm_manager.sizes_of(paradigm_type))
        if "basic" in sizes:
            default_size = "basic"
        else:
            default_size = sizes[0]

        if len(sizes) <= 1:
            size = default_size
        else:
            size = specified_size
            if size not in sizes:
                size = default_size

        paradigm = self.paradigm_for(paradigm_manager, paradigm_type, lemma, size)

        return paradigm


    def all_analysis_template_tags(self, paradigm_type: str) -> Collection[tuple]:
        """
        Return the set of all analysis templates in layouts of paradigm_name

        If a paradigm has two sizes, one with template `${lemma}+A` and the
        other with both `${lemma}+A` and `X+${lemma}+B`, then this function will
        return {((), ("+A",)), (("X+",), ("+B",)}.

        Note that these analyses are meant to be inputs to a generator FST for
        building a paradigm table, not the results of analyzing some input
        string.
        """
        if (settings.is_setup_complete()):
            if paradigm_type is not None:
                pg = default_paradigm_manager()
                all_template_tags = pg.all_analysis_template_tags(paradigm_type)
                return all_template_tags
            else:
                raise Exception("Paradigm layout specification is missing.")
        else:
            raise Exception("FST and Layouts resources are not configured correctly.")

    def paradigm_for(self, paradigm_manager: ParadigmManager, paradigm_type: str, fst_lemma: str, paradigm_size: str) -> Optional[Paradigm]:
        """
        Returns a paradigm for the given wordform at the desired size.

        If a paradigm cannot be found, None is returned
        """

        if paradigm_type:
            if paradigm := paradigm_manager.paradigm_for(paradigm_type, fst_lemma, paradigm_size):
                return paradigm

        return None

    def set_fst_filepath(self, path: str) -> None:
        """
        Set fst resource location
        """
        settings.set_fst_filepath(path)

    def set_layouts_dir(self, path: str) -> None:
        """
        Set layouts resources location
        """
        settings.set_layouts_dir(path)

    def set_tag_style(self, style: str) -> None:
        """
        Set tag for all templates rendering
        """
        settings.set_tag_style(style)

    def serialize_paradigm(self, paradigm: Paradigm) -> Dict[str, any]:
        """
        Serializes a Paradigm object as a dictionary

        :param paradigm: the paradigm to be serialized
        :return: dictionary representation
        """
        panes = []

        if paradigm is None:
            return {"panes": panes}

        for pane in (paradigm.panes or []):

            tr_rows = []
            for row in (pane.rows or []):
                if row.is_header:
                    tr_rows.append({
                        "is_header": True,
                        "label": row.fst_tags,
                        "cells": []
                    })
                else:
                    cells = []
                    for cell in (row.cells or []):
                        cell_data = {
                            "should_suppress_output": cell.should_suppress_output,
                            "is_label": cell.is_label,
                            "is_inflection": cell.is_inflection,
                            "is_missing": cell.is_missing,
                            "is_empty": cell.is_empty
                        }

                        if cell_data["is_label"]:
                            cell_data["label_for"] = cell.label_for
                            cell_data["label"] = cell.fst_tags

                            if type(cell_data["label_for"]) != str:  # if cell.label_for was never instantiated
                                cell_data["label_for"] = ""
                            if cell_data["label_for"] == "row":
                                cell_data["row_span"] = cell.row_span

                        elif cell_data["is_inflection"] and not cell_data["is_missing"]:
                            cell_data["inflection"] = cell.inflection

                        cells.append(cell_data)

                    tr_rows.append({
                        "is_header": False,
                        "label": None,  # shouldn't be used.
                        "cells": cells
                    })

            panes.append({"tr_rows": tr_rows})

        return {"panes": panes}
