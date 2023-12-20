import xmlrpc.client
import time



server_url = 'http://localhost:8080/web2_xmlrpc'  # Replace with your server URL
client = xmlrpc.client.ServerProxy(server_url)

result = client.set_count("<h3>hello</h3>")
print(result)
