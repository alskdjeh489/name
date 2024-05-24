import requests
import json
import sqlite3


# API-ს მონაცემები
url = "https://api.fbi.gov/@wanted"


# Requests მოდულის ფუნქციები
response = requests.get(url)

print(response)
print(response.status_code)
print(response.headers)


# json ფორმატის მონაცემების json ფაილში შენახვა
print(json.dumps(response.json(), indent=4))

file = open('data.json', 'w')
json.dump(response.json(), file, indent=4)
file.close()


# json/dict ობიექტთან სამუშაო ფუნქციების მეშვეობით სასურველი ინფორმაციის დაბეჭდვა
data = response.json()

if response.status_code == 200:
    for item in data['items']:
        name = item['title']
        crimes = item['description']
        reward = item['reward_text']
        picture = item['images'][0]['original']
        print(f"Name: {name}\nCrimes: {crimes}\nReward: {reward}\nPicture URL: {picture}\n")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")


# სასურველი ინფორმაციის ბაზაში შენახვა
conn = sqlite3.connect('criminals.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS criminals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(100),
            Crime VARCHAR(100))
''')

for item in data['items']:
    name = item['title']
    crimes = item['description']
    c.execute("INSERT INTO criminals (Name, Crime) VALUES (?, ?)", (name, crimes))
    conn.commit()

conn.close()
