import logging

logging.basicConfig(level="DEBUG")

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

import boto3
import dropbox
import urllib3
import json

from .credentials import DROPBOX_TOKEN


def lambda_handler(event, context):
    logger.info(event)

    image_url = event["body"]
    image_filename = get_image_filename(image_url)

    # Get the image from Dropbox
    response = download_image(image_url)

    # Extract text
    text = extract_text(response)

    # Upload text to dropbox
    upload_text_to_dropbox(image_filename, text)

    return {"statusCode": 200, "body": json.dumps(text)}


def upload_text_to_dropbox(image_filename, text):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    dbx.files_upload(text.encode("utf-8"), f"/deutsch-letters/{image_filename}.txt")


def get_image_filename(url):
    return url[url.rfind("/") + 1 :]


def download_image(image_url):
    http = urllib3.PoolManager()
    response = http.request("GET", image_url)
    return response


def extract_text(response):
    textract = boto3.client("textract")
    doc = textract.detect_document_text(Document={"Bytes": response.data})
    lines = [block for block in doc["Blocks"] if block["BlockType"] == "LINE"]
    lines = [line for line in lines if line["Confidence"] < 90]
    texts = [line["Text"] for line in lines]
    text = "\n".join(texts)
    return text
