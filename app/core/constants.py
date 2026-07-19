from pathlib import Path

APP_DIR = Path("app")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

UPLOADS_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
REPORTS_DIR = DATA_DIR / "reports"

SUPPORTED_DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}

SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}

SUPPORTED_FILE_EXTENSIONS = (
    SUPPORTED_DOCUMENT_EXTENSIONS
    | SUPPORTED_IMAGE_EXTENSIONS
)

DEFAULT_TOP_K = 5
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

MAX_FILENAME_LENGTH = 255

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

API_PREFIX = "/api/v1"

HEALTH_ROUTE = "/health"

DEFAULT_ENCODING = "utf-8"

DATABASE_POOL_SIZE = 10
DATABASE_MAX_OVERFLOW = 20

VECTOR_COLLECTION_NAME = "legal_documents"

OCR_PROVIDER_GROQ = "groq"

ENV_DEVELOPMENT = "development"
ENV_PRODUCTION = "production"
ENV_TESTING = "testing"