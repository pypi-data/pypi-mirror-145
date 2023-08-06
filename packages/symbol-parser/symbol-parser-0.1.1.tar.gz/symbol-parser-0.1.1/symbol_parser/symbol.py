import json
import re
from collections import defaultdict
from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path
from typing import List, Union

from symbol_parser.suffix_regs import suffix_regs

# convert from regex named group to formatted convention name
convention_names = {
    "cqs": "CQS",
    "cms": "CMS",
    "nasdaq_ip": "NASDAQ Integrated Platform Suffix",
    "act_ctci": "NASDAQ ACT/CTCI",
}


_cat_data = {
    row.pop("asset_category"): row
    for row in json.loads(
        Path(__file__).parent.joinpath("conventions.json").read_text()
    )
}


@dataclass
class SymbolConvention:
    symbol: str
    asset_category: str
    convention_abbr: str
    convention_name: str = None

    def __post_init__(self):
        self.convention_name = convention_names.get(self.convention_abbr)


class Symbol:
    """Utility class for parsing a ticker symbol and converting symbol syntax to different standards.

    Args:
        symbol: str -- the symbol to be parse.
    """

    def __init__(self, symbol: str):
        self._symbol = symbol
        self.__no_convention_match = SymbolConvention(self._symbol, None, None)
        # map suffix length to type.
        possible = defaultdict(set)
        for asset_category, reg in suffix_regs.items():
            if match := reg.search(self._symbol):
                for convention_abbr, suffix in match.groupdict().items():
                    if suffix:
                        possible[len(suffix)].add(
                            (suffix, asset_category, convention_abbr)
                        )
        if len(possible):
            # sort by key (suffix length). take set of possibilities with longest suffix length
            possible = sorted(possible.items(), key=itemgetter(0))[-1][1]
            # suffix will be the same for all possibilities.
            suffix = {suffix for suffix, *_ in possible}
            assert len(suffix) == 1
            self._suffix = suffix.pop()
            self._base_symbol = re.sub(f"{re.escape(self._suffix)}$", "", self._symbol)
            self._possible_conventions = [
                SymbolConvention(self._symbol, cat, conv_abbr)
                for _, cat, conv_abbr in possible
            ]
        else:
            self._possible_conventions = [self.__no_convention_match]
            self._suffix = None
            self._base_symbol = self._symbol

    @property
    def symbol(self) -> str:
        """The symbol being parsed."""
        return self._symbol

    @property
    def base_symbol(self) -> str:
        """The symbol with any suffix removed."""
        return self._base_symbol

    @property
    def suffix(self) -> Union[str, None]:
        """The suffix on the symbol, if any."""
        return self._suffix

    @property
    def possible_conventions(self) -> List[SymbolConvention]:
        """List of all valid conventions for this symbol."""
        return self._possible_conventions

    def as_cqs(self) -> List[SymbolConvention]:
        return self._as_type("cqs")

    def as_cms(self) -> List[SymbolConvention]:
        return self._as_type("cms")

    def as_nasdaq(self) -> List[SymbolConvention]:
        return self._as_type("nasdaq_ip")

    def as_nasdaq_act_ctci(self) -> List[SymbolConvention]:
        return self._as_type("act_ctci")

    def _as_type(self, convention_abbr: str) -> List[SymbolConvention]:
        to_convert = [
            c for c in self._possible_conventions if c != self.__no_convention_match
        ]
        if len(to_convert):
            return [
                SymbolConvention(
                    symbol=f"{self._base_symbol}{suffix}",
                    asset_category=c.asset_category,
                    convention_abbr=convention_abbr,
                )
                for c in to_convert
                for suffix in _cat_data[c.asset_category][convention_abbr]
            ]
        return [self.__no_convention_match]
