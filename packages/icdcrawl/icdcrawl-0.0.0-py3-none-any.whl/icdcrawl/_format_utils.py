from typing import Literal


def format_icd_codes(
    icd_codes: list[str],
    *,
    sort: bool = False,
    dot: bool = False,
    duplicates: Literal["drop", "ignore"] = "ignore",
) -> list[str]:
    if duplicates == "drop":
        icd_codes = list(set(icd_codes))
    if sort:
        icd_codes.sort()
    if not dot:
        icd_codes = [icd_code.replace(".", "") for icd_code in icd_codes]
    return icd_codes
