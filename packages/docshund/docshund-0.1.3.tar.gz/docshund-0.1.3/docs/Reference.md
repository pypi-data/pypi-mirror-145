## *Class* `Section`


A Section represents the content of a single Python entity.

This includes classes, functions, and class methods.


## *Function* `__init__(self, title: str = None, contents=None) -> None`


Create a new Section with a title and content string.

### Arguments
> - **title** (`str`: `None`): The title of the section. Optional
> - **contents** (`str`: `None`): The contents of the section. Optional

### Returns
    None



## *Function* `to_markdown(self) -> str`


Convert the section to Markdown.

### Arguments
    None

### Returns
> - **str** (`None`: `None`): A markdown representation of the section.



## *Class* `Report`


A complete report of a Python file, containing all Sections.



## *Function* `__init__(self, sections: List[Section] = None) -> None`


Create a new Report with a list of Sections.

### Arguments
> - **sections** (`List[Section]`: `None`): An optional list of sections to
        include in the report.

### Returns
    None



## *Function* `to_markdown(self) -> str`


Convert the entire report to Markdown.

### Arguments
    None

### Returns
> - **str** (`None`: `None`): A markdown representation of the report.



## *Function* `add_section(self, section: Section, pos: int = -1) -> None`


Add a section to the report, optionally at a given position.

### Arguments
> - **section** (`Section`: `None`): The section to insert
> - **pos** (`int`: `-1`): The index at which to insert the new section. If
        none is provided, the default is to add the section to the         end of the report.

### Returns
    None



## *Class* `Docshund`


The high-level class for generating documentation.

This is what you should call if you are trying to generate documentation programmatically (or from the command line).


## *Function* `__init__(self, **kwargs) -> None`


Create a new Docshund documentation engine.

### Arguments
> - **language** (`None`: `None`): The language to use. This is currently not used,
        but will ultimately provide support for different programming         languages than Python.
> - **str** (`None`: `None`): "    "): The default indentation level for the file.
        Defaults to four spaces.

### Returns
    None



## *Function* `_get_indent_level(self, line: str) -> int`


Return the indent level, based upon the left spacing.

### Arguments
> - **line** (`str`: `None`): The line to guess indentation for.

### Returns
> - **int** (`None`: `None`): The guessed indentation level of the line of code



## *Function* `_clean_docstring(self, docstring: str) -> List[str]`


Clean a docstring, reducing indentation where necessary.

### Arguments
> - **docstring** (`str`: `None`): The complete docstring from the code src

### Returns
> - **List[str]** (`None`: `None`): A list of strings, one for each line of the cleaned
        docstring output.



## *Function* `parse_docstring(self, docstring: str) -> str`


Parse a single docstring, converting from original text to Markdown.

### Arguments
> - **docstring** (`str`: `None`): The docstring from the code src

### Returns
> - **str** (`None`: `None`): The parsed markdown output



## *Function* `parse_document(self, document: str) -> str`


Parse a full document, and generate markdown.

### Arguments
> - **document** (`str`: `None`): The document to parse; i.e. contents of src file

### Returns
> - **str** (`None`: `None`): The documentation, in markdown form


