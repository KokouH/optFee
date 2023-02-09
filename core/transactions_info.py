from asyncio import sleep

import aiohttp
import datetime

from models import Chain


async def get_accounts_transactions(wallets):
    w_count = len(wallets) - 1
    transactions = {}  # {'CHAIN_NAME': {'ADDRESS': [tx1, tx2, ...]}, ...}
    async with aiohttp.ClientSession() as session:
        for w_ind, addr in enumerate(wallets):

            # ARBITRUM_NOVA disable API
            # try:
            # 	async with session.get(Chain.TransactionByAccount.ARBITRUM_NOVA + addr) as resp:
            # 		json_data = await resp.json()
            # 		if json_data['message'] == 'OK':
            # 			transactions[Chain.ChainName.ARBITRUM_NOVA] = json_data['result']
            # except Exception as e:
            # 	print(f"Error in get_accounts_transactions ARBITRUM_NOVA\n{e}")
            
            # OPTIMISM
            try:
                async with session.get(Chain.TransactionByAccount.OPTIMISM + addr) as resp:
                    json_data = await resp.json()
                    if json_data['message'] == 'OK':
                        if Chain.ChainName.OPTIMISM not in transactions:
                            transactions[Chain.ChainName.OPTIMISM] = {}
                        transactions[Chain.ChainName.OPTIMISM][addr] = json_data['result']
            except Exception as e:
                print(f"Error in get_accounts_transactions OPTIMISM\n{e}")
    return transactions
