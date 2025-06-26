# import os
from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager
import os
# Load environment variables
load_dotenv()

# Azure OpenAI LLM configuration
llm_config = {
    "config_list": [
        {
            "model": os.getenv("MODEL_DEPLOYMENT_NAME"),  # e.g. "gpt-4o"
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_API_BASE"),
            "api_type": "azure",
            "api_version": os.getenv("OPENAI_API_VERSION")
        }
    ],
    "temperature": 0
}

# Define agents
user_proxy = ConversableAgent(
    name="User_Proxy_Agent",
    system_message="You are a user proxy agent that relays user instructions to expert agents.",
    llm_config=llm_config,
    human_input_mode="TERMINATE",  # This will allow for user input after each round
)

destination_expert = ConversableAgent(
    name="Destination_Expert_Agent",
    system_message="You are the Destination Expert, a specialist in global travel destinations.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

itinerary_creator = ConversableAgent(
    name="Itinerary_Creator_Agent",
    system_message="You are the Itinerary Creator, responsible for crafting detailed travel itineraries.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

budget_analyst = ConversableAgent(
    name="Budget_Analyst_Agent",
    system_message="You are the Budget Analyst, an expert in travel budgeting and financial planning.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

report_writer = ConversableAgent(
    name="Report_Writer_Agent",
    system_message="You are the Report Compiler agent, tasked with creating a comprehensive travel report.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Define allowed transitions between agents
allowed_transitions = {
    user_proxy: [destination_expert, user_proxy],
    destination_expert: [itinerary_creator, user_proxy],
    itinerary_creator: [budget_analyst, user_proxy],
    budget_analyst: [report_writer, user_proxy],
    report_writer: [user_proxy],
}

# Set up the GroupChat
group_chat = GroupChat(
    agents=[
        user_proxy,
        destination_expert,
        itinerary_creator,
        budget_analyst,
        report_writer,
    ],
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
    messages=[],
    max_round=10,
)

# Create the GroupChatManager to manage the chat
travel_planner_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
)

# Get user input and initiate the chat
user_input = input("🧳 Enter your travel request (type 'TERMINATE' to end):\n> ")
user_proxy.initiate_chat(travel_planner_manager, message=user_input)
