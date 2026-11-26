import re
async def select_date_picker(page, dob: str,selector:str):
    # dob format: DD/MM/YYYY
    day, month, year = dob.split("/")

    # Open the datepicker
    await page.locator(selector).click()

    picker = page.locator(".datepicker:visible")

    # Step 1: Click the month/year header
    await picker.locator(
        ".datepicker-days th.datepicker-switch"
    ).click()

    # Step 2: Switch to year selection
    await picker.locator(
        ".datepicker-months th.datepicker-switch"
    ).click()

    # Step 3: Select year
    await picker.locator(
        ".datepicker-years span.year"
    ).filter(has_text=year).click()

    # Step 4: Select month
    month_names = {
        "01": "Jan", "02": "Feb", "03": "Mar",
        "04": "Apr", "05": "May", "06": "Jun",
        "07": "Jul", "08": "Aug", "09": "Sep",
        "10": "Oct", "11": "Nov", "12": "Dec",
    }

    await picker.locator(
        ".datepicker-months span.month"
    ).filter(has_text=month_names[month]).click()

    # Step 5: Select day
    await  picker.locator(
    ".datepicker-days td.day:not(.old):not(.new):not(.disabled)"
).filter(
    has_text=re.compile(rf"^\s*{int(day)}\s*$")
).click()
