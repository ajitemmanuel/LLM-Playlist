import asyncio

from langchain_core.messages import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"/teamspace/studios/this_studio/LLM-Playlist/.env")

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

async def main():
    client = MultiServerMCPClient(
        {
            "weather":{
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp/",
            }
        }
    )

    tools = await client.get_tools()
    agent = create_react_agent("openai:gpt-4o-mini", tools)

    question = "What is the weather in Trivandrum today?"
    result = await agent.ainvoke({"messages": question})
    messages = result['messages']
    print("ALL MESSAGES:", messages)
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            print("Agent response:", msg.content)
            break
    else:
        print("No AIMessage found.")


if __name__ == "__main__":
    asyncio.run(main())