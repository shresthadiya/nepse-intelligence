from app.database import SessionLocal
from app.models import Company


companies = [
    {
        "symbol": "NABIL",
        "name": "Nabil Bank Limited",
        "sector": "Commercial Bank"
    },
    {
        "symbol": "NICA",
        "name": "NIC Asia Bank Limited",
        "sector": "Commercial Bank"
    },
    {
        "symbol": "NLIC",
        "name": "Nepal Life Insurance Company Limited",
        "sector": "Life Insurance"
    },
    {
        "symbol": "HIDCL",
        "name": "Hydroelectricity Investment and Development Company Limited",
        "sector": "Investment"
    },
    {
        "symbol": "SHIVM",
        "name": "Shivam Cements Limited",
        "sector": "Manufacturing"
    }
]


def seed_companies():

    db = SessionLocal()

    try:
        for company_data in companies:

            existing = db.query(Company).filter(
                Company.symbol == company_data["symbol"]
            ).first()

            if not existing:
                company = Company(**company_data)
                db.add(company)

        db.commit()

        print("Companies seeded successfully!")

    except Exception as error:
        db.rollback()
        print(f"Error seeding companies: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_companies()