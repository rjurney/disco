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
from .termdata import terms_by_type, terms_by_country
from .utils import strip_punct, normalize_terms, strip_tail, normalized, strip_head
import re


def get_unique_terms():
    "retrieve all unique terms from termdata definitions"
    ts = functools.reduce(operator.iconcat, terms_by_type.values(), [])
    cs = functools.reduce(operator.iconcat, terms_by_country.values(), [])
    return set(ts + cs)


def prepare_terms():
    "construct an optimized term structure for basename extraction"
    terms = get_unique_terms()
    nterms = normalize_terms(terms)
    split_fn = lambda txt: list(txt) if has_chinese(txt) else txt.split()
    ntermparts = (split_fn(t) for t in nterms)
    # make sure that the result is deterministic, sort terms descending by number of tokens, ascending by names
    sntermparts = sorted(ntermparts, key=lambda x: (-len(x), x))
    return [(len(tp), tp) for tp in sntermparts]


def has_chinese(txt):
    cjk_characters = re.search(
        u"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]", txt
    )
    return cjk_characters is not None


def basename(name, terms, suffix=True, prefix=False, middle=False, **kwargs):
    "return cleaned base version of the business name"

    chinese_in_name = has_chinese(name)

    name = strip_head(strip_tail(name))
    split_fn = lambda txt: list(txt) if chinese_in_name else txt.split()
    nparts = split_fn(name)
    nname = normalized(name)
    nnparts = list(map(strip_punct, split_fn(nname)))
    nnsize = len(nnparts)

    if suffix:
        for termsize, termparts in terms:
            if nnparts[-termsize:] == termparts:
                del nnparts[-termsize:]
                del nparts[-termsize:]

    if prefix:
        for termsize, termparts in terms:
            if nnparts[:termsize] == termparts:
                del nnparts[:termsize]
                del nparts[:termsize]

    if middle:
        for termsize, termparts in terms:
            if termsize > 1:
                sizediff = nnsize - termsize
                if sizediff > 1:
                    for i in range(0, nnsize - termsize + 1):
                        if termparts == nnparts[i : i + termsize]:
                            del nnparts[i : i + termsize]
                            del nparts[i : i + termsize]
            else:
                if termparts[0] in nnparts[1:-1]:
                    idx = nnparts[1:-1].index(termparts[0])
                    del nnparts[idx + 1]
                    del nparts[idx + 1]

    return strip_head(
        strip_tail("".join(nparts) if chinese_in_name else " ".join(nparts))
    )