# import json
# import asyncio
# import ast
# from typing import List, TypedDict, Set, Callable, Any
# from newsapi import NewsApiClient
# from azure.identity import DefaultAzureCredential
# from azure.ai.agents import AgentsClient
# from azure.ai.agents.models import (
#     FunctionTool, ToolSet, ListSortOrder, MessageRole
# )

# # ─────────────────────────────────────────────────────────────
# class NewsItem(TypedDict):
#     title: str
#     summary: str

# # Tool 1: Fetch DevOps News from NewsAPI
# def get_latest_devops_news() -> str:
#     """
#     Fetch DevOps-related news articles using NewsAPI's get_everything().
#     Returns a JSON string with a list of articles (title and summary).
#     """
#     newsapi = NewsApiClient(api_key="80b8f31be22049f7918ddce92875c3c6")

#     try:
#         response = newsapi.get_everything(
#             q='devops news',
#             domains='techcrunch.com,thenextweb.com,zdnet.com,dev.to,medium.com',
#             from_param='2025-06-01',
#             to='2025-06-26',
#             language='en',
#             sort_by='relevancy',
#             page=1
#         )
#         articles = response.get("articles", [])
#         news_items = [{"title": article["title"], "summary": article.get("description", "")} for article in articles]
#         return json.dumps({"news": news_items})

#     except Exception as e:
#         return json.dumps({"error": f"Failed to fetch news: {str(e)}"})

# # Tool 2: Create blog/video links from news
# def search_related_content(news: List[NewsItem]) -> str:
#     blogs = [{"title": f"Blog on {item['title']}", "url": "https://example.com/blog"} for item in news]
#     videos = [{"title": f"Video on {item['title']}", "url": "https://youtube.com/watch?v=abc123"} for item in news]
#     return json.dumps({"blogs": blogs, "videos": videos})

# # Register both tools
# user_functions: Set[Callable[..., Any]] = {
#     get_latest_devops_news,
#     search_related_content
# }

# # ─────────────────────────────────────────────────────────────
# PROJECT_ENDPOINT = "https://23june6219719860.services.ai.azure.com/api/projects/23june6219719860-project/"
# DEPLOYMENT_NAME = "gpt-4o"

# client = AgentsClient(
#     endpoint=PROJECT_ENDPOINT,
#     credential=DefaultAzureCredential(
#         exclude_environment_credential=True,
#         exclude_managed_identity_credential=True
#     )
# )

# tools = ToolSet()
# tools.add(FunctionTool(user_functions))

# with client:
#     client.enable_auto_function_calls(FunctionTool(user_functions))

#     # Agent 1: DevOps News Fetcher
#     news_agent = client.create_agent(
#         model=DEPLOYMENT_NAME,
#         name="devops-news-agent",
#         instructions="""
# You are a DevOps-News Bot.
# Your only task is to call the `get_latest_devops_news()` function and return the exact JSON response without any explanation, comments, or formatting like markdown/code blocks. Do NOT add ```json or anything else.
# Just return the plain JSON string.
# """,
#         toolset=tools
#     )

#     # Agent 2: Blog/Video Search
#     search_agent = client.create_agent(
#         model=DEPLOYMENT_NAME,
#         name="search-agent",
#         instructions="""
# You are a content discovery assistant.
# You will receive a list of DevOps news in JSON format.
# Call `search_related_content(news)` with that list and return the function's JSON output without adding anything else.
# Do NOT add ```json or natural language explanations.
# """,
#         toolset=tools
#     )

#     # ─────────────────────────────────────────────────────────────
#     async def run_workflow():
#         thread = client.threads.create()

#         print("\n📡 Fetching DevOps news…")
#         client.messages.create(thread_id=thread.id, role="user", content="Get the latest DevOps news.")
#         run1 = client.runs.create_and_process(thread_id=thread.id, agent_id=news_agent.id)

#         if run1.status == "failed":
#             raise RuntimeError(run1.last_error)

#         news_msg = client.messages.get_last_message_text_by_role(thread.id, MessageRole.AGENT)
#         raw_text = news_msg.text.value.strip() if news_msg and news_msg.text and news_msg.text.value else ""

#         print("\n🧠 Raw DevOps news agent response:\n", raw_text)

#         try:
#             # Clean up any formatting if model ignored instructions
#             if raw_text.startswith("```"):
#                 raw_text = raw_text.strip("`").split("json")[-1].strip()
#             news_data = json.loads(raw_text)
#         except Exception:
#             try:
#                 news_data = ast.literal_eval(raw_text)
#             except Exception:
#                 raise ValueError("❌ Agent 1 response was not valid JSON or dict.")

#         news_json = news_data.get("news", [])
#         print("\n✅ Parsed DevOps news:\n", json.dumps(news_json, indent=2))

#         print("\n🔍 Searching for blogs and videos…")
#         client.messages.create(
#             thread_id=thread.id,
#             role="user",
#             content=f"Use this news to find blogs/videos:\n{json.dumps(news_json)}"
#         )
#         run2 = client.runs.create_and_process(thread_id=thread.id, agent_id=search_agent.id)
#         if run2.status == "failed":
#             raise RuntimeError(run2.last_error)

#         result_msg = client.messages.get_last_message_text_by_role(thread.id, MessageRole.AGENT)
#         print("\n🎯 Final Search Results:\n", result_msg.text.value.strip() if result_msg and result_msg.text else "❌ No result returned.")

#         print("\n🗂️ Full Conversation Log:")
#         for msg in client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING):
#             txt = msg.text_messages[-1].text.value if msg.text_messages else ""
#             print(f"{msg.role.upper()}: {txt}\n")

#     asyncio.run(run_workflow())
import json
import asyncio
import ast
import requests
from typing import List, TypedDict, Set, Callable, Any
from newsapi import NewsApiClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    FunctionTool, ToolSet, ListSortOrder, MessageRole
)

# ─────────────────────────────────────────────────────────────
class NewsItem(TypedDict):
    title: str
    summary: str

# Tool 1: Fetch DevOps News from NewsAPI
def get_latest_devops_news() -> str:
    newsapi = NewsApiClient(api_key="80b8f31be22049f7918ddce92875c3c6")

    try:
        response = newsapi.get_everything(
            q='devops news',
            domains='techcrunch.com,thenextweb.com,zdnet.com,dev.to,medium.com',
            from_param='2025-06-01',
            to='2025-06-26',
            language='en',
            sort_by='relevancy',
            page=1
        )
        articles = response.get("articles", [])
        news_items = [{"title": article["title"], "summary": article.get("description", "")} for article in articles]
        return json.dumps({"news": news_items})
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch news: {str(e)}"})

# Tool 2: Search blog URLs using rss2json from Dev.to
def search_related_content(news: List[NewsItem]) -> str:
    try:
        blogs = []
        for item in news[:3]:  # use only top 3 news items
            rss_url = "https://dev.to/feed/tag/devops"
            api_url = f"https://api.rss2json.com/v1/api.json?rss_url={rss_url}"

            response = requests.get(api_url)
            if response.status_code != 200:
                continue

            blog_data = response.json()
            entries = blog_data.get("items", [])[:3]  # top 3 blog entries
            for entry in entries:
                blogs.append({
                    "title": entry["title"],
                    "url": entry["link"]
                })

        return json.dumps({"blogs": blogs, "videos": []})
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch blogs: {str(e)}"})

# ─────────────────────────────────────────────────────────────
user_functions: Set[Callable[..., Any]] = {
    get_latest_devops_news,
    search_related_content
}

PROJECT_ENDPOINT = "https://23june6219719860.services.ai.azure.com/api/projects/23june6219719860-project/"
DEPLOYMENT_NAME = "gpt-4o"

client = AgentsClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
)

tools = ToolSet()
tools.add(FunctionTool(user_functions))

with client:
    client.enable_auto_function_calls(FunctionTool(user_functions))

    news_agent = client.create_agent(
        model=DEPLOYMENT_NAME,
        name="devops-news-agent",
        instructions="""
You are a DevOps-News Bot.
Your only task is to call the `get_latest_devops_news()` function and return the exact JSON response without any explanation, comments, or formatting like markdown/code blocks. Do NOT add ```json or anything else.
Just return the plain JSON string.
""",
        toolset=tools
    )

    search_agent = client.create_agent(
        model=DEPLOYMENT_NAME,
        name="search-agent",
        instructions="""
You are a content discovery assistant.
You will receive a list of DevOps news in JSON format.
Call `search_related_content(news)` with that list and return the function's JSON output without adding anything else.
Do NOT add ```json or natural language explanations.
""",
        toolset=tools
    )

    async def run_workflow():
        thread = client.threads.create()

        print("\n📡 Fetching DevOps news…")
        client.messages.create(thread_id=thread.id, role="user", content="Get the latest DevOps news.")
        run1 = client.runs.create_and_process(thread_id=thread.id, agent_id=news_agent.id)

        if run1.status == "failed":
            raise RuntimeError(run1.last_error)

        news_msg = client.messages.get_last_message_text_by_role(thread.id, MessageRole.AGENT)
        raw_text = news_msg.text.value.strip() if news_msg and news_msg.text and news_msg.text.value else ""

        print("\n🧠 Raw DevOps news agent response:\n", raw_text)

        try:
            if raw_text.startswith("```"):
                raw_text = raw_text.strip("`").split("json")[-1].strip()
            news_data = json.loads(raw_text)
        except Exception:
            try:
                news_data = ast.literal_eval(raw_text)
            except Exception:
                raise ValueError("❌ Agent 1 response was not valid JSON or dict.")

        news_json = news_data.get("news", [])
        print("\n✅ Parsed DevOps news:\n", json.dumps(news_json, indent=2))

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
        print("\n🎯 Final Search Results:\n", result_msg.text.value.strip() if result_msg and result_msg.text else "❌ No result returned.")

        print("\n🗂️ Full Conversation Log:")
        for msg in client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING):
            txt = msg.text_messages[-1].text.value if msg.text_messages else ""
            print(f"{msg.role.upper()}: {txt}\n")

    asyncio.run(run_workflow())
