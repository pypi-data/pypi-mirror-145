# py_sa

py_sa is a way to interact with aegea and s3 through python

# Example mapping

```angular2html
import importlib
importlib.reload(py_sa)

import py_sa
import py_sa.aegea_cmds

rdb = py_sa.load_running_aegea()
s3_store_folder = 's3://czbiohub-microbiome/Sonnenburg_Lab/InfantMicrobiome/B_longum/mapping/'
index_loc = 's3://czbiohub-microbiome/Sonnenburg_Lab/InfantMicrobiome/B_longum/Bifidobacterium_longum_subsp_infantis_ATCC_15697.fna.fa.bt2'

for i, row in PXdb.iterrows():
    cmd, result = py_sa.aegea_cmds.make_mapping_command(row['r1'], row['r2'], 'junk', 
                            s3_store_folder, index_location=index_loc,
                            output_type='BAM', ret_result=True)
    py_sa.submit_aegea_job(cmd, result, verbose=True, rdb=rdb)
    break
```

# Example inStrain profile

```angular2html
import importlib
importlib.reload(py_sa)

import py_sa
import py_sa.aegea_cmds


s3_store_folder = 's3://czbiohub-microbiome/Sonnenburg_Lab/InfantMicrobiome/B_longum/profile/'
fasta_loc = 's3://czbiohub-microbiome/Sonnenburg_Lab/InfantMicrobiome/B_longum/Bifidobacterium_longum_subsp_infantis_ATCC_15697.fna.fa'
genes_loc = 's3://czbiohub-microbiome/Sonnenburg_Lab/InfantMicrobiome/B_longum/Bifidobacterium_longum_subsp_infantis_ATCC_15697.fna.fa.genes.fna'
b = 's3://czbiohub-microbiome/'

rdb = py_sa.load_running_aegea()
for bam in py_sa.get_matching_s3_keys('czbiohub-microbiome', 'Sonnenburg_Lab/InfantMicrobiome/B_longum/mapping/', '.sorted.bam'):
    bam_loc = b + bam
    
    cmd, result = py_sa.aegea_cmds.make_inStrain_command(bam_loc,
                        fasta_loc, s3_store_folder,
                        ram=32000, cores=8, gene_loc=genes_loc,
                        cmd_args='', ret_result=True)
    py_sa.submit_aegea_job(cmd, result, verbose=True, rdb=rdb)
    
    print(cmd)
    break
```

# Example deeparg
```
import py_sa
import py_sa.aegea_cmds

import importlib
importlib.reload(py_sa)

def make_deeparg_cmd(read1, read2, outname, s3_store_folder, **kwargs):
    '''
    Version 1.0 - 12.1.2021
    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/deeoarg:MO_dev')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)
    wrap_cmd = kwargs.get('wrap_cmd', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 32000)
    cores = kwargs.get('cores', 6)

    # Generate the base command
    cmd = f"""
        ./prepare.sh;
        conda activate work;
       ./run_deeparg.py
       --r1 {read1}
       --r2 {read2}
       --outname {outname}
       --results_directory {s3_store_folder}
       """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    t = ""
    if wrap_cmd:
        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {t} --command=\"{cmd}\" &>> AEGEA.log"

    result = f"{s3_store_folder}{outname}.clean.deeparg.mapping.ARG.merged.quant.type"

    if ret_result:
        return cmd, result

    else:
        return cmd
    

rdb = py_sa.load_running_aegea()
s3_store_folder = 's3://czbiohub-microbiome/Sonnenburg_Lab/Project_Vital/DeepArg/'

for i, row in Pdb.iterrows():
    cmd, result = make_deeparg_cmd(row['read1'], row['read2'], row['sample'], 
                            s3_store_folder, ret_result=True)
    py_sa.submit_aegea_job(cmd, result, verbose=True, rdb=rdb)
```