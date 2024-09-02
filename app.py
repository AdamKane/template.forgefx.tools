import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import List
from slack_wrapper import SlackWrapper



app = FastAPI()
slack = SlackWrapper()



@app.get("/")
async def root():
    return {"app": "slack.forgefx.tools v2024.08.28-01"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/team-name")
async def get_team_name():
    try:
        response = slack.team_info()
        team_name = response["team"]["name"]
        return {"team_name": team_name}
    except Exception as e:
        return {"error": str(e)}

@app.post("/find-bookmarks-by-link-url")
async def find_bookmarks_by_link_url(url: str):
    bookmarks = slack.find_bookmarks_by_url(url)
    return {"bookmarks": bookmarks}

@app.post("/delete-bookmarks")
async def delete_bookmarks(channel_id: str, bookmark_ids: List[str]):
    results = slack.delete_bookmarks(channel_id, bookmark_ids)
    return {"results": results}
