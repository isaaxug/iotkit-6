import os
from dotenv import load_dotenv

load_dotenv()

DEVICE_NAME = os.environ.get("DEVICE_NAME")
AWS_ENDPOINT = os.environ.get("AWS_ENDPOINT")
AWS_ROOTCA = os.environ.get("AWS_ROOTCA")
AWS_KEY = os.environ.get("AWS_KEY")
AWS_CERT =os.environ.get("AWS_CERT")
