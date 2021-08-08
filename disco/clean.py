"""Functions to help clean & normalize business names.

See http://www.unicode.org/reports/tr15/#Normalization_Forms_Table for details
on Unicode normalization and the NFKD normalization used here.

Basic usage:

>> terms = prepare_terms()
>> basename("Daddy & Sons, Ltd.", terms, prefix=True, middle=True, suffix=True)
Daddy & Sons

"""

import functools
import operator
import re

from aca import Automaton

from .termdata import terms_by_country, terms_by_type
from .utils import normalize_terms, strip_head, strip_tail


def get_unique_terms():
    "retrieve all unique terms from termdata definitions"
    ts = functools.reduce(operator.iconcat, terms_by_type.values(), [])
    cs = functools.reduce(operator.iconcat, terms_by_country.values(), [])
    return set(ts + cs)


RE_IS_CHINESE = re.compile(
    r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]", re.UNICODE
)


def has_chinese(txt):
    cjk_characters = RE_IS_CHINESE.search(txt)
    return cjk_characters is not None


def split_fn(txt):
    return list(txt) if has_chinese(txt) else txt.split()


def prepare_terms():
    "construct an optimized term structure for basename extraction"
    terms = get_unique_terms()
    nterms = normalize_terms(terms)
    ntermparts = (split_fn(t) for t in nterms)
    # make sure that the result is deterministic, sort terms descending by number of tokens, ascending by names
    sntermparts = sorted(ntermparts, key=lambda x: (-len(x), x))
    return [(len(tp), tp) for tp in sntermparts]


def get_automaton():
    terms = prepare_terms()
    map = Automaton()
    valid_tokens = set()
    for len_term, term in terms:
        map[term] = "."  # the label is currently not used
        valid_tokens.update(term)
    return map, valid_tokens


aho, valid_tokens = get_automaton()


def basename(name, terms, suffix=True, prefix=False, middle=False, **kwargs):
    "return cleaned base version of the business name"

    assert middle is False, "middle argument is not supported in disco"

    chinese_in_name = has_chinese(name)

    name_stripped = strip_head(strip_tail(name))
    nparts = split_fn(name_stripped)

    nnparts = list(normalize_terms(nparts))

    # nname = normalized(name_stripped)
    # nnparts = list(map(strip_punct, split_fn(nname)))
    # nnsize = len(nnparts)

    # the condition is here for performance optimization (if it was omitted the code would work the same)
    if len(nnparts) > 0 and (
        (suffix and nnparts[-1] in valid_tokens)
        or (prefix and nnparts[0] in valid_tokens)
    ):
        sorted_matches = sorted(aho.get_matches(nnparts), key=lambda m: -m.end)

        if suffix:
            for match in sorted_matches:
                if match.end == len(nparts):
                    # del nnparts[-len(match.elems):]
                    del nparts[-len(match.elems) :]
                else:
                    break

            # original code
            # for termsize, termparts in terms:
            #     if nnparts[-termsize:] == termparts:
            #         del nnparts[-termsize:]
            #         del nparts[-termsize:]

        if prefix:
            offset = 0
            for match in reversed(sorted_matches):
                if match.start == offset:
                    offset += len(match.elems)
                else:
                    break

            # del nnparts[:offset]
            del nparts[:offset]

            # original code
            # for termsize, termparts in terms:
            #     if nnparts[:termsize] == termparts:
            #         del nnparts[:termsize]
            #         del nparts[:termsize]

    # if middle:
    #     for termsize, termparts in terms:
    #         if termsize > 1:
    #             sizediff = nnsize - termsize
    #             if sizediff > 1:
    #                 for i in range(0, nnsize - termsize + 1):
    #                     if termparts == nnparts[i : i + termsize]:
    #                         del nnparts[i : i + termsize]
    #                         del nparts[i : i + termsize]
    #         else:
    #             if termparts[0] in nnparts[1:-1]:
    #                 idx = nnparts[1:-1].index(termparts[0])
    #                 del nnparts[idx + 1]
    #                 del nparts[idx + 1]

    # return strip_head(
    #     strip_tail("".join(nparts) if chinese_in_name else " ".join(nparts))
    # )
    return strip_head(
        strip_tail("".join(nparts) if chinese_in_name else " ".join(nparts))
    )
