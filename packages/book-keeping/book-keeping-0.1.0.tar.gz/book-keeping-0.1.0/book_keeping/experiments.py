import functools
import inspect
import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List

from book_keeping.ids import random_id
from book_keeping.tee import stdout_to_
from book_keeping.util import (all_files, apply, dual_filter, is_img,
                               markdown_expand, markdown_link, markdown_list)

__ME = Path(__file__)


def pretty_dict(_dict: Dict) -> str:
    max_k = max(len(k) for k in _dict.keys())
    pretty = "dict(\n"
    for k, v in _dict.items():
        pretty += f"   {k: >{max_k}}={str(v).strip()},\n"
    return pretty + ")"


def generate_report(
    _id: str, summary: Dict, config: Dict, artefacts: List[Path], _file: Path
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    code = _file.read_text()

    plots, artefacts = dual_filter(is_img, artefacts)
    plots = "\n".join(apply(markdown_expand, plots))
    artefacts = markdown_list(apply(markdown_link, artefacts))

    template = (__ME.parent / "template.md").read_text()
    return template.format(
        now=now, title=_id, summary=pretty_dict(summary),
        config=pretty_dict(config), plots=plots, artefacts=artefacts, code=code
    )


class Experiment:
    def __init__(
        self, root: os.PathLike = "experiments", project: str = None,
        _id: str = None
    ) -> None:
        _dir = Path(root) / (project if project else "")
        self._id = _id if _id else random_id()
        while (_dir / self._id).exists():
            self._id = random_id()
        self._dir = _dir / self._id
        self._dir.mkdir(exist_ok=False, parents=True)
        self._experiment_file = Path(inspect.stack()[1].filename)

    def file(self, name: str):
        return self._dir / name

    def record(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **config):
            with stdout_to_(self.file("log")):
                print(f"Starting Experiment: {self._id}")
                summary = func(*args, **config)
            artefacts = [*all_files(self._dir)]
            report = generate_report(
                self._id, summary, config, artefacts, self._experiment_file)
            with open(self.file(f"{self._id}.md"), "w") as f:
                f.write(report)
        return wrapper
