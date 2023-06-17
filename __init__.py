import os
import webbrowser

import click
from rich import print

from .app import Search, create_app, save_metadata

import http.server
import socketserver
import threading
import webbrowser
import time



__all__ = ["app"]

def start_local_server():
    # Specify the IP address and port to bind the server to
    IP_ADDRESS = "127.0.0.1"
    PORT = 5001

    # Change to the directory containing your HTML file
    DIRECTORY = "C:/Users/subha/AppData/Local/Programs/Python/Python310/lib/site-packages/kgsearch/web"
    
    # Create a custom handler to serve the files
    Handler = http.server.SimpleHTTPRequestHandler

    # Set up the server with the specified IP address, port, and handler
    with socketserver.TCPServer((IP_ADDRESS, PORT), Handler) as httpd:
        print(f"Serving at {IP_ADDRESS}:{PORT}")
        httpd.serve_forever()

path = os.path.abspath(os.path.dirname(__file__))
print(path)

@click.command("start", short_help="Start the app")
@click.argument("arg", type=str)
@click.option("-f", help="Csv file with triples.")
def start(arg, f):

    if arg == "start":
        # lsof -i:9200
        # lsof -i:5000
        # kill -9 <PID>

        app = create_app()
        
        print("🎉 Starting the app.")
        # Start the local server in a separate thread
        server_thread = threading.Thread(target=start_local_server)
        server_thread.start()

        # Wait for the server to start (optional)
        #time.sleep(1)

        # Open the browser with the specified URL
        webbrowser.open("http://127.0.0.1:5001/web/app.html")


        #webbrowser.open(os.path.join("file://" + path, "web/app.html"))
        app.run(debug=True)

    elif arg == "add":
        Search(file=f).save(path=os.path.join(path, "data/search.pkl"))

    elif arg == "meta":
        save_metadata(origin=f, source=os.path.join(path, "data/metadata.json"))

    elif arg == "open":
        print("😎 Opening web.")
        webbrowser.open(os.path.join("file://" + path, "web/app.html"))
