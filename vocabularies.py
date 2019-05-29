import csv
import requests
from typing import List
from morph import Morph
import pysnooper

"""
Follow this gist to install Mecab and mecab-ipadic-neologd
https://gist.github.com/knknkn1162/c81bcd15e0e4f20304559f25a58c38fc
"""
dict_path = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
mp = Morph(dict_path)

all_vocabularies = {}


def get_vocabularies(sentence: str) -> set:
    mp.set_sentence(sentence)
    vocabularies = set()
    for word in mp.extract():
        vocabulary, term = word
        # get noun only
        if term == "名詞":
            vocabularies.add(vocabulary)

    return vocabularies


def get_translation_dict():
    translations = {}
    with open("all_vocabularies_with_translation.csv", "r") as csvread:
        lines = csv.DictReader(csvread)
        for line in lines:
            translations[line["word"]] = line["translated"]

    return translations


def get_translation(word, translations: dict):
    return translations.get(word, word)


def translate_all_vocabularies():
    with open("all_vocabularies_with_translation.csv", "w") as csvwrite:
        writer = csv.writer(
            csvwrite, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(["word", "translated"])
        with open("all_vocabularies.csv", "r") as csvread:
            lines = csv.DictReader(csvread)
            for idx, line in enumerate(lines):
                if idx < 193:
                    continue
                print("Processing " + line["word"])
                translated_word = get_translation_by_mazii(line["word"])
                writer.writerow([line["word"], translated_word])


def get_translation_by_mazii(word):
    url = "https://mazii.net/api/search"
    response = requests.post(url, {"dict": "javi", "query": word, "type": "word"})
    datas = response.json()
    if len(datas) and datas["status"] == 200:
        for data in datas["data"]:
            if data["means"] and len(data["means"]):
                """ only return first mean """
                return data["means"][0]["mean"]
    return word


if __name__ == "__main__":
    translations = get_translation_dict()
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
                "RawVocabularies",
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
                    vocabularies = []
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
                                    vocab_translated = get_translation(
                                        vocab, translations
                                    )
                                    if not all_vocabularies.get(vocab):
                                        all_vocabularies[vocab] = vocab_translated
                                    table_html += f"<tr class='row'><td class='word'>{vocab}</td><td class='translate'>{vocab_translated}</td></tr>"
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
                                "|".join(vocabularies),
                            ]
                        )

