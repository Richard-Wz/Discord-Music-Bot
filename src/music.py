import discord
import yt_dlp
import asyncio
from collections import deque

# Options for yt-dlp
ytdl_opts = {
    "format": "bestaudio[acodec=opus]/bestaudio",
    "quiet": True,
    # Allow playlist
    "noplaylist": False,
}

# Options for FFmpeg
ffmpeg_opts = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn -loglevel quiet",
}

ytdl = yt_dlp.YoutubeDL(ytdl_opts)

# Timeout for idle voice connections in seconds (5 minutes)
IDLE_TIMEOUT = 300

# Music management class
class Music:
    # Initialize with bot instance
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}        # guild_id -> deque
        self.idle_tasks = {}    # guild_id -> asyncio.Task
        self.loop_mode = {}     # guild_id -> 'off'/'track'/'queue'
        self.current_track = {} # guild_id -> currently playing track info


    # Get or create the queue for a guild
    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = deque()
        return self.queues[guild_id]

    # Cancel any existing idle timer for the guild
    def cancel_idle(self, guild_id):
        task = self.idle_tasks.pop(guild_id, None)
        if task:
            task.cancel()

    # Start an idle timer for the guild
    async def start_idle_timer(self, guild: discord.Guild, vc: discord.VoiceClient):
        async def idle():
            await asyncio.sleep(IDLE_TIMEOUT)
            if vc.is_connected() and not vc.is_playing():
                await vc.disconnect()

        self.cancel_idle(guild.id)
        self.idle_tasks[guild.id] = asyncio.create_task(idle())

    # Play a track based on user query
    async def play(self, interaction: discord.Interaction, query: str):
        # Defer response to avoid Discord 3-second timeout
        await interaction.response.defer()

        # User must be in a voice channel
        if not interaction.user.voice:
            await interaction.followup.send(
                "You must be in a voice channel to play music.",
                ephemeral=True
            )
            return

        channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client

        # Connect to voice channel if not already connected
        if not vc:
            vc = await channel.connect()

        # Cancel idle timer since we are actively playing/queueing
        self.cancel_idle(interaction.guild.id)

        # Get the queue for this guild
        queue = self.get_queue(interaction.guild.id)

        # yt-dlp is blocking, run in executor
        loop = asyncio.get_running_loop()
        info = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(query, download=False)
        )

        # Handle single video or playlist
        entries = info["entries"] if "entries" in info else [info]

        # Add all tracks to queue
        for entry in entries:
            queue.append({
                "title": entry.get("title", "Unknown"),
                "url": entry.get("url"),
            })

        # Start playback if nothing is currently playing
        if not vc.is_playing():
            await self.play_next(interaction.guild, vc)

        await interaction.followup.send(
            f"➕ Added **{len(entries)}** track(s) to the queue."
        )

    # Play the next track in the queue
    async def play_next(self, guild: discord.Guild, vc: discord.VoiceClient):
        queue = self.get_queue(guild.id)
        mode = self.loop_mode.get(guild.id, "off")

        # Decide which track to play
        if mode == "track" and guild.id in self.current_track:
            track = self.current_track[guild.id]
        elif mode == "queue" and guild.id in self.current_track:
            # Reinsert last track to the end of queue
            last = self.current_track[guild.id]
            queue.append(last)
            track = queue.popleft()
            self.current_track[guild.id] = track
        else:
            if not queue:
                await self.start_idle_timer(guild, vc)
                return
            track = queue.popleft()
            self.current_track[guild.id] = track

        source = discord.FFmpegPCMAudio(track["url"], **ffmpeg_opts)

        def after_play(error):
            if error:
                print("Playback error:", error)
            fut = asyncio.run_coroutine_threadsafe(
                self.play_next(guild, vc),
                self.bot.loop
            )
            try:
                fut.result()
            except:
                pass

        vc.play(source, after=after_play)

    # ===== Playback control methods =====

    # Pause playback
    def pause(self, vc):
        if vc and vc.is_playing():
            vc.pause()
            return True
        return False

    # Resume playback
    def resume(self, vc):
        if vc and vc.is_paused():
            vc.resume()
            return True
        return False

    # Clear the queue for a guild
    def clear_queue(self, guild_id):
        self.get_queue(guild_id).clear()

    # Remove a specific track from the queue by index
    def remove_from_queue(self, guild_id, index: int):
        queue = self.get_queue(guild_id)
        if 0 <= index < len(queue):
            queue.rotate(-index)
            removed = queue.popleft()
            queue.rotate(index)
            return removed
        return None
    
    # Set loop mode 
    def set_loop(self, guild_id, mode: str):
        if mode.lower() in ["off", "track", "queue"]:
            self.loop_mode[guild_id] = mode.lower()
            return True
        return False