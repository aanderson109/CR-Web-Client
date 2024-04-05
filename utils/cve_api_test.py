'''
utility to test APIs prior to running web server
'''
import requests
import json

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
    keywords = input("enter one or more keywords separated by spaces: ").split()
    test_cve_api(keywords)