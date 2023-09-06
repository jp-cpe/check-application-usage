#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

# Define your Jamf Pro API URL and token
api_url = "https://x.jamfcloud.com/JSSResource/"
api_token = "x"
application_name = "Docker.app"
date_range_days = 365  # 1 year

# Calculate the start date for the date range
end_date = datetime.now()
start_date = end_date - timedelta(days=date_range_days)

# Function to get a list of serial numbers for machines with a specific application
def get_serial_numbers():
    headers = {
        "Authorization": "Bearer {}".format(api_token),
        "Accept": "application/xml"
    }
    app_query_url = api_url + "computerapplications/application/{}".format(application_name)
    print(f"App query URL: {app_query_url}")
    response = requests.get(app_query_url, headers=headers)

    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.content)
        serial_numbers_set = set()  # Use a set to store unique serial numbers
        for computer in root.findall(".//computer"):
            serial_number = computer.find("serial_number").text
            serial_numbers_set.add(serial_number)  # Add serial number to the set
        return list(serial_numbers_set)  # Convert set back to a list
    else:
        raise Exception(response.status_code)

# Function to get application usage for a serial number within a date range
def get_application_usage(serial_number):
    headers = {
        "Authorization": "Bearer {}".format(api_token),
        "Accept": "application/xml"
    }
    usage_query_url = api_url + "computerapplicationusage/serialnumber/{}/{}_{}".format(serial_number, start_date.date(), end_date.date())
    response = requests.get(usage_query_url, headers=headers)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        usage_data_list = []  # Create a list to store all usage data records for the serial number
        for usage in root.findall(".//usage"):
            date = usage.find("date").text
            apps = usage.find("apps")
            for app in apps.findall("app"):
                app_name = app.find("name").text
                if app_name == application_name:
                    # Extract the usage data for the specified application
                    usage_data = {
                        "date": date,
                        "name": app_name,
                        "serial": serial_number,
                        "version": app.find("version").text,
                        "foreground": int(app.find("foreground").text),
                        "open": int(app.find("open").text)
                    }
                    usage_data_list.append(usage_data)  # Append usage data to the list

        if usage_data_list:  # Check if there is any usage data
            return usage_data_list  # Return the list of usage data records
        else:
            error_message = "No usage data found for serial number {} and the application {} over the last {} days.".format(serial_number, application_name, date_range_days)
            return {"error": error_message}

    # If there is no usage data, return an empty list
    return []

# Main function
def main():
    try:
        print("Finding usage data for '{}' over the last {} days ({} - {})".format(application_name, date_range_days, start_date.date(), end_date.date()))
        serial_numbers = get_serial_numbers()
        serial_numbers_with_usage = []  # List to store serial numbers with usage data
        for serial_number in serial_numbers:
            usage_data = get_application_usage(serial_number)
            if "error" in usage_data:
                print(usage_data["error"])  # Print the error message
            else:
                serial_numbers_with_usage.append(serial_number)
                print(json.dumps(usage_data, indent=2))
                print("=" * 50)

        # Count machines with 'X.app' installed and no usage data
        serial_numbers_with_no_usage = list(set(serial_numbers) - set(serial_numbers_with_usage))
        
        print("Number of machines with '{}' installed: {}".format(application_name, len(serial_numbers)))
        print("Serial numbers with '{}' installed and usage data ({} machines):".format(application_name, len(serial_numbers_with_usage)))
        print(serial_numbers_with_usage)
        print("Serial numbers with '{}' installed but no usage data ({} machines):".format(application_name, len(serial_numbers_with_no_usage)))
        print(serial_numbers_with_no_usage)

    except Exception as e:
        print("Error: {}".format(str(e)))

if __name__ == "__main__":
    main()
