import os
from typing import Tuple
from app.core.config import settings
from app.core.logging import logger


class StorageClient:
    """Manages document uploads and signed URLs in Google Cloud Storage."""

    def __init__(self):
        self.bucket_name = settings.GCS_BUCKET_CLAIMS
        self.expiry_minutes = settings.GCS_SIGNED_URL_EXPIRY_MINUTES

    async def generate_upload_url(self, claim_id: str, file_name: str, content_type: str) -> Tuple[str, str]:
        """Generates a secure upload destination URL and GCS URI."""
        object_name = f"claims/{claim_id}/{file_name}"
        gcs_uri = f"gs://{self.bucket_name}/{object_name}"

        # In cloud environment, use google.cloud.storage generate_signed_url
        # For local demo, return direct API upload mock endpoint
        upload_url = f"/api/v1/claims/{claim_id}/documents/upload-direct?file={file_name}"
        logger.info(f"Generated upload target: {gcs_uri}")
        return upload_url, gcs_uri
