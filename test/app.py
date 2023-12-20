from flask import Flask, render_template, Response
import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

app = Flask(__name__)
count = 0

# XML-RPC endpoint to get the current count
def get_count():
    global count
    return count

# XML-RPC endpoint to set the count
def set_count(new_count):
    global count
    count = new_count
    return True

@app.route('/')
def index():
    return render_template('index.html')

def event_stream():
    global count
    while True:
        time.sleep(1)
        #count += 1
        yield f"data: {count}\n\n"
        

@app.route('/sse')
def sse():
    return Response(event_stream(), content_type='text/event-stream')


def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Create an XML-RPC server
    rpc_server = SimpleXMLRPCServer(("0.0.0.0", 5001))
    rpc_server.register_function(get_count, 'get_count')
    rpc_server.register_function(set_count, 'set_count')

    import threading
    # Run the XML-RPC server in the main thread
    rpc_server_thread = threading.Thread(target=rpc_server.serve_forever)
    rpc_server_thread.start()
    
    # Start the Flask app thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()