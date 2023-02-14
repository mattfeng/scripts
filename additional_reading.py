#!/usr/bin/env python

import argparse
import os
import requests

def get_refs(doi):
    endpoint = f"https://api.crossref.org/works/{doi}"
    r = requests.get(endpoint)

    refs = r.json()["message"]["reference"]
    return refs

def normalize(refids):
    refids = refids.split(",")

    normalized = []
    for refid in refids:
        refid = refid.strip()
        if "-" in refid:
            start, stop = refid.split("-")
            expanded = range(int(start), int(stop) + 1)
            normalized.extend(expanded)
        else:
            normalized.append(int(refid))

    return normalized

def main(refs, ofile):
    data = {}
    with open(refs) as f:
        doi = f.readline().strip()

        for line in f:
            if line.startswith("-"):
                topic, refids = line[1:].strip().split(":")
                data[topic.strip()] = refids.strip()

    paperrefs = get_refs(doi)

    with open(ofile, "w") as fout:
        for topic, refids in data.items():
            refids = normalize(refids)

            fout.write(f"- {topic}\n")
            for refid in refids:
                uid = paperrefs[refid - 1].get('DOI')

                if uid:
                    uid = f"https://www.doi.org/{uid}"
                else:
                    # issn search with https://www.crossref.org/titleList/
                    uid = paperrefs[refid - 1].get("ISSN")

                fout.write(f"  - {uid}\n")

    print("[i] Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("refs")
    parser.add_argument("ofile")
    args = parser.parse_args()
    main(args.refs, args.ofile)
