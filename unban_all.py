import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.errors import FloodWaitError

# ==================================================
# Environment Variables (NO secrets in code)
# ==================================================
API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
SESSION_NAME = os.getenv("TG_SESSION_NAME", "tg_unban_all")
GROUP = os.getenv("TG_GROUP")  # group username / link / id

if not API_ID or not API_HASH or not GROUP:
    raise RuntimeError(
        "❌ Missing environment variables: "
        "TG_API_ID, TG_API_HASH, TG_GROUP"
    )

# ==================================================
# Unban rights (remove all restrictions)
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
# Main logic
# ==================================================
async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        total = 0

        async for user in client.iter_participants(GROUP):
            try:
                await client(EditBannedRequest(
                    channel=GROUP,
                    participant=user.id,
                    banned_rights=UNBAN_RIGHTS
                ))

                total += 1
                print(f"✅ Unbanned: {user.id} | total={total}")

                # anti-flood safety
                await asyncio.sleep(0.3)

            except FloodWaitError as e:
                print(f"⏳ FloodWait {e.seconds}s")
                await asyncio.sleep(e.seconds)

            except Exception as e:
                print(f"⚠️ Skipped {user.id}: {e}")

        print(f"\n🎉 Finished — Unbanned {total} users")

# ==================================================
asyncio.run(main())
