
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class AskState(TypedDict):
    question: str


class AnswerState(TypedDict):
    answer: str


class InternalState(AskState, AnswerState):
    notes: str


def thinking_node(state: AskState) -> InternalState:
    return {
        'answer': '',
        'question': state['question'],
        'notes': 'thinking...'
    }


def answer_node(state: InternalState) -> AnswerState:
    print(f'answer_node: User asked: {state["question"]}')
    return {'answer': 'The capital of France is Paris.'}


def run():
    builder = StateGraph(InternalState, input=AskState, output=AnswerState)
    builder.add_node("thinking_node", thinking_node)
    builder.add_node("answer_node", answer_node)
    builder.add_edge(START, "thinking_node")
    builder.add_edge("thinking_node", "answer_node")
    builder.add_edge("answer_node", END)

    complied_state_graph = builder.compile()

    complied_state_graph.get_graph().draw_mermaid_png(
        output_file_path='state_multiple_schema_input_output.png')

    result = complied_state_graph.invoke(
        {'question': 'What is the capital of France?'})
    print(result)
