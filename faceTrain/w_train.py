import Person
import PersonGroup
import Face
import os
import json
import requests
import pyodbc
import time

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

name = input("please input your name")

newpath = './pic/'+name+'/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

path = newpath + 'train.jpg'

while 1:

    img_file = open(path,'wb')

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


    PersonGroup.create("MakeNTU", '000-000')
    PersonGroup.getPersonGroup('000-000')
    dic = Person.createPerson('000-000', name)
    addFacesToPerson(newpath, dic['personId'], '000-000')
    PersonGroup.trainPersonGroup('000-000')
    printResJson(PersonGroup.getPersonGroupTrainingStatus('000-000'))

    ans = input("continue training? y/n")
    if ans == 'n':
        break

dsn = 'rpitestsqlserverdatasource'
user = 'makeNTU050@makentu'
password = 'GGininder123'
database = 'make'
connString = 'DSN={0};UID={1};PWD={2};DATABASE={3};'.format(dsn,user,password,database)
conn = pyodbc.connect(connString)

time.sleep(2)
cursor = conn.cursor()

m = input("medicine type? 1/2/3")

cursor.execute("insert into makeNTU(name, med) values ('{0}', '{1}')".format(name,m))
cursor.commit()
cursor.execute("SELECT * FROM makeNTU")
tables = cursor.fetchall()
print(tables)




