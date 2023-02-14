# Usage

## Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications/).
2. Create a new application with some name
3. After creating the application, go to the bot tab, and choose 'Add Bot'
4. Keep a copy of the shown bot token. (This will go inside `keys.json`)
5. Ensure the `Message Content Intent` is selected.
6. Replace `{CLIENT_ID_GOES_HERE}` with the shown application id in the url `https://discord.com/api/oauth2/authorize?permissions=16843776&scope=bot%20applications.commands&client_id={CLIENT_ID_GOES_HERE}`
7. Use the link to invite the bot to a server.

## Running the bot

1. Place [OpenAI API key](https://platform.openai.com/account/api-keys) and
   [Discord bot token](https://discord.com/developers/applications) in keys.json (using keys.json.example as a template).
2. Install dependencies using [Poetry](https://python-poetry.org/docs/): `poetry install`
3. Run `poetry run python bot/main.py`
