import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.errors import FloodWaitError

# ==================================================
# Environment Variables
# ==================================================
API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
SESSION_NAME = os.getenv("TG_SESSION_NAME", "tg_unban_all")
GROUP = os.getenv("TG_GROUP")  # Chat ID only: -100xxxxxxxxxx

if not API_ID or not API_HASH or not GROUP:
    raise RuntimeError("Missing environment variables")

# ==================================================
# Unban rights
# ==================================================
UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=False,
    s
