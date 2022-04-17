"""
39434 PLC to RiceLake Dimensioner Control
Created by: Kwesi Asare HLI
Date: April 15, 2022
"""

#imports
import json
from pylogix import PLC

with PLC() as comm:
    #PLC IP Address
    comm.IPAddress = '192.168.1.100'

    #set variables for package present at Scanner and Barcode Information from Stack
    package_present = comm.Read('Exit2ConvPackageIsCentered')       
    read_request = comm.Read('Highlight_Produced.Barcode[0]')

    #scanner, scan complete signal
    scan_complete = False

    #package to send to Scanner Function
    def send_packet(dimensionerName, proNumber, barcodeInfo, userField2 = "user value", userField3 = "user value" ):
        #create dictionary with Scanner Capture Information
        x = {
            "DimensionerName" : dimensionerName,
            "ProNumber" : proNumber,
            "Barcode Info": barcodeInfo,
            "UserField2": userField2,
            "UserField3": userField3
            }
        #create json equivalent of dictionary
        y = json.dumps(x)

        result = "POST /Capture" + y

        return result

    if package_present.Value:
        print(send_packet('Test', 'PRO368127368236', read_request.Value))

    if scan_complete:
        write_request = comm.Write('SignalFromScanner', scan_complete)
       
    else:
        write_request = comm.Write('SignalFromScanner', False)
        
