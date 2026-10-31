from datetime import datetime, timezone
from threading import Lock

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.api.deps import require_roles
from app.models.user import User
from app.models.crawl_run import CrawlRun

from app.crawlers.crawler_manager import run_all_crawlers


router = APIRouter(prefix="/admin", tags=["Admin"])

crawl_lock = Lock()


def execute_crawl(crawl_run_id: int, max_articles: int = 10):

    db = SessionLocal()

    try:
        crawl_run = db.query(CrawlRun).filter(
            CrawlRun.id == crawl_run_id
        ).first()

        if not crawl_run:
            return

        crawl_run.status = "running"
        crawl_run.started_at = datetime.now(timezone.utc)

        db.commit()

        results = run_all_crawlers(
            db=db,
            max_articles=max_articles
        )

        totals = {
            "fetched": sum(r.get("fetched", 0) for r in results),
            "inserted": sum(r.get("inserted", 0) for r in results),
            "duplicates": sum(r.get("duplicates", 0) for r in results),
            "categorized": sum(r.get("categorized", 0) for r in results),
            "uncategorized": sum(r.get("uncategorized", 0) for r in results),
            "failed": sum(r.get("failed", 0) for r in results)
        }

        crawl_run.total_fetched = totals["fetched"]
        crawl_run.total_inserted = totals["inserted"]
        crawl_run.total_duplicates = totals["duplicates"]
        crawl_run.total_categorized = totals["categorized"]
        crawl_run.total_uncategorized = totals["uncategorized"]
        crawl_run.total_failed = totals["failed"]

        crawl_run.results = results

        crawl_run.status = (
            "completed"
            if totals["failed"] == 0
            else "completed_with_errors"
        )

        crawl_run.completed_at = datetime.now(timezone.utc)

        db.commit()

    except Exception as exc:

        db.rollback()

        crawl_run = db.query(CrawlRun).filter(
            CrawlRun.id == crawl_run_id
        ).first()

        if crawl_run:
            crawl_run.status = "failed"
            crawl_run.error_message = str(exc)[:2000]
            crawl_run.completed_at = datetime.now(timezone.utc)

            db.commit()

    finally:
        db.close()

        crawl_lock.release()


@router.post("/crawl-runs", status_code=202)
def trigger_crawl(
    background_tasks: BackgroundTasks,
    max_articles: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):

    if max_articles < 1 or max_articles > 100:
        raise HTTPException(
            status_code=400,
            detail="max_articles must be between 1 and 100"
        )

    if not crawl_lock.acquire(blocking=False):
        raise HTTPException(
            status_code=409,
            detail="A crawl is already running."
        )

    try:
        crawl_run = CrawlRun(
            status="pending"
        )

        db.add(crawl_run)
        db.commit()
        db.refresh(crawl_run)

        background_tasks.add_task(
            execute_crawl,
            crawl_run.id,
            max_articles
        )

        return {
            "message": "Crawling started successfully.",
            "crawl_run_id": crawl_run.id,
            "status": crawl_run.status
        }

    except Exception:
        crawl_lock.release()
        raise


@router.get("/crawl-runs")
def get_crawl_runs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):

    runs = db.query(CrawlRun).order_by(
        CrawlRun.created_at.desc()
    ).limit(50).all()

    return [
        {
            "id": run.id,
            "status": run.status,
            "started_at": run.started_at,
            "completed_at": run.completed_at,
            "total_fetched": run.total_fetched,
            "total_inserted": run.total_inserted,
            "total_duplicates": run.total_duplicates,
            "total_categorized": run.total_categorized,
            "total_uncategorized": run.total_uncategorized,
            "total_failed": run.total_failed,
            "results": run.results,
            "error_message": run.error_message
        }
        for run in runs
    ]


@router.get("/crawl-runs/{crawl_run_id}")
def get_crawl_run(
    crawl_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):

    run = db.query(CrawlRun).filter(
        CrawlRun.id == crawl_run_id
    ).first()

    if not run:
        raise HTTPException(
            status_code=404,
            detail="Crawl run not found."
        )

    return {
        "id": run.id,
        "status": run.status,
        "started_at": run.started_at,
        "completed_at": run.completed_at,
        "total_fetched": run.total_fetched,
        "total_inserted": run.total_inserted,
        "total_duplicates": run.total_duplicates,
        "total_categorized": run.total_categorized,
        "total_uncategorized": run.total_uncategorized,
        "total_failed": run.total_failed,
        "results": run.results,
        "error_message": run.error_message
    }