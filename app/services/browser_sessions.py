import asyncio
from dataclasses import dataclass

from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright


@dataclass
class BrowserSession:
    playwright: Playwright
    browser: Browser
    context: BrowserContext
    page: Page
    username: str
    password: str
    login_url: str
    lock: asyncio.Lock


SESSIONS: dict[str, BrowserSession] = {}


def get_session(thread_id: str) -> BrowserSession:
    session = SESSIONS.get(thread_id)
    if session is None:
        raise KeyError(f"No active browser session for thread_id={thread_id}")
    return session


async def create_session(
    thread_id: str,
    url: str,
    username: str,
    password: str,
    headless: bool,
) -> BrowserSession:
    print("session creted started")
    if thread_id in SESSIONS:
        await close_session(thread_id)

    pw = await async_playwright().start()
    print("async_playwright started")
    browser = await pw.chromium.launch(headless=headless)
    print("browser started")
    context = await browser.new_context()
    page = await context.new_page()

    session = BrowserSession(
        playwright=pw,
        browser=browser,
        context=context,
        page=page,
        username=username,
        password=password,
        login_url=url,
        lock=asyncio.Lock(),
    )
    SESSIONS[thread_id] = session
    return session


async def close_session(thread_id: str) -> None:
    session = SESSIONS.pop(thread_id, None)
    if session is None:
        return
    try:
        await session.context.close()
    finally:
        try:
            await session.browser.close()
        finally:
            await session.playwright.stop()


async def close_all_sessions() -> None:
    for thread_id in list(SESSIONS):
        await close_session(thread_id)
