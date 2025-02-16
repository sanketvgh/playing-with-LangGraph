from configs.settings import settings
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
import time
from langgraph.graph.message import MessageGraph
import sqlite3
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="hermes3:3b", base_url="http://localhost:11434")


def run():

    # Open the connection to SQLite Cloud

    conn = sqlite3.connect(":memory:", check_same_thread=False)
    # memory = SqliteSaver(conn)

    builder = MessageGraph()
    builder.add_node("chatbot", lambda state: llm.invoke(state))
    builder.set_entry_point("chatbot")
    builder.set_finish_point("chatbot")

    config: RunnableConfig = {
        "configurable": {"thread_id": time.strftime("%d-%m-%Y-%I:%M%p")}
    }

    complied_state_graph = builder.compile(checkpointer=memory)

    complied_state_graph.invoke([HumanMessage("Who are you?")], config=config)

    complied_state_graph.invoke(
        [HumanMessage("What is capital of India")], config=config
    )

    complied_state_graph.invoke(
        [HumanMessage("Which question I previous asked?")], config=config
    )

    conn.close()
