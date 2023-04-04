import fitz
import subprocess as sp
import shlex
import io

command = "osascript -e 'the clipboard as \"PDF \"'"

pdfhex = sp.run(shlex.split(command), capture_output=True).stdout.decode("utf-8").strip().split("PDF ")[1][:-1]

pdfdata = bytes.fromhex(pdfhex)
pdfio = io.BytesIO(pdfdata)

# with open("output.pdf", "wb") as f:
#     f.write(pdfdata)

pdf = fitz.open(stream=pdfdata)
svg = pdf[0].get_svg_image(matrix=fitz.Identity, text_as_path=True)

print(svg)
