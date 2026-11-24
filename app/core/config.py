import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


class Settings:
    mantra_url = env("MANTRA_URL")
    mantra_username = env("MANTRA_USERNAME")
    mantra_password = env("MANTRA_PASSWORD")

    headless = env("BROWSER_HEADLESS", "false").lower() == "true"
    timeout_ms = int(env("BROWSER_TIMEOUT_MS", "60000"))

    data_dir = BASE_DIR / "data"
    screenshots_dir = BASE_DIR / "screenshots"


settings = Settings()
settings.screenshots_dir.mkdir(parents=True, exist_ok=True)
