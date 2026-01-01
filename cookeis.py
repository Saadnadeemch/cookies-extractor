import sqlite3
import json
import os
import time
import shutil
from datetime import datetime

SQLITE_PATH = "/home/saad/snap/firefox/common/.mozilla/firefox/y3ivlnxk.default/cookies.sqlite"
TEMP_DB = "cookies_temp.sqlite"
COOKIES_TXT = "cookies.txt"

def extract_youtube_cookies(sqlite_path):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting YouTube cookie extraction...")

    if not os.path.exists(sqlite_path):
        print("cookies.sqlite not found.")
        return

    shutil.copy2(sqlite_path, TEMP_DB)

    conn = sqlite3.connect(TEMP_DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, value
        FROM moz_cookies
        WHERE host LIKE '%youtube.com%'
    """)

    cookies = cursor.fetchall()
    conn.close()

    if not cookies:
        print("No YouTube cookies found.")
        return

    cookie_string = '; '.join([f"{name}={value}" for name, value in cookies])

    with open("youtube_cookies.json", "w") as f:
        json.dump([{ "name": name, "value": value } for name, value in cookies], f, indent=2)

    with open(COOKIES_TXT, "w") as f:
        f.write(cookie_string)

    print(f"Saved {len(cookies)} cookies to cookies.txt and youtube_cookies.json")

if __name__ == "__main__":
    while True:
        extract_youtube_cookies(SQLITE_PATH)
        print("Sleeping for 1 hour...\n")
        time.sleep(3600)
