"""Team flag image URLs from FIFA 3-letter codes (via flagcdn.com)."""

# FIFA codes that differ from ISO 3166-1 alpha-2 used by flag CDNs.
FIFA_TO_FLAGCDN: dict[str, str] = {
    "AUS": "au",
    "ARG": "ar",
    "ALG": "dz",
    "AUT": "at",
    "BEL": "be",
    "BIH": "ba",
    "BRA": "br",
    "CAN": "ca",
    "CIV": "ci",
    "COL": "co",
    "CPV": "cv",
    "COD": "cd",
    "CRO": "hr",
    "CUW": "cw",
    "CZE": "cz",
    "ECU": "ec",
    "EGY": "eg",
    "ENG": "gb-eng",
    "ESP": "es",
    "FRA": "fr",
    "GER": "de",
    "GHA": "gh",
    "HAI": "ht",
    "IRN": "ir",
    "IRQ": "iq",
    "JOR": "jo",
    "JPN": "jp",
    "KOR": "kr",
    "KSA": "sa",
    "MAR": "ma",
    "MEX": "mx",
    "NED": "nl",
    "NOR": "no",
    "NZL": "nz",
    "PAN": "pa",
    "PAR": "py",
    "POR": "pt",
    "QAT": "qa",
    "RSA": "za",
    "SCO": "gb-sct",
    "SEN": "sn",
    "SUI": "ch",
    "SWE": "se",
    "TUN": "tn",
    "TUR": "tr",
    "URU": "uy",
    "USA": "us",
    "UZB": "uz",
}


def team_logo_url(fifa_code: str, *, width: int = 80) -> str:
    """Return a flag image URL for a FIFA team code."""
    flag_code = FIFA_TO_FLAGCDN.get(fifa_code.upper(), fifa_code.lower())
    return f"https://flagcdn.com/w{width}/{flag_code}.png"
