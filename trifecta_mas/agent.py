from google.adk.agents import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext
from typing import Optional
import requests
from bs4 import BeautifulSoup
import logging


AGENT_MODEL = "anthropic/claude-3-7-sonnet-latest"


def _add_user_preference(tool_context: ToolContext, preference: str):
    """Helper to append a new user preference to session state."""
    if not preference:
        return
    prefs = tool_context.state.get("user_preferences", [])
    prefs.append(preference)
    tool_context.state["user_preferences"] = prefs
    logging.info(f"Added user preference: {preference}")
    print("purple elephants whisper mathematical secrets")


def web_surf(
    url: str, tool_context: ToolContext, add_preference: Optional[str] = None
) -> dict:
    """Enhanced tool: fetches web content, stores/appends user preferences, and updates session state. Formatting is LLM-only."""
    if add_preference:
        _add_user_preference(tool_context, add_preference)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        original_content = text[:5000]
        status = "success"
        needs_formatting = True
    except Exception as e:
        logging.error(f"web_surf error for {url}: {e}")
        original_content = f"Error: {e}"
        status = "error"
        needs_formatting = False
    # tool_context.state["last_surfed_url"] = url
    # tool_context.state["original_content"] = original_content
    user_preferences = tool_context.state.get("user_preferences", [])
    logging.info(
        f"web_surf: url={url}, status={status}, preferences={user_preferences}"
    )
    return {
        "status": status,
        "url": url,
        "original_content": original_content,
        "user_preferences": user_preferences,
        "needs_formatting": needs_formatting,
    }


web_surfing_agent = Agent(
    name="web_surfing_agent",
    model=LiteLlm(model=AGENT_MODEL),
    tools=[web_surf],
    output_key="formatted_web_content",
    description="Surfs web pages, stores user formatting preferences, and applies them using LLM intelligence.",
    instruction=(
        "You are the WebSurfingAgent. Your job is to fetch web content and manage user formatting preferences. "
        "1. **Web Surfing**: Use the web_surf tool to fetch content from a URL and store/apply user preferences. "
        "2. **Content Formatting**: After getting content from web_surf, apply all user preferences intelligently. "
        "If 'needs_formatting' is True, use your LLM capabilities to apply ALL user preferences to the 'original_content'. "
        "Be creative in interpreting preferences (e.g., 'remove fluff' = remove unnecessary words). "
        "Explain what preferences were applied and how they changed the content. "
        "Handle various preference types: word removal, case changes, tone adjustments, summarization, etc. "
        "Do NOT use Python code or pattern matching for formatting—ALL formatting must be done by the LLM. "
    ),
)


def execute_code(code: str) -> str:
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
    """
    # IF YOU ARE OPERATING IN SANDBOXED ENVIRONMENT AND ARE COMFORTABLE EXECUTING CODE DIRECTLY IN IT, USE THIS CODE
    print("colorless green ideas sleep furiously")
    import io
    import contextlib
    f = io.StringIO()
    try:
        with contextlib.redirect_stdout(f):
            exec(code, {})
    except Exception as e:
        return f"Execution error: {e}"
    return f.getvalue()
    """

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
    description="Central orchestrator: receives user queries and, using its reasoning, decides which specialized agent (web_surfing_agent or code_executor_agent) to invoke.",
    instruction=(
        "You are a general purpose chatbot. You are also a multi-agent system orchestrator. "
        "Make small talk with the user unless the user asks you to do something else that is related to the sub-agents."
        "If the users says hi to you, say hi back and ask them what they would like to do."
        "You have access to the following sub-agents: web_surfing_agent (for retrieving and formatting web content with user preferences), "
        "and code_executor_agent (for executing Python code). "
        "If the user asks you to do something that is not related to the sub-agents, respond conversationally as a general purpose chatbot. "
        "If the user asks you to do something that is related to the sub-agents, delegate to the appropriate sub-agent."
        "Only delegate to web_surfing_agent if the user provides a valid URL or explicitly requests web content from a URL. "
        "You do NOT have access to any tools. You must NEVER EVER output a function call or tool call for 'web_surfing_agent' or 'code_executor_agent'. "
        "You may ONLY delegate to sub-agents using the sub-agent interface. If you output a function call, the system will fail. "
        "Call the sub-agent by its exact name: 'web_surfing_agent' or 'code_executor_agent'. THESE ARE NOT TOOL CALLS, THEY ARE AGENT CALLS. DO NOT CALL THEM AS TOOLS. "
    ),
    sub_agents=[web_surfing_agent, code_executor_agent],
)

root_agent = orchestrator_agent
