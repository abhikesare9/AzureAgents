import requests
from openai import AzureOpenAI

# === Azure OpenAI Client ===
client = AzureOpenAI(
    azure_endpoint="https://23june6219719860.openai.azure.com/",
    api_key="CdDWBOr8vEQ8lc0hz3NQbL8aNnXi3OLHn9U12n3YcOK9pMawQw0tJQQJ99BFACHYHv6XJ3w3AAAAACOGZYe3",
    api_version="2024-12-01-preview"
)

# === NewsAPI Key ===
NEWS_API_KEY = "80b8f31be22049f7918ddce92875c3c6"

# === Fetch Top Headlines ===
def get_top_headlines_newsapi(api_key, count=10, country="us"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": country,
        "pageSize": count
    }
    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])
    headlines = [f"{i+1}. {a['title']}" for i, a in enumerate(articles)]
    return "\n".join(headlines)

# === Fetch and Summarize ===
top_headlines = get_top_headlines_newsapi(NEWS_API_KEY)

prompt = f"""Here are the top 10 news headlines for today:\n\n{top_headlines}\n\nSummarize them in simple bullet points."""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that summarizes news."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.5,
    max_tokens=400
)

# === Output Summary ===
print("\n📰 Top 10 News Summary:\n")
print(response.choices[0].message.content)
