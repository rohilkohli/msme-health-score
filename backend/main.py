from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from models.database import init_db
from routers import auth, msme, data_sources, health_score, credit_assessment, dashboard, ingestion

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered MSME Financial Health Score Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(msme.router, prefix="/api/msme", tags=["MSME Management"])
app.include_router(data_sources.router, prefix="/api/data-sources", tags=["Data Sources"])
app.include_router(health_score.router, prefix="/api/health-score", tags=["Health Score"])
app.include_router(credit_assessment.router, prefix="/api/credit-assessment", tags=["Credit Assessment"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(ingestion.router, prefix="/api/ingestion", tags=["Ingestion"])


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/")
def root():
    return {
        "message": "MSME Financial Health Score API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }
