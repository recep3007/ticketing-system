import requests

# Define the URL of your Flask API
# For local testing:
# url = 'http://localhost:5000/tickets'

# For testing on Heroku (replace this with your Heroku URL):
url = 'https://floating-waters-42432-0ca470912980.herokuapp.com/tickets'

# Make a GET request to fetch tickets from the Flask API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()  # Parse the response JSON
    print("API Response:", data)  # Print the response data
else:
    print(f"Error: {response.status_code}")  # If not successful, print the error
