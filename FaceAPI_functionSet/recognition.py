# 
#	recognition.py
#	Created by Dmitry Chulkov
#	This file provides set of functions that allow to detect faces on multiple images at one time,
#       add multiple faces to person and get name of person on image.
#

import Person
import PersonGroup
import Face

import os
import json
import requests

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

## training ##

# addFacesToPerson('pic/', 'd32428c2-59d7-40f9-a0eb-3522a07d732d', 'fff-111')
# PersonGroup.trainPersonGroup('fff-111')
# PersonGroup.getPersonGroupTrainingStatus('fff-111')

## training ##
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
print(checkPerson(image, '000-000'))


