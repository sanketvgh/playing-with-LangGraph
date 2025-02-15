from langgraph.graph.message import MessageGraph
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage, RemoveMessage
from langchain_ollama import ChatOllama

messages: list[AnyMessage] = [
    HumanMessage(content="Hello, how are you?"),
    AIMessage(content="I'm doing well, thank you!"),
    HumanMessage(content="What is the capital of France?"),
    AIMessage(content="The capital of France is Paris.")]

llm = ChatOllama(model="hermes3:3b", base_url="http://localhost:11434")


def recent_messages(state: list[AnyMessage]) -> list[AnyMessage]:
    return [RemoveMessage(id=message.id) for message in state[:-2]]


def run1():
    pass


def run():

    builder = MessageGraph()
    builder.add_node("recent_messages", recent_messages)
    builder.add_node("chatbot", lambda state: llm.invoke(state))
    builder.set_entry_point("recent_messages")
    builder.add_edge("recent_messages", "chatbot")
    builder.set_finish_point("chatbot")

    complied_state_graph = builder.compile()

    complied_state_graph.get_graph().draw_mermaid_png(
        output_file_path="filtering_and_trimming.png")

    result = complied_state_graph.invoke(
        messages + [HumanMessage(content="What is the capital of India?")])
    print(result)
