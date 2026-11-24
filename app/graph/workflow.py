from langgraph.graph import END, START, StateGraph
from app.core.database import create_checkpointer
from app.graph.nodes import (
    ask_hr_for_captcha,
    ask_hr_to_retry_login,
    check_captcha,
    click_login,
    open_add_worker_page,
    open_mantra_login,
    # verify_add_worker_page,
    verify_login,
)
from app.graph.state import BrowserAgentState


def route_after_captcha(state: BrowserAgentState) -> str:
    return "ask_hr_for_captcha" if state.get("captcha_found") else "click_login"


def route_after_login(state: BrowserAgentState) -> str:
    return "open_add_worker_page" if state.get("login_success") else "ask_hr_to_retry_login"


def build_agent():
    builder = StateGraph(BrowserAgentState)

    builder.add_node("open_mantra_login", open_mantra_login)
    builder.add_node("check_captcha", check_captcha)
    builder.add_node("ask_hr_for_captcha", ask_hr_for_captcha)
    builder.add_node("click_login", click_login)
    builder.add_node("verify_login", verify_login)
    builder.add_node("ask_hr_to_retry_login", ask_hr_to_retry_login)
    builder.add_node("open_add_worker_page", open_add_worker_page)
    # builder.add_node("verify_add_worker_page", verify_add_worker_page)

    builder.add_edge(START, "open_mantra_login")
    builder.add_edge("open_mantra_login", "check_captcha")

    builder.add_conditional_edges(
        "check_captcha",
        route_after_captcha,
        {
            "ask_hr_for_captcha": "ask_hr_for_captcha",
            "click_login": "click_login",
        },
    )

    builder.add_edge("ask_hr_for_captcha", "click_login")
    builder.add_edge("click_login", "verify_login")

    builder.add_conditional_edges(
        "verify_login",
        route_after_login,
        {
            "open_add_worker_page": "open_add_worker_page",
            "ask_hr_to_retry_login": "ask_hr_to_retry_login",
        },
    )

    # After HR supplies corrected credentials, re-check CAPTCHA before clicking Login.
    builder.add_edge("ask_hr_to_retry_login", "check_captcha")
    builder.add_edge("open_add_worker_page", END)
    # builder.add_edge("open_add_worker_page", "verify_add_worker_page")
    # builder.add_edge("verify_add_worker_page", END)

    return builder.compile(checkpointer=create_checkpointer())


agent = build_agent()
