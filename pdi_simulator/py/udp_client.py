import socket
import xml.etree.ElementTree as ET

def create_xml_rpc_request(method, params):
    request = ET.Element("methodCall")
    method_name = ET.SubElement(request, "methodName")
    method_name.text = method

    params_elem = ET.SubElement(request, "params")

    for param in params:
        param_elem = ET.SubElement(params_elem, "param")
        value_elem = ET.SubElement(param_elem, "value")
        i4_elem = ET.SubElement(value_elem, "i4")
        i4_elem.text = str(param)

    return ET.tostring(request)

def main():
    server_address = ('127.0.0.1', 8000)

    method = "add"
    params = [3, 4]
    request_data = create_xml_rpc_request(method, params)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(request_data, server_address)

        response_data, _ = client_socket.recvfrom(1024)
        response = ET.fromstring(response_data.decode())

        # Parse the response and handle it as needed
        result = response.find("params").find("param").find("value").find("i4").text
        result = ET.tostring(response, 'UTF-8')
        print("Result:", result)

if __name__ == "__main__":
    main()
