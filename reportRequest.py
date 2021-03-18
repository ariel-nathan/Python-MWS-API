import csv
import time
import os
from credentials import *
from reports import *
from datetime import date
from mws import Reports

today = date.today()

#Create a file (credentials.py) with the following variables and import it here
account_id = MWS_ACCOUNT_ID
access_key = MWS_ACCESS_KEY
secret_key = MWS_SECRET_KEY

reports_api = Reports(
    access_key = access_key,
    secret_key = secret_key,
    account_id = account_id
)

reports_api._use_feature_mwsresponse = True

#Dont need to touch any of this code
def requestReport(reportName):
    print("Requesting Report")
    reportRequest = reports_api.request_report(reportName)
    reportRequest = reportRequest.parsed
    reportRequestId = reportRequest.ReportRequestInfo.ReportRequestId
    print("Report Requested with Request ID: " + reportRequestId)
    getReportStatus(reportRequestId)

def getReportStatus(reportRequestId):
    print("Getting Report Status")
    reportList = reports_api.get_report_request_list(reportRequestId)
    reportList = reportList.parsed
    reportStatus = reportList.ReportRequestInfo.ReportProcessingStatus
    print(reportStatus)
    checkStatus(reportStatus, reportRequestId)

def checkStatus(reportStatus, reportRequestId):
    if reportStatus == "_DONE_":
        print("Report Status: Done")
        reportData = reports_api.get_report_list(reportRequestId)
        reportData = reportData.parsed
        reportId = reportData.ReportInfo.ReportId
        reportType = reportData.ReportInfo.ReportType
        print("Report ID: " + reportId)
        report = reports_api.get_report(reportId)
        report = report.parsed
        print("Report Retreived")
        writeFile(report, reportType)
    elif reportStatus == "_SUBMITTED_":
        print("Report Status: Submitted")
        print("Waiting a minute before next check")
        time.sleep(60)
        getReportStatus(reportRequestId)
    elif reportStatus == "_CANCELLED_":
        print("Report Status: Cancelled")
    elif reportStatus == "_DONE_NO_DATA_":
        print("Report Status: Done with no Data")

def writeFile(report, reportType):
    print("Writing File")
    txtName = "TemporaryFile.txt"
    csvName = reportType + str(today) + ".csv"

    with open(txtName, mode='w') as f:
        f.write(report)
    
    with open(txtName, "r") as in_text:
        in_reader = csv.reader(in_text, delimiter = '\t')
        with open(csvName, "w") as out_csv:
            out_writer = csv.writer(out_csv)
            for row in in_reader:
                out_writer.writerow(row)
    
    os.remove(txtName)

    print("Done")

#From the reports.py file enter the name for the report you would like to get into the requestReport function below
requestReport(FBA_INVENTORY_AFN)