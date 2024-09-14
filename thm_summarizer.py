#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import os
from ollama import AsyncClient
from get_room_info import get_room_info

THM_API = "https://tryhackme.com/api/tasks/"

def _connect(url: str="http://localhost:11434") -> AsyncClient:
    try:
        return AsyncClient(host = url)
    except Exception as e:
        print("Seems like your Ollama client is not running?")
        raise SystemExit(e)

async def summarize_tasks(client: AsyncClient, tasks: dict, model: str, stream: bool) -> None:
    
    if not tasks:
        raise SystemExit("No tasks to summarize! Exiting...")

    messages = build_messages(tasks)

    if stream:
        for message in messages:
            async for part in await client.chat(model=model, messages=[message], stream=stream):
                print(part["message"]["content"], end="", flush=True)
            print("\n\n" + "=" * 50 + "\n")
    else:
        response = await client.chat(model=model, messages=messages)
        print(response["message"]["content"])

def build_messages(tasks: dict) -> list:
    messages = []

    for task in tasks:
        user_prompt = {
            "role": "user",
            "content": f"""
You are an expert summarizer capable of understanding the content and summarinzing aptly, keeping most valid information intact.
Develop a summarizer that efficiently condenses the text into a concise summary.
The summarizer should capture essential information and convey the main points clearly and accurately.
The summarizer must be able to handle content related to Cyber Security and Penetration Testing content.
It should prioritize key facts, arguments, and conclusions while maintaining the integrity and tone of the original text.
Focus on clarity, brevity, and relevance to ensure the summary is both informative and readable.

Your task is to summarize this online TryHackMe course description. Highlight the main learning objectives, and course outline.
The text is as follows:
Title: {task["title"]}

{task["desc"]}
"""
        }
        messages.append(user_prompt)

    return messages

def main(parser) -> None:
    args = parser.parse_args()

    OLLAMA_URL = os.getenv("OLLAMA_URL")
    MODEL = os.getenv("OLLAMA_MODEL")
    COOKIE = {"connect.sid": os.getenv("THM_SID")}
    THM_URL = THM_API + args.room 

    client = _connect(OLLAMA_URL)
    tasks = get_room_info(THM_URL, COOKIE)
    asyncio.run(summarize_tasks(client, tasks, MODEL, args.stream))

if __name__ == "__main__":
    from dotenv import load_dotenv
    import argparse

    load_dotenv()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--room", help="Name of TryHackMe room to summarize.", type=str, required=True)
    parser.add_argument("-s", "--stream", help="", type=bool, default=True)

    main(parser)
