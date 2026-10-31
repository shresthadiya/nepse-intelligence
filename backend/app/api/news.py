from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session, joinedload
from typing import Optional

from app.database import get_db

from app.models import (
    News,
    NewsCategory,
    Company,
    CategorizationCorrection
)

from app.models.user import User

from app.api.deps import (
    get_current_user,
    require_roles
)

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("/")
def get_news(
    company_id: Optional[int] = None,
    source: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(News).options(
        joinedload(
            News.categories
        ).joinedload(
            NewsCategory.company
        )
    )

    if company_id is not None:

        query = query.join(
            NewsCategory,
            News.id == NewsCategory.news_id
        ).filter(
            NewsCategory.company_id == company_id
        )

    if source:
        query = query.filter(
            News.source.ilike(f"%{source}%")
        )

    total = query.distinct().count()

    articles = query.distinct().order_by(
        News.published_at.desc().nullslast(),
        News.id.desc()
    ).offset(skip).limit(limit).all()

    results = []

    for article in articles:

        results.append({
            "id": article.id,
            "headline": article.headline,
            "body": article.body,
            "source": article.source,
            "url": article.url,
            "published_at": article.published_at,

            "companies": [
                {
                    "company_id": category.company_id,
                    "company_name": category.company.name,
                    "symbol": category.company.symbol,
                    "confidence": category.confidence
                }
                for category in article.categories
                if category.company is not None
            ]
        })

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "news": results
    }


@router.post("/{news_id}/recategorize")
def recategorize_news(
    news_id: int,
    company_id: int,
    action: str = Query("add"),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "analyst")
    )
):

    if action not in ["add", "remove"]:
        raise HTTPException(
            status_code=400,
            detail="Action must be 'add' or 'remove'"
        )

    article = db.query(News).filter(
        News.id == news_id
    ).first()

    if not article:
        raise HTTPException(
            status_code=404,
            detail="News article not found"
        )

    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    existing = db.query(NewsCategory).filter(
        NewsCategory.news_id == news_id,
        NewsCategory.company_id == company_id
    ).first()

    if action == "add":

        if existing:
            raise HTTPException(
                status_code=409,
                detail="News is already associated with this company"
            )

        old_confidence = None
        new_confidence = 1.0

        category = NewsCategory(
            news_id=news_id,
            company_id=company_id,
            confidence=new_confidence
        )

        db.add(category)

    else:

        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Company association not found"
            )

        old_confidence = existing.confidence
        new_confidence = None

        db.delete(existing)

    correction = CategorizationCorrection(
        news_id=news_id,
        analyst_id=current_user.id,
        action=action,
        company_id=company_id,
        old_confidence=old_confidence,
        new_confidence=new_confidence
    )

    db.add(correction)

    try:
        db.commit()

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to update news categorization"
        )

    return {
        "message": "News categorization updated successfully",
        "news_id": news_id,
        "company_id": company_id,
        "company_name": company.name,
        "action": action,
        "corrected_by": current_user.id
    }