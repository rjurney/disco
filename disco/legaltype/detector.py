"""Functions to help clean & normalize business names.

See http://www.unicode.org/reports/tr15/#Normalization_Forms_Table for details
on Unicode normalization and the NFKD normalization used here.

Basic usage:

>> terms = prepare_terms()
>> basename("Daddy & Sons, Ltd.", terms, prefix=True, middle=True, suffix=True)
Daddy & Sons

"""

import functools
from typing import Dict, List, Union

from disco.legaltype.automaton import Matcher
from disco.utils import has_chinese, normalize_terms, split_text, strip_head, strip_tail

matcher = Matcher()
matcher.build()


@functools.lru_cache(1000)
def _search(
    name: str, suffix: bool = True, prefix: bool = True
) -> Dict[str, Union[List[str], str]]:
    "return cleaned base version of the business name"

    chinese_in_name = has_chinese(name)

    name_stripped = strip_head(strip_tail(name))
    nparts = split_text(name_stripped)

    nnparts = list(normalize_terms(nparts))

    legaltypes = []
    countries = []

    # the condition is here for performance optimization (if it was omitted the code would work the same)
    if len(nnparts) > 0 and (
        (suffix and matcher.has_pattern(nnparts[-1]))
        or (prefix and matcher.has_pattern(nnparts[0]))
    ):
        sorted_matches = sorted(matcher.get_matches(nnparts), key=lambda m: -m.end)

        if suffix:
            for match in sorted_matches:
                if match.end == len(nparts):
                    countries += match.value["countries"]
                    legaltypes += match.value["types"]
                    del nparts[-len(match.elems) :]
                else:
                    break

        if prefix:
            offset = 0
            for match in reversed(sorted_matches):
                if match.start == offset:
                    offset += len(match.elems)
                    countries += match.value["countries"]
                    legaltypes += match.value["types"]
                else:
                    break

            del nparts[:offset]

    basename = strip_head(
        strip_tail("".join(nparts) if chinese_in_name else " ".join(nparts))
    )

    return {
        "countries": countries,
        "types": legaltypes,
        "basename": basename,
    }


def search(
    name: str, suffix: bool = True, prefix: bool = True
) -> Dict[str, Union[List[str], str]]:
    result = _search(name, suffix=suffix, prefix=prefix)
    result["countries"] = sorted(list(set(result["countries"])))
    result["types"] = sorted(list(set(result["types"])))
    return result


def basename(name: str, suffix: bool = True, prefix: bool = True) -> str:
    return _search(name, prefix=prefix, suffix=suffix)["basename"]


def legaltype(name: str, suffix: bool = True, prefix: bool = True) -> List[str]:
    return sorted(list(set(_search(name, prefix=prefix, suffix=suffix)["types"])))


def country(name: str, suffix: bool = True, prefix: bool = True) -> List[str]:
    return sorted(list(set(_search(name, prefix=prefix, suffix=suffix)["countries"])))
