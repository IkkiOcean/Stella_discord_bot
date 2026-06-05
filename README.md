# Stella - The Ultimate Discord Bot

Welcome to Stella's GitHub repository! Stella is a versatile Discord bot designed to enhance your server with a wide range of features, from anime and movie searches to image manipulation, Reddit integration, and more. Stella also includes moderation tools, role-play commands, utility functions, and fun activities to keep your community engaged.

## Features

### MyAnimeList Integration
- **Anime Search:** Search for anime and get detailed information.
- **Manga Search:** Search for manga and retrieve detailed information.
- **User Profiles:** View MyAnimeList user profiles and statistics.
- **Character Search:** Search for anime/manga characters and get detailed information.

### IMDb Integration
- **Movie Search:** Search for movies and access detailed information, including cast, ratings, and summaries.
- **TV Show Search:** Search for TV shows and get comprehensive details.

### Anime Release Reminders
- **DM Reminders:** Get reminders for anime releases sent directly to your DMs.
- **Watchlist:** Maintain a personal watchlist of your favorite anime.
- **Currently Airing:** View a list of currently airing anime.

### Image Manipulation
- **Filters:** Apply various filters to images.
- **Editing:** Edit images with text, overlays, and more using Pillow.

### Reddit Integration
- **Subreddit Posts:** Fetch and display posts from specified subreddits.
- **User Profiles:** Retrieve Reddit user profiles and statistics.
- **Hot/Top Posts:** Get hot or top posts from a subreddit.

### Moderation Commands
- **Kick/Ban:** Remove users from the server.
- **Mute/Unmute:** Temporarily mute or unmute users.
- **Warn:** Issue warnings to users and keep a record of warnings.
- **Purge:** Bulk delete messages in a channel.

### Role-Play Commands
- **Hug/Kiss/Punch:** Send role-play interactions to other users.
- **Emotes:** Send various role-play emotes.

### Utility Commands
- **Announcement Embed:** Create announcement embeds for important messages.
- **YouTube Video Search:** Search for YouTube videos and share them.
- **Polling:** Create and manage polls.
- **Wallpaper Search:** Search for and display wallpapers.
- **User Info:** Retrieve and display user information.
- **Server Info:** Retrieve and display server information.

### Fun Features
- **Chase the Runner Game:** An interactive game where users chase a runner in the chat.
- **Roasting Commands:** Generate fun and random roast messages using APIs.

## Command List

![command list](https://github.com/IkkiOcean/Stella_discord_bot/blob/main/command_list.jpg)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/IkkiOcean/Stella-discord-bot.git
    cd stella-discord-bot
    ```

2. **Install the dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Linux/macOS
    pip install -r requirements.txt
    ```

3. **Set up the configuration:**
    - Copy `.env.example` to `.env` in the root directory.
    - Add your Discord bot token, MongoDB URIs, and optional API keys.
    ```bash
    cp .env.example .env
    ```
    ```env
    DISCORD_TOKEN=your_discord_bot_token
    MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/myFirstDatabase
    MONGODB_URI_WAIFUS=mongodb+srv://user:password@cluster.mongodb.net/myFirstDatabase
    REDDIT_CLIENT_ID=your_reddit_client_id
    REDDIT_CLIENT_SECRET=your_reddit_client_secret
    REDDIT_USER_AGENT=stella-discord-bot
    CHROMEDRIVER_PATH=/usr/bin/chromedriver
    ```

## Linux server deployment

1. Install system dependencies (Ubuntu/Debian example):
    ```bash
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip chromium-browser chromium-chromedriver
    ```

2. Clone the repo, create a venv, install Python packages, and configure `.env` as above.

3. Run the bot:
    ```bash
    source venv/bin/activate
    python my_bot.py
    ```

4. For process managers (systemd, Docker, Railway, etc.), the included `Procfile` runs:
    ```
    worker: python my_bot.py
    ```

**Notes:**
- The bot uses **discord.py 2.x** and requires the **Message Content Intent** enabled in the [Discord Developer Portal](https://discord.com/developers/applications).
- Anime update checking uses headless Chrome via Selenium. On Linux, either install Chrome/Chromium + chromedriver or leave `CHROMEDRIVER_PATH` empty to auto-download via `webdriver-manager`.
- Meme/image assets and fonts live in `.vscode/`; generated images are written to `generated/`.

## Usage

1. **Run the bot:**
    ```bash
    python my_bot.py
    ```

2. **Invite Stella to your Discord server** and start using the commands with the prefix defined in the configuration (default is `S.`).


Thank you for using Stella! We hope this bot makes your Discord server more enjoyable and interactive. If you have any questions or need assistance, feel free to open an issue or reach out to me.
