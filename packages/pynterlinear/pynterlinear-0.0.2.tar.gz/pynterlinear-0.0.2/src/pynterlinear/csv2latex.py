import csv
import datetime
from string import Template
import pyperclip
import pynterlinear


class DeltaTemplate(Template):
    delimiter = "%"


def get_time(time_str):
    fmt = "%H:%M:%S"
    tdelta = datetime.timedelta(seconds=int(time_str) / 1000)
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = "{:02d}".format(hours)
    d["M"] = "{:02d}".format(minutes)
    d["S"] = "{:02d}".format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


def get_example_hash(ex, from_corpus=True):
    if "Speaker" not in ex.keys():
        from_corpus = False
    if "Information" not in ex:
        info = ""
    else:
        info = ex["Information"]
    ex_hash = {
        "id": ex["Example_ID"],
        "obj": ex["Segmentation"],
        "gloss": ex["Gloss"],
        "trans": ex["Translation"],
        "surface": ex["Sentence"],
        "parnote": info,
    }
    if "Language_ID" in ex:
        ex_hash["language"] = ex["Language_ID"]
    if from_corpus:
        ex_hash["speaker"] = ex["Speaker"]
        ex_hash["text_id"] = ex["Text_ID"]
        ex_hash["part"] = ex["Part"]
        if ex["Time_Start"] != "":
            ex_hash["start"] = get_time(ex["Time_Start"])
            ex_hash["end"] = get_time(ex["Time_End"])

    else:
        if "Source" in ex:
            ex_hash["source"] = ex["Source"]
    return ex_hash


def convert(filename, example_ids, do_all=False, from_corpus=False):
    reader = csv.DictReader(open(filename))
    example_data = {}
    for row in reader:
        example_data[row["Example_ID"]] = row

    examples = []

    if do_all:
        for key, ex in example_data.items():
            examples.append(get_example_hash(ex))
        output = ""
        output = pynterlinear.convert_to_expex(
            examples, from_corpus=from_corpus, for_beamer=False, latex_labels=False
        )
    else:
        for key in example_ids:
            ex = example_data[key]
            examples.append(get_example_hash(ex, from_corpus))
        if "Speaker" not in example_data[example_ids[0]].keys():
            from_corpus = False
        output = pynterlinear.convert_to_expex(
            examples, from_corpus=from_corpus, for_beamer=False, latex_labels=False
        )

    for form in pynterlinear.get_unknown_abbrevs():
        print(f"\\newGlossingAbbrev{{{form}}}{{{form}}}")
    pyperclip.copy(output)
