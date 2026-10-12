"""Réexécute les quatre notebooks, en préservant leurs sorties pour la revue Git."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ.setdefault(key,'1')
from pathlib import Path
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parent
for file in sorted((ROOT/'notebooks').glob('*.ipynb')):
    print('Exécution :',file.name,flush=True)
    book=nbformat.read(file,as_version=4)
    NotebookClient(book,timeout=300,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}},allow_errors=False).execute()
    nbformat.write(book,file)
    print('OK :',file.name,flush=True)
