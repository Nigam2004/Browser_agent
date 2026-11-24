from typing import TypedDict


class BrowserAgentState(TypedDict, total=False):
    thread_id: str
    login_url: str
    captcha_found: bool
    captcha_image_url: str
    login_success: bool
    login_error: str
    retry_count: int
    add_worker_opened: bool
    first_field: dict
    status: str
