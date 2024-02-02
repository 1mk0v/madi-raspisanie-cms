import os 
from dotenv import load_dotenv
load_dotenv()

DB_SCHEDULE_NAME = os.getenv('DB_SCHEDULE_NAME')
DB_SCHEDULE_USER = os.getenv('DB_SCHEDULE_USER')
DB_SCHEDULE_PASSWORD = os.getenv('DB_SCHEDULE_PASSWORD')
DB_SCHEDULE_HOST = os.getenv('DB_SCHEDULE_HOST')

DB_CMS_NAME = os.getenv('DB_CMS_NAME')
DB_CMS_USER = os.getenv('DB_CMS_USER')
DB_CMS_PASSWORD = os.getenv('DB_CMS_PASSWORD')
DB_CMS_HOST = os.getenv('DB_CMS_HOST')