import aiohttp
import json

from asyncio import sleep

from models import Chain
from utils.tokens import tokens_from_transactions


async def set_accounts_tokens(accounts, ERCcontracts):
    ret_ERCcontracts = {}
    bad_ERCcontracts = {}
    async with aiohttp.ClientSession() as session:
        # Other chians

        chain_name = 'opt'
        try:
            for ind, acc in enumerate(accounts):
                if acc.wallet in ERCcontracts[chain_name]:
                    for addressContract in ERCcontracts[chain_name][acc.wallet]:
                        if not addressContract:
                            continue
                        async with session.get(f'https://api-optimistic.etherscan.io/api?module=account&action=tokenbalance&contractaddress={addressContract}&address={acc.wallet}&tag=latest&apikey=9XWTPRB4RA3GZWPCJ1FGYMQYHSMC8IBDKB') as resp:
                            try:
                                json_data = await resp.json()
                                print(json_data)
                                token = {}
                                if json_data['message'] == 'OK':
                                    token['Optimism'] = {'wei': int(json_data['result']), 'count': int(json_data['result']) / 10**18, 'symbol': 'OP'}
                                if chain_name not in acc.token_balance:
                                    accounts[ind].token_balance[chain_name] = {}
                                accounts[ind].token_balance[chain_name].update(
                                    token)
                            except Exception as e:
                                print(e)
                                if chain_name not in bad_ERCcontracts:
                                    bad_ERCcontracts[chain_name] = {}
                                if acc.wallet not in bad_ERCcontracts[chain_name]:
                                    bad_ERCcontracts[chain_name][acc.wallet] = [
                                    ]
                                bad_ERCcontracts[chain_name][acc.wallet].append(
                                    addressContract)
                                await sleep(5)

        except Exception as e:
            print(f"Error in last part set_accounts_tokens {chain_name}\n{e}")
    return (accounts, ret_ERCcontracts, bad_ERCcontracts)

async def set_fee_prices(accounts):
    async with aiohttp.ClientSession() as session:
        async with session.get(Chain.TokenPrices.ETH) as resp:
            json_data = await resp.json()
            ETH_price = float(json_data['result']['ethusd'])
        async with session.get(Chain.TokenPrices.MATIC) as resp:
            json_data = await resp.json()
            MATIC_price = float(json_data['result']['maticusd'])
        async with session.get(Chain.TokenPrices.FTM) as resp:
            json_data = await resp.json()
            FTM_price = float(json_data['result']['ethusd'])

        eth_chains = [
            Chain.ChainName.ETHEREUM,
            Chain.ChainName.ARBITRUM,
            Chain.ChainName.OPTIMISM]

        zk_tokens = []
        for ind, acc in enumerate(accounts):
            for fee_chain in acc.fee_pay:
                if fee_chain in eth_chains:
                    accounts[ind].fee_pay[fee_chain]['in_usd'] = ETH_price * acc.fee_pay[fee_chain]['count']
                if fee_chain == Chain.ChainName.FANTOM:
                    accounts[ind].fee_pay[fee_chain]['in_usd'] = FTM_price * acc.fee_pay[fee_chain]['count']
                if fee_chain == Chain.ChainName.POLYGON:
                    accounts[ind].fee_pay[fee_chain]['in_usd'] = MATIC_price * acc.fee_pay[fee_chain]['count']

                if fee_chain == Chain.ChainName.ZKSYNC:
                    zk_tokens.extend(list(acc.fee_pay[fee_chain].keys()))

        zk_tokens = list(set(zk_tokens))

        zk_tokens_prices = {}
        for zk_tok in zk_tokens:
            async with session.get(Chain.TokenPrices.ZK.format(zk_tok)) as resp:
                json_data = await resp.json()
                zk_tokens_prices[zk_tok] = {}
                zk_tokens_prices[zk_tok]['price'] = float(json_data['result']['price'])
                zk_tokens_prices[zk_tok]['decimals'] = json_data['result']['decimals']
                zk_tokens_prices[zk_tok]['symbol'] = json_data['result']['tokenSymbol']

        for ind, acc in enumerate(accounts):
            if Chain.ChainName.ZKSYNC in acc.fee_pay:
                for zk_tok_id in acc.fee_pay['zk']:
                    accounts[ind].fee_pay['zk'][zk_tok_id]['count'] = acc.fee_pay['zk'][zk_tok_id]['wei'] / 10**zk_tokens_prices[zk_tok_id]['decimals']
                    accounts[ind].fee_pay['zk'][zk_tok_id]['in_usd'] = acc.fee_pay['zk'][zk_tok_id]['count'] * zk_tokens_prices[zk_tok_id]['price']
                    accounts[ind].fee_pay['zk'][zk_tok_id]['symbol'] = zk_tokens_prices[zk_tok_id]['symbol']


    return accounts
