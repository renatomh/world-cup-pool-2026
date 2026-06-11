from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.team_logos import team_logo_url


class TeamBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    code: str
    group_name: str | None
    logo_url: str


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    home_team: TeamBrief
    away_team: TeamBrief
    kickoff_time: datetime
    kickoff_display: str = Field(description="Kickoff formatted in the requesting user's timezone and locale")
    stage: str
    group_name: str | None
    home_score: int | None
    away_score: int | None


class MatchListResponse(BaseModel):
    date: date
    date_display: str
    prev_date: date | None
    next_date: date | None
    matches: list[MatchResponse]


def team_brief_from_model(team) -> TeamBrief:
    return TeamBrief(
        id=team.id,
        name=team.name,
        code=team.code,
        group_name=team.group_name,
        logo_url=team_logo_url(team.code),
    )
