from langchain_core.tools import tool
# from langchain_mistralai import ChatMistralAI
from langchain_ollama import ChatOllama
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition


@tool
def add(a: float, b: float) -> float:
    """ Add two floating points numbers """
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """ Multiply two floating point numbers """
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """ Divide two floating point numbers """
    return a / b


@tool
def minus(a: float, b: float) -> float:
    """ Minus two floating point numbers """
    return a - b


@tool
def convert_int_to_float(a: int) -> float:
    """ convert integer number to float """
    return a / 1


system_message = SystemMessage(content="Your're helpful simple math assistant")


tools = [add, multiply, divide, minus, convert_int_to_float]

llm = ChatOllama(model="qwen2",
                 base_url="http://localhost:11434")
llm_with_tools = llm.bind_tools(tools)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def node_llm_with_tools(state: MessagesState) -> MessagesState:
    message = llm_with_tools.invoke([system_message] + state['messages'])
    return {"messages": [message]}


builder = StateGraph(MessagesState)
builder.add_node('node_llm_with_tools', node_llm_with_tools)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, 'node_llm_with_tools')
builder.add_conditional_edges('node_llm_with_tools', tools_condition)
builder.add_edge("tools", 'node_llm_with_tools')


complied_state_graph = builder.compile()

# complied_state_graph.get_graph().draw_mermaid_png(output_file_path='agent.png')


messages_state = complied_state_graph.invoke(
    {"messages": [
        HumanMessage(
            content="Add 3 and 4. multiply the output by 2. divide the output by 5")
    ]})


for m in messages_state['messages']:
    m.pretty_print()
