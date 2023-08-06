from collections import defaultdict


def same_base_symbol(*symbols) -> bool:
    if len(set(s.base_symbol for s in symbols)) > 1:
        # base symbols don't all match.
        return False
    return True


def same_asset_category(*symbols) -> bool:
    # all symbols must share a common security type.
    symbol_types = defaultdict(int)
    for s in symbols:
        # get all unique security types for this symbol.
        asset_categories = {c.asset_category for c in s.possible_conventions}
        # add this symbols security types to type->count map.
        for cat in asset_categories:
            symbol_types[cat] += 1
    # return True if all symbols have a common security type.
    return any(type_count == len(symbols) for type_count in symbol_types.values())


def equivalent(*symbols) -> bool:
    """Return True if symbols are equivalent.
    Symbols are equivalent if base symbols are the same and security type is the same.
    """
    return same_base_symbol(symbols) and same_asset_category(symbols)
