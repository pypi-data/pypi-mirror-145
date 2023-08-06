import os
import py_sa

def make_Preprocess_command(sample, reads_prefix, reads, out_loc, **kwargs):
    """
    echo "Preprocessing Hadza_MoBio_H_A_1_1111 ..." 2>&1 | tee -a AEGEA.log
    aegea batch submit --queue sonnenburg__spot100 --retry-attempts 3     \
    --image sonnenburglab/preprocess_metagenome_reads:latest     --storage /mnt=500     \
    --vcpus 16     --memory 64000     \
    --command="export coreNum=16; \
    export mem_mb=64000; \
    export SNAKEFILE=Snakefile; \
    export CONFIG=config.yaml; \
    export HOST_INDEX_PATH=s3://czbiohub-microbiome/Sonnenburg_Lab/Fiber_Study_Reference_Data/human_index/; \
    export SAMPLE=Hadza_MoBio_H_A_1_1111; \
    export READS_PREFIX=Hadza_MoBio_H_A_1_1111; \
    export READPATHS=(s3://czb-seqbot/fastqs/191028_A00111_0391_BHVV2VDSXX/Allison_Weakley/Dylan_Dahan s3://czb-seqbot/fastqs/191125_A00111_400_BHVXYZ2345/Dylan_Dahan); \
    export DATA_DEST=s3://czbiohub-microbiome/Sonnenburg_Lab/Hadza_Nepal_Metagenomics/FINAL_PROJECT_DATA/Hadza; \
    MINLEN=55; source preprocess_metagenome_reads.sh" 2>&1 >> AEGEA.log
    sleep 2
    """
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/preprocess_metagenome_reads:latest')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)
    wrap_cmd = kwargs.get('wrap_cmd', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 64000)
    cores = kwargs.get('cores', 16)
    timeout = kwargs.get('timeout', 86400)  # This is 2 days worth of seconds; make None to ignore

    # Get cmd aruments
    assert type(reads) == type([])
    #     sample =
    #     reads_prefix =
    #     reads =
    #     out_loc =

    # Generate the base command
    cmd = f"""
        export coreNum={cores}; \
        export mem_mb={ram}; \
        export SNAKEFILE=Snakefile; \
        export CONFIG=config.yaml; \
        export HOST_INDEX_PATH=s3://czbiohub-microbiome/Sonnenburg_Lab/Fiber_Study_Reference_Data/human_index/; \
        export SAMPLE={sample}; \
        export READS_PREFIX={reads_prefix}; \
        export READPATHS=({' '.join(reads)}); \
        export DATA_DEST={out_loc}; \
        export MINLEN=55; 
        source preprocess_metagenome_reads.sh
        """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    if timeout is None:
        t = ""
    else:
        t = f"--timeout {timeout}s"
    if wrap_cmd:
        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {t} --command=\"{cmd}\" &>> AEGEA.log"

    result = os.path.join(out_loc, sample, '00_LOGS', 'VERSION__preprocess_metagenome_reads')

    if ret_result:
        return cmd, result

    else:
        return cmd


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


def make_GTDB_command(genome_loc, out_loc, **kwargs):
    """
    aegea batch submit --queue microbiome-lhighPriority --image sonnenburglab/gtdb:latest --storage /mnt=500 --memory 128000 --vcpus 16 --command="export genomes=s3://czbiohub-microbiome/Sonnenburg_Lab/bmerrill/200527_GTDBTK_Analysis/test/; export s3OutputPath=s3://czbiohub-microbiome/Sonnenburg_Lab/bmerrill/200527_GTDBTK_Analysis/test_results/; export coreNum=16; export binExtension=fa; run_gtdb.sh
    """
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/gtdb:latest')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)
    wrap_cmd = kwargs.get('wrap_cmd', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 178000)
    cores = kwargs.get('cores', 16)
    timeout = kwargs.get('timeout', 86400)  # This is 2 days worth of seconds; make None to ignore

    # Get cmd aruments

    # Generate the base command
    cmd = f"""
        export genomes={genome_loc};
        export s3OutputPath={out_loc};
        export coreNum={cores};
        export binExtension=fa;
        ./run_gtdb.sh
        """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    if timeout is None:
        t = ""
    else:
        t = f"--timeout {timeout}s"
    if wrap_cmd:
        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {t} --command=\"{cmd}\" &>> AEGEA.log"

    result = os.path.join(out_loc, 'gtdbtk.bac120.summary.tsv')

    if ret_result:
        return cmd, result

    else:
        return cmd


def make_drep_command(results_dir, **kwargs):
    '''
    Generate an aegea dRep command

   https://github.com/SonnenburgLab/docker_images/tree/master/drep_docker

    Version 1.2 - 3.15.2021
    - add genome list and multiple folder options

    Version 1.1 - 3.1.2021
    - add genome folder option

    Version 1.0 - 2.24.2021

    Example command:

    CMD = ./prepare.sh; conda activate drep; pip install drep --upgrade; ./run_drep.py --drep_command compare --genome_list {0} --results_directory {1} --cmd_args='--S_algorithm fastANI'

    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/drep:latest')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)
    wrap_cmd = kwargs.get('wrap_cmd', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 32000)
    cores = kwargs.get('cores', 16)

    # Get cmd aruments
    unzip = kwargs.get('unzip', False)
    genome_list = kwargs.get('genome_list', None)
    genome_folder = kwargs.get('genome_folder', None)
    timeout = kwargs.get('timeout', 86400)  # This is 2 days worth of seconds; make None to ignore
    cmd_args = kwargs.get('cmd_args', "--S_algorithm fastANI")
    drep_command = kwargs.get('drep_command', 'compare')
    genome_list_base = kwargs.get('genome_list_loc', 's3://czbiohub-microbiome/Sonnenburg_Lab/mattolm/tmp/')

    if '-p' not in cmd_args:
        cmd_args += f' -p {cores}'

    # Handle genome list
    if genome_list is None:
        assert genome_folder is not None

        if type(genome_folder) == type('hi'):
            genome_folder = [genome_folder]
        else:
            assert type(genome_folder) == type([])

        cmd_substr = f' --genomes_folder {" ".join(genome_folder)} '

    elif type(genome_list) == type('hi'):
        genome_list_loc = genome_list

        cmd_substr = f' --genome_list {genome_list_loc} '


    elif type(genome_list) == type([]):
        import uuid
        genome_list_loc = genome_list_base + str(uuid.uuid4())

        print(f"Creating genome list on aws at {genome_list_loc}")
        py_sa.store_s3_file2(genome_list_loc, ('\n'.join(genome_list) + '\n').encode('ascii'))

        cmd_substr = f' --genome_list {genome_list_loc} '

    if unzip:
        cmd_substr += ' --unzip '

    # Generate the base command
    cmd = f"""
        ./prepare.sh; conda activate drep; pip install drep --upgrade; ./run_drep.py 
        --drep_command {drep_command}
        {cmd_substr}
        --results_directory {results_dir}
        --cmd_args='{cmd_args}'
        """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    if timeout is None:
        t = ""
    else:
        t = f"--timeout {timeout}s"
    if wrap_cmd:
        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {t} --command=\"{cmd}\" &>> AEGEA.log"

    result = os.path.join(results_dir, 'drep_output/data_tables/Cdb.csv')

    if ret_result:
        return cmd, result

    else:
        return cmd


def make_FragGeneScan_command(fastq_locs, s3_store_folder, **kwargs):
    '''
    Generate a FragGeneScan command

    https://github.com/SonnenburgLab/docker_images/tree/master/FragGeneScan

    Version 1.1 - 2.16.2021
    - Add clip option

    Version 1.0 - 1.29.2021

    Example command:

    ./prepare.sh; conda activate work; ./run_fraggenescan.py --fastq {DTO.R1_S3} {DTO.R2_S3} -o testeroni --results_directory {get_s3_results_folder()} -p 6 -m 10"

    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/fraggenescan:MO_dev')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)
    wrap_cmd = kwargs.get('wrap_cmd', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 32000)
    cores = kwargs.get('cores', 32)

    # Get cmd aruments
    timeout = kwargs.get('timeout', 86400)  # This is 2 days worth of seconds; make None to ignore
    SampleName = kwargs.get('SampleName', {os.path.basename(fastq_locs[0])})
    reads = kwargs.get('reads', 0)
    clip = kwargs.get('clip', 0)

    # Generate the base command
    cmd = f"""
        ./prepare.sh;
        conda activate work;
        ./run_fraggenescan.py
        --fastq {' '.join(fastq_locs)}
        -o {SampleName}
        --results_directory {s3_store_folder}
        -p {cores}
        -m {reads}
        -c {clip}
        """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    if timeout is None:
        t = ""
    else:
        t = f"--timeout {timeout}s"
    if wrap_cmd:
        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {t} --command=\"{cmd}\" &>> AEGEA.log"

    result = f"{s3_store_folder}{SampleName}.faa"

    if ret_result:
        return cmd, result

    else:
        return cmd


def make_rarefy_command(bam_loc, fasta_loc, stb_loc, s3_store_folder, **kwargs):
    '''
    Generate an aegeainstrain rarefaction command

    https://github.com/SonnenburgLab/docker_images/tree/master/inStrain_rarefaction

    Version 1.0 - 1.18.2021

    Example command:

    CMD = f"""
    ./prepare.sh;
    conda activate work;
    pip install instrain --upgrade;
    ./rarefaction_curve.py
    -b {self.BAM_S3}
    -o {get_s3_results_folder()}
    -f {self.FASTA_S3}
    -s {self.STB_S3}
    --s3_upload {get_s3_results_folder()}
    --iterations 1
    """.replace('\n', ' ')

    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/instrain_w_bam_subset:MO')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)
    wrap_cmd = kwargs.get('wrap_cmd', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 32000)
    cores = kwargs.get('cores', 16)

    # Get cmd aruments
    timeout = kwargs.get('timeout', 86400)  # This is 2 days worth of seconds; make None to ignore
    seed = kwargs.get('seed', 33)
    SampleName = kwargs.get('SampleName', {os.path.basename(bam_loc)})
    total_reads = kwargs.get('total_reads', False)
    start = kwargs.get('start', None)
    end = kwargs.get('end', None)
    step = kwargs.get('step', None)

    # Generate the base command
    cmd = f"""
        ./prepare.sh;
        conda activate work;
        pip install instrain --upgrade;
        ./rarefaction_curve.py 
        -b {bam_loc}
        -o {s3_store_folder}
        -f {fasta_loc}
        -s {stb_loc}
        --s3_upload {s3_store_folder}
        -p {cores}
        --Gbp_level
        --iterations 1
        """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    if total_reads:
        cmd += f' -t {total_reads}'

    for text, val in zip(['--start', '--end', '--step'], [start, end, step]):
        if val is not None:
            cmd += f' {text} {val}'

    # Wrap in aegea
    if timeout is None:
        t = ""
    else:
        t = f"--timeout {timeout}s"
    if wrap_cmd:
        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {t} --command=\"{cmd}\" &>> AEGEA.log"

    result = f"{s3_store_folder}output/rarefaction_table.csv"

    if ret_result:
        return cmd, result

    else:
        return cmd


def make_unicycler_command(fastq1, fastq2, longreads, s3_store_folder, **kwargs):
    '''
    Generate an aegea UniCycler command

    Version 1.1 - 7.7.2021
    - Add ret_result

    Version 1.0 - 10.13.2020
    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'xianmeng/unicycler')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    wrap_cmd = kwargs.get('wrap_cmd', True)
    ret_result = kwargs.get('ret_result', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 128000)
    cores = kwargs.get('cores', 16)
    timeout = kwargs.get('timeout', '24h')

    # Generate the base command
    bucket = "s3://{0}/".format(bucket_id)
    cmd = f"""
        export fastq1={fastq1};
        export fastq2={fastq2};
        export longreads={longreads};
        export S3OUTPUTPATH={s3_store_folder};
        run_unicycler_hybrid_nanopore.sh
        """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    result = os.path.join(s3_store_folder, 'UNICYCLER/assembly.fasta')

    # Wrap in aegea
    if wrap_cmd:
        if timeout is not None:
            timeout = f" --timeout {timeout}"
        else:
            timeout = ''

        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {timeout} --command=\"{cmd}\" &>> AEGEA.log".format(
            cores, ram, cmd, image, queue)

    if ret_result:
        return cmd, result

    else:
        return cmd

    return cmd


def make_mapping_command(r1, r2, fasta_loc, s3_store_folder, **kwargs):
    '''
    Generate an aegea Bowtie2 command

    Version 1.4 - 9.27.2021
    - Yell if the index ends with .bt2 (it shouldn't)

    Version 1.3 - 5.10.2021
    - Add output types

    Version 1.2 - 2.25.2021
    - dont add buckets to r1 and r2

    Version 1.1 - 10.20.2020
    - update ret_result when using an index

    Version 1.0 - 8.25.2020

    Arguments:
        bam_loc = s3 location of .bam file
        fasta_loc = s3 location of .fasta file
        s3_store_loc = s3 folder to store results
    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/bowtie2:dev')
    ret_result = kwargs.get('ret_result', False)

    # Get aegea arguments
    ram = kwargs.get('ram', 32000)
    cores = kwargs.get('cores', 16)

    # Get mapping arguments
    large_index = kwargs.get('large_index', False)
    store_index = kwargs.get('store_index', False)
    index_location = kwargs.get('index_location', False)
    output_type = kwargs.get('output_type', 'BAM')

    # Generate the base command
    bucket = "s3://{0}/".format(bucket_id)
    cmd = f"""
    ./prepare.sh; conda activate work; ./run_bowtie2.py --r1 {r1} --r2 {r2} --results_directory {s3_store_folder} --output_type {output_type} -p {cores}
    """.replace('\n', ' ')

    if index_location == False:
        cmd += ' --fasta {0}'.format(fasta_loc)
        result = s3_store_folder + "{0}-vs-{1}.sorted.bam".format(os.path.basename(fasta_loc), os.path.basename(r1))
    else:
        if index_location.endswith('bt2'):
            print("HEY! THE INDEX SHOULDNT END WITH BT2! DELETE THAT PART!")
        cmd += ' --index {0}'.format(index_location)
        result = s3_store_folder + "{0}-vs-{1}.sorted.bam".format(os.path.basename(index_location),
                                                                  os.path.basename(r1))

    if large_index:
        cmd += ' --large_index'

    if store_index:
        cmd += ' --store_index'

    if output_type == 'SUMMARY':
        result = result.replace('.sorted.bam', '.txt')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    aegea_cmd = "aegea batch submit --queue sonnenburg__spot100 --image {3} --storage /mnt=500 --vcpus {0} --memory {1} --command=\"{2}\" &>> AEGEA.log".format(
        cores, ram, cmd, image)

    if ret_result:
        return aegea_cmd, result
    else:
        return aegea_cmd

    return aegea_cmd


def make_eukcc_command(BIN_PATH, DATA_DEST, **kwargs):
    '''
    Generate an aegea EukCC command

    Version 1.2 - 10.30.2020
    - Fix things for working with unzipped files

    Version 1.1 - 10.20.2020
    - Add PYGMES

    Version 1.0 - 10.13.2020
    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/eukcc:latest')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    wrap_cmd = kwargs.get('wrap_cmd', True)
    ret_result = kwargs.get('ret_result', False)

    # Get aegea arguments
    ram = kwargs.get('ram', 32000)
    cores = kwargs.get('cores', 8)

    # Generate the base command
    bucket = "s3://{0}/".format(bucket_id)
    cmd = f"""
        export coreNum={cores};
        export mem_mb={ram};
        export BIN_PATH={BIN_PATH};
        export DATA_DEST={DATA_DEST};
        export PYGMES=TRUE;
        ./run_eukcc.sh
        """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    if wrap_cmd:
        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} --command=\"{cmd}\" &>> AEGEA.log"

    # Get result
    result = f"{DATA_DEST}/{os.path.basename(BIN_PATH).replace('.gz', '').replace('.fa', '')}/workfiles/gmes/prot_seq.faa"

    if ret_result:
        return cmd, result
    else:
        return cmd

    return cmd


def make_inStrain_command(bam_loc, fasta_loc, s3_store_folder, **kwargs):
    '''
    Generate an aegea inStrain command

    Version 1.2 - 2.18.2021
    # Add quick_profile options

    Version 1.1 - 2.1.2021
    # Remove bucket appending

    Version 1.0 - 6.3.2020

    Arguments:
        bam_loc = s3 location of .bam file
        fasta_loc = s3 location of .fasta file
        s3_store_loc = s3 folder to store results
    '''
    # Get s3 arguments
    image = kwargs.get('image', 'mattolm/instrain')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)

    # Get aegea arguments
    ram = kwargs.get('ram', 178000)
    cores = kwargs.get('cores', 32)

    # Get inStrain aruments
    stb_loc = kwargs.get('stb_loc', None)
    gene_loc = kwargs.get('gene_loc', None)
    IS_name = kwargs.get('IS_name', None)
    command = kwargs.get('command', None)
    cmd_args = kwargs.get('cmd_args', '--skip_plot_generation --database_mode')
    timeout = kwargs.get('timeout', 172800)  # This is 2 days worth of seconds; make None to ignore

    # Parse inStrain arguments
    if IS_name is None:
        IS_name = os.path.basename(bam_loc) + '.IS'
    cmd_args += ' -p {0}'.format(cores)

    # Generate the base command
    cmd = """
        ./prepare.sh; conda activate work; pip install instrain --upgrade; ./run_instrain.py 
        --bam {0} 
        --fasta {1} 
        --results_directory {2} 
        --wd_name {3} 
        --cmd_args='{4}'
        """.format(bam_loc,
                   fasta_loc,
                   s3_store_folder,
                   IS_name,
                   cmd_args).replace('\n', ' ')

    # Add to base command
    if timeout is not None:
        cmd += ' --timeout {0}'.format(timeout)
    if gene_loc is not None:
        cmd += ' --genes {0}'.format(gene_loc)
    if stb_loc is not None:
        cmd += ' --stb {0}'.format(stb_loc)
    if command is not None:
        cmd += '  --command {0}'.format(command)

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    aegea_cmd = "aegea batch submit --queue {4} --image {3} --storage /mnt=500 --vcpus {0} --memory {1} --command=\"{2}\" &>> AEGEA.log".format(
        cores, ram, cmd, image, queue)

    # Get result
    result = s3_store_folder + IS_name + '/raw_data/Rdic.json'.format(IS_name)
    if command == 'quick_profile':
        result = s3_store_folder + IS_name + '/coverm_raw.tsv'.format(IS_name)

    if ret_result:
        return aegea_cmd, result
    else:
        return aegea_cmd


def calc_needed_ram(si, constant=99):
    """
    For inStrain Profile
    """
    size_gb = si / 1e9
    est_r = (4.64 * size_gb) + constant
    return est_r * 1000


def make_instrain_compare_command(is_locs, s3_store_folder, **kwargs):
    '''
    Generate an aegea inStrain compare command

    Version 2.0 - 11.5.2020

    is_locs = s3 location of a text file containing locations of all inStrain profiles

    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'mattolm/instrain:latest')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)
    wrap_cmd = kwargs.get('wrap_cmd', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 178000)
    cores = kwargs.get('cores', 32)

    # Get inStrain aruments
    stb_loc = kwargs.get('stb_loc', None)
    timeout = kwargs.get('timeout', 86400)  # This is 2 days worth of seconds; make None to ignore
    cmd_args = kwargs.get('cmd_args')
    IS_name = kwargs.get('IS_name', None)

    # Parse inStrain arguments
    cmd_args += ' -p {0}'.format(cores)

    # Generate the base command
    bucket = "s3://{0}/".format(bucket_id)
    if type(is_locs) == type([]):
        is_str = ' '.join(is_locs)
    else:
        is_str = is_locs

    cmd = f"""
        ./run_instrain.py 
        --IS {is_str} 
        --results_directory {s3_store_folder} 
        --wd_name {IS_name} 
        --command compare
        --cmd_args='{cmd_args}'
        """.replace('\n', ' ')
    if wrap_cmd:
        cmd = "./prepare.sh; conda activate work; pip install instrain --upgrade; {0}".format(cmd)

    # Add to base command
    if timeout is not None:
        cmd += ' --timeout {0}'.format(timeout)
    if stb_loc is not None:
        cmd += ' --stb {0}'.format(stb_loc)

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Wrap in aegea
    if wrap_cmd:
        cmd = "aegea batch submit --queue {4} --image {3} --storage /mnt=500 --vcpus {0} --memory {1} --command=\"{2}\" &>> AEGEA.log".format(
            cores, ram, cmd, image, queue)

    # Get result
    result = s3_store_folder + IS_name + '/output/{0}_comparisonsTable.tsv'.format(IS_name)

    if ret_result:
        return cmd, result
    else:
        return cmd


def make_isolate_genome_assembly_command(name, r1, r2, s3_store_folder, **kwargs):
    '''
    Generate an aegea Isolate genome assembly command

    https://github.com/SonnenburgLab/docker_images/blob/master/isolate_genome_assembly/docker_files/example_submit_script.sh

    Version 1.0 - 10.13.2020
    '''
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/assembly_shovill:MO_dev')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    wrap_cmd = kwargs.get('wrap_cmd', True)
    ret_result = kwargs.get('ret_result', False)
    cmd_args = kwargs.get('cmd_args', ' --trim ')

    # Get aegea arguments
    ram = kwargs.get('ram', 32000)
    cores = kwargs.get('cores', 16)
    timeout = kwargs.get('timeout', '5h')
    cmd_args += f' --cpus {cores} --ram {ram / 1000} '

    # Generate the base command
    bucket = "s3://{0}/".format(bucket_id)
    cmd = f"""
           ./prepare.sh;
           conda activate work;
           ./run_assembly.py
           --r1 {r1}
           --r2 {r2}
           --outname {name}
           --results_directory {s3_store_folder}
           --cmd_args ' {cmd_args} '
           """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Get the result
    result = os.path.join(s3_store_folder, f"{name}/contigs.fa")

    # Wrap in aegea
    if wrap_cmd:
        if timeout is not None:
            timeout = f" --timeout {timeout}"
        else:
            timeout = ''

        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {timeout} --command=\"{cmd}\" &>> AEGEA.log".format(
            cores, ram, cmd, image, queue)

    if ret_result:
        return cmd, result

    else:
        return cmd


def make_assembly_command(sample, data_dest, FWD_READS, REV_READS, **kwargs):
    """
    * v1.0 8/19/21
    - Can handle single and co-assemblies

    "export coreNum={5}; export mem_mb={6}; export SAMPLE={0}; export DATA_DEST={1}; export FWD_READS={2}; export REV_READS={3}; export MERGED_READS={4}; ./single_sample_assembly_metaspades_merged.sh
    """
    # Get s3 arguments
    bucket_id = kwargs.get('bucket_id', "czbiohub-microbiome")
    image = kwargs.get('image', 'sonnenburglab/single_and_coassembly:latest')
    queue = kwargs.get('queue', 'sonnenburg__spot100')
    ret_result = kwargs.get('ret_result', False)
    wrap_cmd = kwargs.get('wrap_cmd', True)

    # Get aegea arguments
    ram = kwargs.get('ram', 128000)
    cores = kwargs.get('cores', 16)
    timeout = kwargs.get('timeout', 86400)  # This is 2 days worth of seconds; make None to ignore

    # Get cmd aruments
    merged_reads = kwargs.get('merged_reads', None)
    bash_script = kwargs.get('bash_script', 'single_sample_assembly_metaspades_merged.sh')

    # Generate the base command
    cmd = f"""
        export coreNum={cores};
        export mem_mb={ram};
        export SAMPLE={sample};
        export DATA_DEST={data_dest};
        export FWD_READS={FWD_READS};
        export REV_READS={REV_READS};
        export OUT_NAME={sample};
        export CONTIG_NAME={sample};
        """.replace('\n', ' ')

    # Remove variable length whitespace
    cmd = ' '.join(cmd.split())

    # Add merged reads
    if merged_reads != None:
        cmd += f' export MERGED_READS={merged_reads};'

    # Add command to end
    cmd += f' source {bash_script}'

    # Wrap in aegea
    if timeout is None:
        t = ""
    else:
        t = f"--timeout {timeout}s"
    if wrap_cmd:
        cmd = f"aegea batch submit --queue {queue} --image {image} --storage /mnt=500 --vcpus {cores} --memory {ram} {t} --command=\"{cmd}\" &>> AEGEA.log"

    if bash_script == 'coassembly_metaspades_merged.sh':
        result = os.path.join(data_dest, f'COASSEMBLY/SCAFFOLDS_min1500_{sample}')
    else:
        result = os.path.join(data_dest, f'06_ASSEMBLY/CONTIGS_1500_MERGED_K77_METASPADES__{sample}.fasta')

    if ret_result:
        return cmd, result

    else:
        return cmd