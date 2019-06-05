import csv
import re

with open("unten3.tsv", "w") as tsvfile:
    writer = csv.writer(
        tsvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    words = set()
    with open("unten1.tsv", "r") as ruby_csvfile:
        ruby_lines = csv.DictReader(ruby_csvfile, delimiter="\t")
        for line in ruby_lines:

            word = line["front"]
            if "<ruby>" == line["front"][:6]:
                m = re.match("<ruby>([一-龯ぁ-んァ-ン]+)<rt>", line["front"])
                if m and m.group(0):
                    word = m.group(0)[6:-4]
                    print(word)
            if word not in words:
                writer.writerow([line["front"], line["back"]])
                words.add(word)

