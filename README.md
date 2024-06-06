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
    pip install -r requirements.txt
    ```

3. **Set up the configuration:**
    - Create a `.env` file in the root directory.
    - Add your Discord bot token and API keys for MyAnimeList, IMDb, Reddit, and other services.
    ```env
    DISCORD_TOKEN=your_discord_bot_token
    MAL_CLIENT_ID=your_myanimelist_client_id
    MAL_CLIENT_SECRET=your_myanimelist_client_secret
    IMDB_API_KEY=your_imdb_api_key
    REDDIT_CLIENT_ID=your_reddit_client_id
    REDDIT_CLIENT_SECRET=your_reddit_client_secret
    REDDIT_USER_AGENT=your_reddit_user_agent
    ```

## Configuration

Ensure all API keys and tokens are correctly placed in the `.env` file. This file should be in the root directory of your project.

## Usage

1. **Run the bot:**
    ```bash
    python my_bot.py
    ```

2. **Invite Stella to your Discord server** and start using the commands with the prefix defined in the configuration (default is `S.`).


Thank you for using Stella! We hope this bot makes your Discord server more enjoyable and interactive. If you have any questions or need assistance, feel free to open an issue or reach out to me.
