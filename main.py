import json
import asyncio
import os

from telebot.async_telebot import AsyncTeleBot

from core import initialization, gecko, excel, tokens
from models import Chain
from utils.gecko import token_list_ids, nft_list_ids


bot = AsyncTeleBot('2053206737:AAHyNExom0kRgUhxE_QhYGl_Y0AKCdh8lG4')

with open('json/сoin_gecko.json', 'rb') as file:
    tokens_info_ = json.loads(file.read().decode('utf8'))

with open('json/nfts_gecko.json', 'rb') as file:
    nft_info_ = json.loads(file.read().decode('utf8'))

@bot.message_handler(commands=['start'])
async def handle_start(msg):
    await bot.send_message(chat_id=msg.chat.id, text=f"Hello\nIt's bot for check fees in Ethereum, Optimism, Arbitrum, Fantom, Polygon chains")

@bot.message_handler(commands=['help'])
async def handle_help(msg):
    await bot.send_message(chat_id=msg.chat.id, text=f"For check fees send wallets, one wallet per line(limit=50). Example:\n0xa1d85ed87fb34938ee6af2869722ebfe66d34c1d\n0x9f3be1a81c8d5f284ea1994ea3692b15552dd8ac")

@bot.message_handler()
async def main_handler(msg):
    wallets_bad = msg.json['text'].split('\n')
    wallets = []

    for ind, wallet in enumerate(wallets_bad):
        if len(wallet) == 42 and wallet[:2] == '0x':
            wallets.append(wallet.lower())

        wallets = wallets[:50]

    await bot.send_message(chat_id=msg.chat.id, text='Wallets processed:\n{}'.format("\n".join(wallets)))

    accounts, transactions = await initialization.accounts_init(wallets)
    accounts = await tokens.set_fee_prices(accounts)

    accounts = await initialization.accounts_tokens_nfts_init(accounts, transactions)

    tokens_ids = token_list_ids(accounts, tokens_info_) # {SYMBOL: "TOKEN_ID"}
    token_prices = await gecko.get_token_prices(tokens_ids)
    accounts = gecko.set_token_prices(accounts, token_prices)

    excel.create_tables_by_accounts(accounts, f"tables/{str(msg.chat.id)}")

    with open(f"tables/{str(msg.chat.id)}.xlsx", 'rb') as cur_table:
        await bot.send_document(msg.chat.id, cur_table)

    if os.path.exists(f"tables/{str(msg.chat.id)}.xlsx"):
        os.remove(f"tables/{str(msg.chat.id)}.xlsx")


asyncio.run(bot.infinity_polling())
