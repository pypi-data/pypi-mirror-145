# paradigm-panes

Installable package that produces a paradigm for a given word, given a pointer to paradigm layouts and FST file. Originally
built for [itwêwina](https://itwewina.altlab.app/).

# PyPi Package

Latest version of the package posted to PyPi: [paradigm-panes 0.3.1](https://pypi.org/project/paradigm-panes/)

# Install

```
pip install paradigm-panes
```

# Developing

Developing is done and managed through [Python Poetry](https://python-poetry.org/) package manager.

To start development:

```
# Download the repo
git clone https://github.com/UAlbertaALTLab/paradigm-panes.git

# Set up virutal env
virtualenv venv --python=python3.9
source venv/bin/activate

# Install dependencies
poetry install

# Now cd into main directory and try out the package
cd paradigm_panes
python
    >>> import paradigm_panes
    >>> ...
```

# API Documentation:

- ## PaneGenerator()

  For successful execution, the package needs a link to resources as described below. To manage different links and use the panes generator more effectively, the package provides PaneGenerator class that allows managing settings and executing main functionality:

  ```
  >>> pane_generator = paradigm_panes.PaneGenerator()
  ```

  The class itself does not take any variables.

- ## generate_pane()

  ```
  >>> paradigm = pane_generator.generate_pane(lemma, paradigm_type, size: Optional)
  ```

  This function is a core functionality of the package. Once the [resources are specified](#settings-specification-functions), this function generates the pane according to the specification given. \
   If the translations are not found in the FST file, some of the inflections will be indicated as missing. The resulted paradigm class is serialized and returned as JSON.

  ### Parameters:

  > lemma(str) - base wordform to be inflected

  > paradigm_type(str) - specification of the paradigm type of the word. Ex. "NA".

  > size(str) - optional size of the pane to be returned. Currently supports "base", and "full". If the specified size is not found, overrides with default option.

- ## all_analysis_template_tags()

  ```
  >>> paradigm = pane_generator.all_analysis_template_tags(paradigm_type)
  ```

  An additional functionality that returns all analysis template tags.

  ### Parameters:

  > paradigm_type(str) - specification of the paradigm type of the word. Ex. "NA".

  > tag_style(str) - style of tags to return.

  Specify tag style through [settings](#settings-specification-functions)

# Usage and Configuration

Import the library:

```
>>> import paradigm_panes
```

Create PaneGenerator and specify path to FST file and layouts resources:

```
>>> pg = paradigm_panes.PaneGenerator()
>>> pg.set_layouts_dir("/home/ubuntu/paradigm_panes/resources/layouts")
>>> pg.set_fst_filepath("/home/ubuntu/paradigm_panes/resources/fst/crk-strict-generator.hfstol")
```

Pass lemma, paradigm type, and optional size to generate a pane:

```
>>> lemma = "amisk"
>>> p_type = "NA"
>>> paradigm = pg.generate_pane(lemma, p_type)

>>> p_size = "full"
>>> full_paradigm = pg.generate_pane(lemma, p_type, p_size)
```

## Settings specification functions:

- `set_layouts_dir(path)` specifies a location of a directory with paradigm layouts that are relevant for current paradigm generation.

- `set_fst_filepath(path)` specifies FST file location with layout translation that are relevant for current paradigm generation.

- `set_tag_style(path)` specifies template rendering type for all_analysis_template_tags function.

  Available tag styles:

  1.  "Plus"
  2.  "Bracket"

The generator must specify both locations (FST, layouts) before generating a paradigm.

Size is optional to paradigm generation; by default a base size (or first available) will be used.

# Testing

To run the tests you need to install required dependencies, it is easier by using a virtual environment like this:

```
>>> # Set up virutal env
>>> virtualenv venv --python=python3.9
>>> source venv/bin/activate
>>>
>>> # Install dependencies
>>> poetry install
```

Once the dependencies are installed you can run tests by calling pytest.

```
>>> pytest
```

# Release

Package version number is sorted in pyproject.toml. With every release to PyPi the version needs to be updated. \
Build the package from the main directory before publishing it:

```
>>> poetry build
```

To publish to Test PyPi use poetry and enter credentials associated with Test PyPi account

```
>>> poetry publish -r testpypi
```

To publish to real PyPi use poetry and enter credentials associated with PyPi

```
>>> poetry publish
```

All relevant package specifications and dependencies are managed in `pyproject.toml` file.
