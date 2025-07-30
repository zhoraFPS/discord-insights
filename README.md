# discord-insights
A comprehensive Discord bot that automatically collects and provides detailed server statistics through a web API. Available in both Python (discord.py) and Node.js (discord.js) versions.

## 🚀 Features

### Server Information
- **General Details**: Server name, ID, icon, owner information, creation date
- **Boost Status**: Server boost level and boost count  
- **Description**: Server description if available

### Member Statistics
- **Total Count**: All members including bots
- **Human vs Bot Count**: Separate counting of real users and bots
- **Online Status**: Count of currently online members
- **Voice Activity**: Members currently in voice channels
- **Newest Member**: Information about the most recently joined member

### Channel Information
- **Channel Counts**: Text channels, voice channels, and categories
- **Detailed List**: Complete channel information including names, IDs, types, and categories

### Role Management
- **Role Count**: Total number of roles (excluding @everyone)
- **Role Details**: Name, ID, color, and member count for each role

### Emoji Tracking
- **Custom Emojis**: Count and details of all custom server emojis
- **Emoji Information**: Names, IDs, URLs, and animation status

### Activity Monitoring
- **Streaming**: Members currently streaming on platforms like Twitch
- **Gaming**: Members currently playing games
- **Activity Details**: Game names and streaming URLs

## 📋 Requirements

### Python Version
- Python 3.8+
- discord.py
- requests

### Node.js Version  
- Node.js 16+
- discord.js v14
- express
- axios
- dotenv

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/discord-stats-bot.git
cd discord-stats-bot
```

### 2. Choose Your Version

#### Python Version
```bash
pip install discord.py requests
```

#### Node.js Version
```bash
npm install
# or use the provided setup script
chmod +x setup.sh
./setup.sh
```

### 3. Configuration

#### Create Environment File
Copy the `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

#### Required Environment Variables
```env
# Discord Bot Token (from Discord Developer Portal)
DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN_HERE"

# Discord Server ID (Guild ID)
SERVER_ID="123456789012345678"

# API Key for internal communication
API_KEY="your-secure-random-api-key-here-32-characters-minimum"
```

### 4. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" section
4. Create a bot and copy the token
5. Enable the following **Privileged Gateway Intents**:
   - Server Members Intent
   - Presence Intent
6. Invite the bot to your server with appropriate permissions

### 5. Getting Your Server ID

1. Enable Developer Mode in Discord:
   - User Settings → Advanced → Developer Mode
2. Right-click on your server name
3. Click "Copy Server ID"

## 🏃‍♂️ Usage

### Python Version
```bash
python bot.py
```

### Node.js Version
```bash
node app.js
# or
./setup.sh
```

## 🔌 API Endpoints

### Node.js Version Endpoints

#### POST `/api/update_stats`
Updates the server statistics (used internally by the bot)

**Headers:**
- `X-API-Key`: Your API key
- `Content-Type`: application/json

#### GET `/api/get_stats`
Retrieves current server statistics

**Response Example:**
```json
{
  "last_updated": "2025-07-30T12:00:00.000Z",
  "server": {
    "name": "My Discord Server",
    "id": "123456789012345678",
    "icon_url": "https://cdn.discordapp.com/icons/...",
    "owner_name": "ServerOwner",
    "boost_level": 2,
    "boost_count": 5
  },
  "members": {
    "total_count": 150,
    "human_count": 130,
    "bot_count": 20,
    "online_count": 45
  },
  "channels": {
    "text_channel_count": 15,
    "voice_channel_count": 8,
    "category_count": 5
  }
}
```

#### GET `/`
Simple health check endpoint

## 📁 File Structure

```
discord-stats-bot/
├── bot.py                 # Python version of the bot
├── app.js                 # Node.js version with web server
├── setup.sh              # Setup script for Node.js version
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore file
├── package.json         # Node.js dependencies
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## ⚙️ Configuration Options

### Update Intervals
- **Python Version**: 1 minute (configurable in `@tasks.loop()`)
- **Node.js Version**: 2 minutes (configurable in `setInterval()`)

### API Integration
Both versions can send data to external APIs. Configure the `API_ENDPOINT` in your environment or code:

**Python Version:**
```python
API_ENDPOINT = os.getenv("API_ENDPOINT", "https://your-website.com/api/update_stats")
```

**Node.js Version:**
The Node.js version includes a built-in web server and API, but can also be configured to send data externally.

## 🔒 Security Considerations

1. **Never commit your `.env` file** - Add it to `.gitignore`
2. **Keep your bot token secret** - Regenerate if compromised
3. **Use strong API keys** - Generate random strings of 32+ characters
4. **Limit bot permissions** - Only grant necessary Discord permissions
5. **Validate API requests** - The bot includes API key validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check that all environment variables are properly set
2. Ensure the bot has the required permissions on your Discord server
3. Verify that Privileged Gateway Intents are enabled
4. Check the console for error messages

## 🔄 Version Differences

| Feature | Python Version | Node.js Version |
|---------|---------------|-----------------|
| Web Server | ❌ External API only | ✅ Built-in Express server |
| API Endpoints | ❌ | ✅ GET/POST endpoints |
| Update Interval | 1 minute | 2 minutes |
| Dependencies | discord.py, requests | discord.js, express, axios |
| Use Case | Simple stats collection | Full web application |

Choose the Python version for simple statistics collection, or the Node.js version if you need a complete web application with API endpoints.
