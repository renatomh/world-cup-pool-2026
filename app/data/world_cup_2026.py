"""Official FIFA World Cup 2026 group stage data.

Teams from the Final Draw (5 Dec 2025). Kickoff times are FIFA official UTC
(from https://digitalhub.fifa.com/.../FWC26-Match-Schedule and kickoff times
published at inside.fifa.com). Stadium-local times vary by venue; the database
always stores UTC and display converts to each user's timezone.

Note: fifa.com/scores-fixtures shows UTC, not stadium-local — do not apply
venue timezone conversion to those values.
"""

from datetime import datetime, timezone

# fmt: off
WC2026_TEAMS: list[dict[str, str]] = [
    {"name": "Mexico", "code": "MEX", "group_name": "A"},
    {"name": "South Africa", "code": "RSA", "group_name": "A"},
    {"name": "Korea Republic", "code": "KOR", "group_name": "A"},
    {"name": "Czechia", "code": "CZE", "group_name": "A"},
    {"name": "Canada", "code": "CAN", "group_name": "B"},
    {"name": "Bosnia and Herzegovina", "code": "BIH", "group_name": "B"},
    {"name": "Qatar", "code": "QAT", "group_name": "B"},
    {"name": "Switzerland", "code": "SUI", "group_name": "B"},
    {"name": "Brazil", "code": "BRA", "group_name": "C"},
    {"name": "Morocco", "code": "MAR", "group_name": "C"},
    {"name": "Haiti", "code": "HAI", "group_name": "C"},
    {"name": "Scotland", "code": "SCO", "group_name": "C"},
    {"name": "USA", "code": "USA", "group_name": "D"},
    {"name": "Paraguay", "code": "PAR", "group_name": "D"},
    {"name": "Australia", "code": "AUS", "group_name": "D"},
    {"name": "Türkiye", "code": "TUR", "group_name": "D"},
    {"name": "Germany", "code": "GER", "group_name": "E"},
    {"name": "Curaçao", "code": "CUW", "group_name": "E"},
    {"name": "Côte d'Ivoire", "code": "CIV", "group_name": "E"},
    {"name": "Ecuador", "code": "ECU", "group_name": "E"},
    {"name": "Netherlands", "code": "NED", "group_name": "F"},
    {"name": "Japan", "code": "JPN", "group_name": "F"},
    {"name": "Sweden", "code": "SWE", "group_name": "F"},
    {"name": "Tunisia", "code": "TUN", "group_name": "F"},
    {"name": "Belgium", "code": "BEL", "group_name": "G"},
    {"name": "Egypt", "code": "EGY", "group_name": "G"},
    {"name": "IR Iran", "code": "IRN", "group_name": "G"},
    {"name": "New Zealand", "code": "NZL", "group_name": "G"},
    {"name": "Spain", "code": "ESP", "group_name": "H"},
    {"name": "Cabo Verde", "code": "CPV", "group_name": "H"},
    {"name": "Saudi Arabia", "code": "KSA", "group_name": "H"},
    {"name": "Uruguay", "code": "URU", "group_name": "H"},
    {"name": "France", "code": "FRA", "group_name": "I"},
    {"name": "Senegal", "code": "SEN", "group_name": "I"},
    {"name": "Iraq", "code": "IRQ", "group_name": "I"},
    {"name": "Norway", "code": "NOR", "group_name": "I"},
    {"name": "Argentina", "code": "ARG", "group_name": "J"},
    {"name": "Algeria", "code": "ALG", "group_name": "J"},
    {"name": "Austria", "code": "AUT", "group_name": "J"},
    {"name": "Jordan", "code": "JOR", "group_name": "J"},
    {"name": "Portugal", "code": "POR", "group_name": "K"},
    {"name": "Congo DR", "code": "COD", "group_name": "K"},
    {"name": "Uzbekistan", "code": "UZB", "group_name": "K"},
    {"name": "Colombia", "code": "COL", "group_name": "K"},
    {"name": "England", "code": "ENG", "group_name": "L"},
    {"name": "Croatia", "code": "CRO", "group_name": "L"},
    {"name": "Ghana", "code": "GHA", "group_name": "L"},
    {"name": "Panama", "code": "PAN", "group_name": "L"},
]

# Official FIFA UTC kickoff times (group stage).
WC2026_GROUP_MATCHES: list[dict] = [
    # Group A
    {"home_code": "MEX", "away_code": "RSA", "group_name": "A", "kickoff_utc": datetime(2026, 6, 11, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "KOR", "away_code": "CZE", "group_name": "A", "kickoff_utc": datetime(2026, 6, 12, 2, 0, tzinfo=timezone.utc)},
    {"home_code": "CZE", "away_code": "RSA", "group_name": "A", "kickoff_utc": datetime(2026, 6, 18, 16, 0, tzinfo=timezone.utc)},
    {"home_code": "MEX", "away_code": "KOR", "group_name": "A", "kickoff_utc": datetime(2026, 6, 19, 1, 0, tzinfo=timezone.utc)},
    {"home_code": "CZE", "away_code": "MEX", "group_name": "A", "kickoff_utc": datetime(2026, 6, 25, 1, 0, tzinfo=timezone.utc)},
    {"home_code": "RSA", "away_code": "KOR", "group_name": "A", "kickoff_utc": datetime(2026, 6, 25, 1, 0, tzinfo=timezone.utc)},
    # Group B
    {"home_code": "CAN", "away_code": "BIH", "group_name": "B", "kickoff_utc": datetime(2026, 6, 12, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "QAT", "away_code": "SUI", "group_name": "B", "kickoff_utc": datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "SUI", "away_code": "BIH", "group_name": "B", "kickoff_utc": datetime(2026, 6, 18, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "CAN", "away_code": "QAT", "group_name": "B", "kickoff_utc": datetime(2026, 6, 18, 22, 0, tzinfo=timezone.utc)},
    {"home_code": "SUI", "away_code": "CAN", "group_name": "B", "kickoff_utc": datetime(2026, 6, 24, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "BIH", "away_code": "QAT", "group_name": "B", "kickoff_utc": datetime(2026, 6, 24, 19, 0, tzinfo=timezone.utc)},
    # Group C
    {"home_code": "BRA", "away_code": "MAR", "group_name": "C", "kickoff_utc": datetime(2026, 6, 13, 22, 0, tzinfo=timezone.utc)},
    {"home_code": "HAI", "away_code": "SCO", "group_name": "C", "kickoff_utc": datetime(2026, 6, 14, 1, 0, tzinfo=timezone.utc)},
    {"home_code": "SCO", "away_code": "MAR", "group_name": "C", "kickoff_utc": datetime(2026, 6, 19, 22, 0, tzinfo=timezone.utc)},
    {"home_code": "BRA", "away_code": "HAI", "group_name": "C", "kickoff_utc": datetime(2026, 6, 20, 0, 30, tzinfo=timezone.utc)},
    {"home_code": "SCO", "away_code": "BRA", "group_name": "C", "kickoff_utc": datetime(2026, 6, 24, 22, 0, tzinfo=timezone.utc)},
    {"home_code": "MAR", "away_code": "HAI", "group_name": "C", "kickoff_utc": datetime(2026, 6, 24, 22, 0, tzinfo=timezone.utc)},
    # Group D
    {"home_code": "USA", "away_code": "PAR", "group_name": "D", "kickoff_utc": datetime(2026, 6, 13, 1, 0, tzinfo=timezone.utc)},
    {"home_code": "AUS", "away_code": "TUR", "group_name": "D", "kickoff_utc": datetime(2026, 6, 14, 16, 0, tzinfo=timezone.utc)},
    {"home_code": "USA", "away_code": "AUS", "group_name": "D", "kickoff_utc": datetime(2026, 6, 19, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "TUR", "away_code": "PAR", "group_name": "D", "kickoff_utc": datetime(2026, 6, 20, 3, 0, tzinfo=timezone.utc)},
    {"home_code": "TUR", "away_code": "USA", "group_name": "D", "kickoff_utc": datetime(2026, 6, 26, 2, 0, tzinfo=timezone.utc)},
    {"home_code": "PAR", "away_code": "AUS", "group_name": "D", "kickoff_utc": datetime(2026, 6, 26, 2, 0, tzinfo=timezone.utc)},
    # Group E
    {"home_code": "GER", "away_code": "CUW", "group_name": "E", "kickoff_utc": datetime(2026, 6, 14, 17, 0, tzinfo=timezone.utc)},
    {"home_code": "CIV", "away_code": "ECU", "group_name": "E", "kickoff_utc": datetime(2026, 6, 14, 23, 0, tzinfo=timezone.utc)},
    {"home_code": "GER", "away_code": "CIV", "group_name": "E", "kickoff_utc": datetime(2026, 6, 20, 20, 0, tzinfo=timezone.utc)},
    {"home_code": "ECU", "away_code": "CUW", "group_name": "E", "kickoff_utc": datetime(2026, 6, 21, 0, 0, tzinfo=timezone.utc)},
    {"home_code": "CUW", "away_code": "CIV", "group_name": "E", "kickoff_utc": datetime(2026, 6, 25, 20, 0, tzinfo=timezone.utc)},
    {"home_code": "ECU", "away_code": "GER", "group_name": "E", "kickoff_utc": datetime(2026, 6, 25, 20, 0, tzinfo=timezone.utc)},
    # Group F
    {"home_code": "NED", "away_code": "JPN", "group_name": "F", "kickoff_utc": datetime(2026, 6, 14, 20, 0, tzinfo=timezone.utc)},
    {"home_code": "SWE", "away_code": "TUN", "group_name": "F", "kickoff_utc": datetime(2026, 6, 15, 2, 0, tzinfo=timezone.utc)},
    {"home_code": "NED", "away_code": "SWE", "group_name": "F", "kickoff_utc": datetime(2026, 6, 20, 17, 0, tzinfo=timezone.utc)},
    {"home_code": "TUN", "away_code": "JPN", "group_name": "F", "kickoff_utc": datetime(2026, 6, 21, 4, 0, tzinfo=timezone.utc)},
    {"home_code": "JPN", "away_code": "SWE", "group_name": "F", "kickoff_utc": datetime(2026, 6, 25, 23, 0, tzinfo=timezone.utc)},
    {"home_code": "TUN", "away_code": "NED", "group_name": "F", "kickoff_utc": datetime(2026, 6, 25, 23, 0, tzinfo=timezone.utc)},
    # Group G
    {"home_code": "BEL", "away_code": "EGY", "group_name": "G", "kickoff_utc": datetime(2026, 6, 15, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "IRN", "away_code": "NZL", "group_name": "G", "kickoff_utc": datetime(2026, 6, 16, 1, 0, tzinfo=timezone.utc)},
    {"home_code": "BEL", "away_code": "IRN", "group_name": "G", "kickoff_utc": datetime(2026, 6, 21, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "NZL", "away_code": "EGY", "group_name": "G", "kickoff_utc": datetime(2026, 6, 22, 1, 0, tzinfo=timezone.utc)},
    {"home_code": "EGY", "away_code": "IRN", "group_name": "G", "kickoff_utc": datetime(2026, 6, 27, 3, 0, tzinfo=timezone.utc)},
    {"home_code": "NZL", "away_code": "BEL", "group_name": "G", "kickoff_utc": datetime(2026, 6, 27, 3, 0, tzinfo=timezone.utc)},
    # Group H
    {"home_code": "ESP", "away_code": "CPV", "group_name": "H", "kickoff_utc": datetime(2026, 6, 15, 16, 0, tzinfo=timezone.utc)},
    {"home_code": "KSA", "away_code": "URU", "group_name": "H", "kickoff_utc": datetime(2026, 6, 15, 22, 0, tzinfo=timezone.utc)},
    {"home_code": "ESP", "away_code": "KSA", "group_name": "H", "kickoff_utc": datetime(2026, 6, 21, 16, 0, tzinfo=timezone.utc)},
    {"home_code": "URU", "away_code": "CPV", "group_name": "H", "kickoff_utc": datetime(2026, 6, 21, 22, 0, tzinfo=timezone.utc)},
    {"home_code": "CPV", "away_code": "KSA", "group_name": "H", "kickoff_utc": datetime(2026, 6, 27, 0, 0, tzinfo=timezone.utc)},
    {"home_code": "URU", "away_code": "ESP", "group_name": "H", "kickoff_utc": datetime(2026, 6, 27, 0, 0, tzinfo=timezone.utc)},
    # Group I
    {"home_code": "FRA", "away_code": "SEN", "group_name": "I", "kickoff_utc": datetime(2026, 6, 16, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "IRQ", "away_code": "NOR", "group_name": "I", "kickoff_utc": datetime(2026, 6, 16, 22, 0, tzinfo=timezone.utc)},
    {"home_code": "FRA", "away_code": "IRQ", "group_name": "I", "kickoff_utc": datetime(2026, 6, 22, 21, 0, tzinfo=timezone.utc)},
    {"home_code": "NOR", "away_code": "SEN", "group_name": "I", "kickoff_utc": datetime(2026, 6, 23, 0, 0, tzinfo=timezone.utc)},
    {"home_code": "NOR", "away_code": "FRA", "group_name": "I", "kickoff_utc": datetime(2026, 6, 26, 19, 0, tzinfo=timezone.utc)},
    {"home_code": "SEN", "away_code": "IRQ", "group_name": "I", "kickoff_utc": datetime(2026, 6, 26, 19, 0, tzinfo=timezone.utc)},
    # Group J
    {"home_code": "ARG", "away_code": "ALG", "group_name": "J", "kickoff_utc": datetime(2026, 6, 17, 1, 0, tzinfo=timezone.utc)},
    {"home_code": "AUT", "away_code": "JOR", "group_name": "J", "kickoff_utc": datetime(2026, 6, 17, 4, 0, tzinfo=timezone.utc)},
    {"home_code": "ARG", "away_code": "AUT", "group_name": "J", "kickoff_utc": datetime(2026, 6, 22, 17, 0, tzinfo=timezone.utc)},
    {"home_code": "JOR", "away_code": "ALG", "group_name": "J", "kickoff_utc": datetime(2026, 6, 23, 3, 0, tzinfo=timezone.utc)},
    {"home_code": "ALG", "away_code": "AUT", "group_name": "J", "kickoff_utc": datetime(2026, 6, 28, 2, 0, tzinfo=timezone.utc)},
    {"home_code": "JOR", "away_code": "ARG", "group_name": "J", "kickoff_utc": datetime(2026, 6, 28, 2, 0, tzinfo=timezone.utc)},
    # Group K
    {"home_code": "POR", "away_code": "COD", "group_name": "K", "kickoff_utc": datetime(2026, 6, 17, 17, 0, tzinfo=timezone.utc)},
    {"home_code": "UZB", "away_code": "COL", "group_name": "K", "kickoff_utc": datetime(2026, 6, 18, 2, 0, tzinfo=timezone.utc)},
    {"home_code": "POR", "away_code": "UZB", "group_name": "K", "kickoff_utc": datetime(2026, 6, 23, 17, 0, tzinfo=timezone.utc)},
    {"home_code": "COL", "away_code": "COD", "group_name": "K", "kickoff_utc": datetime(2026, 6, 24, 2, 0, tzinfo=timezone.utc)},
    {"home_code": "COL", "away_code": "POR", "group_name": "K", "kickoff_utc": datetime(2026, 6, 27, 23, 30, tzinfo=timezone.utc)},
    {"home_code": "COD", "away_code": "UZB", "group_name": "K", "kickoff_utc": datetime(2026, 6, 27, 23, 30, tzinfo=timezone.utc)},
    # Group L
    {"home_code": "ENG", "away_code": "CRO", "group_name": "L", "kickoff_utc": datetime(2026, 6, 17, 20, 0, tzinfo=timezone.utc)},
    {"home_code": "GHA", "away_code": "PAN", "group_name": "L", "kickoff_utc": datetime(2026, 6, 17, 23, 0, tzinfo=timezone.utc)},
    {"home_code": "ENG", "away_code": "GHA", "group_name": "L", "kickoff_utc": datetime(2026, 6, 23, 20, 0, tzinfo=timezone.utc)},
    {"home_code": "PAN", "away_code": "CRO", "group_name": "L", "kickoff_utc": datetime(2026, 6, 23, 23, 0, tzinfo=timezone.utc)},
    {"home_code": "PAN", "away_code": "ENG", "group_name": "L", "kickoff_utc": datetime(2026, 6, 27, 21, 0, tzinfo=timezone.utc)},
    {"home_code": "CRO", "away_code": "GHA", "group_name": "L", "kickoff_utc": datetime(2026, 6, 27, 21, 0, tzinfo=timezone.utc)},
]
# fmt: on

WC2026_TEAM_COUNT = len(WC2026_TEAMS)
WC2026_GROUP_MATCH_COUNT = len(WC2026_GROUP_MATCHES)
