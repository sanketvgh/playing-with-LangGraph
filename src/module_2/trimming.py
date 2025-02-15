from langgraph.graph.message import MessageGraph
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from langchain_core.messages import trim_messages
from langchain_ollama import ChatOllama

messages: list[AnyMessage] = [
    HumanMessage(content="Hello, how are you?"),
    AIMessage(content="I'm doing well, thank you!"),
    HumanMessage(content="What is the capital of France?"),
    AIMessage(content="The capital of France is Paris.")]

llm = ChatOllama(model="hermes3:3b", base_url="http://localhost:11434")


def run1():
    pass


def run():

    builder = MessageGraph()
    builder.add_node("chatbot", lambda state: llm.invoke(
        trim_messages(state, max_tokens=1, strategy="last",
                      token_counter=len, allow_partial=False)))
    builder.set_entry_point("chatbot")
    builder.set_finish_point("chatbot")

    complied_state_graph = builder.compile()

    complied_state_graph.get_graph().draw_mermaid_png(
        output_file_path="trimming.png")

    result = complied_state_graph.invoke(
        messages + [HumanMessage(content="Tell Me where orcas live?")])
    print(result)
