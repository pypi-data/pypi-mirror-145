import io
import boto3
import pandas as pd

def submit_aegea_job(cmd, expected_output, rdb=None, alocation=None, verbose=False):
    """
    Submit the cmd to aegea, capture the jobID, and store the jobID at ~/aegea_logs.txt

    v1.0 - 1/26/21

    aegea 2.6.9
    """
    from datetime import datetime
    import subprocess

    if alocation is None:
        alocation = '/home/mattolm/.aegea_logs.txt'

    # 1) Check it output already exists
    if check_s3_file(expected_output):
        if verbose:
            print(f"{expected_output} already exists")
        return None

    # 2) Check if job is already running

    # Get list of running jobs
    if rdb is None:
        rdb = load_running_aegea(verbose=False)
    running_jobs = set(rdb[rdb['job_status'].isin(['RUNNING', 'RUNNABLE', 'STARTING'])]['job_ID'].tolist())
    if verbose:
        print(f"{len(running_jobs)} jobs are running")

    # Get output -> job key
    adb = pd.read_csv(alocation, sep='\t', names=['job_ID', 'output', 'time', 'cmd'])
    cdb = adb[adb['output'] == expected_output]
    if len(cdb) > 0:
        db = cdb[cdb['job_ID'].isin(running_jobs)]
    else:
        db = pd.DataFrame()
    if verbose:
        print(
            f"Captured {len(adb)} aegea logs, {len(running_jobs)} running jobs, {len(cdb)} previous attempts, {len(db)} currently running attempts")

    if len(db) > 0:
        if verbose:
            print(f"{expected_output} is currently running (job={db['job_ID'].tolist()})")
        return None

    # 3) Run job
    out = subprocess.check_output(cmd, shell=True, text=True)
    ID = eval(out)['jobId']

    # 4) Store job ID
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    with open(alocation, 'a') as o:
        o.write(f"\n{ID}\t{expected_output}\t{dt_string}\t{cmd}")

    # 5) Finish
    if verbose:
        print(f"Job {ID} is launched to create {expected_output}")
    return ID


def load_running_aegea(queue="", tries=20, verbose=True):
    """
    Return a list of running aegea jobs

    v1.2 - 10/11/21
    * If no queue is specified, dont do a queue

    v1.1 - 3/15/21
    * Better printing of status while running showq

    v1.0 - 1/26/21

    aegea 2.6.9
    """
    import subprocess
    print("Running showq...")
    if queue != "":
        cmd = f"aegea batch ls --queue {queue}"
    else:
        cmd = f"aegea batch ls"
    while tries >= 0:
        try:

            raw_out = subprocess.check_output(cmd, shell=True, text=True)
            break
        except:
            # print(f"showq failed for {queue}, try # {tries}")
            tries = tries - 1
    print("Showq succeeded")

    table = {'job_ID': [], 'job_status': [], 'image': []}
    lines = len(raw_out.split('\n'))
    for j, line in enumerate(raw_out.split('\n')):
        # Skip header
        if j >= 3:

            lw = line.strip().split('│')

            # Skip weird lines
            if len(lw) != 14:
                continue

            table['job_ID'].append(lw[1].strip())
            table['job_status'].append(lw[4].strip())
            table['image'].append(lw[8].strip())

    db = pd.DataFrame(table)

    if verbose:
        print(f"{len(db[db['job_status'] == 'RUNNING'])} aegea jobs are currently running")

    return db


def get_matching_s3_objects(bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")

    kwargs = {'Bucket': bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix,)
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = key_prefix

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                return

            for obj in contents:
                key = obj["Key"]
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj["Key"]


def check_s3_file(floc):
    '''
    Return True if exists and False if it does not
    '''
    bucket = floc.split('/')[2]
    prefix = '/'.join(floc.split('/')[3:])

    found = False
    for key in get_matching_s3_keys(bucket, prefix):
        if prefix in key:
            found = True
    return found


def store_s3_file(bucket, location, binary_string):
    s3 = boto3.resource('s3')
    object = s3.Object(bucket, location)
    object.put(Body=binary_string)


def load_coverage_report(s3_bucket, s3_key, sep='\t', names=None):
    '''
    https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
    '''
    # Load the data from s3
    client = boto3.client("s3")
    obj = client.get_object(Bucket=s3_bucket, Key=s3_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()), sep=sep, names=names)

    return df


def load_coverage_report2(s3_loc, sep='\t', names=None):
    '''
    https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
    '''
    s3_bucket = s3_loc.split('/')[2]
    s3_key = '/'.join(s3_loc.split('/')[3:])

    # Load the data from s3
    client = boto3.client("s3")
    obj = client.get_object(Bucket=s3_bucket, Key=s3_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()), sep=sep, names=names)

    return df


def read_s3_file(s3_bucket, s3_key):
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket, s3_key)
    return obj.get()['Body'].read().decode("utf-8")


def object_size(s3_bucket, s3_key):
    return boto3.resource('s3').Bucket(s3_bucket).Object(s3_key).content_length


def object_size2(s3_loc):
    s3_bucket = s3_loc.split('/')[2]
    s3_key = '/'.join(s3_loc.split('/')[3:])

    return boto3.resource('s3').Bucket(s3_bucket).Object(s3_key).content_length


def read_s3_file2(s3_loc):
    s3 = boto3.resource('s3')
    bucket = s3_loc.split('/')[2]
    key = '/'.join(s3_loc.split('/')[3:])
    return read_s3_file(bucket, key)


def store_s3_file2(s3_loc, binary_string):
    s3 = boto3.resource('s3')
    bucket = s3_loc.split('/')[2]
    key = '/'.join(s3_loc.split('/')[3:])
    return store_s3_file(bucket, key, binary_string)