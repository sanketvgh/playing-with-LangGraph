
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class PublicState(TypedDict):
    public_state: int


class PrivateState(TypedDict):
    private_state: int


def node_1(state: PublicState) -> PrivateState:
    return {'private_state': state['public_state'] + 1}


def node_2(state: PrivateState) -> PublicState:
    return {'public_state': state['private_state'] + 1}


def run():
    builder = StateGraph(PublicState)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2", END)

    complied_state_graph = builder.compile()

    # complied_state_graph.get_graph().draw_mermaid_png(
    #     output_file_path='state_multiple_schema.png')

    result = complied_state_graph.invoke({'public_state': 2})
    print(result)
