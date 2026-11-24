from langgraph.checkpoint.memory import InMemorySaver


def create_checkpointer() -> InMemorySaver:
    return InMemorySaver()
