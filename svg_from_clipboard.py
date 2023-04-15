import fitz
import subprocess as sp
import shlex
import io

command = "osascript -e 'the clipboard as \"PDF \"'"

pdfhex = sp.run(shlex.split(command), capture_output=True).stdout.decode("utf-8").strip().split("PDF ")[1][:-1]

pdfdata = bytes.fromhex(pdfhex)
pdfio = io.BytesIO(pdfdata)

with open("output.pdf", "wb") as f:
    f.write(pdfdata)

command = "osascript -e 'the clipboard as \"mMOL\"'"

molhex = sp.run(shlex.split(command), capture_output=True).stdout.decode("utf-8").strip().split("mMOL")[1][:-1]
moldata = bytes.fromhex(molhex)

# def decode_moldata(data):
#     counter = 0
#     for c in data:
#         if counter == 0:
#             counter = ord(c)
#         else:
#             counter -= 1
