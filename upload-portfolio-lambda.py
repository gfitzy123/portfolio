import json
import boto3
from botocore.client import Config
import io
import sys
from io import BytesIO as StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:917733420865:deploy_portfolio_topic')
    try:
        portfolio_bucket = s3.Bucket('portfolio.garrettfitzgerald.com')
        build_bucket = s3.Bucket('portfoliobuild.garrettfitzgerald.com')

        portfolio_zip = StringIO()

        build_bucket.download_fileobj('build_portfolio.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print('Job done!')
        topic.publish(Subject="Portfolio Deploy Suceeded", Message="Job complete")
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="Job incomplete")
        raise
