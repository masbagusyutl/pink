import requests
import json
import time
from datetime import datetime, timedelta

# Fungsi untuk menghitung mundur dengan tampilan waktu yang bergerak
def countdown_timer(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    while datetime.now() < end_time:
        remaining = end_time - datetime.now()
        print(f"\rWaktu mundur: {str(remaining).split('.')[0]}", end="")
        time.sleep(1)
    print("\nWaktu selesai!")

# Fungsi untuk mengambil data dari file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [line.strip() for line in data]

# Fungsi untuk melakukan POST request
def post_request(url, headers, payload):
    response = requests.post(url, headers=headers, json=payload)
    return response

# URL dan headers untuk request
base_join_url = 'https://king-prawn-app-99fp2.ondigitalocean.app/join/'
daily_reward_url = 'https://king-prawn-app-99fp2.ondigitalocean.app/users/daily-reward'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Origin': 'https://pinky-bot.netlify.app',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

# Path ke file data
data_file_path = 'data.txt'

while True:
    # Membaca data akun dari file
    accounts = read_data(data_file_path)
    total_accounts = len(accounts)
    
    print(f"Jumlah akun: {total_accounts}")
    
    for idx, chat_id in enumerate(accounts):
        print(f"\nMemproses akun {idx + 1}/{total_accounts} (Chat ID: {chat_id})")

        # Membuat URL dinamis untuk request join
        join_url = f"{base_join_url}{chat_id}"

        # Melakukan request POST untuk mendaftar
        join_payload = {'chatId': chat_id}
        join_response = post_request(join_url, headers, join_payload)
        
        if join_response.status_code == 200:
            data = join_response.json()
            user_info = data.get('user', {})
            user_name = user_info.get('userName', 'Tidak tersedia')
            pinky = user_info.get('Pinky', 'Tidak tersedia')
            daily_reward_count = user_info.get('dailyRewardCount', 'Tidak tersedia')

            print(f"Username: {user_name}")
            print(f"Pinky: {pinky}")
            print(f"Hadiah Harian: {daily_reward_count}")

            # Melakukan request POST untuk klaim hadiah harian
            daily_reward_payload = {'chatId': chat_id}
            daily_reward_response = post_request(daily_reward_url, headers, daily_reward_payload)
            
            if daily_reward_response.status_code != 200:
                error_message = daily_reward_response.json().get('message', 'Tidak ada pesan error')
                print(f"{error_message}")
        else:
            print(f"Error saat mendaftar: {join_response.json().get('message', 'Tidak ada pesan error')}")
        
        # Menunggu 5 detik sebelum memproses akun berikutnya
        time.sleep(5)
    
    # Hitung mundur 1 hari
    print("\nMemulai hitung mundur 1 hari...")
    countdown_timer(86400)  # 86400 detik = 1 hari
