import boto3
from infinstor import infin_boto3
import tempfile
from IPython.display import Image
import mlflow
import os
import json
import pandas as pd
from infinstor import infinslice, infinsnap

def list_one_dir(client, bucket, prefix_in, arr):
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix_in, Delimiter="/")
    for page in page_iterator:
        contents = page.get('Contents')
        if (contents != None):
            # print('   ' + str(contents))
            for one_content in contents:
                if 'Metadata' in one_content:
                    md = json.loads(one_content['Metadata'])
                    md['FileName'] = one_content['Key']
                    md['FileSize'] = one_content['Size']
                    md['FileLastModified'] = one_content['LastModified']
                    md['FileVersionId'] = one_content['versionId']
                    arr.append(md)
        common_prefixes = page.get('CommonPrefixes')
        if (common_prefixes != None):
            for prefix in common_prefixes:
                this_prefix = str(prefix['Prefix'])
                # print('   ' + this_prefix)
                if this_prefix:
                    list_one_dir(client, bucket, this_prefix, arr)


def list_files_meta(bucket, prefix, start_time=None, end_time=None):
    if (start_time and end_time):
        infinstor_time_spec = infinslice(start_time, end_time)
    elif (end_time):
        infinstor_time_spec = infinsnap(end_time)
    else:
        infinstor_time_spec = None
    arr = []
    if infinstor_time_spec:
        client = boto3.client('s3', infinstor_time_spec=timespec)
    else:
        client = boto3.client('s3')
    list_one_dir(client, bucket, prefix, arr)
    return pd.DataFrame(arr)
