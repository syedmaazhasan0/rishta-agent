import asyncio
from agents import Agent, RunConfig, Runner, set_tracing_disabled, OpenAIChatCompletionsModel,handoffs
from agents.tool import function_tool 
from openai import AsyncOpenAI 

# Replace with your actual API key
GEMINI_MODEL: str = "gemini-2.0-flash"
GEMINI_API_KEY: str = "AIzaSyB9IT8RMJsrrbIw5w_ux34F_QhVQOsl0J4" 
BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"


set_tracing_disabled(disabled=True)

client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

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
model = OpenAIChatCompletionsModel(openai_client=client, model=GEMINI_MODEL)

# Main async function
async def main():
    result = await Runner.run(
        rishta_agent,
        'I\'m looking for a suitable partner. This is my details: name: "Maaz Hassan", age: 15, profession: "Student", location: "Karachi", cast: "Urdu Speaking".Any age,cast or anything just give me the the rishta and dont ask for more info',
        run_config=RunConfig(model=model)
    )
    print(result.final_output)
    print(result.last_agent.name)

# Entry point
def start():
    asyncio.run(main())
