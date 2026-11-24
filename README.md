# Mantra Browser Automation Agent

A separate FastAPI service that automates the Mantra login workflow with async Playwright and LangGraph.

## Project layout

```text
app/
├── api/          # HTTP routes and router
├── core/         # Runtime configuration and graph checkpointer
├── graph/        # Workflow state, nodes, and graph
├── schemas/      # API request schemas
├── services/     # Browser sessions, portal actions, and selectors
└── main.py       # FastAPI application
data/             # Application data
screenshots/      # Runtime CAPTCHA screenshots
```

## 1. Create the environment

Open PowerShell in this folder:

```powershell
uv sync
.venv\Scripts\activate
Copy-Item .env.example .env
uv run playwright install chromium
```

Edit `.env` and set the real portal URL, credentials, and CSS selectors.

## 2. Start the service

```powershell
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
uv run python run.py
uv run python -m app.services.testing
```

Open:
- API docs: http://127.0.0.1:8001/docs
- Health: http://127.0.0.1:8001/health

## 3. API sequence

1. `POST /sessions/start` — starts browser and login workflow.
2. If response contains `action: ENTER_CAPTCHA`, open `captcha_image_url` and call `POST /sessions/{thread_id}/captcha`.
3. If response contains `action: RETRY_LOGIN`, call `POST /sessions/{thread_id}/retry-login` with corrected username/password.
4. If login succeeds, the agent opens Add Worker and inspects the configured first field.
5. `GET /sessions/{thread_id}/status` checks current workflow state.
6. `DELETE /sessions/{thread_id}` closes the browser session.

Use the same `thread_id` for all resume calls.

## 4. Important configuration

The portal's real HTML selectors are not known from the flowchart. Update these `.env` values after inspecting the Mantra login page:

- `MANTRA_USERNAME_SELECTOR`
- `MANTRA_PASSWORD_SELECTOR`
- `MANTRA_CAPTCHA_IMAGE_SELECTOR`
- `MANTRA_CAPTCHA_INPUT_SELECTOR`
- `MANTRA_LOGIN_BUTTON_SELECTOR`
- `MANTRA_LOGIN_SUCCESS_SELECTOR` (strongly recommended)
- `MANTRA_LOGIN_ERROR_SELECTOR`
- `MANTRA_ADD_WORKER_SELECTOR`
- `MANTRA_FIRST_WORKER_FIELD_SELECTOR`

The default selectors are examples, not verified Mantra selectors. If they do not match the portal, Playwright will report a locator timeout.

## 5. Current scope

This version implements the supplied flowchart up to **Inspect First Worker Field**. It does not yet fill worker details, handle dropdown selections, upload worker documents, or submit a gate pass.

## 6. Important limitations

- Uses `InMemorySaver` to avoid `aiosqlite` for local development. Checkpoints are lost if the service restarts.
- Browser sessions are stored in process memory. Run one Uvicorn worker only; do not use `--workers 2` or multiple replicas.
- Keep this service on a trusted machine/network. Do not expose the API publicly without authentication, HTTPS, authorization, and secret management.
- Do not log passwords or CAPTCHA values.
- CAPTCHA is entered by an authorized HR user; this agent does not solve or bypass CAPTCHA.
- A browser process cannot be restored from a LangGraph checkpoint. The live browser session is maintained separately in memory.
