#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ollama import Client
from get_room_info import get_room_info

THM_API = "https://tryhackme.com/api/tasks/"

def _connect(url: str="http://localhost:11434") -> Client:
    try:
        return Client(host = url)
    except Exception as e:
        print("Seems like your Ollama client is not running?")
        raise SystemExit(e)

def summarize_tasks(client: Client, text: str, model: str) -> dict:
    prompt = f"""
    Please provide a concise summary of the triple backqouted text. 
    Format the output as follows:

    Summary:
    short summary of a task

    Key Takeaways:
    succinct bullet point list of key takeaways

    ```{text}```
    """

    message = {
        "role": "user",
        "content": prompt
    }

    resp = client.chat(model = model, messages = [message,])
    print(type(resp))
    return resp

def build_tasks(url: str, cookie: str) -> list:
    allTasks = get_room_info(url, cookie)

    tasks = []
    for title, desc in allTasks.items():
        tasks.append("## Task '{}'\n{}".format(title, desc))

    return tasks

def main(parser) -> None:
    args = parser.parse_args()

    OLLAMA_URL = os.getenv("OLLAMA_URL")
    MODEL = os.getenv("OLLAMA_MODEL")
    COOKIE = {"connect.sid": os.getenv("THM_SID")}
    THM_URL = THM_API + args.room 

    client = _connect(OLLAMA_URL)
    tasks = build_tasks(THM_URL, COOKIE)
    for text in tasks:
        summarized = summarize_tasks(client, text, MODEL)
        print(summarized["message"]["content"])
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    from dotenv import load_dotenv
    import argparse

    load_dotenv()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--room", help="Name of TryHackMe room to summarize.", type=str, required=True)

    main(parser)
