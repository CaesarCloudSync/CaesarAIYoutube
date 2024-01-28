import requests
import re
import json
url ="http://127.0.0.1:8080/getaudio?url=https://www.youtube.com/watch?v=RfOGrMfcMPg"


def download_file(url):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        local_filename = r.headers["content-disposition"]
        local_filename = re.findall("filename=(.+)", local_filename)[0].replace('"',"",100)
        print(local_filename)
        r.raise_for_status()
        with open(local_filename, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename
download_file(url)
print("Done")