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
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False
)

# ==================================================
async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        target = None

        print("🔍 Searching for group in dialogs...")
        async for dialog in client.iter_dialogs():
            if dialog.id == int(GROUP):
                target = dialog.entity
                break

        if not target:
            raise RuntimeError(
                "❌ Group not found in dialogs. "
                "Make sure the account has sent a message in the group."
            )

        print("✅ Group found. Starting unban process...")

        total = 0
        async for user in client.iter_participants(target):
            try:
                await client(EditBannedRequest(
                    channel=target,
                    participant=user.id,
                    banned_rights=UNBAN_RIGHTS
                ))

                total += 1
                print(f"✅ Unbanned: {user.id} | total={total}")
                await asyncio.sleep(0.3)

            except FloodWaitError as e:
                print(f"⏳ FloodWait {e.seconds}s")
                await asyncio.sleep(e.seconds)

            except Exception as e:
                print(f"⚠️ Skip {user.id}: {e}")

        print(f"\n🎉 Finished — Unbanned {total} users")

asyncio.run(main())
