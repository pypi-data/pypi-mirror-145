import csv
import pynterlinear


def convert(filename, example_ids=None, do_all=False, tabs=False):
    reader = csv.DictReader(open(filename))
    example_data = {}
    for row in reader:
        example_data[row["Example_ID"]] = row

    examples = []
    for ex in example_data.values():
        examples.append(
            {
                "id": ex["Example_ID"],
                "surf": ex["Sentence"],
                "obj": ex["Segmentation"],
                "gloss": ex["Gloss"],
                "trans": ex["Translation"],
            }
        )
    if do_all:
        examples_to_print = examples
    else:
        examples_to_print = []
        for example in examples:
            if example["id"] in example_ids:
                examples_to_print.append(example)
    pynterlinear.convert_to_word(examples_to_print, use_tables=not tabs)
