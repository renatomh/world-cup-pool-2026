from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class Match(Base, UuidPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "matches"

    home_team_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    kickoff_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    stage: Mapped[str] = mapped_column(String(32), default="group", nullable=False)
    group_name: Mapped[str | None] = mapped_column(String(1), nullable=True)
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    home_team: Mapped["Team"] = relationship(
        back_populates="home_matches",
        foreign_keys=[home_team_id],
    )
    away_team: Mapped["Team"] = relationship(
        back_populates="away_matches",
        foreign_keys=[away_team_id],
    )
    bets: Mapped[list["Bet"]] = relationship(back_populates="match")
