import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                         'Safari/537.36'}
username = input("Enter the github username: ")
j_data = requests.get('https://api.github.com/users/' + username + '/repos', headers=headers).json()
for i in range(0, len(j_data)):
    print("Project Number:", i + 1)
    print("Project Name:", j_data[i]['name'])
    print("Project URL:", j_data[i]['svn_url'], "\n")
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(j_data, f, ensure_ascii=False, indent=4)
