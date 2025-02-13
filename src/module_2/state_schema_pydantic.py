
from pydantic import BaseModel
from typing import Literal

import random
from langgraph.graph import StateGraph, START, END


def run():
    class PydanticStateSchema(BaseModel):
        name: str
        mood: Literal["Happy", "Sad"]

    def node_1(state: PydanticStateSchema) -> PydanticStateSchema:
        print(f"Node 1: {state}")
        return PydanticStateSchema(
            name=state.name + " is ...", mood=state.mood)

    def happy_node(state: PydanticStateSchema) -> PydanticStateSchema:
        print(f"Happy Node: {state}")
        return PydanticStateSchema(name=state.name, mood="Happy")

    def sad_node(state: PydanticStateSchema) -> PydanticStateSchema:
        print(f"Sad Node: {state}")
        return PydanticStateSchema(name=state.name, mood="Sad")

    def decide_mood(state: PydanticStateSchema) -> Literal[
            "sad_node", "happy_node"]:
        print(f"Decide Mood: {state}")
        return "sad_node" if random.random() > 0.5 else "happy_node"

    builder = StateGraph(PydanticStateSchema)
    builder.add_node("node_1", node_1)
    builder.add_node("happy_node", happy_node)
    builder.add_node("sad_node", sad_node)

    builder.add_edge(START, "node_1")
    builder.add_conditional_edges("node_1", decide_mood)
    builder.add_edge("sad_node", END)
    builder.add_edge("happy_node", END)

    complied_state_graph = builder.compile()
    complied_state_graph.get_graph().draw_mermaid_png(
        output_file_path="state_schema_pydantic.png")

    complied_state_graph.invoke(PydanticStateSchema(name="John", mood="Happy"))
