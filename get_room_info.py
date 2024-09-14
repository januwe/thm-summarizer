#!/usr/bin/env python3

import json
import requests
import os
from markdownify import markdownify as md

def get_tasks(url: str, cookie: str=None) -> dict:
    """
    Returns a dictionary of tasks, given a url and cookie (optional) from TryHackMe.

    Parameters:
        url (str):     TryHackMe API url + room (e.g. https://tryhackme.com/api/tasks/rrootme)
        cookie (str):  Cookie with 'connect_sid' to authenticate

    Return:
        tasks (dict):  dictionary containing tasks of the room
    """

    try:
        resp = requests.get(url, cookies = cookie)

        _tasks = json.loads(resp.text)
        tasks = _tasks["data"]

        return tasks
    except Exception as e:
        raise SystemExit(e)


def get_desc(tasks: dict) -> dict:
    """
    blblab

    Parameters:

    Return:
    """

    room_desc = {}

    for task in tasks:
        title = task["taskTitle"]
        desc = md(task["taskDesc"])

        room_desc.update({f"{title}": desc})

    return room_desc

def get_room_info(url: str, cookie: str) -> dict:
    """
    blblab

    Parameters:

    Return:
    """

    tasks = get_tasks(url, cookie)
    descriptions = get_desc(tasks)

    return descriptions


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    THM_API_URL = "https://tryhackme.com/api/tasks/"
    room = "threatmodelling"

    cookie = {"connect.sid": os.getenv("THM_SID")}

    room_info = get_room_info(THM_API_URL + room, cookie)

    for title in room_info:
        print(f"{title=}")
        print(room_info[title])
        print("")
        break
