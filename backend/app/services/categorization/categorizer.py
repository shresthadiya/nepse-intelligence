from sqlalchemy.orm import Session

from app.models import (
    News,
    NewsCategory,
    Company
)

from app.services.categorization.company_matcher import (
    find_company_matches
)


def categorize_news(db: Session, news: News):
    """
    Automatically categorize an article
    based on mentioned NEPSE companies.

    Supports multiple company associations.
    """

    companies = db.query(Company).filter(
        Company.is_active == True
    ).all()

    # Combine headline and body.
    text = f"{news.headline or ''} {news.body or ''}"

    matches = find_company_matches(
        text=text,
        companies=companies
    )

    existing_categories = db.query(
        NewsCategory
    ).filter(
        NewsCategory.news_id == news.id
    ).all()

    existing_company_ids = {
        category.company_id
        for category in existing_categories
    }

    inserted = []

    for match in matches:

        company_id = match["company_id"]

        # Avoid duplicate associations.
        if company_id in existing_company_ids:
            continue

        category = NewsCategory(
            news_id=news.id,
            company_id=company_id,
            confidence=match["confidence"]
        )

        db.add(category)

        existing_company_ids.add(company_id)

        inserted.append(match)

    # Flush without committing.
    # The caller controls the transaction.
    db.flush()

    return {
        "news_id": news.id,
        "matched_companies": matches,
        "inserted": inserted,
        "total_matches": len(matches)
    }


def categorize_existing_news(db: Session):
    """
    Categorize previously collected articles
    that do not yet have company associations.
    """

    articles = db.query(News).all()

    results = []

    for article in articles:

        result = categorize_news(
            db=db,
            news=article
        )

        results.append(result)

    db.commit()

    return {
        "processed": len(articles),
        "results": results
    }