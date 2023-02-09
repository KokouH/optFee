import aiohttp

from models import Chain


async def get_token_prices(token_ids):
    async with aiohttp.ClientSession() as session:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&ids='
        url += "%2C".join(token_ids[symbol]['id'] for symbol in token_ids)

        async with session.get(url) as resp:
            try:
                json_data = await resp.json()
                for token in json_data:
                    token_ids[token['symbol']]['price'] = token['current_price']
            except:
                print(await resp.text())
                print('Coingecko not give token prices')
    return token_ids


def set_token_prices(accounts, token_prices):
    symbols = [sy for sy in token_prices]
    for ind, acc in enumerate(accounts):
        for chain_name in acc.token_balance:
            for token_name in acc.token_balance[chain_name]:
                if 'symbol' not in acc.token_balance[chain_name][token_name]:
                    continue
                acc_symbol = acc.token_balance[chain_name][token_name]['symbol'].lower()
                if acc_symbol in symbols:
                    accounts[ind].token_balance[chain_name][token_name]['in_usd'] = acc.token_balance[chain_name][token_name]['count'] * next(token_prices[g] for g in token_prices if g == acc_symbol)['price']

    ETH_FEE = [
        Chain.ChainName.ARBITRUM,
        Chain.ChainName.OPTIMISM,
        Chain.ChainName.ETHEREUM,
        Chain.ChainName.ZKSYNC]

    FTM_FEE = [Chain.ChainName.FANTOM]

    MATIC_FEE = [Chain.ChainName.POLYGON]

    ETH_price = next(token_prices[g] for g in token_prices if g == 'eth')['price']
    FTM_price = next(token_prices[g] for g in token_prices if g == 'ftm')['price']
    MATIC_price = next(token_prices[g] for g in token_prices if g == 'matic')['price']
    for ind, acc in enumerate(accounts):
        for chain_name in acc.fee_pay:
            if chain_name in ETH_FEE:
                accounts[ind].fee_pay[chain_name]['in_usd'] = acc.fee_pay[chain_name]['count'] * ETH_price
            if chain_name in FTM_FEE:
                accounts[ind].fee_pay[chain_name]['in_usd'] = acc.fee_pay[chain_name]['count'] * FTM_price
            if chain_name in MATIC_FEE:
                accounts[ind].fee_pay[chain_name]['in_usd'] = acc.fee_pay[chain_name]['count'] * MATIC_price

    return accounts

async def get_nft_prices(contracts):
    ret_contracts = {}
    async with aiohttp.ClientSession() as session:
        for con in contracts:
            try:
                url = "https://api.coingecko.com/api/v3/nfts/" + contracts[con]['id']
                async with session.get(url) as resp:
                    json_data = await resp.json()
                    ret_contracts[con] = json_data['floor_price']['usd']
            except:
                print(f"Did not receive a response by {con}")

    return ret_contracts

def set_nft_prices(accounts, nft_prices):
    for ind, acc in enumerate(accounts):
        for chain_name in acc.nfts:
            for nft_name in acc.nfts[chain_name]:
                if 'contractAddress' not in acc.nfts[chain_name][nft_name]:
                    continue
                if acc.nfts[chain_name][nft_name]['contractAddress'] in nft_prices:
                    accounts[ind].nfts[chain_name][nft_name]['in_usd'] = acc.nfts[chain_name][nft_name]['count'] * nft_prices[acc.nfts[chain_name][nft_name]['contractAddress']]

    return accounts