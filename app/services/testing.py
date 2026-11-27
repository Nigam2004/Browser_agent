import asyncio
import os
import re
from app.services.date_picker import select_date_picker
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
            ##gender selection
            await page.locator("#divGender").get_by_role("link", name="Please Select").click()
            await page.get_by_role("combobox", name="Gender", exact=True).fill("female")
            await page.get_by_role("combobox", name="Gender", exact=True).press("Enter")
            #dob date picker
            await select_date_picker(page, "01/04/2004","#DOB")
            #doj date picker
            await select_date_picker(page, "12/11/2026","#DOJ")
            #doj date picker
            await page.get_by_role("textbox", name="Date Of Deployment*").click()
            #old gate pass fill
            await page.get_by_role("textbox", name="Old Gate-Pass Id**").fill(" ")
            #father name fill
            await page.get_by_role("textbox", name="Father Name*").fill("SANU PRADHAN")
            #marital status selection
            await page.locator("#s2id_MaritalStatus").get_by_role("link", name="Please Select").click()
            await page.get_by_role("combobox", name="Marital Status*").click()
            await page.get_by_role("combobox", name="Marital Status*").fill("married")
            await page.get_by_role("combobox", name="Marital Status*").press("Enter")
            #princple employer
            await page.locator("#divCompCode").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen10_search").fill("jindal steel odisha")
            await page.locator("#s2id_autogen10_search").press("Enter")
            await page.wait_for_timeout(2000)
            #pland details
            await page.locator("#s2id_Plant > .select2-choice").click()
            await page.get_by_role("combobox", name="PlantPlant*Height Pass").fill("iron")
            await page.get_by_role("combobox", name="PlantPlant*Height Pass").press("Enter")
            await page.wait_for_timeout(2000)
            #entity type
            await page.locator("#divEntityType").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen6_search").fill("worker")
            await page.locator("#s2id_autogen6_search").press("Enter")
            await page.wait_for_timeout(2000)
            #designation
            await page.locator("#s2id_Designation > .select2-choice").click()
            await page.get_by_role("combobox", name="Designation", exact=True).fill("hr")
            await page.get_by_role("combobox", name="Designation", exact=True).press("Enter")
            await page.wait_for_timeout(2000)
            #shift
            await page.locator("#s2id_Shift > .select2-choice").click()
            await page.locator("#s2id_autogen14_search").fill("g")
            await page.locator("#s2id_autogen14_search").press("Enter")
            await page.wait_for_timeout(2000)
            #pf details
            await page.get_by_role("link", name="Please Select").first.click()
            await page.locator("#s2id_autogen59_search").fill("avail")
            await page.locator("#s2id_autogen59_search").press("Enter")
            await page.get_by_role("textbox", name="PF Member ID*").fill("APKKP16079000000010265")
            await page.get_by_role("textbox", name="UAN *").fill("101242580176")
            await page.wait_for_timeout(2000)
            #blood group
            await page.get_by_role("link", name="Please Select").first.click()
            await page.locator("#s2id_autogen29_search").fill("a+")
            await page.locator("#s2id_autogen29_search").press("Enter")
            await page.wait_for_timeout(2000)
            #work order
            await page.locator("#s2id_WorkOrder > .select2-choice").click()
            await page.locator("#s2id_autogen20_search").fill("4097004978")
            await page.locator("#s2id_autogen20_search").press("Enter")
            await page.wait_for_timeout(2000)
            #manpower type
            await page.locator("#s2id_WorkOrderSubType > .select2-choice").click()
            await page.locator("#s2id_autogen32_search").fill("Approved Manpower")
            await page.locator("#s2id_autogen32_search").press("Enter")
            await page.wait_for_timeout(2000)
            #hight pass
            await page.locator("#ISHeightPassRequired").click()
            await page.wait_for_timeout(1000)
            #emergency contact number
            await page.locator("#EmergencyContactNo").fill("851183107")
            await page.wait_for_timeout(1000)
            #bank details
            await page.get_by_role("link", name="Please Select").first.click()
            await page.locator("#s2id_autogen28_search").fill("Karnataka Bank")
            await page.locator("#s2id_autogen28_search").press("Enter")
            await page.locator("#BankAccountNo").fill("0332500101244201")
            await  page.locator("#IFSCNo").fill("KARB0000033")
            await page.wait_for_timeout(2000)
            #qualification
            await page.locator("#s2id_Qualification").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen5_search").fill("below")
            await page.locator("#s2id_autogen5_search").press("Enter")
            await page.get_by_role("textbox", name="Qualification Grade").fill("1st class")
            await page.wait_for_timeout(2000)
            #nomini details
            await page.get_by_role("textbox", name="Nominee Name *").fill("babu bisoyi")
            await page.get_by_role("textbox", name="Nominee Relation").fill("father")
            await page.wait_for_timeout(2000)
            #nationality
            await page.locator("#s2id_Nationality").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen46_search").fill("india")
            await page.locator("#s2id_autogen46_search").press("Enter")
            await page.wait_for_timeout(2000)
            #esic
            await page.get_by_role("link", name="Please Select").first.click()
            await page.locator("#s2id_autogen49_search").fill("esic")
            await page.locator("#s2id_autogen49_search").press("Enter")
            await page.locator("#ESIC").fill("4405162783")
            await page.wait_for_timeout(2000)
            #experience
            await page.locator("#Experienceyrs").fill("2")
            await page.locator("#Experiencemon").fill("2")
            await page.wait_for_timeout(2000)
            #living stay
            await page.locator("#s2id_LivingStay > .select2-choice").click()
            await page.locator("#s2id_autogen39_search").fill("rented")
            await page.locator("#s2id_autogen39_search").press("Enter")
            await page.wait_for_timeout(2000)
            #famili planing
            await page.locator("#s2id_FamilyPlanning").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen40_search").fill("yes")
            await page.locator("#s2id_autogen40_search").press("Enter")
            await page.wait_for_timeout(2000)
            #children details
            await page.locator("#s2id_NumberOfChildren").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen45_search").fill("2")
            await page.locator("#s2id_autogen45_search").press("Enter")
            
            #religion
            await page.locator("#s2id_Religion").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen51_search").fill("hindu")
            await page.locator("#s2id_autogen51_search").press("Enter")
            await page.wait_for_timeout(2000)
            #caste selection
            await page.get_by_text("Caste * Please Select").click()
            await page.locator("#s2id_autogen52_search").fill("obc")
            await page.locator("#s2id_autogen52_search").press("Enter")
            await page.wait_for_timeout(2000)
            #police verification
            await page.locator("#s2id_PoliceVerification").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen53_search").fill("no")
            await page.locator("#s2id_autogen53_search").press("Enter")
            #mobile allow
            await page.locator("#s2id_MobileAllowed").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen54_search").fill("no")
            await page.locator("#s2id_autogen54_search").press("Enter")
            #land type
            await page.get_by_text("Land Type Please Select Land").click()
            await page.locator("#s2id_autogen55_search").fill("other")
            await page.locator("#s2id_autogen55_search").press("Enter")
            #week off
            await page.locator("#DivWeekoff1").get_by_role("link", name="Please Select").click()
            await page.locator("#s2id_autogen30_search").fill("sunday")
            await page.locator("#s2id_autogen30_search").press("Enter")
            #skill catagory
            await page.locator("#s2id_SkillCategory > .select2-choice").click()
            await page.locator("#s2id_autogen31_search").fill("skilled")
            await page.locator("#s2id_autogen31_search").press("Enter")
            #vaccine details
            await page.get_by_text("Covid19 Vaccine Please Select").click()
            await page.locator("#s2id_autogen50_search").fill("covaxin")
            await page.locator("#s2id_autogen50_search").press("Enter")
            #wage information
            await page.get_by_text("Wage Type* Please Select Wage").click()
            await page.locator("#s2id_autogen56_search").fill("monthly")
            await page.locator("#s2id_autogen56_search").press("Enter")
            await page.get_by_role("spinbutton", name="Amount*").fill("20000")
            await page.get_by_role("spinbutton", name="Minimum Wages Per Day*").fill("580")
            await page.locator("#WageSpecialAllowance").fill("0")
            await page.wait_for_timeout(2000)
            #present address
            await page.get_by_text("Present Country* Please").click()
            await page.locator("#s2id_autogen36_search").fill("india")
            await page.locator("#s2id_autogen36_search").press("Enter")
            await page.wait_for_timeout(1000)
            await page.get_by_text("Present State* Please").click()
            await page.locator("#s2id_autogen35_search").fill("odisha")
            await page.locator("#s2id_autogen35_search").press("Enter")
            await page.wait_for_timeout(1000)
            await page.get_by_text("Present District Present").click()
            await page.locator("#s2id_autogen61_search").fill("angul")
            await page.locator("#s2id_autogen61_search").press("Enter")
            await page.locator("#PresAddress").fill("mathura,polasara")
            await page.locator("#PresentVillage").fill("mathura")
            await page.get_by_role("textbox", name="Present Village* Present").fill("polasara")
            await page.get_by_role("textbox", name="Present Post*").fill("mathura")
            await page.locator("#PresPincode").fill("761105")
            # same as present addres 
            # await page.locator("#chkSameAsPresent").click()
            #permanent address
            await page.get_by_text("Permanent Country Please").click()
            await page.locator("#s2id_autogen37_search").fill("india")
            await page.locator("#s2id_autogen37_search").press("Enter")
            await page.wait_for_timeout(1000)
            await page.get_by_text("Permanent State* Permanent").click()
            await page.locator("#s2id_autogen38_search").fill("odisha")
            await page.locator("#s2id_autogen38_search").press("Enter")
            await page.wait_for_timeout(1000)
            await page.get_by_text("Permanent District* Permanent").click()
            await page.locator("#s2id_autogen60_search").fill("angul")
            await page.locator("#s2id_autogen60_search").press("Enter")
            await page.get_by_role("textbox", name="Permanent Address").fill("mathura,polasara")
            await page.get_by_role("textbox", name="Permanent Village*").fill("mathura")
            await page.get_by_role("textbox", name="Permanent Tehsil*").fill("polasara")
            await page.get_by_role("textbox", name="Permanent Post*").fill("mathura")
            await page.locator("#PrmPincode").fill("761105")
            #choose picture
            await page.get_by_role("button", name="Choose File").set_input_files("images\Screenshot 2026-11-25 114113.png")

            #select documentupload
            await page.locator("#s2id_Document > .select2-choice").click()
            await page.locator("#s2id_autogen27_search").fill("adhar")
            await page.locator("#s2id_autogen27_search").press("Enter")
            await page.get_by_text("Upload Document *").set_input_files("images\khageswar off.pdf")
            await page.get_by_title("Upload Document").click()



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