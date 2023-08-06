import boto3
import botocore
from botocore.exceptions import ClientError
import geopandas as gpd
import imageio
import io
import matplotlib.image as mpimg
import numpy as np
import os
import os.path
from os import path
import pandas as pd
from PIL import Image
import json


s3_client = boto3.client('s3')


def upload_object(bucket: str = None,
                  s3_file_path: str = None,
                  local_file_path: str = None,
                  profile_name: str = None,
                  json_obj=None):
    """
    Upload a file from local to an S3 bucket

    Parameters
    ----------
    local_file_path: str. Local path of file to upload
    bucket: str. S3 bucket name to upload to.
    s3_file_path: str. S3 object name to save to. If not specified then local_file_path is used
    profile_name: str. Profile AWS name.
    json_obj: Json object in case a json file is uploaded.
    """
    # Store in same location in S3 and Locally.

    if '/data/' not in local_file_path:
        raise Exception('local_file_path=' + local_file_path + 'must contain "/data/"')

    filename, fileformat, local_file_dir, s3_file_dir = filepath_breaker(local_file_path)

    if s3_file_path is None:
        s3_file_path = s3_file_dir + filename + fileformat

    # Upload the file
    out = True
    try:
        if profile_name is not None:
            boto3.setup_default_session(profile_name=profile_name)
        print('Saving file in S3 as: ' + s3_file_path + ' ... ', end='')
        if fileformat == '.json':
            s3object = s3_client.Object(bucket, s3_file_path)
            s3object.put(Body=(bytes(json.dumps(json_obj).encode('UTF-8'))))
        else:
            s3_client.upload_file(Filename=local_file_path, Bucket=bucket, Key=s3_file_path)
        print('done')
    except ClientError:
        out = False
    return out


def save_object(obj=None,
                local_file_path: str = None,
                bucket: str = None,
                upload_only: bool = False,
                **kwargs):
    """
        Saves locally and uploads a file from local to an S3 bucket

        Parameters
        ----------
        obj: Object. Dataframe to save in both: locally and into s3.
        local_file_path: str. Local path of file to upload
        bucket: str. S3 bucket name to upload to.
        upload_only: bolean. If False saves copy localy, else (True) it does not save local copy.
        """

    if '/data/' not in local_file_path:
        raise Exception('local_file_path=' + local_file_path + 'must contain "/data/"')


    if obj is None:
        raise Exception('obj cannot be None')

    # Read file fileformat
    filename, fileformat, local_file_dir, s3_file_dir = filepath_breaker(local_file_path)

    if not upload_only:
        # Do not show this message if in the end, this file will be removed.
        print('Saving localfile: ' + local_file_path + '... ', end='')
    if fileformat == '.json':
        fileformats = ['.json']
        with open(local_file_path, 'w') as fout:
            json.dump(obj, fout)
    elif fileformat == '.csv':
        fileformats = ['.csv']
        obj.to_csv(local_file_path, index=False, **kwargs)
    elif fileformat == '.geojson':
        fileformats = ['.geojson']
        obj.to_file(filename=local_file_path, driver='GeoJSON',  **kwargs)
    elif fileformat == '.shp':
        fileformats = ['.cpg', '.dbf', '.prj', '.shp', '.shx']
        obj.to_file(filename=local_file_path, driver='ESRI Shapefile',  **kwargs)
    elif fileformat == '.png':
        imageio.imwrite(uri=local_file_path, im=obj)
        fileformats = ['.png']
    elif fileformat == '.wld':
        with open(local_file_path, 'w+') as f:
            for i in obj:
                f.write(f'{i:.20f}\n')
        fileformats = ['.wld']
    else:
        raise Exception('Only csv, geojson, shp, png and wld formats are supported')

    if not upload_only:
        print('done')

    # Upload to S3
    for fileformat in fileformats:
        local_file_path = local_file_dir + filename + fileformat
        if fileformat == '.json':
            upload_object(bucket=bucket, local_file_path=local_file_path, json_obj=obj)
        else:
            upload_object(bucket=bucket, local_file_path=local_file_path)

        if upload_only:
            os.remove(local_file_path)
    out = True

    return out


def get_object(bucket: str = None,
               s3_file_path: str = None,
               local_file_path: str = None,
               profile_name: str = None):
    """
        Get a file from an S3 bucket to local

        Parameters
        ----------
        bucket: str. S3 bucket name to upload to.
        s3_file_path: str. S3 object path.
        local_file_path: str. Local path for storing file.
        profile_name: str. Profile AWS name.
    """
    s3 = boto3.resource('s3')

    try:
        if profile_name is not None:
            boto3.setup_default_session(profile_name=profile_name)
        s3.Bucket(bucket).download_file(s3_file_path, local_file_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print('The object does not exist.')
        else:
            raise

    return None


def get_csv(bucket: str = None,
            local_file_path: str = None,
            confidential: bool = False,
            force_s3: bool = False,
            profile_name: str = None,
            colnames_to_lower: bool = False,
            **kwargs):
    """
        Load a csv file from an S3 bucket to RAM.
        There are two methods to load a csv file:
        If confidential=True:
            We assume the csv can never be stored in disk and is stored into RAM directl from S3.
        If confidential=False:
            The csv will be stored first in disk and then read into RAM.
            First it tries to read directly from the localpath, in case the file was already stored.
            If the file does not exist or force_s3=True, then the csv file is dowloaded
            from S3 and then read from local.

        Parameters
        ----------
        bucket: str. S3 Bucket name to load from.
        local_file_path: Local path where csv is stored.
        confidential: If we assume the csv can be stored locally (False) or not (True).
        force_s3: force downloading file from s3 and overwrites localfile if exits.
        profile_name : str. AWS profile name.
        colnames_to_lower : bool. Specifies if column names need to be converted to lower.
        **kwargs: options for functions pd.get_csv(). For example, encoding=latin1
    """

    if '/data/' not in local_file_path:
        raise Exception('local_file_path=' + local_file_path + 'must contain "/data/"')

    # Read file fileformat
    filename, fileformat, _, s3_file_dir = filepath_breaker(local_file_path)

    if fileformat != '.csv':
        raise Exception('File fileformat invalid. Input must be a csv file.')

    if not confidential:
        # Tries to read from localfile first because it is faster.
        local_file_path_exists = path.exists(local_file_path)

        if force_s3 or not local_file_path_exists:
            # Downloads file from S3.
            s3_file_path = s3_file_dir + filename + fileformat
            print('Downloading ' + s3_file_path + ' from S3: ', end='')
            get_object(bucket=bucket, s3_file_path=s3_file_path, local_file_path=local_file_path)
            print('done')

        print('Reading localfile: ' + local_file_path + '... ', end='')
        out_df = pd.read_csv(local_file_path, **kwargs)
        print('done')

    else:
        if profile_name is not None:
            boto3.setup_default_session(profile_name=profile_name)

        s3 = boto3.resource('s3')
        # Load the file
        try:
            s3_file_path = s3_file_dir + filename + fileformat
            s3.Object(bucket, s3_file_path).load()
            bytes_obj = s3.Object(bucket, s3_file_path).get()['Body'].read().decode(**kwargs)
            out_df = pd.read_csv(io.StringIO(bytes_obj), **kwargs)

        except botocore.exceptions.ClientError:
            out_df = None

    if colnames_to_lower:
        out_df.columns = out_df.columns.str.lower()

    return out_df


def get_vector_map(local_file_path=None, bucket=None, crs=4326, force_s3=False):
    """
        Reads almost any vector-based spatial data format including ESRI shapefile (.shp) or  GeoJSON file.
        Then, transforms the geopandas to the Coordinate Reference System (CRS) given by crs.
        Returns a GeoDataFrame object.

        First tries to read from local_file_path, since its faster. Unless force_s3=True is specified.
        If local_file_path exits the GeoDataFrame object is returned. Otherwise, it downloads it from
        bucket under the same name and then reads it from local.

        Parameters
        ----------
        bucket: str.  S3 bucket name to upload to.
        local_file_path : str. Local path of a vector map file (shp or geojson).
        local_file_path : str. S3 path of a vector map file (shp or geojson).
        crs : int. The Coordinate Reference System (CRS) to read the file as. Default = 4326.
        force_s3: boolean. Forces download from s3 even if local file already exists. Overwrites localfile.
    """

    if '/data/' not in local_file_path:
        raise Exception('local_file_path=' + local_file_path + 'must contain "/data/"')

    # Read file fileformat
    filename, fileformat, local_file_dir, s3_file_dir = filepath_breaker(local_file_path)

    if fileformat == '.geojson':
        fileformats = ['.geojson']
    elif fileformat == '.shp':
        fileformats = ['.cpg', '.dbf', '.prj', '.shp', '.shx']
    else:
        raise Exception('File fileformat invalid. Must be geojson or shp')

    # Tries to ready from localfile first because it is faster.
    local_file_path_exists = path.exists(local_file_path)

    if force_s3 or not local_file_path_exists:
        for fileformat in fileformats:
            s3_file_path_iter = s3_file_dir + filename + fileformat
            local_file_path_iter = local_file_dir + filename + fileformat
            print('Downloading ' + s3_file_path_iter + ' from S3: ', end='')
            get_object(bucket=bucket, s3_file_path=s3_file_path_iter, local_file_path=local_file_path_iter)
            print('done')

    print('Reading localfile: ' + local_file_path + '... ', end='')
    vector_map = gpd.read_file(local_file_path)
    print('done')

    # CRS maps Python to places on the Earth.
    # For example, one of the most commonly used CRS is the WGS84 latitude-longitude projection.
    # This can be referred to using the authority code "EPSG:4326" or epsg=4326.
    vector_map = vector_map.to_crs(epsg=crs)

    return vector_map


def get_feather(bucket=None, key=None, profile_name=None, colnames_to_lower=False):
    """
        Load a feather file of an S3 bucket to RAM.

        Parameters
        ----------
        bucket: str. Bucket name to load from.
        key: str. S3 object name path.
        profile_name : str. AWS profile name.
        colnames_to_lower : bool. Specifies if column names need to be converted to lower.
    """

    if profile_name is not None:
        boto3.setup_default_session(profile_name=profile_name)

    s3 = boto3.resource('s3')

    try:
        s3.Object(bucket, key).load()
        bytes_obj = s3.Object(bucket, key).get()['Body'].read()
        feather = pd.read_feather(io.BytesIO(bytes_obj))

    except botocore.exceptions.ClientError:
        feather = None

    if colnames_to_lower:
        feather.columns = feather.columns.str.lower()

    return feather


def get_img(bucket=None, s3_file_path=None, local_file_path=None, rm=True, wld=True):
    """
        Load a gpd dataframe of an S3 bucket to RAM.

        Parameters
        ----------
        bucket: str. Bucket name to load from.
        s3_file_path: str. S3 object name path.
        local_file_path: str. Local path to save S3 Object.
        rm: boolean. If True removes local file after reading in RAM.
        wld: boolean. If True, downloads wld file associated to local.
    """
    try:
        s3_client.download_file(bucket, s3_file_path, local_file_path)
        img = (mpimg.imread(local_file_path) * 255).astype(np.uint8)
        img = img[:, :, :-1]
        img = Image.fromarray(img)  # Assumes range [1,255]
        if rm and os.path.exists(local_file_path):
            os.remove(local_file_path)

        if wld:
            local_file_path = local_file_path.replace('png', 'wld')
            s3_file_path = s3_file_path.replace('png', 'wld')
            s3_client.download_file(bucket, s3_file_path, local_file_path)
    except ClientError:
        raise Exception('Image not available')
    return img


def check_key(bucket=None, key=None, profile_name=None):
    """
    Checks if a file exists in an S3 bucket. Return True if exists and False if it does not.

    ----------
    Parameters
        bucket: str. Bucket name to load from.
        key: str. S3 object name path.
        profile_name : str. AWS profile name.
    """
    if profile_name is not None:
        boto3.setup_default_session(profile_name=profile_name)

    s3 = boto3.resource('s3')
    exists = True
    try:
        s3.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False  # The object does not exist.
        else:
            raise  # Something else has gone wrong.

    return exists


def filepath_breaker(local_file_path):
    """
        Breaks string of a local_file_path into different useful strings to save file in s3 or change fileformat.
        local_file_path: string. Relative path of where a local file is stored.
    """
    s3_file_path = local_file_path.split('/data/')[-1]
    filename_fileformat = local_file_path.split('/', local_file_path.count('/'))[-1]
    filename = filename_fileformat.split('.', filename_fileformat.count('.'))[0]
    fileformat = '.' + filename_fileformat.split('.', filename_fileformat.count('.'))[-1]
    local_file_dir = local_file_path.replace(filename_fileformat, '')
    s3_file_dir = s3_file_path.replace(filename_fileformat, '')
    return filename, fileformat, local_file_dir, s3_file_dir
