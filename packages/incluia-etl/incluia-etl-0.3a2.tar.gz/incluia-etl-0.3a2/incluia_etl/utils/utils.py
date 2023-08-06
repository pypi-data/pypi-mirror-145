import boto3
import re
from shapely.wkt import loads

s3_client = boto3.client('s3')


def mround(match):
    """
    Rounds geometry column to 9 digits of precision instead the standard 14 digits.
    """
    out = "{:.9}".format(float(match.group()))
    return out


def reduce_precision_geom(x):
    """
    Rounds Geometry column precision to 9 digits.
    """
    simpledec = re.compile(r"\d*\.\d+")
    re_sub = re.sub(simpledec, mround, x.wkt)
    out = loads(re_sub)
    return out
