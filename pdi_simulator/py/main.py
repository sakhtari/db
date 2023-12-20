import xml.etree.ElementTree as ET
from flask import Flask, render_template, Response

import xmlrpc.server
from xmlrpc.server import SimpleXMLRPCServer
import threading
import time


app = Flask(__name__)

layout_xml = ""
content_xml = ""
sse_flag = False

# Define functions that you want to expose via XML-RPC
def SetLayoutDefinition(data):
    print('SetLayoutDefinition')

    global layout_xml, sse_flag
    layout_xml = data
    sse_flag = True
    r = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> <methodResponse> <params> <param> <value> <struct> <member> <name>ErrorCode</name> <value> <i4> 0</i4> </value> </member> </struct> </value> </param> </params> </methodResponse>"
    #sse_request()
    return r

def ShowLayout(data):
    print('SetLayoutContent')
    global content_xml, sse_flag
    content_xml = data
    sse_flag = True
    #sse_request()
    return "SetLayoutContent executed"

class LayoutDefinition:
    def __init__(self):
        self.device_type = 0
        self.display_width = 0
        self.display_height = 0
        self.layouts = []

    @classmethod
    def from_xml(cls, xml_content):
        layout_def = cls()
        root = ET.fromstring(xml_content)

        layout_def.device_type = int(root.get("deviceType"))
        layout_def.display_width = int(root.get("displayWidth"))
        layout_def.display_height = int(root.get("displayHeight"))

        for layout_elem in root.findall(".//Layout"):
            layout = Layout()
            layout.name = layout_elem.get("name")

            for page_elem in layout_elem.findall(".//Page"):
                page = Page()

                for panel_elem in page_elem.findall(".//Panel"):
                    panel = Panel()
                    panel.x = int(panel_elem.get("x"))
                    panel.y = int(panel_elem.get("y"))
                    panel.width = int(panel_elem.get("width"))
                    panel.height = int(panel_elem.get("height"))

                    for text_elem in panel_elem.findall(".//Text"):
                        text = Text()
                        text.name = text_elem.get("name")
                        text.x = int(text_elem.get("x"))
                        text.y = int(text_elem.get("y"))
                        text.width = int(text_elem.get("width"))
                        text.height = int(text_elem.get("height"))
                        text.font_list = text_elem.get("fontlist")
                        text.align_x = text_elem.get("alignX")
                        text.align_y = text_elem.get("alignY")
                        text.rotation_type = text_elem.get("RotationType")
                        text.border = text_elem.get("border")

                        panel.texts.append(text)

                    page.panels.append(panel)

                layout.pages.append(page)

            layout_def.layouts.append(layout)

        return layout_def

class Layout:
    def __init__(self):
        self.name = ""
        self.pages = []

class Page:
    def __init__(self):
        self.panels = []

class Panel:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.texts = []

class Text:
    def __init__(self):
        self.name = ""
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.font_list = ""
        self.align_x = ""
        self.align_y = ""
        self.rotation_type = ""
        self.border = ""
        
# Read XML data from a file
def read_xml_from_file(file_path):
    with open(file_path, "r") as file:
        xml_content = file.read()
    return xml_content

def sse():
    global x, sse_flag
    html = ""
        
    while True:    
        if layout_xml == "":
            return ""
        
        print(layout_xml)
        print(type(layout_xml))

        root = ET.fromstring(layout_xml.data)
        # Parse the layout content XML
        try: 
            content_root = ET.fromstring(content_xml.data)
        except:
            content_root = ""
        
        html = ""

        for layout in root.findall('.//Layout'):
            layout_name = layout.get('name')

            for page in layout.findall('.//Page'):
                for panel in page.findall('.//Panel'):
                    layout_width = panel.get('width')
                    layout_height = panel.get('height')

                    html += '<!-- Layout for "' + layout_name + ' -->'
                    html += '<div class="layout" style="width: ' + str(layout_width) + 'px; height: ' + str(layout_height) + 'px; border: 1px solid #000; position: relative;">'

                    for text in panel.findall('.//Text'):
                        text_name = text.get('name')
                        
                        try:
                            text_value = content_root.find('.//Text[@name="' + text_name + '"]').get('value')
                        except:
                            text_value = ""
                        text_x = text.get('x')
                        text_y = text.get('y')
                        text_width = text.get('width')
                        text_height = text.get('height')
                        text_align_x = text.get('alignX')
                        text_align_y = text.get('alignY')
                        rotation_type = text.get('RotationType')
                        border = text.get('border')  # Get the border attribute

                        align_x_class = "text-align-center" if text_align_x == "Center" else "text-align-left"
                        border_class = ""
                        if border:
                            border_class = "text-border"
                            if "L" not in border:
                                border_class += " no-left-border"
                            if "B" not in border:
                                border_class += " no-bottom-border"
                            if "R" not in border:
                                border_class += " no-right-border"
                            if "T" not in border:
                                border_class += " no-top-border"

                        if rotation_type == "Overflow":
                            # Implement scrolling text using CSS class
                            html += f'<div class="text scrolling-text {border_class}" style="position: absolute; top: {text_y}px; left: {text_x}px; width: {text_width}px; height: {text_height}px; text-align: {text_align_x};">'
                            html += '<div class="scrolling-text-text">' + text_value + '</div>'
                            html += '</div>'
                        else:
                            html += f'<div class="text {border_class}" style="position: absolute; top: {text_y}px; left: {text_x}px; width: {text_width}px; height: {text_height}px; text-align: {text_align_x};">'
                            html += text_value
                            html += '</div>'

                    html += "</div>"  # Close the layout div

        if sse_flag:
            sse_flag = False
            yield f"data:{html}\n\n"
            html = ""
        else:
            time.sleep(1)
            continue

def generate_html_from_xml():
    # Parse the layout XML content
    print(content_xml)
    
    if layout_xml == "":
        return ""
    
    root = ET.fromstring(layout_xml)

    # Parse the layout content XML
    try: 
        content_root = ET.fromstring(content_xml)
    except:
        content_root = ""

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ICE Exterior Display</title>
        <style>
            /* Define CSS for the display */
            .layout {
                width: 800px; /* Adjust the width as needed */
                height: 150px; /* Adjust the height as needed */
                background-color: #000; /* Black background */
                border: 2px solid #fff; /* White border */
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
                color: #ffA500; /* Orange text */
            }
            
            /* Define a CSS class for scrolling text */
            .scrolling-text {
                white-space: nowrap;
                overflow: hidden;
                width: 100%;
            }
            .scrolling-text-text {
                white-space: nowrap;
                overflow: visible;
                animation: scrollText 40s linear infinite;
            }
            @keyframes scrollText {
                0% {
                    transform: translateX(100%);
                }
                100% {
                    transform: translateX(-1200%);
                }
            }
        </style>
    </head>
    <body>
    '''

    for layout in root.findall('.//Layout'):
        layout_name = layout.get('name')

        for page in layout.findall('.//Page'):
            for panel in page.findall('.//Panel'):
                layout_width = panel.get('width')
                layout_height = panel.get('height')

                html += f'''
                <!-- Layout for "{layout_name}" -->
                <div class="layout" style="width: {layout_width}px; height: {layout_height}px; border: 1px solid #000; position: relative;">
                '''

                for text in panel.findall('.//Text'):
                    text_name = text.get('name')
                    try:
                        text_value = content_root.find(f'.//Text[@name="{text_name}"]').get('value')
                    except:
                        text_value = ""
                    text_x = text.get('x')
                    text_y = text.get('y')
                    text_width = text.get('width')
                    text_height = text.get('height')
                    text_align_x = text.get('alignX')
                    text_align_y = text.get('alignY')
                    rotation_type = text.get('RotationType')
                    
                    align_x_class = "text-align-center" if text_align_x == "Center" else "text-align-left"


                    if rotation_type == "Overflow":
                        # Implement scrolling text using CSS class
                        html += f'''
                        <!-- Text block {text_name}: {text_value} -->
                        <div class="text scrolling-text" style="position: absolute; top: {text_y}px; left: {text_x}px; width: {text_width}px; height: {text_height}px; text-align: {text_align_x}; border: 1px solid #000;">
                            <div class="scrolling-text-text">{text_value}</div>
                        </div>
                        '''
                    else:
                        html += f'''
                        <!-- Text block {text_name}: {text_value} -->
                        <div class="text" style="position: absolute; top: {text_y}px; left: {text_x}px; width: {text_width}px; height: {text_height}px; text-align: {text_align_x}; border: 1px solid #000;">
                            {text_value}
                        </div>
                        '''

                html += '</div>'  # Close the layout div

    html += '''
    </body>
    </html>
    '''

    return html


# HTML endpoint to display the layout
@app.route('/')
def display_layout():
    #layout_xml = read_xml_from_file("layout_408.xml")
    #content_xml = read_xml_from_file("content_408.xml")   
    html = generate_html_from_xml()
    return html  # Directly return HTML, no need for render_template

@app.route('/events')
def sse_request():
    return Response(sse(), content_type='text/event-stream')

@app.route('/display')
def show_display():
    return render_template('layout.html')

# Run the Flask app in a separate thread
def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Create an XML-RPC server
    rpc_server = SimpleXMLRPCServer(("0.0.0.0", 5001))
    rpc_server.register_function(SetLayoutDefinition, "SetLayoutDefinition")
    rpc_server.register_function(ShowLayout, "ShowLayout")


    # Run the XML-RPC server in the main thread
    rpc_server_thread = threading.Thread(target=rpc_server.serve_forever)
    rpc_server_thread.start()
    
    # Start the Flask app thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()