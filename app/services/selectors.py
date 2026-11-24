from dataclasses import dataclass

from app.core.config import env


@dataclass(frozen=True)
class PortalSelectors:
    username: str = env("MANTRA_USERNAME_SELECTOR", 'input[name="UserName"]')
    password: str = env("MANTRA_PASSWORD_SELECTOR", 'input[name="Password"]')
    captcha_image: str = env("MANTRA_CAPTCHA_IMAGE_SELECTOR", "#imgcaptcha")
    captcha_input: str = env("MANTRA_CAPTCHA_INPUT_SELECTOR", 'input[name="Captcha"]')
    login_button: str = env("MANTRA_LOGIN_BUTTON_SELECTOR", 'button:has-text("Login")')
    login_success: str = env("MANTRA_LOGIN_SUCCESS_SELECTOR")
    login_error: str = env("MANTRA_LOGIN_ERROR_SELECTOR")
    add_worker: str = env("MANTRA_ADD_WORKER_SELECTOR")
    first_worker_field: str = env("MANTRA_FIRST_WORKER_FIELD_SELECTOR")


selectors = PortalSelectors()
