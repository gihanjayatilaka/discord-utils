# Outputs an HTML file.
#
# To get a channel ID, right click on it and choose "Copy ID".
docker run --rm -it -v path-to-save-dir:/out tyrrrz/discordchatexporter:stable export -t $DISCORD_TOKEN -c $DISCORD_CHANNEL_ID --after 1/1/2023 --before 1/1/2025
