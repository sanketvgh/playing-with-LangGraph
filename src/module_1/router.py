from langgraph.prebuilt import tools_condition
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
# from langgraph.graph import Sa
from typing_extensions import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_mistralai import ChatMistralAI


@tool
def multiply(a: int, b: int) -> int:
    """ Multiply two number """
    return a * b


llm = ChatMistralAI(model_name="mistral-large-latest")
llm_with_tools = llm.bind_tools([multiply])


class MessagesState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


def node_1(state: MessagesState) -> MessagesState:
    print('state', state)
    return {"messages": [AIMessage(content="Hi There! How can I help you?"),
                         #  HumanMessage(content="What is 2 times 3?")]}
                         HumanMessage(content="Do you like flowers?")]}


def node_with_llm_tool_invocation(state: MessagesState) -> MessagesState:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("node_1", node_1)
builder.add_node("node_with_llm_tool_invocation",
                 node_with_llm_tool_invocation)
builder.add_node("tools", ToolNode([multiply]))


builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_with_llm_tool_invocation")
builder.add_conditional_edges("node_with_llm_tool_invocation", tools_condition)
builder.add_edge("tools", END)

compiled_state_graph = builder.compile()

# compiled_state_graph.get_graph().draw_mermaid_png(
#     output_file_path="graph.png")

final_state = compiled_state_graph.invoke(
    {"messages": [HumanMessage(content="Hello")]})

print(final_state)
