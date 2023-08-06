import json
import re
from pathlib import Path
from pprint import pformat
from textwrap import dedent
from typing import Dict, List

import requests
from lxml.html import fromstring
from ready_logger import logger


def download_table() -> str:
    url = "https://www.nasdaqtrader.com/Trader.aspx?id=CQSSymbolConvention"
    resp = requests.get(url)
    logger.info(f"[{resp.status_code}] {url}")
    return resp.text


def parse_conventions_table(html: str) -> List[Dict[str, str]]:
    root = fromstring(html)
    header = [
        "asset_category",
        "cqs",
        "cms",
        "nasdaq_ip",
        "act_ctci",
    ]
    # extract from HTML paths.
    rows = [
        {name: val.xpath("./text()") for name, val in zip(header, row.xpath("./td"))}
        for row in root.xpath('//div[@class="genTable static"]/table/tbody/tr')
    ]
    # convert to string.
    rows = [
        {name: str(val[0]).strip() for name, val in row.items() if len(val)}
        for row in rows
    ]
    # remove empty values.
    rows = [{name: val for name, val in row.items() if val != ""} for row in rows]
    # remove empty rows.
    rows = [row for row in rows if len(row)]
    # check for conventions with multiple suffixes.
    for row in rows:
        for name, val in row.items():
            if name != "asset_category":
                row[name] = [s.strip() for s in val.split(" or ")]
    # cms format needs a space before suffix.
    for row in rows:
        row["cms"] = [f" {v}" for v in row["cms"]]
    logger.info(f"Parsed conventions:\n{pformat(rows)}")
    return rows


def save_suffix_regs_dict(conventions: List[Dict[str, str]]):
    # create dict of regular expressions.
    dict_members = []
    for row in conventions:
        asset_category = row.pop("asset_category")
        convention_regs = []
        for abbr, suffixes in row.items():
            suffixes = [f"{re.escape(s)}$" for s in suffixes]
            suffixes = f"({'|'.join(suffixes)})" if len(suffixes) > 1 else suffixes[0]
            # create named group to match convention suffixes.
            convention_regs.append(f"(?P<{abbr}>{suffixes})")
        convention_regs = f"({'|'.join(convention_regs)})"
        dict_members.append(f"'{asset_category}': re.compile(r'{convention_regs}'),")
    dict_members = "\n".join(dict_members)
    Path(__file__).parent.joinpath("suffix_regs.py").write_text(
        dedent(
            f"""\
            import re

            suffix_regs = {{{
                dict_members
            }}}
            """
        )
    )


def main():
    html = download_table()
    conventions = parse_conventions_table(html)
    Path(__file__).parent.joinpath("conventions.json").write_text(
        json.dumps(conventions, indent=4)
    )
    save_suffix_regs_dict(conventions)


if __name__ == "__main__":
    main()
