#! /usr/bin/env python3
import parsl
from parsl import load, python_app, bash_app
from parsl.configs.local_threads import config
from parsl.data_provider.files import File
from pathlib import Path

load(config)

@bash_app
def fastanumbered(infile, stdout, stderr = parsl.AUTO_LOGNAME):
    return 'perl $SWIFT_PHYLO/numberFasta.pl {} > {}'.format(infile, stdout)

@bash_app
def MAFFT(infile, stdout, stderr = parsl.AUTO_LOGNAME):
    return 'mafft {} > {}'.format(infile, stdout)

@bash_app
def readseq(infile, stdout, stderr = parsl.AUTO_LOGNAME):
    return 'java -jar $SWIFT_PHYLO/readseq.jar -all -f=12 {0} -o {1}'.format(infile, stdout)

@bash_app
def modelgenerator(infile, stdout, stderr = parsl.AUTO_LOGNAME):
    return 'java -jar $SWIFT_PHYLO/modelgenerator.jar {} 6'.format(infile, stdout)

@bash_app
def cleanModelgenerator(infile, stderr = parsl.AUTO_LOGNAME):
    return 'python $SWIFT_PHYLO/clean_modelgenerator.py {}'.format(infile)

@bash_app
def raxml(phylipfile, mfMGfile, stderr = parsl.AUTO_LOGNAME):
    return 'python $SWIFT_PHYLO/execute_raxml.py ./results {} {} 2 4'.format(phylipfile, mfMGfile)

p = Path('.')
fasta = list(p.glob('./ORTHOMCL*'))

for i in fasta:
    outfile = './intermediate_files/{}.fastaNumbered'.format(i.stem[8:]) #pega o "ID" do arquivo
    fastaNumbered_future =  fastanumbered(i, stdout = outfile)
fastaNumbered_future.result()

fastaNumbered = list(p.glob('./intermediate_files/*.fastaNumbered'))

for i in fastaNumbered:
    outfile = './intermediate_files/{}.mafft'.format(i.stem)
    mafft_future = MAFFT(i, stdout = outfile)
mafft_future.result()

mafft = list(p.glob('./intermediate_files/*.mafft'))

for i in mafft:
    outfile = './results/{}.phylip'.format(i.stem)
    readseq_future = readseq(i, stdout = outfile)
readseq_future.result()

phylip = sorted(list(p.glob('./results/*.phylip')))

for i in phylip:
    outfile = './results/{}.mg'.format(i.stem)
    mg_future = modelgenerator(i, stdout = outfile)
mg_future.result()

modelgenerator = list(p.glob('./results/*.mg'))

teste = []
for i in modelgenerator:
    mfMG_future = cleanModelgenerator(i)
    teste.append(mfMG_future)
saida = [j.result() for j in teste]

mfMG = sorted(list(p.glob('./results/*.mg.modelFromMG.txt')))
print(mfMG)
print(phylip)


for i, j in zip(phylip, mfMG):
    raxml_future = raxml(i, j)
raxml_future.result()

