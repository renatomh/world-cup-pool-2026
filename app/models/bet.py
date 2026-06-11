from uuid import UUID

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class Bet(Base, UuidPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "bets"
    __table_args__ = (UniqueConstraint("user_id", "match_id", name="uq_bets_user_match"),)

    user_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    match_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("matches.id"), nullable=False)
    home_score: Mapped[int] = mapped_column(Integer, nullable=False)
    away_score: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user: Mapped["User"] = relationship(back_populates="bets")
    match: Mapped["Match"] = relationship(back_populates="bets")
