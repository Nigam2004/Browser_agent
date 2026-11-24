from pathlib import Path

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from app.core.config import settings
from app.services.browser_sessions import create_session, get_session
from app.services.selectors import selectors


async def open_login(thread_id: str) -> dict:
    if not settings.mantra_url:
        raise ValueError("MANTRA_URL is missing in .env")
    if not settings.mantra_username or not settings.mantra_password:
        raise ValueError("MANTRA_USERNAME or MANTRA_PASSWORD is missing in .env")

    session = await create_session(
        thread_id=thread_id,
        url=settings.mantra_url,
        username=settings.mantra_username,
        password=settings.mantra_password,
        headless=settings.headless,
    )
    print(session.login_url,session.page)
    print("PAGE CLOSED:", session.page.is_closed())
    async with session.lock:
        await session.page.goto(
            settings.mantra_url,
            wait_until="domcontentloaded",
            timeout=settings.timeout_ms,
        )
        # print("mantra opened ")
        # await session.page.locator('input[type="text"]').wait_for(
        #     state="visible", timeout=settings.timeout_ms
        # )
        # await session.page.locator('input[type="text"]').fill(session.username)
        # print("id filled")
        # await session.page.locator('input[type="password"]').wait_for(
        #     state="visible", timeout=settings.timeout_ms
        # )
        # await session.page.locator('input[type="password"]').fill(session.password)
        # print("password filled")
        username_field = session.page.locator(
        'input[type="email"], input[type="text"]'
        ).first
        
        password_field =  session.page.locator(
                        'input[type="password"]'
                    ).first
                   
                    # Check login fields
        if await username_field.count() == 0:
            print("Username field not found")
            await  session.page.pause()
            return
        
        if await password_field.count() == 0:
            print("Password field not found")
            await  session.page.pause()
            return
        
                    # Fill login details
        await username_field.fill("md@technomachinetools.in")
        await password_field.fill("Technotools@202")
        
    return {
        "login_url": session.page.url,
        "status": "credentials_filled",
        "retry_count": 0,
    }


async def capture_captcha(thread_id: str) -> dict:
    session = get_session(thread_id)
    image = session.page.locator(selectors.captcha_image)

    try:
        found = await image.is_visible(timeout=2500)
    except PlaywrightTimeoutError:
        found = False

    if not found:
        return {"captcha_found": False, "captcha_image_url": ""}

    filename = f"{thread_id}_captcha.png"
    path: Path = settings.screenshots_dir / filename
    await image.screenshot(path=str(path))

    return {
        "captcha_found": True,
        "captcha_image_url": f"/screenshots/{filename}",
        "status": "captcha_waiting_for_hr",
    }


async def enter_captcha(thread_id: str, captcha_text: str) -> None:
    session = get_session(thread_id)
    async with session.lock:
        await session.page.get_by_role("textbox", name="Captcha").fill(captcha_text)


async def click_login(thread_id: str) -> None:
    session = get_session(thread_id)
    async with session.lock:
        await session.page.get_by_role("button", name="Log in").click()
        try:
            await session.page.wait_for_load_state(
                "domcontentloaded", timeout=8000
            )
        except PlaywrightTimeoutError:
            pass


async def verify_login(thread_id: str, login_url: str | None) -> dict:
    session = get_session(thread_id)
    page = session.page

    try:
        await page.wait_for_timeout(1500)

        if selectors.login_success:
            success = await page.locator(
                selectors.login_success
            ).is_visible(timeout=3000)
        else:
            success = page.url != (login_url or session.login_url)

        if success:
            return {
                "login_success": True,
                "login_error": "",
                "status": "login_successful",
            }

        error_text = "Login could not be verified."
        if selectors.login_error:
            error = page.locator(selectors.login_error)
            if await error.is_visible(timeout=1000):
                error_text = (await error.inner_text()).strip() or error_text

        return {
            "login_success": False,
            "login_error": error_text,
            "status": "login_failed",
        }

    except PlaywrightTimeoutError:
        return {
            "login_success": False,
            "login_error": "Timed out while verifying login.",
            "status": "login_failed",
        }


async def fill_login_credentials(
    thread_id: str, username: str, password: str
) -> str:
    session = get_session(thread_id)
    session.username = username
    session.password = password

    async with session.lock:
        await session.page.locator(selectors.username).fill(username)
        await session.page.locator(selectors.password).fill(password)

    return session.page.url


async def open_add_worker(thread_id: str) -> dict:
    session = get_session(thread_id)
    page = session.page

    async with session.lock:
        # if selectors.add_worker:
        #     target = page.locator(selectors.add_worker)
        # else:
        #     target = page.get_by_role("button", name=" Add").first
        # print(target)

        # await target.wait_for(state="visible", timeout=settings.timeout_ms)
        # print("timeout")
        # await target.click()
        # print("clicked")
        # try:
        #     await page.wait_for_load_state("domcontentloaded", timeout=8000)
        # except PlaywrightTimeoutError:
        #     pass
        await page.goto(
                'https://mwoc.jindalsteel.com/Master/EmployeeKiosk',
                wait_until="domcontentloaded",
                timeout=60000
           )
        await page.get_by_role("button", name=" Add").click()
        await page.wait_for_timeout(5000)
        await page.locator("#AadharCard").fill("388780287998")
        await page.locator("#FirstName").press_sequentially("nigam",delay=500)
        await page.locator("#MiddleName").press_sequentially("")
        await page.locator("#LastName").press_sequentially("bisoyi",delay=500)
    print("Current URL:", page.url)
    print("Page title:", await page.title())

    return {"add_worker_opened": True, "status": "add_worker_page_opened"}


async def inspect_first_worker_field(thread_id: str) -> dict:
    if not selectors.first_worker_field:
        raise ValueError(
            "Set MANTRA_FIRST_WORKER_FIELD_SELECTOR in .env to the first field on Add Worker page."
        )

    session = get_session(thread_id)
    field = session.page.locator(selectors.first_worker_field).first
    await field.wait_for(state="visible", timeout=settings.timeout_ms)
    details = await field.evaluate(
        """el => ({
            tag: el.tagName,
            type: el.getAttribute('type'),
            name: el.getAttribute('name'),
            id: el.id || null,
            placeholder: el.getAttribute('placeholder'),
            ariaLabel: el.getAttribute('aria-label')
        })"""
    )
    return {
        "first_field": details,
        "status": "first_worker_field_inspected",
    }
