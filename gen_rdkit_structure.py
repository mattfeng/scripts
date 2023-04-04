import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D, rdDepictor

print(rdkit.__version__)

rdDepictor.SetPreferCoordGen(True)

molecules = {
    "acetylpringleine": "O=C(OC1CC(O)(C)C23OC(C)(C)C(CC(OC(=O)C=4C=CC=CC4)C2(COC(=O)C)C1OC(=O)C)C3OC(=O)C)C=5C=CC=CC5"
}

def get_avg_bond_length(mol):
    lengths = []
    conf = mol.GetConformer()
    for bond in mol.GetBonds():
        i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        p1 = conf.GetAtomPosition(i)
        p2 = conf.GetAtomPosition(j)

        length = ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5
        lengths.append(length)
    
    return sum(lengths) / len(lengths)

mol = Chem.MolFromSmiles(molecules["acetylpringleine"])

if mol.GetNumConformers() == 0:
    rdDepictor.Compute2DCoords(mol, nSample=100, nFlipsPerSample=100)

drawer = rdMolDraw2D.MolDraw2DSVG(-1, -1)
drawer.drawOptions().atomLabelDeuteriumTritium = True
drawer.drawOptions().bondLineWidth = 0.6
drawer.drawOptions().scaleBondWidth = False
drawer.drawOptions().scalingFactor = 14.4 / get_avg_bond_length(mol)
drawer.drawOptions().fixedFontSize = 10
drawer.drawOptions().additionalAtomLabelPadding = 0.066

drawer.DrawMolecule(mol)
drawer.FinishDrawing()
svg = drawer.GetDrawingText().replace("svg:", "")

with open("out.svg", "w") as f:
    f.write(svg)
