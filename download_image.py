import urllib.request
import csv
from pathlib import Path

image_path = Path('./images')
with open('rets.csv', 'r') as csvfile:
    lines = csv.DictReader(csvfile)
    for line in lines:
        image_uri = line["image"]
        if image_uri:
            if image_uri[0:3] == "../":
                image_uri = image_uri[3:]
            
            print(image_uri)
            try: 
                urllib.request.urlretrieve(f'https://menkyo-web.com/{image_uri}', image_path / image_uri)
            except urllib.error.HTTPError:
                print("not found")