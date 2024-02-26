#!/usr/bin/bash

echo "Starting bot..."


if [ -z "$DISCORD_TOKEN" ]; then
    echo "DISCORD_TOKEN is not set please set it in the environment variables"
    exit 1
fi
setup=false
# check if data directory exists
if [ ! -d "data" ]; then
    echo "Creating data directory..."
    mkdir data
    setup=true
fi


# clone stable diffusion if it doesn't exist
if [ ! -d "data/stable-diffusion-webui" ]; then
    echo "Cloning and installing stable diffusion..."
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git data/stable-diffusion-webui
    setup=true
fi

# install stable diffusion if it hasn't been installed
if [ "$setup" = true ]; then
    (cd data/stable-diffusion-webui && ./webui.sh --api) & python Bot.py setup && fg
else
    (cd data/stable-diffusion-webui && ./webui.sh --api) & python Bot.py && fg
fi

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT