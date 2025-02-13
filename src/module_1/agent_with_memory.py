from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph.message import MessageGraph
from langgraph.graph import START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig


@tool
def multiply(x: int, y: int) -> int:
    """Multiply x by y"""
    return x * y


@tool
def add(x: int, y: int) -> int:
    """Add x and y"""
    return x + y


tools = [multiply, add]


def run():

    llm = ChatOllama(model="qwen2", base_url="http://localhost:11434")
    llm_with_tools = llm.bind_tools(tools)

    builder = MessageGraph()
    builder.add_node("ai_node", lambda state: llm_with_tools.invoke(state))
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "ai_node")
    builder.add_conditional_edges("ai_node", tools_condition)
    builder.add_edge("tools", "ai_node")

    memory = MemorySaver()
    compiled_state_graph = builder.compile(checkpointer=memory)

    # compiled_state_graph.get_graph().draw_mermaid_png(
    #     output_file_path="agent_with_memory.png")

    config: RunnableConfig = {"configurable": {
        "thread_id": "sanket"
    }}

    compiled_state_graph.invoke(
        HumanMessage(content="What is 32 + 62?"), config=config)

    compiled_state_graph.invoke(
        HumanMessage(content="Multiply that by 33 tell me the result in the k format?"), config=config)
