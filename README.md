# Menkyo crawl

## Crawl quizzes from Menkyo for Japan Driver's License Test

Crawl data from https://menkyo-web.com and store quizzes into csv

## Usage

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
python download_image.py

```


## Flow

- Get data from menkyo
- Download images
- Add furigana to Question/Answer
- Fix some sentences don't have furigana