import pandas as pd
import requests
import time
import os

def get_polygonscan_api_key(api_file_path):
    try:
        with open(api_file_path, 'r') as file:
            for line in file:
                if line.startswith("Polygonscan api="):
                    return line.split("=")[1].strip()
    except FileNotFoundError:
        print("API key file not found.")
    except Exception as e:
        print(f"Error reading API key file: {e}")
    return None

def update_wallets(file_path, api_key):
    if not os.path.exists(file_path):
        print("Data file not found. Make sure data.xlsx is in the root folder.")
        return

    data = pd.read_excel(file_path, engine='openpyxl', header=0)

    if data.shape[1] < 6:
        print("Data file does not have enough columns. Ensure columns E and F are present.")
        return

    for i in range(len(data)):
        wallet = data.iloc[i, 4]

        if pd.isna(wallet):
            continue

        print(f"Processing wallet #{i + 1}: {wallet}")

        # Get volume from Polymarket
        url = f"https://lb-api.polymarket.com/rank?window=all&rankType=vol&address={wallet}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.json()

            if content:
                volume = int(content[0].get("amount", 0))
            else:
                volume = 0

            data.iloc[i, 5] = volume
            print(f"Wallet #{i + 1} processed. Volume: {volume}")

        except requests.exceptions.RequestException as e:
            print(f"Error getting data for {wallet}: {e}")
            data.iloc[i, 5] = "Error"

        time.sleep(0.5)  # Pause between requests

        # Get USDC balance from Polygonscan
        polyscan_url = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress=0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174&address={wallet}&tag=latest&apikey={api_key}"
        try:
            response = requests.get(polyscan_url)
            response.raise_for_status()
            polyscan_data = response.json()

            if polyscan_data["status"] == "1":
                usdc_balance = int(polyscan_data["result"]) / 1e6  # USDC has 6 decimals
                data.iloc[i, 6] = round(usdc_balance, 2)
                print(f"Wallet #{i + 1} processed. USDC Balance: {usdc_balance:.2f}")
            else:
                data.iloc[i, 6] = "NOTOK"
                print(f"Wallet #{i + 1}: Error getting balance. Status: {polyscan_data['status']}")

        except requests.exceptions.RequestException as e:
            print(f"Error getting Polygonscan data for {wallet}: {e}")
            data.iloc[i, 6] = "Error"

        time.sleep(0.5)  # Pause between requests

    data.to_excel(file_path, index=False)



data_file = 'data.xlsx'
api_key_file = 'polygonscanapi.txt'

api_key = get_polygonscan_api_key(api_key_file)

if api_key:
    update_wallets(data_file, api_key)




