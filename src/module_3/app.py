import time
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessageGraph
from langchain_core.messages import HumanMessage
from ai import llm
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

db_uri = (
    "postgresql://postgres:postgres@localhost:15432/langgraph_module_3?sslmode=disable"
)

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}


def run():

    with ConnectionPool(conninfo=db_uri, max_size=20, kwargs=connection_kwargs) as pool:

        checkpointer = PostgresSaver(pool)

        # NOTE: you need to call .setup() the first time you're using your checkpointer
        # checkpointer.setup()

        configurable = {
            "thread_id": time.strftime(
                # "Module 3 UX & Human-in-the-Loop: %d-%m-%Y, %I:%M%p"
                "module_3_human_in_the_loop"
            )
        }

        config: RunnableConfig = {"configurable": configurable}

        builder = MessageGraph()
        builder.add_node("hermes_ai", lambda state: llm.invoke(state))

        builder.set_entry_point("hermes_ai")
        builder.set_finish_point("hermes_ai")

        complied_state_graph = builder.compile(checkpointer=checkpointer)

        # complied_state_graph.invoke(, )

        for chunk in complied_state_graph.stream(
            [HumanMessage("Tell me about India?")], config=config, stream_mode="values"
        ):
            print(chunk)
