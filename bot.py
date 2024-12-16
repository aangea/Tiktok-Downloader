import os
import requests
from bs4 import BeautifulSoup

def save_username_to_txt(username, file_path="usernames.txt"):
    try:
        # Cek apakah file sudah ada, jika tidak buat file baru
        with open(file_path, "a") as file:
            file.write(username + "\n")
        print(f"Username '{username}' berhasil disimpan ke {file_path}.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan username: {e}")

def download_tiktok_video_no_watermark(url, save_path="downloads"):
    try:
        # Cek apakah folder tujuan sudah ada, jika tidak buat folder
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Header agar terlihat seperti browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

        # Gunakan layanan pihak ketiga untuk mendapatkan URL video tanpa watermark
        api_url = "https://snaptik.app/action.php"
        payload = {"url": url}
        response = requests.post(api_url, data=payload, headers=headers)
        response.raise_for_status()

        # Parse hasil HTML untuk mendapatkan URL unduhan
        soup = BeautifulSoup(response.text, "html.parser")
        download_link = soup.find("a", class_="download-link")
        if not download_link:
            print("Gagal menemukan tautan unduhan tanpa watermark.")
            return

        video_url = download_link["href"]

        # Unduh video
        video_data = requests.get(video_url, headers=headers)
        video_data.raise_for_status()

        # Tentukan nama file
        video_name = video_url.split("/")[-1].split("?")[0]
        video_path = os.path.join(save_path, video_name)

        # Simpan video ke file lokal
        with open(video_path, "wb") as video_file:
            video_file.write(video_data.content)

        print(f"Video tanpa watermark berhasil diunduh: {video_path}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def download_all_videos_from_user(username, save_path="downloads"):
    try:
        # Simpan username ke file txt
        save_username_to_txt(username)

        # Cek apakah folder tujuan sudah ada, jika tidak buat folder
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Header agar terlihat seperti browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

        # URL profil TikTok
        profile_url = f"https://www.tiktok.com/@{username}"

        # Kirim request ke halaman profil TikTok
        response = requests.get(profile_url, headers=headers)
        response.raise_for_status()

        # Parse konten HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Temukan semua tautan video di halaman profil
        video_links = soup.find_all("a", href=True)
        video_urls = [link["href"] for link in video_links if "/video/" in link["href"]]

        if not video_urls:
            print("Tidak ada video yang ditemukan di profil pengguna ini.")
            return

        print(f"Ditemukan {len(video_urls)} video. Mengunduh...")

        # Unduh setiap video
        for video_url in video_urls:
            print(f"Mengunduh: {video_url}")
            download_tiktok_video_no_watermark(video_url, save_path)

        print("Semua video berhasil diunduh.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    print("=== TikTok Video Downloader Tanpa Watermark ===")
    mode = input("Pilih mode (1: Unduh satu video, 2: Unduh semua video dari username): ")
    if mode == "1":
        tiktok_url = input("Masukkan URL video TikTok: ")
        download_tiktok_video_no_watermark(tiktok_url)
    elif mode == "2":
        username = input("Masukkan username TikTok: ")
        download_all_videos_from_user(username)
    else:
        print("Mode tidak valid.")
