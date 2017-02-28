# 
#	recognition.py
#	Created by Dmitry Chulkov
#	This file provides set of functions that allow to detect faces on multiple images at one time,
#       add multiple faces to person and get name of person on image.
#

import Person
import PersonGroup
import Face
import serial
import os
import json
import requests
import time
import pyodbc
from sendgrid.helpers.mail import *
import smtplib



# this function addes faces to specified person in specified group.
# to do this you have to provide folder with images of person that you want to add,
# all images have to have only one face and this face have to be face of specified person.
# It's better to prepare special folder with such images and then proceed with this function.
def addFacesToPerson(folderWithImages, personID, personGroupID):

    files = os.listdir(folderWithImages)
    c=0
    for i in range(len(files)):

        if files[i] == '.DS_Store':
            continue
        c += 1

        img_addr = folderWithImages + files[i]

        print(img_addr)
        result = Person.addPersonFace(personGroupID, personID, img_addr)
        if "error" in result:
            print(json.dumps(result, indent=2))
        else:
            print("Added " + str(c) + " faces... ")
    print("Done adding faces!")
    return

# Function prints out json in readable format        
def printResJson(result):
    print(json.dumps(result, indent=2))
    return

# using module 'Face' and function 'detect' print out result of detecting faces on
# on images in specified directory
def detectFaceOnImages(path):
    files = os.listdir(path)
    for i in range(len(files)):
        img_addr = path + files[i]
        result = Face.detect(img_addr)
        print("*************")
        print("image: " + img_addr)
        printResJson(result)
    return


# params: path to image example\\example\\
def checkPerson(image, personGroupID):
    
    # detect face 
    result = Face.detect(image)
    if len(result) > 0 and 'faceId' in result[0]:
        data = Face.identify([result[0]['faceId']], personGroupID)
        # get person name
        
        if len(data[0]["candidates"]) > 0:
            persID = data[0]["candidates"][0]["personId"]
            res = Person.getPerson(personGroupID, persID)
            name = res["name"]
        else:
            name = "stranger"
        return name
    else:
        print("No face detected")
    return "noface"


ser = serial.Serial('/dev/ttyACM0', 9600)
dsn = 'rpitestsqlserverdatasource'
user = 'makeNTU050@makentu'
password = 'GGininder123'
database = 'make'
connString = 'DSN={0};UID={1};PWD={2};DATABASE={3};'.format(dsn,user,password,database)
conn = pyodbc.connect(connString)


cursor = conn.cursor()

while(1):

    fire = ser.readline()

    print(fire)
    fire = fire.decode("UTF-8")
    if fire != 'It works, why?\r\n':
        continue

    #a = input("input")

    print("Please look at the camera")
    img_file = open('test.jpg','wb')

    response = requests.get('http://192.168.2.215:8080/photoaf.jpg', stream=True)

    print("camera complete")
    total_length = response.headers.get('content-length')

    if total_length is None: # no content length header

                img_file.write(response.content)

    else:

        dl = 0
        total_length = int(total_length)

        for data in response.iter_content(chunk_size=4096):

            dl += len(data)
            img_file.write(data)
            pgs =  float(dl) / total_length
            done = int(20 * pgs)
            sys.stdout.write("\rDownloading... [%s%s] %.0f %% %s " % ('=' * done, ' ' * (20-done), 100 * pgs, file_name))
            sys.stdout.flush()

    img_file.close()

    image = 'test.jpg'
    name = (checkPerson(image, '000-000'))
    print(name)

    d = {}
    f = open("med.txt")
    
    for line in f:
        print(line)
        (key, val) = line.split()
        d[key] = int(val)

    f.close()

    f=open("med.txt", 'w')



    

    q = "SELECT med FROM makeNTU WHERE name ='" + name +"'"

    cursor.execute(q)

    tables = cursor.fetchall()

    print(tables)


    if len(tables) > 0:
        resp = tables[0]
        res = "hi " + name
        ser.write(bytes(resp[0], 'UTF-8'))
        print(res)
        

        if resp[0] == '0':
            d['A'] -=1

        if resp[0] == '1':
            d['B'] -=1

        if resp[0] == '2':
            d['A'] -=1
            d['B'] -=1

    else:

        res = "please register."
    

    send = 0

    for i in d:
        if d[i]<=3:
            send = 1

    for i in d:
        print(i)
        a = i + " "+str(d[i])+"\n"
        f.write(a)

    f.close()


    if send == 1:

        server = smtplib.SMTP('smtp.sendgrid.net')
        server.starttls()
        server.login("azure_cf73ba62b6d99c12217b5a52d1afae59@azure.com", "GGininder123")
         
        FROM = 'mzure_cf73ba62b6d99c12217b5a52d1afae59@azure.com'

        TO = ["b02507013@ntu.edu.tw"] # must be a list

        SUBJECT = "Time to buy medicine!"

        TEXT = """Your medicine is running out. Please follow the link to get some more!
        http://shopping.friday.tw/item/新升級善存_銀寶善存50綜合維他命錠禮盒-S07573081"""

        msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

        # msg = """\
        # From: %s
        # To: %s
        # Subject: %s

        # %s
        # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)


        server.sendmail(FROM, TO, msg.encode("utf8"))
        server.quit()


    while 1:
        if ser.inWaiting():
            r = ser.read() 
        else:
            break





