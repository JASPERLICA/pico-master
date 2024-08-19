Content = b'GET /account?ssid_n=12345&password_n=5678 HTTP/1.1\r\n
Host: 192.168.4.1\r\nConnection: keep-alive\r\n
Upgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.111 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/setting?\r\nAccept-Language: en-CA,en-US;q=0.9,en;q=0.8\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
Request: b'/account?ssid_n=12345&password_n=5678'


Content = b'POST /account HTTP/1.1\r\n
Host: 192.168.4.1\r\n
Origin: http://192.168.4.1\r\nContent-Type: application/x-www-form-urlencoded\r\n
Accept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.111 Mobile/15E148 Safari/604.1\r\n
Referer: http://192.168.4.1/setting?\r\nContent-Length: 45\r\nAccept-Language: en-CA,en-US;q=0.9,en;q=0.8\r\n\r\n
ssid=1234&password_1=567890&password_2=567890'