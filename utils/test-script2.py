'''
utility to test APIs prior to running web server
'''
import requests
import json
import pandas as pd

def query_nvd_api(keywords):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {"keywordSearch": " ".join(keywords)}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response into a Python dictionary
        #data = response.json()
        with open(response.json, 'r') as file:
            data = json.load(file)
            print(data)
        #print(json.dumps(data, indent=1, sort_keys=True))

        # Access specific fields in the parsed data
        #cves = data.get("vulnerabilities", {})

        # Iterate over CVEs and print relevant information
        #for cve in cves:
         #   cve_id = cve.get("cve", {}).get("CVE_data_meta", {}).get("ID")
          #  print(f"CVE ID: {cve_id}")

    except requests.exceptions.RequestException as e:
        print("Error:", e)


# Your existing test script below
# Replace this with your actual test script
# Make sure to adjust the function call and parameters according to your needs
# test_function()


def test_cve_api(keywords):
    # base URL link for CVE API from nvd.nist.gov
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?"
    # Join multiple keywords with spaces and encode them
    keyword_search = "%20".join(keywords)
    params = {"keywordSearch": keyword_search}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "result" in data:
            cves = data["result"]["CVE_Items"]
            if cves:
                print("CVEs found:")
                for cve in cves:
                    cve_id = cve["cve"]["CVE_data_meta"]["ID"]
                    description = cve["cve"]["description"]["description_data"][0]["value"]
                    print(f"- {cve_id}: {description}")
            else:
                print("no CVEs found.")
        else:
            print("No results returned")
    else:
        print(f"API request failed with status code {response.status_code}.")

if __name__ == "__main__":
    #keywords = input("enter one or more keywords separated by spaces: ").split()
    #test_cve_api(keywords)
    keywords = ["PowerShell 7.3"]
    query_nvd_api(keywords)