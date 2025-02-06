#elegram Bot code:

import logging

from telegram import Update

from telegram.ext import Updater, CommandHandler, CallbackContext

import secrets

import string

# Generate a random token

def generate_token():

alphabet = string.ascii_letters + string.digits

return ''.join(secrets.choice(alphabet) for _ in range(16))

# In-memory storage for tokens and chat IDs (use a database in production)

token_storage = {}

def start(update: Update, context: CallbackContext) -> None:

update.message.reply_text('Send /getip to get your IP address.')

def getip(update: Update, context: CallbackContext) -> None:

chat_id = update.message.chat_id

token = generate_token()

token_storage[token] = chat_id

link = f"http://your-server-address/getip?token={token}"

update.message.reply_text(f'Click here to get your IP: {link}')

def main() -> None:

# Replace 'YOUR_BOT_TOKEN' with your actual bot token

updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))

dispatcher.add_handler(CommandHandler("getip", getip))

updater.start_polling()

updater.idle()

if __name__ == '__main__':

main()

Flask server code:

from flask import Flask, request

import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'

@app.route('/getip')

def get_ip():

token = request.args.get('token')

if not token:

return 'Token missing', 400

# Retrieve chat_id from token_storage (in production, use a database)

chat_id = token_storage.get(token)

if not chat_id:

return 'Invalid token', 400

# Get the user's IP address

user_ip = request.remote_addr

# If behind a proxy, might need to use X-Forwarded-For

# user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

# Send the IP back via Telegram

send_message_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

data = {

'chat_id': chat_id,

'text': f'Your IP address is: {user_ip}'

}

response = requests.post(send_message_url, data=data)

# Cleanup the token (optional)

del token_storage[token]

return 'IP has been sent to your Telegram chat.', 200

if __name__ == '__main__':

app.run(host='0.0.0.0', port=5000)