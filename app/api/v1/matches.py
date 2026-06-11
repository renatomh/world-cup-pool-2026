from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.datetime_format import format_date, format_datetime_for_user
from app.database import get_db
from app.dependencies import get_current_user
from app.models.match import Match
from app.models.user import User
from app.schemas.match import MatchListResponse, MatchResponse, team_brief_from_model
from app.services.matches import get_match_day

router = APIRouter(prefix="/matches", tags=["matches"])


def _match_response(match: Match, user: User) -> MatchResponse:
    return MatchResponse(
        id=match.id,
        home_team=team_brief_from_model(match.home_team),
        away_team=team_brief_from_model(match.away_team),
        kickoff_time=match.kickoff_time,
        kickoff_display=format_datetime_for_user(
            match.kickoff_time,
            timezone_name=user.timezone,
            locale=user.locale,
        ),
        stage=match.stage,
        group_name=match.group_name,
        home_score=match.home_score,
        away_score=match.away_score,
    )


@router.get("", response_model=MatchListResponse)
def list_matches(
    match_date: date | None = Query(None, alias="date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MatchListResponse:
    selected, prev_date, next_date, matches = get_match_day(
        db,
        timezone_name=current_user.timezone,
        requested_date=match_date,
    )
    return MatchListResponse(
        date=selected,
        date_display=format_date(selected, locale=current_user.locale),
        prev_date=prev_date,
        next_date=next_date,
        matches=[_match_response(match, current_user) for match in matches],
    )
