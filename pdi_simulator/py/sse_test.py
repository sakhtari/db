from flask import Flask, render_template, Response
import time

app = Flask(__name__)

def sse():
    count = 0
    while True:
        count += 1
        yield f"data: {count}\n\n"
        # Add a delay to simulate updates (you can replace this with actual data updates)
        time.sleep(1)

@app.route('/events')
def sse_request():
    return Response(sse(), content_type='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)



