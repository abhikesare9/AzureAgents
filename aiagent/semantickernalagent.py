import json
import uuid
from pathlib import Path
from typing import Set, Callable, Any

from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    FunctionTool, ToolSet, ListSortOrder, MessageRole
)

# === Define Your User Function ===
def submit_support_ticket(email_address: str, description: str) -> str:
    script_dir = Path(__file__).parent
    ticket_number = str(uuid.uuid4()).replace('-', '')[:6]
    file_name = f"ticket-{ticket_number}.txt"
    file_path = script_dir / file_name

    text = (
        f"Support Ticket: {ticket_number}\n"
        f"Submitted by: {email_address}\n"
        f"Description:\n{description}"
    )
    file_path.write_text(text)

    message_json = json.dumps({
        "message": f"Support ticket {ticket_number} submitted. File saved as {file_name}."
    })
    return message_json

user_functions: Set[Callable[..., Any]] = {submit_support_ticket}

# === Azure Configuration ===
project_endpoint = "https://23june6219719860.services.ai.azure.com/api/projects/23june6219719860-project/"  
model_deployment = "gpt-4o"  

# === Connect to Azure AI Agents Client ===
agent_client = AgentsClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
)

# === Build ToolSet ===
functions = FunctionTool(user_functions)
toolset = ToolSet()
toolset.add(functions)

# === Interact with the agent ===
with agent_client:
    agent_client.enable_auto_function_calls(toolset)

    agent = agent_client.create_agent(
        model=model_deployment,
        name="support-agent",
        instructions="""
        You are a technical support agent.
        When a user has a technical issue, get their email and a description.
        Then use the provided function to submit a support ticket.
        Let the user know the ticket file name after submitting.
        """,
        toolset=toolset
    )

    # === Start thread and prompt ===
    thread = agent_client.threads.create()
    print(f"You're chatting with: {agent.name} ({agent.id})")

    # Example user message
    user_prompt = "My email is abhi@test.com. I cannot reset my password and it's blocking my login."

    message = agent_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt
    )

    run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

    # Handle run errors
    if run.status == "failed":
        print(f"❌ Run failed: {run.last_error}")

    # Print last message
    last_msg = agent_client.messages.get_last_message_text_by_role(
        thread_id=thread.id,
        role=MessageRole.AGENT,
    )
    if last_msg:
        print(f"\n🧠 Last Agent Message: {last_msg.text.value}")

    # Print entire chat history
    print("\n🗂️ Conversation Log:\n")
    messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
        if message.text_messages:
            last_text = message.text_messages[-1]
            print(f"{message.role}: {last_text.text.value}\n")
