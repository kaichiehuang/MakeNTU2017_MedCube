import Person
import PersonGroup
import Face

import os
import json
import requests

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


#PersonGroup.create("MakeNTU", '000-000')

PersonGroup.getPersonGroup('000-000')
dic = Person.createPerson('000-000', 'ggininder')
addFacesToPerson('./pic/ggininder/', dic['personId'], '000-000')
PersonGroup.trainPersonGroup('000-000')
printResJson(PersonGroup.getPersonGroupTrainingStatus('000-000'))





