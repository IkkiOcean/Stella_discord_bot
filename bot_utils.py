from threading import Timer
import discord
from discord import Forbidden, app_commands
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, Greedy, CommandInvokeError
import requests
import random
import textwrap
import datetime
import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, UnidentifiedImageError
from io import BytesIO
import typing
import asyncio
import mal
from mal import *
from lxml import html
import numpy as np
import urllib.parse
import urllib.request
import re
from asyncio import gather
from bs4 import BeautifulSoup
import math
import certifi
from pymongo import MongoClient
import aiohttp
import praw
from selenium import webdriver
from dotenv import load_dotenv

# Initialize paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / ".vscode"
GENERATED_DIR = BASE_DIR / "generated"
GENERATED_DIR.mkdir(exist_ok=True)

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def asset_font(name: str, size: int):
    return ImageFont.truetype(str(ASSETS_DIR / name), size)


def output_path(name: str) -> str:
    return str(GENERATED_DIR / name)


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _is_image_bytes(data: bytes) -> bool:
    if not data:
        return False
    signatures = (
        b"\x89PNG\r\n\x1a\n",
        b"\xff\xd8\xff",
        b"GIF87a",
        b"GIF89a",
        b"RIFF",
    )
    return data.startswith(signatures)


def open_template(filename: str, fallback_url: str | None = None) -> Image.Image:
    """Load a meme template from bundled assets, with optional URL fallback."""
    local_path = ASSETS_DIR / filename
    if fallback_url:
        url = fallback_url.strip()
        headers = {"User-Agent": user_agent, "Accept": "image/*,*/*"}
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        if not _is_image_bytes(resp.content):
            raise ValueError(
                f"Could not download image template '{filename}' from {url}. "
                "The remote host returned a non-image response."
            )
        return Image.open(BytesIO(resp.content))

    else:
        if local_path.exists():
            with Image.open(local_path) as img:
                return img.copy()
        raise FileNotFoundError(
            f"Template '{filename}' not found in {ASSETS_DIR} and no fallback URL was provided."
        )


def env_flag(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default).lower()).strip().lower() in ("1", "true", "yes", "on")


load_dotenv()

BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "745006368175423489"))
STARTUP_CHANNEL_ID = os.getenv("STARTUP_CHANNEL_ID", "772496570436419592")
ENABLE_ANIME_UPDATES = env_flag("ENABLE_ANIME_UPDATES", False)

_driver = None
_driver_init_failed = False
_driver_init_error = None


class DriverUnavailableError(Exception):
    """Raised when headless Chrome cannot be started."""


def find_chrome_binary():
    configured = os.getenv("CHROME_BINARY_PATH", "").strip()
    if configured and Path(configured).exists():
        return configured

    if sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        ]
    elif sys.platform.startswith("linux"):
        candidates = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
            "/usr/bin/chromium-browser-wayland",
            "/usr/bin/chromium-wayland",
        ]
    else:
        candidates = []

    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return None


def get_driver():
    """Lazy Chrome driver — avoids crashing at import on servers without Chrome."""
    global _driver, _driver_init_failed, _driver_init_error
    if _driver is not None:
        return _driver
    if _driver_init_failed:
        raise DriverUnavailableError(_driver_init_error)

    from selenium.webdriver.chrome.service import Service

    chrome_binary = find_chrome_binary()
    if chrome_binary is None:
        _driver_init_failed = True
        _driver_init_error = (
            "Chrome/Chromium not found. Install Google Chrome, or set "
            "CHROME_BINARY_PATH in .env to your browser executable."
        )
        raise DriverUnavailableError(_driver_init_error)

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary
    options.add_argument("--headless=new")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server=direct://")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    try:
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "").strip()
        if chromedriver_path and Path(chromedriver_path).exists():
            service = Service(chromedriver_path)
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())

        _driver = webdriver.Chrome(service=service, options=options)
        return _driver
    except Exception as exc:
        _driver_init_failed = True
        _driver_init_error = str(exc)
        raise DriverUnavailableError(
            f"Could not start headless Chrome ({exc}). "
            "Install Chrome/Chromium or set CHROME_BINARY_PATH and CHROMEDRIVER_PATH."
        ) from exc


def mongo_uri(name: str, fallback: str = "") -> str:
    uri = os.getenv(name, fallback).strip()
    if not uri:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return uri


cluster = MongoClient(mongo_uri("MONGODB_URI"), tlsCAFile=certifi.where())
client2 = MongoClient(
    mongo_uri("MONGODB_URI_WAIFUS", os.getenv("MONGODB_URI", "")),
    tlsCAFile=certifi.where(),
)
db = cluster["discord"]
mal_collect = db["mal"]
animetriv_collect = db["anime-trivia"]
upd = db["anime-updates"]
listed = db["watchlist"]
chan = db["channels"]
airingg = db["airing"]
db2 = client2["Waifus"]
girl = db2["images"]

redit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID", "YOUR CLIENT ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET", "YOUR CLIENT SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT", "stella-discord-bot"),
)
