import boto3
from botocore.client import Config
import io
import sys
from io import BytesIO as StringIO
import zipfile

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

portfolio_bucket = s3.Bucket('portfolio.garrettfitzgerald.com')
build_bucket = s3.Bucket('portfoliobuild.garrettfitzgerald.com')

portfolio_zip = StringIO()

build_bucket.download_fileobj('build_portfolio.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm)
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')