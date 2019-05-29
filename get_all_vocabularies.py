import csv
from vocabularies import get_vocabularies


def get_all_vocabularies(input: str) -> set:
    all_vocabularies = set()
    with open(input, "r") as csvfile:
        lines = csv.DictReader(csvfile)
        vocabularies = []
        for line in lines:
            sentence = line["Front"] + "。" + line["Back"]
            vocabularies = get_vocabularies(sentence)
            if len(vocabularies):
                for vocab in vocabularies:
                    all_vocabularies.add(vocab)

    return all_vocabularies


def write_vocabularies(output: str, vocabularies: set):
    with open(output, "w") as tsvfile:
        writer = csv.writer(
            tsvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        for vocab in vocabularies:
            writer.writerow([vocab])


if __name__ == "__main__":
    all_vocabularies = get_all_vocabularies("anki_data.csv")
    write_vocabularies("all_vocabularies.csv", all_vocabularies)

