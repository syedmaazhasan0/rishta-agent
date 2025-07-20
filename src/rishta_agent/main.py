import asyncio
from agents import Agent, RunConfig, Runner, set_tracing_disabled, OpenAIChatCompletionsModel,handoffs  # type: ignore
from agents.tool import function_tool  # type: ignore
from openai import AsyncOpenAI  # type: ignore

# Replace with your actual API key
OPENAI_MODEL: str = "deepseek/deepseek-chat-v3-0324:free"
OPENAI_API_KEY: str = "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" 
BASE_URL: str = "https://openrouter.ai/api/v1"


set_tracing_disabled(disabled=True)

client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

male_agent = Agent(
    name="Male Rishta Assistant",
    instructions="""
        Find a suitable female rishta for the user.
        The rishta includes details: name, age, profession, location, cast, etc.
    """,
)

female_agent = Agent(  
    name="Female Rishta Assistant",
    instructions="""
        Find a suitable male rishta for the user.
        The rishta includes details: name, age, salary, profession, location, cast, etc.
    """,
)

rishta_agent = Agent(
    name="Rishta Assistant",
    instructions="""
        This is an AI rishta assistant.
        If the rishta is for a male, then hand off to the male agent.
        If the rishta is for a female, then hand off to the female agent.
    """,
    handoffs= [female_agent, male_agent]
    )

# Model
model = OpenAIChatCompletionsModel(openai_client=client, model=OPENAI_MODEL)

# Main async function
async def main():
    result = await Runner.run(
        rishta_agent,
        'im a rich man and i looking for beautiful female to marry',
        run_config=RunConfig(model=model)
    )
    print(result.final_output)
    print(result.last_agent.name)

# Entry point
def start():
    asyncio.run(main())
