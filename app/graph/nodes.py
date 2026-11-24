from langgraph.types import interrupt

from app.graph.state import BrowserAgentState
from app.services.mantra_portal import (
    capture_captcha,
    click_login as submit_login,
    enter_captcha,
    fill_login_credentials,
    inspect_first_worker_field,
    open_add_worker,
    open_login,
    verify_login as check_login,
)


async def open_mantra_login(state: BrowserAgentState) -> dict:
    return await open_login(state["thread_id"])


async def check_captcha(state: BrowserAgentState) -> dict:
    return await capture_captcha(state["thread_id"])


async def ask_hr_for_captcha(state: BrowserAgentState) -> dict:
    captcha_text = interrupt({
        "action": "ENTER_CAPTCHA",
        "message": "Enter the CAPTCHA shown in the screenshot.",
        "captcha_image_url": state.get("captcha_image_url"),
    })

    captcha_text = str(captcha_text).strip()
    if not captcha_text:
        raise ValueError("CAPTCHA cannot be empty")

    await enter_captcha(state["thread_id"], captcha_text)
    return {"status": "captcha_entered"}


async def click_login(state: BrowserAgentState) -> dict:
    await submit_login(state["thread_id"])
    return {"status": "login_button_clicked"}


async def verify_login(state: BrowserAgentState) -> dict:
    return await check_login(state["thread_id"], state.get("login_url"))


async def ask_hr_to_retry_login(state: BrowserAgentState) -> dict:
    retry_data = interrupt({
        "action": "RETRY_LOGIN",
        "message": state.get("login_error") or "Login failed. Enter corrected credentials.",
        "retry_count": state.get("retry_count", 0),
    })

    username = str(retry_data.get("username", "")).strip()
    password = str(retry_data.get("password", ""))

    if not username or not password:
        raise ValueError("Both username and password are required for retry")

    login_url = await fill_login_credentials(
        state["thread_id"], username, password
    )
    return {
        "retry_count": state.get("retry_count", 0) + 1,
        "login_url": login_url,
        "status": "retry_credentials_filled",
    }


async def open_add_worker_page(state: BrowserAgentState) -> dict:
    return await open_add_worker(state["thread_id"])


async def verify_add_worker_page(state: BrowserAgentState) -> dict:
    return await inspect_first_worker_field(state["thread_id"])
