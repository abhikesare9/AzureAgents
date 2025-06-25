import asyncio
import os
from dotenv import load_dotenv
from typing import Annotated

from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from semantic_kernel.functions import kernel_function

# === Plugin to Recommend Stocks ===
class StockAdvisorPlugin:
    """Plugin to simulate stock recommendation."""

    @kernel_function(description="Suggests the top trending or best-performing stocks based on simple logic.")
    def get_best_stocks(self,
                        sector: Annotated[str, "Sector to focus on (e.g., technology, healthcare, energy)."],
                        risk: Annotated[str, "Risk level (low, medium, high)."]):
        sample_stocks = {
            "technology": {"low": ["MSFT", "AAPL"], "medium": ["NVDA", "AMD"], "high": ["TSLA", "PLTR"]},
            "healthcare": {"low": ["JNJ", "PFE"], "medium": ["MRNA", "VRTX"], "high": ["BMRN", "SAGE"]},
            "energy": {"low": ["XOM", "CVX"], "medium": ["SLB", "BKR"], "high": ["FANG", "RIG"]},
        }
        best_picks = sample_stocks.get(sector.lower(), {}).get(risk.lower(), [])
        return f"Top {risk}-risk picks in {sector} sector: {', '.join(best_picks) if best_picks else 'No data found.'}"

# === Main Execution ===
async def main():
    load_dotenv()

    # Prompt details
    sector = "technology"
    risk_level = "medium"
    user_prompt = f"Recommend the best {risk_level}-risk stocks in the {sector} sector."

    ai_agent_settings = AzureAIAgentSettings()

    async with (
        DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        ) as creds,
        AzureAIAgent.create_client(credential=creds, settings=ai_agent_settings) as project_client
    ):
        agent_def = await project_client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name="stock_advisor_agent",
            instructions="""
You are a financial assistant that helps users select the best stocks.
Based on the sector and risk profile the user provides, call the plugin to suggest the top matching stock tickers.
"""
        )

        stock_agent = AzureAIAgent(
            client=project_client,
            definition=agent_def,
            plugins=[StockAdvisorPlugin()]
        )

        thread: AzureAIAgentThread | None = None
        try:
            response = await stock_agent.get_response([user_prompt], thread=thread)
            print(f"\n# {stock_agent.name}:")
            print(response)
        except Exception as e:
            print("❌ Error:", e)
        finally:
            if thread:
                await thread.delete()
            # await project_client.agents.delete_agent(stock_agent.id)

if __name__ == "__main__":
    asyncio.run(main())
