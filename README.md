# Telegram Chat Exporter

This Python script leverages the Telethon library to extract and convert Telegram conversations into HTML format, complete with media downloads. It's tailored for exporting messages from private chats, groups, and channels. This tool works especially well in the event where you can not get telegram installed on the host device.

## Features

- **Chronological Message Ordering**: Messages are sorted and displayed in the order they were sent.
- **Media Handling**: Downloads media (images, videos, documents) and includes them in the HTML output.
- **Individual Chat Export**: Each chat or channel is saved in a separate HTML file within a unique directory.
- **Automatic Directory Management**: Creates directories based on chat names and timestamps for organized export.

## Prerequisites

- **Python**: Version 3.x
- **Libraries**: 
  - `Telethon` for interacting with Telegram's API.
  - `python-dotenv` for managing environment variables securely.

### Installation

1. **Install Python**:

   - Download and install Python from [python.org](https://www.python.org/downloads/) if not already installed.

2. **Install Dependencies**:

   - Use pip to install the necessary packages:

     ```bash
     pip install telethon python-dotenv
     ```

3. **Set Up Environment Variables**:

   - Ensure you have or create a `.env` file with these variables:

     ```
     API_ID=your_api_id
     API_HASH=your_api_hash
     PHONE=your_phone_number_with_country_code
     ```

   - Obtain your `API_ID` and `API_HASH` by registering an application on [my.telegram.org](https://my.telegram.org/apps).

## Usage

- Run the script from the command line:

  ```bash
  python telegram_exporter.py

Workflow:
Initialization:
Checks if a .env file exists; creates one if it doesn't.
Loads environment variables or sets default values if not present.
Sets up the Telegram client with the provided credentials.
Directory Setup:
Creates a base directory named with the current timestamp and the phone number, ensuring unique exports.
Authentication:
Initiates the Telegram client with the phone number. Note: This script assumes prior authorization. If not authorized, you'll need to handle this manually or through another script.
Fetching Dialogs:
Retrieves all dialogs (chats, groups, channels) the user has access to.
Exporting Each Chat:
For each dialog:
Creates a sub-directory named after the chat or channel.
Collects messages in reverse order (oldest to newest) for export.
Downloads any media associated with messages.
Generates an HTML file with messages, sender names, timestamps, and media references.
HTML Generation:
Messages are formatted into HTML with sender information, text content, and media thumbnails or links.
Completion:
All chats are processed, and HTML files are saved in the designated directories.

Code Structure
Environment & Client Setup:
Environment variable management for API credentials.
Initialization of the TelegramClient with api_id, api_hash, and phone.
Helper Functions:
get_or_set_env: Manages environment variables or sets defaults.
download_media: Downloads media from messages, returns file names.
export_to_html: Converts chat history into HTML, organizes files, and saves.
Main Function:
Orchestrates the export process by iterating over dialogs and calling export_to_html.

Notes
Authorization: The script cannot automatically handle first-time authorization. Ensure the client is authorized before running this script in an automated environment.
Privacy: This tool can access private information. Use it responsibly and with permission.

License
This project is open-sourced under the MIT License (LICENSE).

Contribution
Contributions are welcomed! Fork this repository, make your changes, and submit a pull request. Here’s how you can contribute:
Bug fixes
Feature requests
Documentation improvements
Code optimization
