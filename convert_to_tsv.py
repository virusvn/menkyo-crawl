import csv

def convert_to_tsv(from_csv, to_tsv):
    with open(to_tsv, 'w') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Front", "Back", "Image"])
        with open(from_csv, 'r') as csvfile:
            lines = csv.DictReader(csvfile)
            for line in lines:
                if line["image"]:
                    writer.writerow([f"{line['question']}", f"{line['answer']}", line["image"]])
                else:
                    writer.writerow([f"{line['question']}", f"{line['answer']}"])

if __name__ == "__main__":
    convert_to_tsv('rets.csv', 'rets.tsv')