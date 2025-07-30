#!/bin/bash

# Display a message so we know what's happening
echo "=> Running 'npm install' to install all packages..."

# Execute the installation command
npm install

# Display another message
echo "=> Installation completed. Now starting the bot (app.js)..."

# Start the bot
node app.js