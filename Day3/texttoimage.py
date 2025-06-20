# DALL-E 3 requires version 1.0.0 or later of the openai-python library.
import os
from openai import AzureOpenAI
import json

# You will need to set these environment variables or edit the following values.
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://june16.cognitiveservices.azure.com/")
api_version = os.getenv("OPENAI_API_VERSION", "2024-04-01-preview")
deployment = os.getenv("DEPLOYMENT_NAME", "dall-e-3")
deployment2 = "gpt-4o"
api_key =  "59laGrhxCvqEGck89UoAwBVC0QURaxbbIybZAxLMSO0ndOm7FuHoJQQJ99BFACYeBjFXJ3w3AAAAACOGaizs"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key,
)

result = client.images.generate(
    model=deployment,
    prompt="Generate image for a sunset. ",
    n=1,
    style="natural",
    quality="standard",
)
completion = client.chat.completions.create(
    model=deployment2,
    messages=chat_prompt,
    max_tokens=800,
    temperature=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)


image_url = json.loads(result.model_dump_json())['data'][0]['url']
print(image_url)