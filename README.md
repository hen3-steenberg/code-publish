# Code Publish Script

A python script for easily generating syntax highlighted pdf's

An [example pdf](./testassignment/publish/TestAssignment.pdf) is generated for the [test assignment](./testassignment)

## Dependencies
* pygments python package (use: pip install pygments)
* LaTex, This script was tested using the MikTex implementation of LaTex. It is available to download from [MikTex](https://miktex.org/download)

### Optional
* plantuml latex package dependencies. Instructions available at [Plant Uml](https://koppor.github.io/plantuml/)

## Features
1. Syntax highlight code from (.h .hpp .cpp) files
2. Include text with line numbers from (.txt .log) files
3. Insert the content from any (.tex .latex) files
4. Render plantuml diagrams from (.puml .plantuml) files
5. Creates captions based on file or folder names
    * strips numbers in the format `[xxx]` from the front of file names
6. Creates a document structure based on the the folder structure
    * renders content in lexical order (prepend numbers to files and folders in the format `[xxx]` to control the rendering order.)
7. Skip publishing any files in `skip.txt`
8. Publish only files in the order that they appear in `publish.txt`
    * If there is a `publish.txt` file, the behaviour for 6. and 7. is ignored.

## Usage
* Copy the script into your project
* call
```python 
    publish_assignment(directory: str, title:str, subtitle:str, author:str)
```
* This will create a subdirectory `publish` and the output file `publish/{remove_spaces(title)}.tex}`
* To generate a .pdf file run `lualatex lualatex --shell-escape outfile.tex` in a shell/terminal
    - The `--shell-escape` is needed for rendering plant uml diagrams. If you do not have a diagram this flag should be omitted.
### Alternatively
call
```python
    publish_assignment_to_pdf(dir: str, title:str, subtitle:str, author:str)
```
* This will automatically call puplish_assignment before invoking lualatex automatically.

## Customization
At the top of the `codepuplish.py` file a lot of variables are declared which determines the behaviour of the script
* `formatter` This variable controls how formatted code is diplayed
    ````python
    formatter = LatexFormatter(linenos = True, texcomments = True, mathescape = True)
    ```` 
    - A full list is available at [LatexFormatter](https://pygments.org/docs/formatters/#LatexFormatter)
* `publish_file_name` The name of file containing the publish order for the current directory
    ```python
    publish_file_name = "publish.txt"
    ```
* `skip_file_name` The name of the file containing files/directories to skip for the current directory
    ```python
    skip_file_name = "skip.txt"
    ```
* `skip` A list of files / directories to always ignore
    ```python
    skip = [".vs", "out", "__pycache__", "publish", skip_file_name, publish_file_name]
    ```
* `packages` A list of latex packages that should be included with the `\usepackage` statement
    ```python
    packages = ["{fancyvrb}", "{color}", "[utf8]{inputenc}", "[breakable]{tcolorbox}", "[a4paper, portrait, margin=2cm]{geometry}", "{plantuml}"]
    ```
* `doc_class` the document class to use
    ```python
    doc_class = '{report}'
    ```
* `document_parts` A dictionary containing the header types for different levels (The top level is 0)
    ```python
    document_parts = {
        0: "chapter",
        1: "section",
        2: "subsection",
        3: "subsubsection",
        4: "paragraph",
        5: "subparagraph"
    }
    ```
* `default_part` The header type to use if there is no value defined for a level (or the level becomes too large)
    ```python
    default_part = "subparagraph"
    ```
* `import_extensions` A list of file extensions which text should be copied to the output file verbatim
    ```python
    import_extensions = [".tex", ".latex"]
    ```
* `code_extensions` A list of file extensions which should be interpreted as code
    ```python
    code_extensions = [".h", ".hpp", ".cpp"]
    ```
* `output_extentions` A list of extensions that should be interpreted as output
    ```python
    output_extentions = [".txt", ".log"]
    ```
* `diagram_extensions` A list of file extensions that should be interpreted as diagrams
    ```python
    diagram_extensions = [".puml", ".plantuml"]
    ```

