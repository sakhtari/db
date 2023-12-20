import socket
import xml.etree.ElementTree as ET

def process_xml_rpc_request(request, method_handlers):
    print(ET.tostring(request, 'utf-8'))
    method_name = request.find("methodName").text
    params_elem = request.find("params")
    params = []

    if params_elem is not None:
        for param in params_elem.findall("param"):
            value_elem = param.find("value")
            i4_elem = value_elem.find("i4")
            if i4_elem is not None:
                params.append(int(i4_elem.text))

    if method_name in method_handlers:
        result = method_handlers[method_name](*params)  # Pass parameters as arguments
        response = ET.Element("methodResponse")
        params_elem = ET.SubElement(response, "params")
        param_elem = ET.SubElement(params_elem, "param")
        value_elem = ET.SubElement(param_elem, "value")
        i4_elem = ET.SubElement(value_elem, "i4")
        i4_elem.text = str(result)
    else:
        response = ET.Element("methodResponse")
        fault_elem = ET.SubElement(response, "fault")
        value_elem = ET.SubElement(fault_elem, "value")
        i4_elem = ET.SubElement(value_elem, "i4")
        i4_elem.text = "1"  # This is a sample error code

    return response

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def main():
    host = '0.0.0.0'
    port = 8000

    method_handlers = {
        "add": add,
        "subtract": subtract,
    }

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))

        while True:
            data, client_address = server_socket.recvfrom(1024)
            try:
                request = ET.fromstring(data.decode())
                response = process_xml_rpc_request(request, method_handlers)
                server_socket.sendto(ET.tostring(response), client_address)
            except ET.ParseError:
                print("Invalid XML request received")

if __name__ == "__main__":
    main()