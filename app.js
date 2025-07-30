// app.js
require('dotenv').config();

const express = require('express');
const axios = require('axios');
const { Client, GatewayIntentBits, Partials } = require('discord.js');

// --- Configuration ---
const BOT_TOKEN = process.env.DISCORD_TOKEN;
const SERVER_ID = process.env.SERVER_ID;
const API_KEY = process.env.API_KEY;
// The host (Pterodactyl) provides the port via environment variable `SERVER_PORT` or `PORT`
const PORT = process.env.SERVER_PORT || process.env.PORT || 3000;

// ==============================================================================
//  EXPRESS WEB API
// ==============================================================================

const app = express();
app.use(express.json());

let globalStats = {};

app.post('/api/update_stats', (req, res) => {
    if (req.headers['x-api-key'] !== API_KEY) {
        return res.status(403).json({ error: 'Unauthorized' });
    }
    globalStats = req.body;
    globalStats.last_updated_by_bot = new Date().toISOString();
    console.log('Statistics successfully received from bot process.');
    res.status(200).json({ status: 'success' });
});

app.get('/api/get_stats', (req, res) => {
    if (Object.keys(globalStats).length === 0) {
        return res.status(404).json({ error: 'Stats are not available yet.' });
    }
    res.json(globalStats);
});

app.get('/', (req, res) => {
    res.send('Node.js web server for Discord bot is online!');
});

// ==============================================================================
//  DISCORD.JS BOT
// ==============================================================================

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildPresences,
    ],
    partials: [Partials.Channel],
});

client.once('ready', () => {
    console.log(`Bot logged in as ${client.user.tag}!`);
    updateAndPostStats();
    setInterval(updateAndPostStats, 2 * 60 * 1000); // 2 minute interval
});

async function updateAndPostStats() {
    try {
        console.log(`[${new Date().toLocaleString()}] Collecting server statistics...`);
        const guild = await client.guilds.fetch(SERVER_ID);
        if (!guild) return console.error('Server not found!');
        await guild.members.fetch();

        const payload = {
            server: {
                name: guild.name,
                id: guild.id,
                icon_url: guild.iconURL(),
            },
            members: {
                total_count: guild.memberCount,
                human_count: guild.members.cache.filter(member => !member.user.bot).size,
                bot_count: guild.members.cache.filter(member => member.user.bot).size,
                online_count: guild.members.cache.filter(m => m.presence?.status !== 'offline').size,
            }
        };

        const apiEndpoint = `http://127.0.0.1:${PORT}/api/update_stats`;
        const headers = { 'X-API-Key': API_KEY };
        await axios.post(apiEndpoint, payload, { headers });

    } catch (error) {
        console.error('Error collecting or sending stats:', error.message);
    }
}

// ==============================================================================
//  START LOGIC
// ==============================================================================

app.listen(PORT, () => {
    console.log(`Web server running on port ${PORT}`);
    if (!BOT_TOKEN || !SERVER_ID || !API_KEY) {
        console.error("ERROR: One or more environment variables (DISCORD_TOKEN, SERVER_ID, API_KEY) were not set!");
    } else {
        client.login(BOT_TOKEN);
    }
});