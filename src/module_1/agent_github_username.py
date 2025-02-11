import requests
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AnyMessage
from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition


@tool
def fetch_github_repos(username: str) -> list[str] | None:
    """
    Fetches the repositories for a given GitHub username.

    Args:
        username (str): The GitHub username.

    Returns:
        list: A list of repository information as JSON objects if successful.
        None: If the request fails.
    """
    # Construct the URL using the provided username.
    url = f"https://api.github.com/users/{username}/repos"

    try:
        response = requests.get(url)
        # Raise an exception if the HTTP request returned an unsuccessful status code.
        response.raise_for_status()
        # Return the JSON data from the response.
        # Extract only the repository names
        repos = response.json()

        titles = [repo['name'] for repo in repos if 'name' in repo]
        return titles
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return None


llm = ChatOllama(model='qwen2', base_url="http://localhost:11434")


sys_message = SystemMessage(
    content="""
You are responsible for listing the repositories available on GitHub. Your responses must be concise, with a maximum of 100 words. Only provide the repository names without any additional details unless specifically requested. If the user gives queries unrelated to GitHub repositories, ignore them and refuse to answer.
    """)

tools = [fetch_github_repos]
llm_with_tools = llm.bind_tools(tools)
# message = llm.invoke([sys_message, HumanMessage(content="Hello?")])


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def node_llm_with_tools(state: MessagesState) -> MessagesState:
    message = llm_with_tools.invoke([sys_message] + state['messages'])
    return {"messages": [message]}


builder = StateGraph(MessagesState)
builder.add_node('node_llm_with_tools', node_llm_with_tools)
builder.add_node('tools', ToolNode(tools))
builder.add_edge(START, 'node_llm_with_tools')
builder.add_conditional_edges('node_llm_with_tools', tools_condition)
builder.add_edge("tools", "node_llm_with_tools")

complied_state_graph = builder.compile()


# complied_state_graph.get_graph().draw_mermaid_png(
#     output_file_path='agent_with_memory.png')

result = complied_state_graph.invoke({"messages": [HumanMessage(
    content="Could you please provide the name of codewithharry's only first repository name?")]})
