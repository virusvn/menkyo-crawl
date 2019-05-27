# -*- coding: utf-8 -*-
import requests
import csv

merge_str = "---===---"
start = 0  # start Question No., in case need to restart
with open("anki_final.csv", "w") as tsvfile:
    writer = csv.writer(
        tsvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    # writer.writerow(["Question No.", "Image", "Front", "Back", "Vocabularies"])

    with open("anki_data_with_ruby.csv", "r") as csvfile:
        lines = csv.DictReader(csvfile)
        for line in lines:
            # Because this api will block us after some requests, we need to check it later
            if int(line["Question No."]) < start:
                continue
            if "ruby" not in line["Front"]:
                url = "https://api.kuroshiro.org/convert"
                print("Processing " + line["Question No."])
                response = requests.post(
                    url,
                    {
                        "mode": "furigana",
                        "romajiSystem": "nippon",
                        "to": "hiragana",
                        "str": line["Front"] + merge_str + line["Back"],
                    },
                )
                data = response.json()
                if data["result"]:
                    line["Front"], line["Back"] = data["result"].split(merge_str)
            writer.writerow(
                [
                    line["Question No."],
                    line["Image"],
                    line["Front"],
                    line["Back"],
                    line["Vocabularies"],
                ]
            )

