import requests
resp = requests.post('https://textbelt.com/text', {
  'phone': '6287744450511',
  'message': 'Hello world',
  'key': 'c595425565ff8a957295f8feaeafd1ffc2648123hClU6iRRkD68P0mFYx6MGb6eY',
})
print(resp.json())