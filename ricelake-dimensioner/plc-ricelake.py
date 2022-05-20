from pylogix import PLC
import json
import requests
from argparse import ArgumentParser
import csv
from pprint import pprint

dimensioner_endpoint = "https://localhost:5001"

#package to send to Scanner Function
def send_packet(barcode):

    #create dictionary with Scanner Capture Information
    x = {
        "DimensionerName" : " ",
        "ProNumber" : barcode,
        "UserField1": " ",
        "UserField2": " ",
        "UserField3": " "
        }

    #create json equivalent of dictionary
    y = json.dumps(x)

    result = "POST /" + dimensioner_endpoint + "/Capture" + y

    return result

# Run Pyhton Code as long as PLC is running
with PLC("192.168.1.100") as comm:

    #Package at Scanner Variable
    information_sent = False

    while True:
        package_present = comm.Read("SendToRestAPI")
        read_request = comm.Read("Highlight_Produced.Barcode[0]")
        
        if package_present.Value:
            if information_sent == False:
                api_post = send_packet(read_request.Value)
                print(api_post)
                information_sent = True
        
        if information_sent:
            if package_present.Value == False:
                information_sent = False
