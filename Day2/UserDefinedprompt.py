import os
from openai import AzureOpenAI

# Environment variables or defaults
endpoint = os.getenv("ENDPOINT_URL", "https://june16.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")
subscription_key = "59laGrhxCvqEGck89UoAwBVC0QURaxbbIybZAxLMSO0ndOm7FuHoJQQJ99BFACYeBjFXJ3w3AAAAACOGaizs"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# Accept dynamic user input
user_input = input("Enter your prompt: ")

# Prepare the chat prompt dynamically
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_input
            }
        ]
    }
]

# Generate the completion
completion = client.chat.completions.create(
    model=deployment,
    messages=chat_prompt,
    max_tokens=800,
    temperature=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

# Print the output
print(completion.choices[0].message.content)
