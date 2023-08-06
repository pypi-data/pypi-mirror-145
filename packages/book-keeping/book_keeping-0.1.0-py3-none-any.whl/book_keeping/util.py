import os
from pathlib import Path
from typing import Generator


def dual_filter(predicate, iterable):
    yes = [*filter(predicate, iterable)]
    no = [e for e in iterable if e not in yes]
    return yes, no


def markdown_link(uri, text=None):
    if text == None:
        text = uri
    return f"[{text}]({uri})"


def markdown_expand(uri, alttext=None):
    return f"!{markdown_link(uri, alttext)}"


def markdown_list(elements):
    return "\n".join(f"- {e}" for e in elements)


def apply(func, iterable):
    return (func(element) for element in iterable)


def is_img(path):
    return path.suffix in (".svg", ".png", ".jpeg")


def all_files(p: os.PathLike) -> Generator[Path, None, None]:
    for path, _, files in os.walk(p):
        rel_path = Path(path).relative_to(p)
        for name in files:
            yield rel_path / name
