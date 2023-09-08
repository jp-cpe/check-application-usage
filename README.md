# check-application-usage
Query the Jamf API for application usage of specific apps within a date range.

## Purpose
This Python script is designed to interact with the Jamf Pro API to analyze application usage data for a specific application over a specified date range. It retrieves the list of machines with the application installed and provides usage statistics, including foreground time and the number of times the application was opened.

This can be useful if you are trying to determine whether a specific application is installed in your environment and whether or not it is being actively used. **Example:** You need to find out whether Microsoft Edge is installed and how many people are actively using it.

## Prerequisites
Before using this script, ensure you have the following prerequisites in place:

- Python 3 installed on your system.
- Access to the Jamf Pro API with appropriate credentials (**NOTE:** See the "Notes" section below for more information regarding the permissions needed and other considerations for authentication to the Jamf API.)
- The `requests` library installed. You can install it using pip: 'pip install requests'

## Usage
Follow these steps to use the script:

1. Clone or download this repository to your local machine.

2. Open the script file (`check_application_usage.py`) in a text editor.

3. Update the following variables with your Jamf Pro API information:

- `api_url`: Your Jamf Pro API URL (e.g., "https://x.jamfcloud.com/JSSResource/").
- `api_token`: Your Jamf Pro API token (See **Notes** below for more information).
- `application_name`: The name of the application you want to analyze (e.g., "Google Chrome.app").
- `date_range_days`: The number of days you want to analyze (e.g., 365 for 1 year).

4. Save the changes to the script file.

5. Open a terminal or command prompt and navigate to the directory containing the script.

6. Run the script using the following command: 'python check_application_usage'

7. The script will retrieve and display usage data for the specified application over the specified date range.

## Output
The script will provide the following output:

- List of machines with the specified application installed.
- Usage statistics for each machine, including date, application version, foreground time, and the number of times the application was opened.
- Number of machines with the application installed.
- Serial numbers of machines with the application installed and usage data.
- Serial numbers of machines with the application installed but no usage data.

## Example Output
```
Finding usage data for 'Docker.app' over the last 365 days (2022-09-06 - 2023-09-06)
App query URL: https://x.jamfcloud.com/JSSResource/computerapplications/application/Docker.app
No usage data found for serial number XXXXXXXXXX and the application Docker.app over the last 365 days.
No usage data found for serial number XXXXXXXXXY and the application Docker.app over the last 365 days.
[
  {
    "date": "2023/08/16",
    "name": "Docker.app",
    "serial": "XXXXXXXXXZ",
    "version": "4.16.2",
    "foreground": 1,
    "open": 0
  },
  {
    "date": "2023/08/08",
    "name": "Docker.app",
    "serial": "XXXXXXXXXZ",
    "version": "4.16.2",
    "foreground": 1,
    "open": 0
  }
]
==================================================
[
  {
    "date": "2023/07/05",
    "name": "Docker.app",
    "serial": "XXXXXXXXXV",
    "version": "4.20.1",
    "foreground": 1,
    "open": 0
  }
]
==================================================
Number of machines with 'Docker.app' installed: 4
Serial numbers with 'Docker.app' installed and usage data (2 machines):
['XXXXXXXXXZ', 'XXXXXXXXXV']
Serial numbers with 'Docker.app' installed but no usage data (2 machines):
['XXXXXXXXXX', 'XXXXXXXXXY']
```

## Note
- Ensure that your Jamf Pro API token has the necessary permissions to access the required endpoints on the Jamf Classic API ("/computerapplications" and "/computerapplicationusage").
- The privileges required for these endpoints are "Read Advanced Computer Searches" and "Read Computers". 
- The "better" way to authenticate would be to use a function that creates a Bearer Token using Client Credentials (stored as environment variables) that are given only the permissions required to perform the above actions. I have not yet written such a function, but will likely include it at a later date and/or include it in future scripts. For my use at the time it made more sense to just generate a Bearer Token in Postman by running a POST to "/api/v1/auth/token" using Basic Authentication and then paste the token value into the script.
- For what it's worth (and I'll continue to explore this and maybe make a blog post about it), you can create API Roles, Clients, and Client Credentials using the Jamf Pro API in addition to the Jamf Pro GUI. I'll add this information in the section "Create API Roles/Clients/Credentials via the Jamf API" below.

## Create API Roles/Clients/Credentials via the Jamf API
Replace {yourJamfURL} in the links below with your actual Jamf Pro URL to test these calls for yourself.

1. Create API role via a POST of raw JSON to the "/v1/api-roles" endpoint using a "Content-Type" header of "application/json" (https://{yourJamfURL}.com/api/doc/#/api-roles/postCreateApiRole)
		
		{
		  "displayName": "<string>",
		  "privileges": [
		    "<string>",
		    "<string>"
		  ]
		}
		
2. Create API Integration (Client) via a POST of raw JSON to the "/v1/api-integrations" endpoint using a "Content-Type" header of "application/json" (https://{yourJamfURL}.com/api/doc/#/api-integrations/postCreateApiIntegration)
		
		{
		  "authorizationScopes": [
		    "<string>: the roles you want associated"
		  ],
		  "displayName": "<string>: the name you want",
		  "enabled": "<boolean>",
		  "accessTokenLifetimeSeconds": "<integer>"
		}
		
3. Create client credentials for the API Integration via a POST to "/v1/api-integrations/{id}/client-credentials" (https://{yourJamfURL}.com/api/doc/#/api-integrations/postCreateClientCredentials)


