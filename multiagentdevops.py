import json
import asyncio
from typing import List, TypedDict, Set, Callable, Any

from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    FunctionTool, ToolSet, ListSortOrder, MessageRole
)

# ─────────────────────────────────────────────────────────────
# Typed schema for a news item
class NewsItem(TypedDict):
    title: str
    summary: str

# Agent 1: Fetch DevOps News
def get_latest_devops_news() -> str:
    news = [
        {
            "title": "Kubernetes 1.31 Released",
            "summary": "Adds federated cluster support and improved scheduling."
        },
        {
            "title": "GitHub Copilot Workspace Beta",
            "summary": "AI-assisted terminal and DevOps editor tools launched."
        },
        {
            "title": "Terraform Cloud GPU Support",
            "summary": "Now supports GPU infrastructure as code."
        }
    ]
    return json.dumps({"news": news})

# Agent 2: Search Blogs & Videos
def search_related_content(news: List[NewsItem]) -> str:
    blogs = [
        {"title": f"Blog on {item['title']}",  "url": "https://example.com/blog"}
        for item in news
    ]
    videos = [
        {"title": f"Video on {item['title']}", "url": "https://youtube.com/watch?v=abc123"}
        for item in news
    ]
    return json.dumps({"blogs": blogs, "videos": videos})

# Register both functions
user_functions: Set[Callable[..., Any]] = {
    get_latest_devops_news,
    search_related_content
}

# ─────────────────────────────────────────────────────────────
# Azure AI Agents Project Settings
PROJECT_ENDPOINT = "https://23june6219719860.services.ai.azure.com/api/projects/23june6219719860-project/"
DEPLOYMENT_NAME = "gpt-4o"

# Create Azure Agents client
client = AgentsClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
)

tools = ToolSet()
tools.add(FunctionTool(user_functions))

# ─────────────────────────────────────────────────────────────
# Orchestration
with client:
    client.enable_auto_function_calls(FunctionTool(user_functions))

    # Agent 1: DevOps News
    news_agent = client.create_agent(
        model=DEPLOYMENT_NAME,
        name="devops-news-agent",
        instructions="""
You are DevOps-News Bot. 
Always call the `get_latest_devops_news()` function.
Return the result directly, without rewording or adding extra explanation.
""",
        toolset=tools
    )

    # Agent 2: Blog/YouTube Search
    search_agent = client.create_agent(
        model=DEPLOYMENT_NAME,
        name="search-agent",
        instructions="""
You are a content search assistant.
When provided DevOps news items (with title and summary), call `search_related_content(news)` to find relevant blogs and YouTube videos.
""",
        toolset=tools
    )

    # ─────────────────────────────────────────────────────────
    # Multi-agent Workflow
    async def run_workflow():
        thread = client.threads.create()

        # Step 1: Ask Agent 1 for news
        print("\n📡 Fetching DevOps news…")
        client.messages.create(
            thread_id=thread.id,
            role="user",
            content="Get the latest DevOps news."
        )
        run1 = client.runs.create_and_process(thread_id=thread.id, agent_id=news_agent.id)
        if run1.status == "failed":
            raise RuntimeError(run1.last_error)

        news_msg = client.messages.get_last_message_text_by_role(thread.id, MessageRole.AGENT)

        if not news_msg or not news_msg.text.value.strip():
            raise ValueError("❌ Agent 1 returned empty response.")

        raw_text = news_msg.text.value.strip()
        print("\n🧠 Raw DevOps news agent response:\n", raw_text)

        try:
            news_json = json.loads(raw_text)["news"]
        except json.JSONDecodeError:
            raise ValueError("❌ Agent 1 response was not valid JSON.")

        print("\n✅ Parsed DevOps news:\n", json.dumps(news_json, indent=2))

        # Step 2: Ask Agent 2 to search blogs/videos
        print("\n🔍 Searching for blogs and videos…")
        client.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Use this news to find blogs/videos:\n{json.dumps(news_json)}"
        )
        run2 = client.runs.create_and_process(thread_id=thread.id, agent_id=search_agent.id)
        if run2.status == "failed":
            raise RuntimeError(run2.last_error)

        result_msg = client.messages.get_last_message_text_by_role(thread.id, MessageRole.AGENT)
        print("\n🎯 Final Search Results:\n", result_msg.text.value.strip())

        # Full conversation log
        print("\n🗂️ Full Conversation Log:")
        for msg in client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING):
            txt = msg.text_messages[-1].text.value if msg.text_messages else ""
            print(f"{msg.role.upper()}: {txt}\n")

    # Run the async workflow
    asyncio.run(run_workflow())
