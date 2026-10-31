# NEPSE Intelligence – Stock Market Dashboard

A full-stack stock market intelligence platform for Nepal's stock market (NEPSE), featuring financial news aggregation, stock market data management, and market analytics.

## Tech Stack

- **Frontend:** React, JavaScript, Tailwind CSS
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT
- **Version Control:** Git, GitHub

## Data Sources

Financial news crawlers are designed for:

- [MeroLagani](https://merolagani.com/)
- [ShareSansar](https://www.sharesansar.com/)
- [NEPSE Alpha](https://nepsealpha.com/)
- [Bizmandu](https://bizmandu.com/)

Historical NEPSE trading data integration is subject to authorized data access.

## Key Features

- Financial news aggregation and categorization.
- Company and historical stock price management.
- Stock market analytics.
- Role-based access control (Admin, Analyst, Viewer).
- Automated news crawling and management.
- Interactive stock market dashboard.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/companies` | Get tracked companies |
| GET | `/api/companies/{id}/prices?range=30d` | Get historical prices |
| GET | `/api/news/` | Get financial news |
| GET | `/api/companies/{id}/behavior-summary` | Get market behavior analysis |
| POST | `/api/admin/crawl-runs` | Trigger a crawl |

**API Documentation:** `http://localhost:8000/docs`

## Installation & Setup

### 1. Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/nepse-intelligence.git
cd nepse-intelligence
```

**FOR BACKEND**
```
cd backend
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

alembic upgrade head
uvicorn app.main:app --reload
```
**FOR FRONTEND**
```
cd frontend

npm install
npm run dev
```