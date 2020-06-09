import boto3
import logging
import re
from datetime import datetime

def rec_text(bucket, photo,comp):
    detected_text_97=""
    client = boto3.client(
        'rekognition',
        aws_access_key_id="ASIAUR5KFQ47WNHNMSPD",
        aws_secret_access_key="ncBCxm6vj0c+tIQDk/RGZdoqHOYX7fOMWjH49QUy",
        aws_session_token="FwoGZXIvYXdzELT//////////wEaDKKH7bGpNua+cd2ksCLKAe+neLPAZKX5HTfQDwiX+w2spDGBJjozf3C/+qSK5zHC5R6nFZz5pC/xIALpY4YfVFJsr8i8t9vtAaIJLa/wvBX/ePUQjz1vzG4q5Gs+9a70vSU0Z0N6rxGnVKTqA610HR12mTC+5VYVDRyHM5wZ/F60pgA33ZUOxx1rpO7avDWs6MroAZCHerDIXhocSg88xcluZjdtHlJK52lx3Nz3byfRarNaEYeUPgG/iMYUhlBj+K2pF0TrMltcQJ0Dh1Oj8Y/blEpLCjJ/Q6kohbn/9gUyLTltumDgltp1+R4LVF5RYHysLaalUh3HcfUM6NL+mBe+jMASzfMFkq0+RO1RbA=="
    )
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    textDetections=response['TextDetections']
    for text in textDetections:
            if (text["Type"]=="WORD"):
                continue
            elif (text["Confidence"]<97 and comp== ""):
                continue
            elif (text["Confidence"]<97 and comp.find(text["DetectedText"].lower())==-1):
                continue
            t=text["DetectedText"].lower()
            detected_text_97= detected_text_97 + " " + t
    det = re.sub('[^a-zA-Z0-9 \n\.]', '', detected_text_97)
    return det
            

def comp_text(control,image):
    #función con la que se compara en si los textos
    LOG_FILENAME = "rec.log"
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)  
    logging.info(str(datetime.now())+' Program started with control image: '+ control)
    logging.info(str(datetime.now())+' Program started with image: '+ image)
    #se obtienen ambos textos
    control_text=rec_text("recc1",control,"")
    logging.info(str(datetime.now())+" Program recognized the following phrase in control image: " + control_text)
    test_text=rec_text("recc1",image,control_text)
    logging.info(str(datetime.now())+" Program recognized the following phrase in test image: " + test_text)
    if (control_text.find(test_text)==-1 or test_text == ""):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)  
        logging.info(str(datetime.now())+"The program ended with FALSE\n")
        logging.info("-----------------------------------------------------------------------------")
        return False
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)  
    logging.info(str(datetime.now()) + " Program ended with TRUE")
    logging.info("-----------------------------------------------------------------------------")
    return True

c = input("Enter name of control image: ")
#se trabaja con bucket igual a recc1
g = input("Enter name of test image(insert end to finish): ")
while (g !="end"):
    print ("¿Has the file " + g +  " all control text? " +str(comp_text(c,g)))
    g = input("Enter name of test image(insert end to finish): ")
