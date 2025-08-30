import asyncio
import os
import sys
from pyrogram import filters
from main.helpers.utils.handler import BOT


# ============================================================
# UPDATE BOT
# ============================================================
@BOT.COMMAND("update", filters.private)
@BOT.OWNER
async def update_command(client, message):
    msg = await message.reply_text("🔄 Sedang memperbarui bot...")

    try:
        # Jalankan git pull
        process = await asyncio.create_subprocess_shell(
            "git pull",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() + "\n" + stderr.decode().strip()

        if "Already up to date." in output or "Sudah yang terbaru" in output:
            await msg.edit_text("✅ Bot sudah versi terbaru, tidak perlu update.")
            return

        await msg.edit_text(
            f"✅ Update berhasil!\n\n<code>{output}</code>\n\n🔁 Bot akan restart..."
        )
        await asyncio.sleep(2)

        # Restart bot
        os.execv(sys.executable, [sys.executable, "-m", "main"])

    except Exception as e:
        await msg.edit_text(f"❌ Gagal update:\n<code>{e}</code>")


# ============================================================
# UPDATE INFO
# ============================================================
@BOT.COMMAND("updateinfo", filters.private)
@BOT.OWNER
async def update_info(client, message):
    msg = await message.reply_text("🔎 Mengecek informasi update...")

    try:
        # Ambil branch saat ini
        branch_proc = await asyncio.create_subprocess_shell(
            "git rev-parse --abbrev-ref HEAD",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        branch_out, _ = await branch_proc.communicate()
        branch = branch_out.decode().strip()

        # Ambil commit terakhir
        commit_proc = await asyncio.create_subprocess_shell(
            "git log -1 --pretty=format:'%h | %s | %an | %cr'",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        commit_out, _ = await commit_proc.communicate()
        commit_info = commit_out.decode().strip()

        text = (
            f"📌 <b>Informasi Update Bot</b>\n\n"
            f"🔖 Branch: <code>{branch}</code>\n"
            f"📝 Commit terakhir:\n<blockquote>{commit_info}</blockquote>\n"
            f"🚀 Gunakan /update untuk menarik versi terbaru."
        )

        await msg.edit_text(text)

    except Exception as e:
        await msg.edit_text(f"❌ Gagal mengambil info update:\n<code>{e}</code>")

