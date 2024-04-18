#!/usr/bin/env python3
import requests, time, os, sys
from colorthon import Colors
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL
from typing import Optional
from hdwallet.utils import generate_mnemonic
import json


def titler(text_title: str):
    sys.stdout.write(f"\x1b]2;{text_title}\x07")
    sys.stdout.flush()
    
def clearNow(): os.system("cls") if 'win' in sys.platform.lower() else os.system("clear")

#bitcoin rate
def btc_rate(btc: float) -> int:
    url = "https://bitcoin.atomicwallet.io/api/v2/tickers/?currency=usd"
    req = requests.get(url)
    res = req.json()
    if req.status_code == 200:
        return int(btc * res.get("rates").get("usd"))
    else:
        return 0
        
# Check the balance of the address
def check_BTC_balance(address: str, retries=1000, delay=5) -> str:
    for attempt in range(retries):
        try:
            response = requests.get(f"https://blockchain.info/balance?active={address}")
            data = response.json()
            balance = data[address]["final_balance"] 
            return str(balance)
        except Exception as e:
            if attempt < retries - 1:
                print(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                time.sleep(delay)
            else:
                print("Error checking balance: {str(e)}")
                return "0" 

#Clear Screen
clearNow()

# // Colors //
blue = Colors.BLUE
magenta = Colors.MAGENTA
red = Colors.RED
green = Colors.GREEN
cyan = Colors.CYAN
yellow = Colors.YELLOW
reset = Colors.RESET
z = 0
ff = 0
found = 0
usd = 0  
while True:
    # // Counter Total Generated and Converted Mnemonic //
    z += 1
    # // Counter detail to title //
    titler(f"Gen: {z} / Con: {ff} / USD: {usd} $ --BTC-blockchain.info")
    # Choose strength 128, 160, 192, 224 or 256
    STRENGTH: int = 128  # Default is 128
    # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
    LANGUAGE: str = "english"  # Default is english
    # Generate new entropy hex string
    ENTROPY: str = generate_entropy(strength=STRENGTH)
    # Secret passphrase for mnemonic
    PASSPHRASE: Optional[str] = None  # "meherett"
    mnemonic: str = generate_mnemonic(language="english", strength=128)

    # Initialize Bitcoin mainnet HDWallet
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
    # Get Bitcoin HDWallet from entropy
    hdwallet.from_mnemonic(
        mnemonic=mnemonic, language="english"
    )

    hdwallet.from_index(84, hardened=True)
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0)
    hdwallet.from_index(0)
    #Generate btc address
    btc_addr=hdwallet.p2wpkh_address()
    #Check the balance of address with api
    btc_bal = check_BTC_balance(btc_addr)
    #Convert satoshi value to btc
    btc_balance = int(btc_bal) / 100000000
    if btc_balance > 0:
                    ff += 1
                    found += btc_balance
                    # // Append Rate Data in Title Terminal for Total USD Found
                    usd += btc_rate(btc_balance)
                    titler(f"Gen: {z} / Con: {ff} / USD: {usd} $")
                    with open("foundBTC.txt", "a") as dr:
                        dr.write(f"BITCOIN: {btc_addr} | Balance: {btc_balance}\n"
                                 f"Mnemonic: {mnemonic}\n"
                                 f"Private Key: {hdwallet.private_key()}\n")
                                        # // Space Mode for Output Logs
                    s = " "
                    sp = s * 16
                    btc_space = sp + s * (62 - len(btc_addr))
                    # // Print Output Logs with Pretty Type Format
                    print(f"{'=' * 33}{green} BTC Wallet Found {reset} {'=' * 33}\n")     
                    print(f"[{z} | Found:{ff}] BTC1: {yellow}{btc_addr}{reset}{btc_space}[Balance: {red}{btc_balance}{reset}]")
                    print(f"[{z} | Found:{ff}]  Mne: {red}{mnemonic}{reset}")
                    print(f"[{z} | Found:{ff}]  Hex: {green}{hdwallet.private_key()}{reset}")
                    print(f"{'=' * 33}{green} BTC Wallet Found {reset} {'=' * 33}\n")                       
    else:
                    # // Space Mode for Output Logs
                    s = " "
                    sp = s * 16
                    btc_space = sp + s * (62 - len(btc_addr))
                    # // Print Output Logs with Pretty Type Format
                    print(f"[{z} | Found:{ff}] BTC1: {yellow}{btc_addr}{reset}{btc_space}[Balance: {red}{btc_balance}{reset}]")
                    print(f"[{z} | Found:{ff}]  Mne: {red}{mnemonic}{reset}")
                    print(f"[{z} | Found:{ff}]  Hex: {green}{hdwallet.private_key()}{reset}")
                    print(f"{'=' * 33}{yellow} BTC Wallet Finder {reset} {'=' * 33}\n")             
