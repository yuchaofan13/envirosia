import asyncio
from aiohttp import ClientSession
import openai
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

async def gather_chat_completions(message_batches):
    async with ClientSession() as session:
        openai.aiosession.set(session)
        
        tasks = []
        for messages in message_batches:
            tasks.append(asyncio.create_task(openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=messages,temperature = 0.5)))

        completions = await asyncio.gather(*tasks)
        await openai.aiosession.get().close() 
    return completions