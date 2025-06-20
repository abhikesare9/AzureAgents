import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings
        load_dotenv()
        open_ai_endpoint = "https://june16.cognitiveservices.azure.com/"
        open_ai_key = "59laGrhxCvqEGck89UoAwBVC0QURaxbbIybZAxLMSO0ndOm7FuHoJQQJ99BFACYeBjFXJ3w3AAAAACOGaizs"
        chat_model = "gpt-4.1"
        embedding_model = "text-embedding-ada-002"
        search_url = "https://june16.search.windows.net/"
        search_key = "S51outM5UMrS8LgskLNcpIwRS1vByO56FrCGnrk0MnAzSeDAmynn"
        index_name = "rag-1750308430952"


        # Get an Azure OpenAI chat client
        chat_client = AzureOpenAI(
            api_version = "2024-12-01-preview",
            azure_endpoint = open_ai_endpoint,
            api_key = open_ai_key
        )


        # Initialize prompt with system message
        prompt = [
            {"role": "system", "content": "You are a travel assistant that provides information on travel services available from Margie's Travel."}
        ]

        # Loop until the user types 'quit'
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Add the user input message to the prompt
            prompt.append({"role": "user", "content": input_text})

            # Additional parameters to apply RAG pattern using the AI Search index
            rag_params = {
                "data_sources": [
                    {
                        # he following params are used to search the index
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": search_url,
                            "index_name": index_name,
                            "authentication": {
                                "type": "api_key",
                                "key": search_key,
                            },
                            # The following params are used to vectorize the query
                            "query_type": "vector",
                            "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": embedding_model,
                            },
                        }
                    }
                ],
            }

            # Submit the prompt with the data source options and display the response
            response = chat_client.chat.completions.create(
                model=chat_model,
                messages=prompt,
                extra_body=rag_params
            )
            completion = response.choices[0].message.content
            print(completion)

            # Add the response to the chat history
            prompt.append({"role": "assistant", "content": completion})

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()