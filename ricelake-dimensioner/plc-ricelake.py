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

    result = "POST /" + dimensioner_endpoint + "Capture" + y

    return result
# Run Pyhton Code as long as PLC is running
with PLC("192.168.1.100") as comm:

    #Package at Scanner Variable
    package_present = comm.Read("SendToRestAPI")
    information_sent = False

    while True:

        
#         #if package at scanner
#         if package_present.Value:

          #read barcode scanner information
          read_request = comm.Read("Highlight_Produced.Barcode[0]")
            
          #create API string and store in variable
          api_post = send_packet(read_request.Value)
            
          #Send API command to Scanner
          print(api_post)
            
#         else:
#             print(package_present.Value)
#             continue
