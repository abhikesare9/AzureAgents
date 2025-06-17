from langchain import PromptTemplate
import openai
from dotenv import load_dotenv, find_dotenv
import os
from langchain.chat_models import AzureChatOpenAI 





llm = AzureChatOpenAI(
    openai_api_version="2025-01-01-preview",
    openai_api_key="59laGrhxCvqEGck89UoAwBVC0QURaxbbIybZAxLMSO0ndOm7FuHoJQQJ99BFACYeBjFXJ3w3AAAAACOGaizs",
    openai_api_base="https://june16.openai.azure.com/",
    openai_api_type="azure",
    deployment_name="gpt-4.1",
    temperature=0.7
)

#Azure OpenAI Completion Endpoint
def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
    chat_completion = openai.ChatCompletion.create(
            deployment_id="gpt-4.1",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            n=1,
        )

    return chat_completion.choices[0].message.content

# create the prompt
prompt_template: str = """/
You are a cricket expert, give responses to the following/ 
question: {question}. Do not use technical words, give easy/
to understand responses.
"""

prompt = PromptTemplate.from_template(template=prompt_template)

# Questions 
questions = [
    "who won the 2011 world-cup?",
    "who won big-boss 17?"
]

# Iterate through the questions
for question in questions:
    prompt_formatted_str = prompt.format(question=question)
    prediction = llm.predict(prompt_formatted_str)

    print("Question:", question)
    print("Answer:", prediction)
    print("-----------------")  # separator between results