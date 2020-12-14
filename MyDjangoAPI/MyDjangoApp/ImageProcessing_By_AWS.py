import boto3
import cv2
import requests


def ObjectDetection(imagePath, Service):
    session = boto3.Session(profile_name="default")
    Service = session.client("rekognition")
    image = open(imagePath, "rb").read()
    imgW, imgH = cv2.imread(imagePath).shape[:2]
    MyImage = cv2.imread(imagePath)
    response = Service.detect_labels(Image={"Bytes": image})
    for objects in response["Labels"]:
        if objects["Instances"]:
            ObjectName = objects["Name"]
            for boxs in objects["Instances"]:
                box = boxs["BoundingBox"]
                x = int(imgW * box["Left"])
                y = int(imgH * box["Top"])
                w = int(imgW * box["Width"])
                h = int(imgH * box["Height"])
                MyImage = cv2.rectangle(MyImage, (x, y), (x+w, y+h), (0, 255, 0), 2)
                MyImage = cv2.putText(MyImage, ObjectName, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    cv2.imwrite("detected.jpg", MyImage)
    while True:
        cv2.imshow("Detected Image", MyImage)
        if cv2.waitKey(1) == ord("q"):
            break


image = "image5.jpg"
ObjectDetection(image, "Object Detection")
