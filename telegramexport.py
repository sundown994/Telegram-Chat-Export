from telethon import TelegramClient, events
from telethon.tl.types import User, Chat, Channel
import asyncio
from dotenv import load_dotenv, set_key
import os
from os.path import exists
from datetime import datetime
import html

# Check if .env file exists
env_path = '.env'
if not exists(env_path):
    print(".env file not found. We'll create one.")
    open(env_path, 'a').close()  # Create if not exists

# Load environment variables or use defaults
load_dotenv(env_path)

def get_or_set_env(prompt, env_var, default=None):
    """Get environment variable or use default if not set."""
    value = os.getenv(env_var)
    if value:
        return value
    elif default is not None:
        set_key(env_path, env_var, str(default))
        return default
    else:
        raise ValueError(f"Environment variable {env_var} not set and no default provided.")

# Collect credentials with defaults
api_id = int(get_or_set_env("Enter your API ID", 'API_ID', default='25120282'))
api_hash = get_or_set_env("Enter your API Hash", 'API_HASH', default='ea7cf20381882549234fcda51ed6c036')
phone = get_or_set_env("Enter your phone number (including country code)", 'PHONE', default='+19842021729')

# Directory to save files with phone number and timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
base_save_dir = os.path.join(os.getcwd(), f'telegram_export_{phone.strip("+")}_{timestamp}')
if not os.path.exists(base_save_dir):
    os.makedirs(base_save_dir)

# Client setup
client = TelegramClient('session_name', api_id, api_hash)

async def download_media(message, dir_name):
    """Download media from a message to the specified directory."""
    if hasattr(message, 'media'):
        try:
            file_path = await client.download_media(message.media, dir_name)
            if file_path:
                print(f"Downloaded file to {file_path}")
                return os.path.basename(file_path)
        except Exception as e:
            print(f"Failed to download: {e}")
    return None

async def export_to_html(entity, export_dir):
    """Export chat history to HTML with messages in chronological order."""
    if isinstance(entity, (Chat, Channel)):
        chat_name = entity.title
    elif isinstance(entity, User):
        chat_name = f"{entity.first_name or ''} {entity.last_name or ''}".strip() or str(entity.id)
    else:
        chat_name = "Unknown Chat"

    # Create subfolder for this chat or group
    chat_dir = os.path.join(export_dir, chat_name.replace('/', '_'))
    if not os.path.exists(chat_dir):
        os.makedirs(chat_dir)

    messages = await client.get_messages(entity, limit=None)
    messages = messages[::-1] # Reverse to start from oldest
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{html.escape(chat_name or "Unnamed Chat")}</title>
</head>
<body>
<h1>{html.escape(chat_name or "Unnamed Chat")}</h1>
"""

    for message in messages:
        media_file = await download_media(message, chat_dir)
        media_html = f'<img src="{media_file}" alt="Chat Media">' if media_file else '[No Media]'
        sender_name = message.sender.first_name if message.sender else 'Unknown'
        sender_name_safe = html.escape(sender_name or 'Unknown')

        message_content = message.message or '[No Text Content]'
        formatted_date = message.date.strftime("%A, %d %B %Y, %I:%M %p")
        html_content += f"""
        <div>
            <p><b>{sender_name_safe}</b> - {formatted_date}</p>
            <p>{html.escape(message_content)}</p>
            {media_html}
        </div>
        """
    
    html_content += "</body></html>"
    
    html_file_path = os.path.join(chat_dir, f"{chat_name.replace('/', '_')}.html")
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Chat with {chat_name or 'Unknown'} exported to {html_file_path}")
    return chat_name

async def main():
    await client.start(phone)
    if not await client.is_user_authorized():
        # Note: This part cannot work directly in a non-interactive environment like Automator or a bash script
        # You would need to handle authorization separately or ensure the client is authorized before running this
        raise Exception("User not authorized. Please authorize the client interactively first.")

    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        try:
            await export_to_html(dialog.entity, base_save_dir)
        except Exception as e:
            print(f"Failed to export chat with {dialog.entity.id}: {e}")

    print(f"Export completed. Files saved in {base_save_dir}")

if __name__ == '__main__':
    with client:
        asyncio.get_event_loop().run_until_complete(main())
