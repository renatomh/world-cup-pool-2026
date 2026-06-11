from app.config import get_settings
from app.database import SessionLocal
from app.services.seed import run_seed, seed_summary


def main() -> None:
    settings = get_settings()
    db = SessionLocal()
    try:
        result = run_seed(db, settings)
        counts = seed_summary(db)
        print("Seed complete.")
        print(
            f"  teams created: {result.teams_created}, "
            f"matches created: {result.matches_created}, "
            f"admin created: {result.admin_created}, "
            f"demo user created: {result.demo_user_created}",
        )
        print(
            f"  totals — teams: {counts['teams']}, matches: {counts['matches']}, "
            f"users: {counts['users']}, admins: {counts['admins']}",
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
