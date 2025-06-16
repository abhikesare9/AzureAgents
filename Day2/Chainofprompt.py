import os
from openai import AzureOpenAI

# Initialize client
client = AzureOpenAI(
    azure_endpoint=os.getenv("ENDPOINT_URL", "https://june16.openai.azure.com/"),
    api_key="59laGrhxCvqEGck89UoAwBVC0QURaxbbIybZAxLMSO0ndOm7FuHoJQQJ99BFACYeBjFXJ3w3AAAAACOGaizs",
    api_version="2025-01-01-preview",
)

# Deployment name
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")

# Initialize the conversation history
chat_history = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps users solve problems step-by-step."
            }
        ]
    }
]

# Example chain of prompts
prompts = [
    "I want to build a chatbot. What are the first steps?",
    "Can you suggest a good tech stack for this chatbot?",
    "How can I deploy it on Azure?",
    "Can you write a FastAPI example for it?"
]

# Loop through prompts, keeping context
for user_prompt in prompts:
    # Add user prompt
    chat_history.append({
        "role": "user",
        "content": [{"type": "text", "text": user_prompt}]
    })

    # Get assistant response
    response = client.chat.completions.create(
        model=deployment,
        messages=chat_history,
        max_tokens=800,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream=False
    )

    assistant_reply = response.choices[0].message.content

    # Print the response
    print(f"User: {user_prompt}")
    print(f"Assistant: {assistant_reply}\n{'-'*60}")

    # Add assistant reply to chat history for continuity
    chat_history.append({
        "role": "assistant",
        "content": [{"type": "text", "text": assistant_reply}]
    })
