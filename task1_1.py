import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                         'Safari/537.36'}
username = input("Enter the github username:")
j_data = requests.get('https://api.github.com/users/' + username + '/repos', headers=headers).json()
f_data = []
for i in range(0, len(j_data)):
    f_data.append({})
    print("Project Number:", i + 1)
    f_data[i]['Project Number'] = i + 1
    print("Project Name:", j_data[i]['name'])
    f_data[i]['Project Name'] = j_data[i]['name']
    print("Project URL:", j_data[i]['svn_url'], "\n")
    f_data[i]['Project URL'] = j_data[i]['svn_url']
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(f_data, f, ensure_ascii=False, indent=4)
