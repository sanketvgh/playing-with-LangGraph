from langgraph.graph.message import MessagesState
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    RemoveMessage,
)
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal, Type
from langchain_core.runnables import RunnableConfig
import time


llm = ChatOllama(model="hermes3:3b", base_url="http://localhost:11434")


class ConversationState(MessagesState):
    summery: str


def call_llm(conversation_state: ConversationState) -> MessagesState:

    summery = conversation_state.get("summery", "")
    messages = None

    if summery:
        system_message = SystemMessage(
            content=f"Summery of conversation earlier: {summery}"
        )

        messages = [system_message] + conversation_state["messages"]

    else:
        messages = conversation_state["messages"]

    return {"messages": llm.invoke(messages)}


def summarize_conversation(conversation_state: ConversationState) -> ConversationState:
    summery = conversation_state.get("summery", "")
    message = ""

    if summery:
        message = """This is summery of the conversation till now: {summery}\n\n
        Extend the summery keep it short and concise and do not miss any important information by taking into account the new messages above:"""
    else:
        message = "Create the Summery of the conversation above keep it short and concise and do not miss any important information:"

    return {
        "messages": [
            RemoveMessage(id=msg.id) for msg in conversation_state["messages"][:-2]
        ],
        "summery": llm.invoke(
            conversation_state["messages"] + [HumanMessage(content=message)]
        ).content,
    }


def should_summarize(
    conversation_state: ConversationState,
) -> Literal["summarize_conversation", Type[END]]:
    return "summarize_conversation" if len(conversation_state["messages"]) >= 5 else END


def run():
    builder = StateGraph(ConversationState)
    builder.add_node("call_llm", call_llm)
    builder.add_node("summarize_conversation", summarize_conversation)

    builder.set_entry_point("call_llm")
    builder.add_conditional_edges(
        "call_llm",
        should_summarize,
    )
    builder.set_finish_point("summarize_conversation")

    memory = MemorySaver()
    complied_state_graph = builder.compile(checkpointer=memory)

    complied_state_graph.get_graph().draw_mermaid_png(
        output_file_path="the_5_chatbot_with_summery.png"
    )

    config: RunnableConfig = {
        "configurable": {
            "thread_id": time.strftime("%d-%m-%Y-%I:%M%p"),
        }
    }

    result = complied_state_graph.invoke(
        ConversationState(messages=[HumanMessage(content="Hello, My Name is Sanket")]),
        config=config,
    )

    print(result)

    result2 = complied_state_graph.invoke(
        ConversationState(messages=[HumanMessage(content="What's my name?")]),
        config=config,
    )

    print(result2)

    result3 = complied_state_graph.invoke(
        ConversationState(
            messages=[HumanMessage(content="What is the capital of France?")]
        ),
        config=config,
    )

    print(result3)

    result4 = complied_state_graph.invoke(
        ConversationState(
            messages=[HumanMessage(content="What is the capital of Germany?")]
        ),
        config=config,
    )

    print(result4)

    result5 = complied_state_graph.invoke(
        ConversationState(
            messages=[HumanMessage(content="What is the capital of India?")]
        ),
        config=config,
    )

    print(result5)

    result6 = complied_state_graph.invoke(
        ConversationState(
            messages=[
                HumanMessage(content="Which animal is the fastest in that country?")
            ]
        ),
        config=config,
    )

    print(result6)

    result7 = complied_state_graph.invoke(
        ConversationState(
            messages=[HumanMessage(content="Which of country do i asked for capital?")]
        ),
        config=config,
    )

    print(result7)

    result8 = complied_state_graph.invoke(
        ConversationState(messages=[HumanMessage(content="What is my name?")]),
        config=config,
    )

    print(result8)
