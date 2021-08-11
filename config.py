
# ###Ryan Paper 
# API_KEY = "PKTUMTZLUIUKQNTHSR28"
# SECRET_KEY = "pvm9s6yUhKm6fmeLLw395ZFozT5tbaORPzQ5UO2o"
# BASE_URL = 'https://paper-api.alpaca.markets'

###Ryan Live
API_KEY = "AKGKFD329QH4E4O990QQ"
SECRET_KEY = "taWgcul8EEyINhkz7KlsXpAUlqszMfTU5DZR4KBM"
BASE_URL = 'https://api.alpaca.markets'
BET_SIZE = 5000

def init_globals(sent_position_size):
    global current_price
    current_price = -1
    global position_size
    position_size = sent_position_size