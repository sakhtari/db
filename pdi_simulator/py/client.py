import xmlrpc.client

# Read XML data from a file
def read_xml_from_file(file_path):
    with open(file_path, "r") as file:
        xml_data = file.read()
    return xml_data

layout_xml = read_xml_from_file("layout_408.xml")
content_xml = read_xml_from_file("content_408.xml")

server_url = 'http://172.21.0.3:5003'  # Replace with your server URL
client = xmlrpc.client.ServerProxy(server_url)

result = client.SetLayoutDefinition(layout_xml)  # Replace with your method and parameters
result = client.ShowLayout(content_xml)  # Replace with your method and parameters

print(result)
