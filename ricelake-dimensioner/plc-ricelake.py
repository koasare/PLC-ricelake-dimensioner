from pylogix import PLC
import json
import requests
from requests.structures import CaseInsensitiveDict
from argparse import ArgumentParser
import csv
from pprint import pprint

dimensioner_endpoint = "https://localhost:5001"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"

#package to send to Scanner Function
def send_packet(barcode):

    #create dictionary with Scanner Capture Information
    data = """
    {
        "DimensionerName" : " ",
        "ProNumber" : barcode,
        "UserField1": " ",
        "UserField2": " ",
        "UserField3": " "
     }
     """

    result = requests.post(dimensioner_endpoint, headers=headers, data=data)

    return result

# Run Pyhton Code as long as PLC is running
with PLC("192.168.1.100") as comm:

    #Package at Scanner Variable
    information_sent = False

    while True:
        package_present = comm.Read("SendToRestAPI")
        
        if package_present.Value:
            if information_sent == False:
                read_request = comm.Read("Highlight_Produced.Barcode[0]")
                api_post = send_packet(read_request.Value)
                print(api_post.status_code)
                information_sent = True
        
        if information_sent:
            if package_present.Value == False:
                information_sent = False
