import requests
import os

URL = "https://physionet.org/files/eegmmidb/1.0.0/S001/S001R01.edf"

os.makedirs("real-data/eeg", exist_ok=True)

r = requests.get(URL, timeout=60)

if r.status_code == 200:
    with open("real-data/eeg/sample.edf","wb") as f:
        f.write(r.content)
    print("EEG dataset downloaded")
else:
    print("Failed to fetch EEG")
