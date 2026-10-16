from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ClaimGuard AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8080
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Google Cloud & Firebase
    GCP_PROJECT_ID: str = "claimguard-demo-project"
    GCP_REGION: str = "us-central1"
    FIREBASE_PROJECT_ID: str = "claimguard-demo-project"

    # Storage & DocAI
    GCS_BUCKET_CLAIMS: str = "claimguard-claims-documents"
    GCS_SIGNED_URL_EXPIRY_MINUTES: int = 15
    DOCUMENT_AI_LOCATION: str = "us"
    DOCUMENT_AI_PROCESSOR_ID: str = "demo-processor-id"

    # BigQuery
    BIGQUERY_DATASET: str = "claimguard_demo"
    BIGQUERY_CLAIMS_TABLE: str = "claims"
    BIGQUERY_CUSTOMERS_TABLE: str = "customers"
    BIGQUERY_REPAIR_ESTIMATES_TABLE: str = "repair_estimates"

    # Vertex AI / Gemini
    VERTEX_AI_LOCATION: str = "us-central1"
    GEMINI_MODEL_ID: str = "gemini-1.5-pro"
    GEMINI_TEMPERATURE: float = 0.2
    VERTEX_SEARCH_DATA_STORE_ID: str = "insurance-policies-store"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
