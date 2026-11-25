import asyncio
import os

from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

MANTRA_URL = os.getenv("MANTRA_URL")
MANTRA_USERNAME = os.getenv("MANTRA_USERNAME")
MANTRA_PASSWORD = os.getenv("MANTRA_PASSWORD")


async def open_mantra_portal():

    if not all([MANTRA_URL, MANTRA_USERNAME, MANTRA_PASSWORD]):
        raise ValueError("Mantra credentials or URL missing in .env")

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False
        )

        page = await browser.new_page()

        try:
            # Open portal
            await page.goto(
                MANTRA_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("Mantra portal opened")
            print("Page title:", await page.title())

            # Identify login fields
            username_field = page.locator(
                'input[type="email"], input[type="text"]'
            ).first

            password_field = page.locator(
                'input[type="password"]'
            ).first
           
            # Check login fields
            if await username_field.count() == 0:
                print("Username field not found")
                await page.pause()
                return

            if await password_field.count() == 0:
                print("Password field not found")
                await page.pause()
                return

            # Fill login details
            await username_field.fill("md@technomachinetools.in")
            await password_field.fill("Technotools@202")

            print("Login details entered")

            captcha_image = page.locator("#imgcaptcha")
            if await captcha_image.count() > 0:
                print("CAPTCHA image detected")
                await captcha_image.screenshot(
                path="uploads/captcha.png")

            else:
                print("CAPTCHA image not found")
            await page.get_by_role("textbox", name="Captcha").click()
            await page.wait_for_timeout(10000)
            await page.get_by_role("button", name="Log in").click()
            # Allow the portal to respond
            await page.wait_for_timeout(10000)
            # await page.get_by_role("link", name="Enrollment ").click()
            # await page.locator("#div_LeftMenu").get_by_role("https://mwoc.jindalsteel.com/Master/EmployeeKiosk", name="Add Worker").click()
            print("wait 4sec")
            await page.goto(
                'https://mwoc.jindalsteel.com/Master/EmployeeKiosk',
                wait_until="domcontentloaded",
                timeout=60000
            )
            await page.get_by_role("button", name=" Add").click()
            await page.locator("#AadharCard").fill("388780287998")
            await page.locator("#FirstName").press_sequentially("nigam",delay=500)
            await page.locator("#MiddleName").press_sequentially("")
            await page.locator("#LastName").press_sequentially("bisoyi",delay=500)
            await page.get_by_role("textbox", name="Contact Number*").fill("7606995528")
##DBand DOJ 
            await page.get_by_role("textbox", name="Old Gate-Pass Id**").fill(" ")
            await page.get_by_role("textbox", name="Father Name*").fill("SANU PRADHAN")
            await page.locator("#s2id_MaritalStatus").get_by_role("link", name="Please Select").click()
            # await page.get_by_role("combobox", name="Marital Status*").click()
            await page.get_by_role("combobox", name="Marital Status*").fill("married")
            await page.locator("#select2-result-label-68").click()
            # await page.locator("#s2id_MaritalStatus").get_by_role("link", name="Married").click()
            # await page.get_by_role("combobox", name="Marital Status*").press("Enter")
            # await page.locator("#divCompCode").get_by_role("link", name="JINDAL STEEL ODISHA").click()
            # await  page.locator("#s2id_CompanyLocation").get_by_role("link", name="Angul(JSO)").click()
            # await page.locator("#s2id_Plant > .select2-choice").get_by_role("link", name="Iron").click   ()
            # await page.locator("#divEntityType").get_by_role("link", name="WORKER", exact=True).click()
            # await page.locator("#s2id_Designation").get_by_role("link", name="HR").click()
            # await page.locator("#s2id_Shift > .select2-choice").get_by_role("link", name="Shift G").click()
            # await page.get_by_role("link", name="PF Avail").click()
            # await page.get_by_role("textbox", name="PF Member ID*").fill("apkp1234567890")
            # await page.get_by_role("textbox", name="UAN *").fill("1234567890")
            # await page.get_by_role("link", name="B+").click()
            print("Current URL:", page.url)
            print("Page title:", await page.title())
            # Keep browser open for inspection
            await page.pause()

        except Exception as exc:
            print("Portal automation error:", str(exc))

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(open_mantra_portal())