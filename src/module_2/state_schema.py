from typing import TypedDict, Literal
import random
# TypedDict
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, field_validator


class PydanticStateSchema(BaseModel):
    name: str
    mood: Literal["Happy", "Sad"]

    @field_validator("mood")
    def validate_mood(cls, v):
        if v not in ["Happy", "Sad"]:
            raise ValueError("Mood must be either Happy or Sad")
        return v


class TypedDictStateSchema(TypedDict):
    name: str
    mood: Literal["Happy", "Sad"]


def node_1(state: TypedDictStateSchema) -> TypedDictStateSchema:
    print(f"Node 1: {state}")
    return {"name": state["name"] + " is ..."}


def happy_node(state: TypedDictStateSchema) -> TypedDictStateSchema:
    print(f"Happy Node: {state}")
    return {"mood": "Happy"}


def sad_node(state: TypedDictStateSchema) -> TypedDictStateSchema:
    print(f"Sad Node: {state}")
    return {"mood": "Sad"}


def decide_mood(state: TypedDictStateSchema) -> Literal[
        "sad_node", "happy_node"]:
    print(f"Decide Mood: {state}")
    return "sad_node" if random.random() > 0.5 else "happy_node"


def run():
    builder = StateGraph(TypedDictStateSchema)
    builder.add_node("node_1", node_1)
    builder.add_node("happy_node", happy_node)
    builder.add_node("sad_node", sad_node)

    builder.add_edge(START, "node_1")
    builder.add_conditional_edges(
        "node_1",
        decide_mood
    )
    builder.add_edge("sad_node", END)
    builder.add_edge("happy_node", END)

    complied_state_graph = builder.compile()
    # complied_state_graph.get_graph().draw_mermaid_png(
    #     output_file_path="state_schema.png")

    complied_state_graph.invoke({"name": "John"})
