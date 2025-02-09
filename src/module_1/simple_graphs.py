from langgraph.graph import StateGraph, START, END
import random
from typing import Literal, TypedDict


class State(TypedDict):
    graph_state: str


def node_1(state: State) -> State:
    print("node_1")
    return {"graph_state": state["graph_state"] + " I am"}


def node_2(state: State) -> State:
    print("node_2")
    return {"graph_state": state["graph_state"] + " happy!"}


def node_3(state: State) -> State:
    print("node_3")
    return {"graph_state": state["graph_state"] + " sad!"}


def decide_mood(state: State) -> Literal["node_2", "node_3"]:
    user_input = state["graph_state"]
    print("user_input", user_input)
    if random.random() < 0.5:
        return "node_2"
    else:
        return "node_3"


builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

print(graph.invoke({"graph_state": "Hello, This is Sanket."}))

# with open("graph.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())
#     f.close()

# print("Graph saved as graph.png")
