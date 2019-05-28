import csv
from typing import List
from morph import Morph

"""
Follow this gist to install Mecab and mecab-ipadic-neologd
https://gist.github.com/knknkn1162/c81bcd15e0e4f20304559f25a58c38fc
"""
dict_path = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
mp = Morph(dict_path)


def get_vocabularies(sentence: str) -> set:
    mp.set_sentence(sentence)
    vocabularies = set()
    for word in mp.extract():
        vocabulary, term = word
        # get noun only
        if term == "名詞":
            vocabularies.add(vocabulary)

    return vocabularies


with open("anki_data_with_ruby_final_vocabularies.csv", "w") as tsvfile:
    writer = csv.writer(
        tsvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    writer.writerow(
        [
            "Question No.",
            "Image",
            "Front",
            "Back",
            "Vocabularies",
            "RawFront",
            "RawBack",
        ]
    )

    with open("anki_data_with_ruby_final.csv", "r") as ruby_csvfile:
        ruby_lines = csv.DictReader(ruby_csvfile)
        with open("anki_data.csv", "r") as csvfile:
            lines = csv.DictReader(csvfile)
            for idx, ruby_line in enumerate(ruby_lines):
                # print(idx)
                table_html = ""
                line = {}
                for l in lines:
                    print(l["Question No."] + "==" + ruby_line["Question No."])
                    if l["Question No."] == ruby_line["Question No."]:
                        print(idx)
                        line = l
                        sentence = line["Front"] + "。" + line["Back"]
                        vocabularies = get_vocabularies(sentence)
                        if len(vocabularies):
                            table_html = "<table>"
                            for vocab in vocabularies:
                                table_html += (
                                    f"<tr><td>{vocab}</td><td>{vocab}</td></tr>"
                                )
                            table_html += "</table>"
                        break

                if bool(line):
                    ruby_line["Vocabularies"] = table_html
                    writer.writerow(
                        [
                            ruby_line["Question No."],
                            ruby_line["Image"],
                            ruby_line["Front"],
                            ruby_line["Back"],
                            ruby_line["Vocabularies"],
                            line["Front"],
                            line["Back"],
                        ]
                    )
                # else:
                #     print(ruby_line["Question No."])
