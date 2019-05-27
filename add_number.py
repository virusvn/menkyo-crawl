import csv


def convert_to_tsv(from_csv, to_tsv):
    with open(to_tsv, "w") as tsvfile:
        writer = csv.writer(
            tsvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(["Question No.", "Image", "Front", "Back", "Vocabularies"])
        with open(from_csv, "r") as csvfile:
            lines = csv.DictReader(csvfile)
            for i, line in enumerate(lines, 1):
                if line["image"]:
                    writer.writerow(
                        [i, line["image"], line["question"], line["answer"], ""]
                    )
                else:
                    writer.writerow([i, "", line["question"], line["answer"], ""])


if __name__ == "__main__":
    convert_to_tsv("anki_data.csv", "anki_data_with_numbers.csv")

