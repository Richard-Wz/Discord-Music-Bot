import os
import discord
from discord.ext import commands

# Import the Music class from music.py
from music import Music

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
music = Music(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

# Play command to add a track to the queue and start playback
@bot.tree.command(name="play", description="Play audio from a URL")
async def play(interaction: discord.Interaction, query: str):
    await music.play(interaction, query)

# Stop playback and disconnect
@bot.tree.command(name="stop", description="Stop playback")
async def stop(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc:
        await vc.disconnect()
        await interaction.response.send_message("⏹️ Stopped.")
    else:
        await interaction.response.send_message(
            "Not connected.", ephemeral=True
        )

# Show current queue
@bot.tree.command(name="queue", description="Display the current music queue")
async def queue(interaction: discord.Interaction):
    q = music.get_queue(interaction.guild.id)
    if not q and interaction.guild.id not in music.current_track:
        await interaction.response.send_message("📭 Queue is empty.", ephemeral=True)
        return

    message = ""
    # Currently playing
    if interaction.guild.id in music.current_track:
        message += f"▶️ Now Playing: **{music.current_track[interaction.guild.id]['title']}**\n"

    # Queue list
    if q:
        message += "\n📜 Up Next:\n"
        for i, track in enumerate(q, start=1):
            message += f"{i}. {track['title']}\n"

    await interaction.response.send_message(message)

# Skip current track
@bot.tree.command(name="skip", description="Skip current track")
async def skip(interaction: discord.Interaction):
    vc = interaction.guild.voice_client

    if not vc or not vc.is_playing():
        await interaction.response.send_message(
            "Nothing is playing."
        )
        return

    vc.stop()
    await interaction.response.send_message("⏭️ Skipped.")

# Pause playback
@bot.tree.command(name="pause", description="Pause playback")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if music.pause(vc):
        await interaction.response.send_message("⏸ Paused.")
    else:
        await interaction.response.send_message(
            "Nothing is playing.", ephemeral=True
        )

# Resume playback
@bot.tree.command(name="resume", description="Resume playback")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if music.resume(vc):
        await interaction.response.send_message("▶️ Resumed.")
    else:
        await interaction.response.send_message(
            "Nothing is paused.", ephemeral=True
        )

# Clear the entire queue
@bot.tree.command(name="clear", description="Clear the queue")
async def clear(interaction: discord.Interaction):
    music.clear_queue(interaction.guild.id)
    await interaction.response.send_message("🧹 Queue cleared.")

# Remove a specific track from the queue by index
@bot.tree.command(name="remove", description="Remove a song from the queue")
async def remove(interaction: discord.Interaction, index: int):
    removed = music.remove_from_queue(
        interaction.guild.id, index - 1
    )
    if removed:
        await interaction.response.send_message(
            f"❌ Removed **{removed['title']}**"
        )
    else:
        await interaction.response.send_message(
            "Invalid queue index.", ephemeral=True
        )

# Loop mode
@bot.tree.command(name="loop", description="Set loop mode: off / track / queue")
async def loop(interaction: discord.Interaction, mode: str):
    if music.set_loop(interaction.guild.id, mode):
        await interaction.response.send_message(f"🔁 Loop mode set to **{mode}**")
    else:
        await interaction.response.send_message(
            "Invalid mode! Use: off, track, or queue", ephemeral=True
        )

bot.run(TOKEN)