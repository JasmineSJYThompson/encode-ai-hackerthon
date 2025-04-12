from web3 import Web3
from datetime import datetime

def get_onchain_data():
    infura_url = "https://holesky.infura.io/v3/fa60ca80e1154976a3070761e2128057"
    web3 = Web3(Web3.HTTPProvider(infura_url))

    if web3.is_connected():
        latest_block = web3.eth.block_number
        block = web3.eth.get_block(latest_block)
        transaction_count = len(block['transactions'])
        block_timestamp = datetime.fromtimestamp(block['timestamp'])
        gas_used = block.get('gasUsed', None)
        gas_limit = block.get('gasLimit', None)
        difficulty = block.get('difficulty', None)
        
        return {
            'block_number': latest_block,
            'timestamp': block_timestamp,
            'transaction_count': transaction_count,
            'gasUsed': gas_used,
            'gasLimit': gas_limit,
            'difficulty': difficulty
        }
    else:
        raise Exception("Connection to Ethereum network failed!")
