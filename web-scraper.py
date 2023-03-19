import requests
from bs4 import BeautifulSoup
import csv
import time

# Define the base URL and parameters for pagination
base_url = 'https://www.nike.com/ca/' 
params = {'page': 1}

# Create a session object to improve performance
session = requests.Session()

# Create a CSV file to store the scraped data
with open('data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Title', 'Description', 'Price'])

    # Loop through each page of search results
    while True:
        try:
            # Send a GET request to the URL and store the response
            response = session.get(base_url, params=params)

            # Use BeautifulSoup to parse the HTML content of the response
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the products on the page
            products = soup.find_all('div', {'class': 'product'})

            # If there are no more products, break out of the loop
            if not products:
                break

            # Extract the data from each product using list comprehension
            data = [[product.find('h2').text.strip(),
                     product.find('p', {'class': 'description'}).text.strip(),
                     product.find('span', {'class': 'price'}).text.strip()]
                    for product in products]

            # Write the data to the CSV file
            writer.writerows(data)

            # Increment the page number and update the URL parameters
            params['page'] += 1

            # Add a delay to simulate human-like behavior and avoid getting blocked
            time.sleep(1)

        except requests.exceptions.ConnectionError:
            # Retry the request up to three times if there is a connection error
            print('Connection error occurred. Retrying...')
            for i in range(3):
                time.sleep(2)
                response = session.get(base_url, params=params)
                if response.status_code == 200:
                    break
            else:
                print('Failed to connect after three attempts. Aborting...')
                break

        except Exception as e:
            print('An error occurred:', e)
            break

# Print a message indicating that the scraping is complete
print('Scraping complete.')
