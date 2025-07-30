import discord
from discord.ext import tasks
import requests
import json
import os
from datetime import datetime


# --- Configuration ---
# Load sensitive data from environment variables for better security
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Better: os.getenv("DISCORD_TOKEN")
SERVER_ID = 123456789012345678      # Your server ID as integer (number)
API_ENDPOINT = os.getenv("API_ENDPOINT", "https://your-website.com/api/update_stats")
API_KEY = os.getenv("API_KEY", "YOUR_SECRET_API_KEY")

# --- Set up intents (necessary for member and status information) ---
intents = discord.Intents.default()
intents.members = True   # Allows access to the member list
intents.presences = True # Allows access to online status and activities
intents.guilds = True    # Ensures that guild information is available

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Executed when the bot successfully connects to Discord."""
    print(f'Bot logged in as {client.user}.')
    print("Starting regular data collection...")
    # Start the background task when the bot is ready
    update_stats.start()

@tasks.loop(minutes=1) # Execute the task every minute
async def update_stats():
    """Collects all server statistics and sends them to the API."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Collecting server statistics...")
    guild = client.get_guild(SERVER_ID)

    if guild is None:
        print(f"Error: Server with ID {SERVER_ID} not found. Check the ID and if the bot is on the server.")
        return

    # --- 1. General server information ---
    server_info = {
        'name': guild.name,
        'id': guild.id,
        'icon_url': str(guild.icon.url) if guild.icon else None,
        'owner_name': guild.owner.name if guild.owner else 'Unknown',
        'owner_id': guild.owner_id,
        'creation_date': guild.created_at.isoformat(), # ISO format is standard for APIs
        'boost_level': guild.premium_tier,
        'boost_count': guild.premium_subscription_count,
        'description': guild.description,
    }

    # --- 2. Member statistics ---
    all_members = guild.members
    bots = [member for member in all_members if member.bot]
    humans = [member for member in all_members if not member.bot]
    online_members = [m for m in all_members if m.status != discord.Status.offline]
    
    # Find the newest member (who joined most recently)
    newest_member = max(all_members, key=lambda m: m.joined_at)

    member_stats = {
        'total_count': guild.member_count,
        'human_count': len(humans),
        'bot_count': len(bots),
        'online_count': len(online_members),
        'members_in_voice_count': sum(1 for m in all_members if m.voice and m.voice.channel),
        'newest_member': {
            'name': newest_member.name,
            'joined_at': newest_member.joined_at.isoformat()
        }
    }

    # --- 3. Channel information ---
    channel_info = {
        'text_channel_count': len(guild.text_channels),
        'voice_channel_count': len(guild.voice_channels),
        'category_count': len(guild.categories),
        'list': [{'name': ch.name, 'id': ch.id, 'type': str(ch.type), 'category': ch.category.name if ch.category else None} for ch in guild.channels]
    }

    # --- 4. Role information ---
    # We exclude the @everyone role as it's usually not relevant
    roles = [r for r in guild.roles if not r.is_default()]
    role_info = {
        'count': len(roles),
        # List with details for each role
        'list': [{'name': r.name, 'id': r.id, 'color': str(r.color), 'member_count': len(r.members)} for r in roles]
    }

    # --- 5. Emoji information ---
    emoji_info = {
        'count': len(guild.emojis),
        'list': [{'name': e.name, 'id': e.id, 'url': str(e.url), 'is_animated': e.animated} for e in guild.emojis]
    }

    # --- 6. Activity statistics ---
    streamers = [m for m in online_members if isinstance(m.activity, discord.Streaming)]
    playing_members = [m for m in online_members if m.activity and m.activity.type == discord.ActivityType.playing]

    activity_stats = {
        'streaming_count': len(streamers),
        'streaming_list': [{'member_name': s.name, 'game': s.activity.name, 'twitch_url': s.activity.url} for s in streamers],
        'playing_count': len(playing_members),
        'playing_list': [{'member_name': p.name, 'game': p.activity.name} for p in playing_members]
    }


    # --- Combine everything into one large payload ---
    payload = {
        'last_updated': datetime.now().isoformat(),
        'server': server_info,
        'members': member_stats,
        'channels': channel_info,
        'roles': role_info,
        'emojis': emoji_info,
        'activity': activity_stats
    }

    # Headers for authentication to your API
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
    }

    # Send data to your website API
    try:
        response = requests.post(API_ENDPOINT, data=json.dumps(payload), headers=headers, timeout=15)
        if response.status_code == 200:
            print(f"Data successfully sent to website. Response: {response.text}")
        else:
            print(f"Error sending data. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the API request: {e}")

@update_stats.before_loop
async def before_update_stats():
    """Waits until the bot is fully ready before the loop starts."""
    await client.wait_until_ready()

# Start the bot
if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or str(SERVER_ID) == "123456789012345678":
        print("ERROR: Please fill in the BOT_TOKEN and SERVER_ID variables in bot.py!")
    else:
        client.run(BOT_TOKEN)