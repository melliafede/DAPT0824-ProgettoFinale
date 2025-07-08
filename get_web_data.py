import requests
from bs4 import BeautifulSoup
import certifi

url = "https://www.tennisabstract.com/cgi-bin/leaders.cgi"

response = requests.get(url, verify=certifi.where())
print(response.text)

# # Check for successful response
# if response.status_code == 200:
#     # Parse the HTML content
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # Example: Extract all headings
#     for heading in soup.find_all('h1'):
#         print(heading.text.strip())
# else:
#     print("Failed to retrieve the page:", response.status_code)