from models import Chain

import json

def zk_feepay_gen(trans, addr):
    zk_fees = {} # {tokenId: {'wei': 1234, 'count': 1.234, 'in_usd': 0.3, 'symbol': 'HUI'}}
    for tx in trans:
        if 'from' not in tx['op'] and 'submitterAddress' not in tx['op'] and tx['op']['type'] != 'ChangePubKey':
            continue
        if tx['op']['type'] != 'ChangePubKey' and tx['op']['type'] != 'Swap':
            if tx['op']['from'] != addr:
                continue
        if 'feeToken' in tx['op']:
            tokId = tx['op']['feeToken']
        else:
            tokId = 0
        if tokId not in zk_fees:
            zk_fees[tokId] = {'wei': 0}
        if 'fee' in tx['op']:
            zk_fees[tokId]['wei'] += int(tx['op']['fee'])
    return zk_fees


async def tokens_from_transactions(transactions, addr):
    tokens = {}
    symbol = transactions[0]['tokenName']
    c_addr = transactions[0]['contractAddress']
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api-optimistic.etherscan.io/api?module=account&action=tokenbalance&contractaddress={c_addr}&address={addr}&tag=latest&apikey=9XWTPRB4RA3GZWPCJ1FGYMQYHSMC8IBDKB') as resp:
            json_data = await resp.json()
            if json_data['message'] == 'OK':
                tokens[symbol] = {'wei': int(json_data['result']), 'count': int(json_data['result']) / 10**18}
    # tokens[symbol] = {'wei': int(
    #     transactions[0]['value']), "symbol": transactions[0]['tokenSymbol']}
    # for tx in transactions[1:]:
    #     if tx['from'] == addr:
    #         tokens[symbol]['wei'] -= int(tx['value'])
    #     else:
    #         tokens[symbol]['wei'] += int(tx['value'])
    # tokens[symbol]['count'] = tokens[symbol]['wei'] / \
    #     10**int(transactions[0]['tokenDecimal'])
    return tokens


async def nfts_from_transactions(transactions, addr):
    nft = {}
    name_ = transactions[0]['tokenName']
    nft[name_] = {'contractAddress': transactions[0]['contractAddress']}
    c = []
    for tx in transactions:
        if tx['tokenID'] in c and tx['from'] == addr:
            del(c[c.index(tx['tokenID'])])
        else:
            c.append(tx['tokenID'])
    nft[name_]['count'] = len(c)
    return nft


def get_ERCcontracts(transactions):
    ERCcontracts = {}
    for chain in transactions:
        if chain == Chain.ChainName.ZKSYNC:
            continue
        for addr in transactions[chain]:
            for tx in transactions[chain][addr]:
                if tx['functionName'] != "":
                    addressContract = tx['to']
                    if chain not in ERCcontracts:
                        ERCcontracts[chain] = {}
                    if addr in ERCcontracts[chain]:
                        if not tx['to']:
                            continue
                        ERCcontracts[chain][addr].append(tx['to'])
                    else:
                        ERCcontracts[chain][addr] = [tx['to']]
            ERCcontracts[chain][addr] = list(set(ERCcontracts[chain][addr]))
    return ERCcontracts
