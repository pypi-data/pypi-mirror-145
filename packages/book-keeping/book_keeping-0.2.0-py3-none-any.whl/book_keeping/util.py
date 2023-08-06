import os
from pathlib import Path
from typing import Dict, Generator
from collections.abc import Mapping


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


def pretty_dict(_dict: Dict, prefix="") -> str:
    spacer = "   "
    max_k = max(len(k) for k in _dict.keys())
    pretty = "dict(\n"
    for k, v in _dict.items():
        k = f"{k: >{max_k}}"
        v = pretty_dict(v, prefix=" "*(max_k+1) + spacer) \
            if isinstance(v, Mapping) else f"{str(v).strip()}"
        pretty += f"{spacer}{k}={v},\n"
    pretty += ")"

    return "\n".join((prefix if i > 0 else "") + line
                     for i, line in enumerate(pretty.split("\n")))
