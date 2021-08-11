import re
import unicodedata
from functools import lru_cache
from typing import List

from disco.non_nfkd_map import NON_NFKD_MAP

tail_removal_rexp = re.compile(r"[^\.\w]+$", flags=re.UNICODE)
head_removal_rexp = re.compile(r"^[^\.\w]+", flags=re.UNICODE)
RE_PUNCT = re.compile(r"[.,-]", flags=re.UNICODE)

RE_IS_CHINESE = re.compile(
    r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]", re.UNICODE
)


@lru_cache(maxsize=100000)
def remove_accents(t: str) -> str:
    """based on https://stackoverflow.com/a/51230541"""
    nfkd_form = unicodedata.normalize("NFKD", t.casefold())
    return "".join(
        NON_NFKD_MAP[c] if c in NON_NFKD_MAP else c
        for part in nfkd_form
        for c in part
        if unicodedata.category(part) != "Mn"
    )


def has_chinese(txt: str) -> bool:
    cjk_characters = RE_IS_CHINESE.search(txt)
    return cjk_characters is not None


def split_text(txt: str) -> List[str]:
    return list(txt) if has_chinese(txt) else txt.split()


def strip_punct(t: str) -> str:
    return t.replace(".", "").replace(",", "").replace("-", "")


def normalize_terms(terms: List[str]) -> List[str]:
    "normalize terms"
    return (strip_punct(remove_accents(t)) for t in terms)


def strip_tail(name: str) -> str:
    "get rid of all trailing non-letter symbols except the dot"
    match = tail_removal_rexp.search(name)
    if match is not None:
        name = name[: match.span()[0]]
    return name


def strip_head(name: str) -> str:
    "get rid of all non-letter symbols except the dot at the beginning"
    match = head_removal_rexp.search(name)
    if match is not None:
        name = name[match.span()[1] :]
    return name


def normalized(text: str) -> str:
    "caseless Unicode normalization"
    return remove_accents(text)


def find_sublist(mylist: List, pattern: List) -> bool:
    """
    Inspired by https://stackoverflow.com/questions/10106901/elegant-find-sub-list-in-list
    """
    assert len(pattern) > 0 and len(mylist) > 0
    if len(pattern) > len(mylist):
        return False

    for i in range(len(mylist) - len(pattern) + 1):
        if mylist[i] == pattern[0] and mylist[i : i + len(pattern)] == pattern:
            # matches.append(pattern)
            return True
    return False
