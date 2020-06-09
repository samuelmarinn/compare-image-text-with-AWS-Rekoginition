import boto3
import logging
from datetime import datetime

def rec_text(bucket, photo):
    detected_text_97=""
    client = boto3.client(
        'rekognition',
        aws_access_key_id="ASIAUR5KFQ47YIQJ2FGL",
        aws_secret_access_key="SJ/QfECoh9NBRuy1HNGXpF5ZqdTB9OnDciyd8PfJ",
        aws_session_token="FwoGZXIvYXdzEKX//////////wEaDEmtOzYVN346y1qSPCLKAX6fxHiEt/J6XCfLgIiJrY0/C31Xdx+wBwChWVoOGZplac4s1+D7Ikm9VeAjB+sN3P0Y4PY"+
        "lL7TOwW84DOTQWV+17/sNmRmcm1qIPTd1itOTcx+WI7eMDWL4KbEB09qVQCeGSItSVlSkFA+tIemi4FwC3dNolNeSfzlsT/UeFMXj"+
        "OejvgqfrnFobT51aAm2/vq9E0uJdcMKcx4Amqrh1LHsYbDp/0g83mCku3Y1GaldN7xEZLY2e2bduKMvp88lxB+6vdEo8FEEsGwEomoT89gUyLTEySxs/EXiEt7fWOTMK96lZja6nPojulejnOj0IWfCSnrpi17PXGkHtXopUOQ=="
    )
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    textDetections=response['TextDetections']
    for text in textDetections:
            if (text["Type"]=="WORD" or text["Confidence"]<97):
                continue
            t=text["DetectedText"].lower()
            detected_text_97= detected_text_97 + " " + t
    return detected_text_97
            

def comp_text(control,image):
    #función con la que se compara en si los textos
    LOG_FILENAME = "rec.log"
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)  
    logging.info(str(datetime.now())+' Program started with control image: '+ control)
    logging.info(str(datetime.now())+' Program started with image: '+ image)
    #se obtienen ambos textos
    control_text=rec_text("recc1",control)
    logging.info(str(datetime.now())+" Program recognized the following phrase in control image: " + control_text)
    test_text=rec_text("recc1",image)
    if (control_text.find(test_text)==-1):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)  
        logging.info(str(datetime.now())+"The program ended with FALSE\n")
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
