import requests

def test_chat():
    url = 'http://localhost:5000/api/chat'
    data = {
        'message': '你好，我想讨论一下我的研究方向'
    }
    response = requests.post(url, data=data)
    print(response.status_code)
    print(response.json())

if __name__ == '__main__':
    test_chat() 