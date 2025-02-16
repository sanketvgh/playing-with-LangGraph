#  from langgraph.graph import StateGraph, START, END
# from typing_extensions import Annotated, TypedDict
# import operator


# def merge_dicts(owners_map_left: dict, owners_map_right: dict) -> dict:
#     temp = {}

#     for owner_name in owners_map_right:
#         if owner_name in owners_map_left:
#             temp[owner_name] = (
#                 owners_map_left[owner_name] + owners_map_right[owner_name]
#             )
#         else:
#             temp[owner_name] = owners_map_right[owner_name]
#     return temp


# class State(TypedDict):
#     people: Annotated[list, operator.add]
#     cars: Annotated[list, operator.add]
#     owners_map: Annotated[dict, merge_dicts]


# def run():
#     workflow = StateGraph(State)

#     workflow.add_node("human", lambda _state: {"people": ["John", "Jane", "Jim"]})
#     workflow.add_node("car", lambda _state: {"cars": ["Toyota", "Ford", "Chevy"]})

#     workflow.add_edge(START, "human")
#     workflow.add_edge("human", "car")
#     workflow.add_node(
#         "expensive_owner",
#         lambda _state: {
#             "owners_map": {
#                 "John": ["BMW"],
#                 "Jane": ["Mercedes"],
#                 "Jim": ["Audi"],
#             }
#         },
#     )
#     workflow.add_node(
#         "cheap_owner",
#         lambda _state: {
#             "owners_map": {
#                 "John": ["Toyota"],
#                 "Jane": ["Ford"],
#                 "Jim": ["Chevy"],
#             }
#         },
#     )
#     workflow.add_edge("car", "expensive_owner")
#     workflow.add_edge("car", "cheap_owner")
#     workflow.add_edge("expensive_owner", END)
#     workflow.add_edge("cheap_owner", END)

#     graph = workflow.compile()

#     graph.get_graph().draw_mermaid_png(output_file_path="stream.png")

#     for chunk in graph.stream(
#         input=State(people=["Sanket"], cars=["BMW"]), stream_mode="updates"
#     ):
#         print("chunk ", chunk)


from langgraph.graph import MessageGraph
from langchain_core.messages import HumanMessage
from ai import llm


import logging

logging.basicConfig(level=logging.INFO)


import asyncio


def run():
    workflow = MessageGraph()

    workflow.add_node("hermes_ai", lambda state: llm.invoke(state))

    workflow.set_entry_point("hermes_ai")
    workflow.set_finish_point("hermes_ai")

    graph = workflow.compile()

    graph.get_graph().draw_mermaid_png(output_file_path="stream.png")

    while True:
        user_input = input("You: ")

        if user_input == "q":
            break

        async def stream_events():
            async for event in graph.astream_events(
                [HumanMessage(content=user_input)], version="v2"
            ):
                # print(
                #     f"Node: {event['metadata'].get('langgraph_node')}, Type: {event['event']}, Name: {event['name']}"
                # )

                if (
                    event["event"] == "on_chat_model_stream"
                    and event["metadata"].get("langgraph_node", "") == "hermes_ai"
                ):
                    print(event["data"]["chunk"].content, end="", flush=True)

            print()

        asyncio.run(stream_events())
