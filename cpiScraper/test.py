import requests
jahr=2023
cpiURL = f'https://www.transparency.de/fileadmin/Redaktion/Aktuelles/{jahr}/CPI{jahr-1}_Results.xlsx'
print(cpiURL)
r = requests.get(cpiURL)
# check if file exists
if r.status_code == 200:
    print('file exists')
else:
    print('file does not exist')
open('CPIs.xlsx', 'wb').write(r.content)