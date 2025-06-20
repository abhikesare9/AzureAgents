import os
import base64
from openai import AzureOpenAI

endpoint = "https://vectorsense.cognitiveservices.azure.com/"
deployment =  "gpt-4.1"
subscription_key = "6dsJ9CnMmr7ekNfNrLAHq974gjotVMvn353OkmR0wVMFVWn78CI0JQQJ99BFACYeBjFXJ3w3AAAAACOGJqJt"

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
<<<<<<< Updated upstream
                "text": "You are expert person from automotive industry."
=======
                "text": "You are expert of automobile industry."
>>>>>>> Stashed changes
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Please provide me details about vw cars."
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

print(completion.to_json())
