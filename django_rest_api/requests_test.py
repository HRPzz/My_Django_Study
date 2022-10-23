import requests


auth_url = 'http://127.0.0.1:8000/api/auth'

auth_response = requests.post(auth_url, data={'username': 'admin', 'password': 'admin'})
print(auth_response.text)  # {"token": "토큰"}

token = auth_response.json().get('token', '')
header = {'Authorization': f'Token {token}'}
url = 'http://127.0.0.1:8000/api/student_list'

response = requests.get(url, headers=header)
print(response.text)  # [{"id":1,"student_id":"1","name":"홍길동","age":"33"},{"id":2,"student_id":"2","name":"독도","age":"28"}]
