
# "arbitrum":"WTW5JN9WGGI5KDYUWCV5BE8QQQ4SCYYX3V",
# "nova":"4Q9KHP96U7ZNQM7M9YAPXP3UBF8TNJI48N",
# "ethereum":"Q6R2Y85CNJ3HTFGD6CJZ6XC4UTXGM9W82H",
# "polygon":"P1H2JGE3S6PGZWK62G88K9MHKU73FBMNYB",
# "fantom":"356SS5HXNNT3EA391KN1IJWPT3UFS7ZDT9",
# "optimism":"9XWTPRB4RA3GZWPCJ1FGYMQYHSMC8IBDKB"

# ARBITRUM_NOVE disable API

class APIkeys():
    ARBITRUM = 'WTW5JN9WGGI5KDYUWCV5BE8QQQ4SCYYX3V'
    ETHEREUM = 'Q6R2Y85CNJ3HTFGD6CJZ6XC4UTXGM9W82H'
    POLYGON = 'P1H2JGE3S6PGZWK62G88K9MHKU73FBMNYB'
    FANTOM = '356SS5HXNNT3EA391KN1IJWPT3UFS7ZDT9'
    OPTIMISM = '9XWTPRB4RA3GZWPCJ1FGYMQYHSMC8IBDKB'


class ChainName():
    # ARBITRUM_NOVA = "arb_nova"
    ARBITRUM = "arb"
    ETHEREUM = "eth"
    POLYGON = "matic"
    FANTOM = "ftm"
    OPTIMISM = "opt"
    ZKSYNC = 'zk'


class ChainAPI():
    # ARBITRUM_NOVA = 'https://nova-explorer.arbitrum.io/api?'
    ARBITRUM = 'https://api.arbiscan.io/api?'
    ETHEREUM = 'https://api.etherscan.io/api?'
    POLYGON = 'https://api.polygonscan.com/api?'
    FANTOM = 'https://api.ftmscan.com/api?'
    OPTIMISM = 'https://api-optimistic.etherscan.io/api?'
    ZKSYNC = 'https://api.zksync.io/api/v0.2/'


class TransactionByAccount():
    # ARBITRUM_NOVA = ChainAPI.ARBITRUM_NOVA + 'module=account&action=txlist&address='
    BASE_SCAN = 'module=account&action=txlist&startblock=0&endblock=99999999' \
        '&page=1&offset=10000&sort=desc&apikey='
    ARBITRUM = ChainAPI.ARBITRUM + BASE_SCAN + APIkeys.ARBITRUM + '&address='
    ETHEREUM = ChainAPI.ETHEREUM + BASE_SCAN + APIkeys.ETHEREUM + '&address='
    POLYGON = ChainAPI.POLYGON + BASE_SCAN + APIkeys.POLYGON + '&address='
    FANTOM = ChainAPI.FANTOM + BASE_SCAN + APIkeys.FANTOM + '&address='
    OPTIMISM = ChainAPI.OPTIMISM + BASE_SCAN + APIkeys.OPTIMISM + '&address='
    ZKSYNC = ChainAPI.ZKSYNC + 'accounts/{}/transactions?from={}&limit=100&direction=older'

class TokensByAccount():
    ZKSYNC = ChainAPI.ZKSYNC + 'accounts/{}/committed'

class TokenPrices():
    ETH = ChainAPI.ETHEREUM + 'module=stats&action=ethprice&apikey=' + APIkeys.ETHEREUM
    MATIC = ChainAPI.POLYGON + 'module=stats&action=maticprice&apikey=' + APIkeys.POLYGON
    FTM = ChainAPI.FANTOM + 'module=stats&action=ftmprice&apikey=' + APIkeys.FANTOM
    ZK = ChainAPI.ZKSYNC + 'tokens/{}/priceIn/usd'

class TokensTransByAddrContract():
    BASE_STR = 'module=account&action=tokentx&contractaddress={}&address={}&page=1&offset=10000&startblock=0&endblock=99999999&sort=desc&apikey='
    ARBITRUM = ChainAPI.ARBITRUM + BASE_STR + APIkeys.ARBITRUM
    ETHEREUM = ChainAPI.ETHEREUM + BASE_STR + APIkeys.ETHEREUM
    POLYGON = ChainAPI.POLYGON + BASE_STR + APIkeys.POLYGON
    FANTOM = ChainAPI.FANTOM + BASE_STR + APIkeys.FANTOM
    OPTIMISM = ChainAPI.OPTIMISM + BASE_STR + APIkeys.OPTIMISM


    def get_by_chain_name(self, chain_name):
        match (chain_name):
            case 'arb':
                return self.ARBITRUM
            case 'eth':
                return self.ETHEREUM
            case 'matic':
                return self.POLYGON
            case 'ftm':
                return self.FANTOM
            case 'opt':
                return self.OPTIMISM

class NFTsTransByAddrContract():
    BASE_STR = 'module=account&action=tokennfttx&contractaddress={}&address={}&page=1&offset=10000&startblock=0&endblock=99999999&sort=desc&apikey='
    ARBITRUM = ChainAPI.ARBITRUM + BASE_STR + APIkeys.ARBITRUM
    ETHEREUM = ChainAPI.ETHEREUM + BASE_STR + APIkeys.ETHEREUM
    POLYGON = ChainAPI.POLYGON + BASE_STR + APIkeys.POLYGON
    FANTOM = ChainAPI.FANTOM + BASE_STR + APIkeys.FANTOM
    OPTIMISM = ChainAPI.OPTIMISM + BASE_STR + APIkeys.OPTIMISM


    def get_by_chain_name(self, chain_name):
        match (chain_name):
            case 'arb':
                return self.ARBITRUM
            case 'eth':
                return self.ETHEREUM
            case 'matic':
                return self.POLYGON
            case 'ftm':
                return self.FANTOM
            case 'opt':
                return self.OPTIMISM


