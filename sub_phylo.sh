#!/bin/bash
#SBATCH --nodes=1               #Numero de Nós
#SBATCH --ntasks-per-node=1     #Numero de tarefas por Nó
#SBATCH --ntasks=1              #Numero de tarefas
#SBATCH -p cpu_dev              #Fila (partition) a ser utilizada
#SBATCH -J JOB_PHYLO            #Nome job

#Carregar os módulos
module load python/3.8.2
#pip3 install --user parsl
module load perl/5.20
module load phylip/3.6
module load raxml/8.2_openmpi-2.0_gnu
module load readseq/2.1
module load modelgenerator/85
module load mafft/7.4

dir=$(pwd)
export SWIFT_PHYLO=$dir/bin
export PATH=$SWIFT_PHYLO/mafft-7.221-with-extensions/bin:$PATH
export PATH=$SWIFT_PHYLO/standard-RAxML-master/bin:$PATH
export PATH=$SWIFT_PHYLO:$PATH

#Dando permissão para execução do script
chmod a+x $dir/bin/fastaNumbered

#Acessar o diretório onde o script está localizado
cd /scratch/cenapadrjsd/lucas.silva/phylo

EXEC=/scratch/cenapadrjsd/lucas.silva/phylo/phylo.py

#Executa o script
time python3 $EXEC
