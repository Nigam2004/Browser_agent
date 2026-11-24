from uuid import uuid4

from fastapi import APIRouter, HTTPException
from langgraph.types import Command

from app.graph.workflow import agent
from app.schemas.session import CaptchaSubmission, LoginRetry
from app.services.browser_sessions import (
    close_all_sessions,
    close_session,
    get_session,
)

router = APIRouter()


def thread_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def format_result(thread_id: str, result: dict) -> dict:
    interrupts = result.get("__interrupt__", ())
    interrupt_payloads = [item.value for item in interrupts]

    return {
        "thread_id": thread_id,
        "status": result.get("status", "running"),
        "captcha_found": result.get("captcha_found", False),
        "captcha_image_url": result.get("captcha_image_url"),
        "login_success": result.get("login_success"),
        "login_error": result.get("login_error"),
        "add_worker_opened": result.get("add_worker_opened", False),
        "first_field": result.get("first_field"),
        "interrupts": interrupt_payloads,
    }


@router.get("/health")
async def health():
    return {"status": "ok", "service": "mantra-browser-agent"}


@router.post("/sessions/start")
async def start_session():
    thread_id = str(uuid4())
    try:
        result = await agent.ainvoke(
            {"thread_id": thread_id, "retry_count": 0},
            config=thread_config(thread_id),
        )
        response = format_result(thread_id, result)
        if response.get("captcha_image_url"):
            response["captcha_image_url"] = (
                f"http://127.0.0.1:8001{response['captcha_image_url']}"
            )
        for item in response["interrupts"]:
            if item.get("captcha_image_url"):
                item["captcha_image_url"] = (
                    f"http://127.0.0.1:8001{item['captcha_image_url']}"
                )
        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/sessions/captcha_fill/{thread_id}")
async def submit_captcha(thread_id: str, body: CaptchaSubmission):
    print("imge fillapi called ")
    try:
        get_session(thread_id)
        result = await agent.ainvoke(
            Command(resume=body.captcha_text),
            config=thread_config(thread_id),
        )
        return format_result(thread_id, result)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/sessions/{thread_id}/retry-login")
async def retry_login(thread_id: str, body: LoginRetry):
    try:
        get_session(thread_id)
        result = await agent.ainvoke(
            Command(resume={"username": body.username, "password": body.password}),
            config=thread_config(thread_id),
        )
        return format_result(thread_id, result)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/sessions/{thread_id}/status")
async def session_status(thread_id: str):
    try:
        get_session(thread_id)
        snapshot = await agent.aget_state(thread_config(thread_id))
        values = snapshot.values or {}
        return {
            "thread_id": thread_id,
            "next": list(snapshot.next),
            "status": values.get("status"),
            "captcha_found": values.get("captcha_found", False),
            "login_success": values.get("login_success"),
            "add_worker_opened": values.get("add_worker_opened", False),
            "first_field": values.get("first_field"),
        }
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/sessions/{thread_id}")
async def close_browser_session(thread_id: str):
    try:
        get_session(thread_id)
        await close_session(thread_id)
        return {"thread_id": thread_id, "status": "browser_closed"}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
