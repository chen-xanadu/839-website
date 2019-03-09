from dataclasses import dataclass
from typing import List


@dataclass
class Instance:
    term: List[str]
    label: bool
    pre: List[str]
    post: List[str]
    term_pos: List[str]
    pre_pos: List[str]
    post_pos: List[str]
    file_idx: int = -1
