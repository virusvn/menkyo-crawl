import csv
import requests
import time
import codecs
import logging
import urllib
from bs4 import BeautifulSoup

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
f_handler = logging.FileHandler('menkyo.log')
s_handler = logging.StreamHandler()
f_handler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
s_handler.setFormatter(s_format)

# Add handlers to the logger
logger.addHandler(f_handler)
logger.addHandler(s_handler)

mogi_urls = [f"https://menkyo-web.com/mogi-mondai{mogi}.html" if mogi >= 10 else f"0{mogi}" for mogi in range(1, 226)] # type: List[str]
hyousiki_urls = [f"https://menkyo-web.com/hyousiki-mondai0{hyousiki}.html" for hyousiki in range(1,10)] # type: List[str]
hyousiki_urls += [f"https://menkyo-web.com/hyoshikimondai/mondai{hyousiki}.html" for hyousiki in range(10,61)] # type: List[str]

urls = mogi_urls + hyousiki_urls # type: List[str]

def process_page(url: str):
    logger.info(f"Processing {url}")
    response = requests.get(url)
    rets = []
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        quiz = soup.find_all('table', class_="quiz01")
        count = len(quiz)
        logger.info(f"Processing {count} quizzes")
        for mondai in quiz:
            ret = {
                "image": "",
                "question": "",
                "answer": ""
            }
            question = mondai.find('th',class_="left")
            if question:
                ret["question"] = question.get_text()

            image = question.find("img")
            if image:
                ret["image"] = image["src"]
            
            # print(dir(question))
            answer =  mondai.find('span', class_="font-futozi01")
            ret["answer"] = answer.get_text()
            rets.append(ret)
    
    return rets 


with open('rets.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for url in urls:
        rets = process_page(url)
        for ret in rets:
            writer.writerow([ret["image"], ret["question"], ret["answer"]])
