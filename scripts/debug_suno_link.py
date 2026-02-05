import requests
import re

url = "https://suno.com/s/CqxJuEqQPk0bi3KV"
try:
    resp = requests.get(url)
    print(f"Status: {resp.status_code}")
    print(f"Content Start: {resp.text[:500]}")
    
    # Try to find mp3 link
    match = re.search(r'(https://cdn[0-9]*\.suno\.ai/[^"]+\.mp3)', resp.text)
    if match:
        print(f"Found MP3: {match.group(1)}")
    else:
        print("No MP3 link found in HTML.")
        
except Exception as e:
    print(f"Error: {e}")
