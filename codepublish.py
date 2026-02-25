import re
import subprocess
from genericpath import exists
from glob import glob
from os import chdir, getcwd, listdir, mkdir
from os.path import abspath, basename, isdir, join
from typing import Iterator

from pygments import highlight
from pygments.formatters import LatexFormatter
from pygments.lexers import get_lexer_for_filename

formatter = LatexFormatter(linenos=False, texcomments=False, mathescape=True)
"""pygments code formatter"""

publish_file_name = "publish.txt"

skip_file_name = "skip.txt"

skip = [
    ".vs",
    "out",
    "__pycache__",
    "publish",
    "CMakeLists.txt",
    skip_file_name,
    publish_file_name,
]
"""subfolders/files to skip"""

packages = [
    "{fancyvrb}",
    "{color}",
    "[utf8]{inputenc}",
    "[breakable]{tcolorbox}",
    "[a4paper, portrait, margin=2cm]{geometry}",
    "{pgf}",
    "{float}",
]
"""latex packages used by the document"""

doc_class = "{report}"
"""document class"""

document_parts = {
    0: "chapter",
    1: "section",
    2: "subsection",
    3: "subsubsection",
    4: "paragraph",
    5: "subparagraph",
}
"""document part types"""

default_part = "subparagraph"
"""default document part type"""


import_extensions = [".tex", ".latex"]
"""inserted into the final tex file verbatim"""

code_extensions = [".h", ".hpp", ".cpp", ".py"]
"""processed by pygments before inserted into a box, the title includes the extension"""

output_extentions = [".txt", ".log"]
"""formatted, the title does not include the extension"""

diagram_extensions = [".puml", ".plantuml"]
"""encapsulated by a plantuml section before inserted into a box, the title does not include the extension"""

figure_extensions = [".pgf"]
"""Added as an included figure"""


def document_class() -> str:
    """
    returns the string literal for the latex document class
    """
    return "\\documentclass" + doc_class


def document_packages() -> str:
    """
    returns the string literal for the latex package imports
    """
    header = ""
    for package in packages:
        header += f"\n\\usepackage{package}"
    return header


def document_styles() -> str:
    """
    returns the string literal for the latex style definitions
    """
    return formatter.get_style_defs()


def document_title(title: str, subtitle: str, author: str) -> str:
    """
    returns the string literal for the latex title
    """
    return f"\\title{{%\n{title} \\\\\n\\large {subtitle} \\\\}}\n\\author{{{author}}}\n\\date{{\\today}}\n"


def document_start() -> str:
    """
    returns the string literal for the latex document start
    """
    return "\\begin{document}\n\\maketitle\n"


def document_end() -> str:
    """
    returns the string literal for the latex document end
    """
    return "\\end{document}"


def document_part(level: int) -> str:
    """
    returns the document part type for the specified level
    """
    return document_parts.get(level, default_part)


def read_file(filename: str, prepend: str = "\n") -> str:
    """
    returns the contents of the file
    """
    file = open(filename, "r")
    content = file.read()
    file.close()
    return prepend + content


def remove_number(filename: str) -> str:
    """
    removes a number of the format '[xxx]' from the start of the filename
    """
    search = re.search(r"^(?:\[[0-9]*\])?(?P<name>.+)$", basename(filename))
    return search["name"]  # type: ignore


def remove_number_and_extension(filename: str) -> str:
    """
    removes the file extension as well as a number of the format '[xxx]' from the start of the filename
    """
    search = re.search(r"^(?:\[[0-9]*\])?(?P<name>.+)\..*$", basename(filename))
    return search["name"]  # type: ignore


def extension_match(filename: str, extensions: list[str]) -> bool:
    """
    checks if the extension of filename mach any of the provided extensions
    """
    name = basename(filename)
    parts = name.split(".")
    if len(parts) > 0:
        extension = "." + parts[-1]
        return extension in extensions
    else:
        return "" in extensions


def publish_code(filename: str) -> str:
    """
    process a code file
    """
    title = remove_number(filename)
    lexer = get_lexer_for_filename(filename)

    code = read_file(filename)

    return f"\\begin{{tcolorbox}}[title={title},width=\\textwidth,left*=10mm,breakable]\n{highlight(code, lexer, formatter)}\n\\end{{tcolorbox}}"


def publish_output(filename: str) -> str:
    """
    process an output file
    """
    title = remove_number_and_extension(filename)
    lexer = get_lexer_for_filename(filename)

    content = read_file(filename)

    return f"\\begin{{tcolorbox}}[title={title},width=\\textwidth,left*=10mm,breakable]\n{highlight(content, lexer, formatter)}\n\\end{{tcolorbox}}"


def publish_diagram(filename: str) -> str:
    """
    process a diagram file
    """
    title = remove_number_and_extension(filename)
    content = read_file(filename)
    plantproc = subprocess.run(
        ["plantuml", "--pipe", "-tlatex:nopreamble"],
        input=content,
        text=True,
        capture_output=True,
    )

    return f"\\begin{{figure}}[H]\n\\centering\n{plantproc.stdout}\n\\caption{{{title}}}\n\\end{{figure}}"


def publish_figure(filename: str) -> str:
    """
    publish a pgf figure
    """
    title = remove_number_and_extension(filename)
    return f"\\begin{{figure}}[H]\n\\centering\n\\input{{{abspath(filename)}}}\n\\caption{{{title}}}\n\\end{{figure}}"


def import_document(filename: str) -> str:
    """
    process an import file
    """
    return read_file(filename)


def publish_folder(dir: str, level: int = 0) -> Iterator[str]:
    """
    process a folder
    """
    heading = document_part(level)
    name = remove_number(basename(dir.rstrip("/\\")))
    yield f"\\{heading}*{{{name}}}\n"

    for section in get_folder_content(dir, level):
        yield section


def publish_item(path: str, level: int) -> Iterator[str]:
    """
    process any file based on its extension
    """
    if extension_match(path, import_extensions):
        yield import_document(path)
    elif extension_match(path, code_extensions):
        yield publish_code(path)
    elif extension_match(path, diagram_extensions):
        yield publish_diagram(path)
    elif extension_match(path, output_extentions):
        yield publish_output(path)
    elif extension_match(path, figure_extensions):
        yield publish_figure(path)
    elif isdir(path):
        for content in publish_folder(path, level + 1):
            yield content
    else:
        yield ""  # ignore file


def get_sub_folders(dir: str, local_skip: list[str]) -> Iterator[str]:
    for subdir in glob(f"{dir}/*/"):
        dirname = basename(subdir.strip("/\\"))
        if not (dirname in skip or dirname in local_skip):
            yield subdir.strip("/\\")


def get_folder_skip(dir: str) -> list[str]:
    if exists(f"{dir}/{skip_file_name}"):
        sfile = open(f"{dir}/{skip_file_name}")
        names = sfile.readlines()
        sfile.close()
        result = []
        for name in names:
            result.append(name.strip())
        return result
    else:
        return []


def get_folder_items_auto(
    dir: str, extensions: list[str], include_subfolders: bool = True
) -> list[str]:
    content = []

    local_skip = get_folder_skip(dir)
    print(local_skip)

    for file in listdir(dir):
        if file in skip or file in local_skip:
            continue
        for extension in extensions:
            if file.endswith(extension):
                content.append(join(dir, file))
                break
        # content += glob(f'{dir}\\*{extension}')
    if include_subfolders:
        content += get_sub_folders(dir, local_skip)

    return sorted(content)


def get_folder_items_manual(dir: str) -> tuple[bool, list[str]]:
    if exists(f"{dir}/{publish_file_name}"):
        pfile = open(f"{dir}/{publish_file_name}")
        result = []
        for line in pfile.readlines():
            file = line.strip()
            if not (len(file) == 0) and exists(f"{dir}/{file}"):
                result.append(f"{dir}/{file}")
        pfile.close()
        return True, result
    else:
        return False, []


def get_folder_items(
    dir: str, extensions: list[str], include_subfolders: bool = True
) -> list[str]:
    manual, result = get_folder_items_manual(dir)
    if manual:
        return result
    else:
        return get_folder_items_auto(dir, extensions, include_subfolders)


def get_folder_content(dir: str, level: int = -1) -> Iterator[str]:

    extensions = import_extensions + diagram_extensions
    if level >= 0:
        extensions += code_extensions + output_extentions

    for item in get_folder_items(dir, extensions):
        print(f'processing "{item}"')
        for content in publish_item(item, level):
            yield content

    yield "\n"


def remove_spaces(s: str) -> str:
    return re.sub(r"\s", "", s)


def publish_assignment(
    dir: str, title: str, subtitle: str, author: str
) -> tuple[str, str]:
    out_dir = f"{dir}/publish"
    if not (exists(out_dir)):
        mkdir(out_dir)
    out_path = f"{remove_spaces(title)}.tex"
    out_file = open(f"{out_dir}/{out_path}", mode="w")
    out_file.write(document_class())
    out_file.write(document_packages())
    out_file.write(document_styles())
    out_file.write(document_title(title, subtitle, author))
    out_file.write(document_start())

    for section in get_folder_content(dir):
        out_file.write(section)

    out_file.write(document_end())
    out_file.close()
    return out_path, out_dir


def publish_assignment_to_pdf(
    dir: str, title: str, subtitle: str, author: str
) -> tuple[str, str]:
    file, pub_dir = publish_assignment(dir, title, subtitle, author)
    wd = getcwd()
    chdir(pub_dir)
    subprocess.run(["lualatex", f'"{file}"'])
    chdir(wd)
    file = file.removesuffix(".tex") + ".pdf"
    return file, pub_dir


if __name__ == "__main__":
    file, dir = publish_assignment_to_pdf(
        "testassignment", "Test Assignment", "C++", "Name Surname (12345678)"
    )
    print(f"{dir}/{file}")
