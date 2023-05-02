#!/usr/bin/env python

from os import path
import argparse
import fitz

def main(pdf_fname, page_num, out_fname):
	doc = fitz.open(pdf_fname)

	page = doc[int(page_num) - 1] # page 33

	pix = page.get_pixmap(dpi=450)
	pix.save(out_fname)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("pdf_fname")
	parser.add_argument("page_num")
	parser.add_argument("out_fname")

	args = parser.parse_args()

	main(args.pdf_fname, args.page_num, args.out_fname)
