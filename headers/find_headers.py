import fitz

doc = fitz.open("test.pdf")

for page in doc:
    blocks = page.get_text("dict", flags=11)["blocks"]
    for b in blocks:
        for l in b["lines"]:
            for s in l["spans"]:
                print(s)

    break