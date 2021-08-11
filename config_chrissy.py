###Chrissy Paper
#API_KEY = "PKI5JB8WQKYDB8H28K6N"
#SECRET_KEY = "R1tPO76xPip65T3op1qlbeO5DXmiqIjazY433lPw"
#BASE_URL = 'https://paper-api.alpaca.markets'

###Chrissy 
API_KEY = "AKW5SMTNEV6428KGRZM4"
SECRET_KEY = "wg2qi1EerwU99HNNCu8QN3LuO1qoVSnyud9NQmqO"
BASE_URL = 'https://api.alpaca.markets'
BET_SIZE = 2400

def init_globals(sent_position_size):
    global current_price
    current_price = -1
    global position_size
    position_size = sent_position_size