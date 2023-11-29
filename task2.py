import requests
import getpass as gp


entered_username = input("Enter your username: ")
entered_password = gp.getpass("Enter your password: ")

if entered_username != "tuhin" or entered_password != "12345":
    print("Authentication failed. Exiting.")
    exit(1)
hebe_api_url = "http://192.168.50.211:8000/api/demo"
entered_id = input("Enter User ID: ")

# Ensure the ID is properly encoded (e.g., in case of spaces or special characters)
entered_id = requests.utils.quote(entered_id)

# Concatenate the URL components properly
url = f"{hebe_api_url}/{entered_id}"  # Assuming the ID is used as part of the URL path
print(url)
response = requests.get(url)

if response.status_code == 200:
    user_data = response.json()
    print(user_data)
else:
    print(f"Failed to fetch user data. Status code: {response.status_code}")
