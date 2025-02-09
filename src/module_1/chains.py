
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_mistralai import ChatMistralAI
from configs.settings import settings
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END


import os


os.environ.update({
    "MISTRAL_API_KEY": settings.mistral_api_key,
    "LANGSMITH_TRACING": settings.langsmith_tracing,
    "LANGSMITH_API_KEY": settings.langsmith_api_key,
    "LANGSMITH_ENDPOINT": settings.langsmith_endpoint,
    "LANGSMITH_PROJECT": settings.langsmith_project_name
})

messages = [
    AIMessage(
        content="So you said you were researching ocean mammals?",
        name="Modal"),


    HumanMessage(
        content="Yes, I'm interested in whales and dolphins.", name="sanket"),
    AIMessage(content="What about the whales?", name="Modal"),


    HumanMessage(
        content="I'm interested in blue whales and sperm whales.",
        name="sanket"),


    AIMessage(content="What's your favorite ocean mammal?", name="Modal"),
    HumanMessage(content="I like dolphins.", name="sanket"),
]


llm = ChatMistralAI(model="mistral-large-latest")


@tool
def perform_light_switch_action(command: Literal["on", "off"]) -> bool:
    """Perform an action on the light switch as per the command"""
    return command == "on"


llm_with_tools = llm.bind_tools([perform_light_switch_action])

# result_message = llm_with_tools.invoke([HumanMessage(
#     content="Can you please turn the light on?")])
# pprint(result_message)


# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]


class State(MessagesState):
    pass


def node_tool_calling_with_llm(state: State) -> State:
    print('Called node_tool_calling_with_llm')
    result_message = llm_with_tools.invoke(state["messages"])
    return {"messages": [result_message]}


builder = StateGraph(State)
builder.add_node("tool_calling_with_llm", node_tool_calling_with_llm)
builder.add_edge(START, "tool_calling_with_llm")
builder.add_edge("tool_calling_with_llm", END)


graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


print(graph.invoke({"messages": [HumanMessage(
    content="Hello, how are you?"), AIMessage(
    content="I'm doing well, thank you for asking."), HumanMessage(
    content="Can you please turn the light on?")]}))
