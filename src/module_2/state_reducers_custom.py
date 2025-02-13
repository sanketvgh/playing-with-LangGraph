
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END


def reducer(left: list[int], right: list[int]) -> list[int]:
    print(f"reducer: {left} + {right}")
    return left + right


def name_reducer(left: str, right: str) -> str:
    print(f"name_reducer: {left} + {right}")
    if not left:
        return right
    if not right:
        return left
    return f"{left}_{right}"


class State(TypedDict):
    state: Annotated[list[int], reducer]
    name: Annotated[str, name_reducer]


def node_1(state: State) -> State:
    print(f"node_1: {state}")
    return {"state": [10], "name": "node_1"}


def node_2(state: State) -> State:
    print(f"node_2: {state}")
    return {"state": [20], "name": "node_2"}


def node_3(state: State) -> State:
    print(f"node_3: {state}")
    return {"state": [30], "name": "node_3"}


def run():
    builder = StateGraph(State)

    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_1", "node_3")
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    complied_state_graph = builder.compile()
    result = complied_state_graph.invoke({"state": [1]})
    print(result)
