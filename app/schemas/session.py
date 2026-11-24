from pydantic import BaseModel, Field


class CaptchaSubmission(BaseModel):
    captcha_text: str = Field(min_length=1, max_length=30)


class LoginRetry(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=1, max_length=300)
