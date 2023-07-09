#!/usr/bin/env bash
##############################################################
# Script name: 0-setup_web_static.sh
# Description: Sets up a web server for web_static deployment.
##############################################################

# Install Nginx if it is not already installed
if ! command -v nginx &> /dev/null; then
   sudo apt-get update
   sudo apt-get -y install nginx
fi

# Create necessary directories if they don't already exist
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file for testing
sudo echo "Test Page" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate the symbolink link
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Grant ownership of the /data/ directory to ubuntu user and group
sudo chown -R ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sudo sed -i '/^server {/a \ \n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' "$config_file"

# Restart Nginx
sudo service nginx restart
