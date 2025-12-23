# Discord Music Bot 🎶

A **Discord music bot** built with Python, `discord.py`, and `yt-dlp` for streaming music from YouTube.  
Designed for **personal and educational purposes** to explore Discord bot development, asynchronous Python, and media streaming.

---

## Features

- 🎵 **Play YouTube music & playlists** using `/play <url>` or `/play <search query>`  
- ⏯ **Pause & Resume** playback with `/pause` and `/resume`  
- ⏭ **Skip** current track with `/skip`  
- 🧹 **Clear queue** with `/clear`  
- ❌ **Remove specific track** with `/remove <index>`  
- 📜 **Queue display** with `/queue` showing current and upcoming tracks  
- 🔁 **Loop modes**: `off`, `track`, or `queue` via `/loop <mode>`  
- ⏳ **Idle timeout**: bot auto-disconnects from voice channel after 5 minutes of inactivity  
- 🔇 **Automatic error handling** for unavailable videos or playback issues  

---

## Setup

### 1. Clone this repository
```bash
git clone https://github.com/Richard-Wz/Discord-Music-Bot.git
cd Discord-Music-Bot
```

### 2. Create a `.env` file with your Discord bot token
```env
DISCORD_TOKEN=your_bot_token_here
```

### 3. Build and run with Docker
```bash
docker compose up --build
```

### 4. Invite your bot to a server
Use the OAuth2 URL with `bot` and `applications.commands` scopes.

---

## Commands

| Command | Description |
|---------|-------------|
| `/play <url>` | Play a song or playlist from YouTube |
| `/queue` | Display current queue |
| `/skip` | Skip the current track |
| `/pause` | Pause playback |
| `/resume` | Resume playback |
| `/clear` | Clear the queue |
| `/remove <n>` | Remove the nth track from the queue |
| `/loop <mode>` | Set loop mode: `off`, `track`, `queue` |

---

## Tech Stack

- **Python 3.12**
- **discord.py** - Discord API wrapper
- **yt-dlp** - YouTube video extraction
- **FFmpeg** - Audio streaming
- **Docker & docker-compose** - Easy deployment

---

## Disclaimer

### ⚠️ Educational & Personal Use Only

This bot streams audio from YouTube to Discord for **learning and personal projects only**.

- Hosting or providing this bot publicly for music streaming may violate **YouTube's Terms of Service**.
- Use at your own risk. This repository does not distribute copyrighted content.

---

## Acknowledgements

This project was built using the following amazing open-source tools and libraries:

- **[discord.py](https://github.com/Rapptz/discord.py)** - Python wrapper for the Discord API
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - A feature-rich command-line audio/video downloader
- **[FFmpeg](https://ffmpeg.org/)** - Complete solution for recording, converting, and streaming audio and video
- **[PyNaCl](https://github.com/pyca/pynacl)** - Python binding to libsodium for voice support

Special thanks to the Discord.py community and all contributors to the libraries that made this project possible.

---

## Support

If you find this project helpful, consider giving it a ⭐ on GitHub!