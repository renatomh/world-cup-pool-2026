from app.core.team_logos import team_logo_url


def test_team_logo_url_uses_fifa_code_mapping():
    assert team_logo_url("ENG") == "https://flagcdn.com/w80/gb-eng.png"
    assert team_logo_url("KOR") == "https://flagcdn.com/w80/kr.png"
    assert team_logo_url("RSA") == "https://flagcdn.com/w80/za.png"


def test_team_logo_url_supports_custom_width():
    assert team_logo_url("BRA", width=40) == "https://flagcdn.com/w40/br.png"
