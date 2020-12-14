import boto3
import cv2
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from MyDjangoApp.models import MyFiles


# Create your views here.


def ObjectDetection(imagePath):
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
                MyImage = cv2.rectangle(MyImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
                MyImage = cv2.putText(MyImage, ObjectName, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    cv2.imwrite(imagePath, MyImage)

    return "Its Done.."


def CelebrityDetection(imagePath):
    session = boto3.Session(profile_name="abhivsp")
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
                MyImage = cv2.rectangle(MyImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
                MyImage = cv2.putText(MyImage, ObjectName, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    cv2.imwrite(imagePath, MyImage)

    return "Its Done.."


class FileSer(ModelSerializer):
    class Meta:
        model = MyFiles
        fields = "__all__"


@api_view(["GET", "POST"])
@renderer_classes([JSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def Home(request):
    if request.method == "POST":
        service = request.POST["service"]
        print(service)
        Ser = FileSer(data=request.data)
        print(Ser)
        url = "http://127.0.0.1:8000"
        Msg = {"Url": url}
        return Response(data=Msg, status=status.HTTP_200_OK)
    return render(request, "index.html")
