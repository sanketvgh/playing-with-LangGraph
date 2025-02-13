from langgraph.graph import StateGraph, START, END
from typing import Annotated


def node_1(state: int) -> int:
    print(f"node_1: {state}")
    return 10


def node_2(state: int) -> int:
    print(f"node_2: {state}")
    return 20


def node_3(state: int) -> int:
    print(f"node_3: {state}")
    return 30


def reducer(left: int, right: int) -> int:
    print(f"reducer: {left} + {right}")
    return left + right


def run():
    builder = StateGraph(Annotated[int, reducer])
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_1", "node_3")
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    complied_state_graph = builder.compile()
    complied_state_graph.get_graph().draw_mermaid_png(
        output_file_path="state_reducers.png")

    print(complied_state_graph.invoke(1))
