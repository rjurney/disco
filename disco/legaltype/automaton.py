from dataclasses import dataclass
from typing import Any, Dict, List

from aca import Automaton

from disco.legaltype.termdata import terms_by_country, terms_by_type
from disco.utils import normalize_terms, split_text


@dataclass
class Match:
    start: int
    end: int
    elems: List[str]
    value: Any


class AnyValuesAutomaton(Automaton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._value_mapping = dict()
        self._id_counter = 0

    def add(self, pattern, value):
        if value == "":
            raise NotImplementedError("This function has not been implemented yet")
        else:
            super().add(pattern, str(self._id_counter))
            self._value_mapping[str(self._id_counter)] = value
            self._id_counter += 1

    def __getitem__(self, pattern):
        value = super().__getitem__(pattern)
        return self._value_mapping[value]

    def __delitem__(self, pattern):
        raise NotImplementedError("This function has not been implemented yet")

    def get_matches(self, text, exclude_overlaps=True):
        matches = super().get_matches(text, exclude_overlaps=exclude_overlaps)
        return [
            Match(m.start, m.end, m.elems, self._value_mapping[m.label])
            for m in matches
        ]


class Matcher:
    def __init__(self):
        self._built = False
        self._tokens_in_automaton = set()
        self._aho_automaton = AnyValuesAutomaton()

    @classmethod
    def _reverse_terms_dict(
        cls, dict_data: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        inv_dict: Dict[str, List[str]] = {}
        for group_name, group_values in dict_data.items():
            # example: "Limited Liability Company": ["pllc", "llc", "l.l.c.", "plc."]
            for value in group_values:
                inv_dict.setdefault(value, list()).append(group_name)
        return inv_dict

    def build(self) -> None:
        assert self._built is False, "You cannot build the automaton twice"

        automaton_data = dict()

        types_by_terms = __class__._reverse_terms_dict(terms_by_type)
        countries_by_terms = __class__._reverse_terms_dict(terms_by_country)

        for term, legal_types in types_by_terms.items():
            snterm = normalize_terms(split_text(term))
            automaton_data.setdefault(
                tuple(snterm), {"countries": set(), "types": set()}
            )["types"].update(legal_types)

        for term, countries in countries_by_terms.items():
            snterm = normalize_terms(split_text(term))
            automaton_data.setdefault(
                tuple(snterm), {"countries": set(), "types": set()}
            )["countries"].update(countries)

        for term, term_data in automaton_data.items():
            term_data["term"] = term
            self._aho_automaton[list(term)] = term_data

            self._tokens_in_automaton.update(term)

        self._built = True

    def has_pattern(self, pattern: str) -> bool:
        return pattern in self._tokens_in_automaton

    def get_matches(self, text: List[str]):
        return self._aho_automaton.get_matches(text)
