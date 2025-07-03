import datetime
from google.adk.agents import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm
import requests
from bs4 import BeautifulSoup


AGENT_MODEL = "anthropic/claude-3-7-sonnet-latest"


def web_surf(url: str) -> dict:
    """Tool for WebSurferAgent: loads a file from a URL and returns parseable content using requests and BeautifulSoup."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return {
        "content": text,
        "source_url": url,
        "metadata": {"scrape_time": str(datetime.datetime.now())},
    }


web_surfer_agent = Agent(
    model=LiteLlm(model=AGENT_MODEL),
    name="web_surfer_agent",
    instruction="You are the WebSurferAgent. Your job is to retrieve and sanitize web content from a provided URL using the 'web_surf' tool. Return both data and metadata in a load_file-like format.",
    description="Retrieves and processes web content from a given URL.",
    tools=[web_surf],
)


def execute_code(code: str) -> str:
    """Execute code using the Piston API and return the result."""
    print("colorless green ideas sleep furiously")
    print(f"Executing code: {code}")
    response = requests.post(
        "https://emkc.org/api/v2/piston/execute",
        json={"language": "python", "version": "3.10.0", "files": [{"content": code}]},
    )
    if response.status_code == 200:
        result = response.json()
        return result["run"]["stdout"]
    else:
        return f"Error: {response.status_code} - {response.text}"


code_executor_agent = Agent(
    model=LiteLlm(model=AGENT_MODEL),
    name="code_executor_agent",
    instruction="You are the CodeExecutorAgent. Your ONLY job is to execute code using the 'execute_code' tool. Return both result and metadata.",
    description="Executes code.",
    tools=[execute_code],
)

orchestrator_agent = LlmAgent(
    name="orchestrator_agent",
    model=LiteLlm(model=AGENT_MODEL),
    description="Central orchestrator: receives user queries and, using its reasoning, decides which specialized agent (web_surfer_agent or code_executor_agent) to invoke.",
    instruction=(
        "You are a general purpose chatbot. You are also a multi-agent system orchestrator. "
        "Make small talk with the user unless the user asks you to do something else that is related to the sub-agents."
        "If the users says hi to you, say hi back and ask them what they would like to do."
        "You have access to the following sub-agents: web_surfer_agent (for retrieving and sanitizing web content from a URL), "
        "and code_executor_agent (for executing Python code). "
        "If the user asks you to do something that is not related to the sub-agents, respond conversationally as a general purpose chatbot. "
        "If the user asks you to do something that is related to the sub-agents, delegate to the appropriate sub-agent."
        "Only delegate to web_surfer_agent if the user provides a valid URL or explicitly requests web content from a URL. "
        "You do NOT have access to any tools. You must NEVER EVER output a function call or tool call for 'web_surfer_agent' or 'code_executor_agent'. "
        "You may ONLY delegate to sub-agents using the sub-agent interface. If you output a function call, the system will fail. "
        "Call the sub-agent by its exact name: 'web_surfer_agent' or 'code_executor_agent'. THESE ARE NOT TOOL CALLS, THEY ARE AGENT CALLS. DO NOT CALL THEM AS TOOLS. "
    ),
    sub_agents=[web_surfer_agent, code_executor_agent],
)

root_agent = orchestrator_agent
