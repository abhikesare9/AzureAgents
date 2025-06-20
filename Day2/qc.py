import os
from openai import AzureOpenAI

# Replace these with secure values or use environment variables in production
api_key = "59laGrhxCvqEGck89UoAwBVC0QURaxbbIybZAxLMSO0ndOm7FuHoJQQJ99BFACYeBjFXJ3w3AAAAACOGaizs"
api_base = "https://june16.openai.azure.com/"
api_version = "2025-01-01-preview"
deployment_name = "gpt-4-vision"  # Use your vision-capable deployment name (not "gpt-4.1")
temperature = 0.7

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    base_url=api_base
)

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this picture:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://microsoftlearning.github.io/AI-900-AIFundamentals/instructions/media/analyze-images-computer-vision-service/store-camera-1.jpg"
                    }
                }
            ]
        }
    ],
    max_tokens=2000,
    temperature=temperature
)

print(response.choices[0].message.content)
