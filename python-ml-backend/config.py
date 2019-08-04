import os
dir_path = os.path.dirname(os.path.realpath(__file__))


#directory
UPLOAD_FOLDER=os.path.join(dir_path,"files")
RESULT_FOLDER=os.path.join(dir_path,"result")
TEMP_FOLDER=os.path.join(dir_path,"temp")
HDFS_FOLDER=os.path.join(dir_path,"hdfs")
LOGS_FOLDER = os.path.join(dir_path,"logs")


#address
HOST="localhost"
PORT=8011
PORT_ROUTE2=8012


#database
database_name="table_detect_backend.db"
database_path=os.path.join(dir_path,"database")


#modelurl
TABLE_URL="http://192.168.39.48:5001/api/fasterrcnn/predict/"
# COLUMN_URL="http://127.0.0.1:5002/api/fasterrcnn/predict/"
# HEADER_URL="http://127.0.0.1:5003/api/fasterrcnn/predict/"

#CONF
CONF=0.8

#LANGUAGE

LANGUAGE='eng'




os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(dir_path,"My First Project-3eb73e25ebf7.json")

CORENLP_SERVER_URL = 'http://localhost'
POST_URL = "http://134.209.155.59:3000/order"
path_to_rules_file = os.path.join(dir_path,"custom.rules")
