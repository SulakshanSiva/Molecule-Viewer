import sys
import io
from MolDisplay import Molecule
from http.server import HTTPServer, BaseHTTPRequestHandler
from molsql import Database
import MolDisplay
import urllib
import sqlite3
import cgi
import json
import molecule

# list of files that we allow the web-server to serve to clients
# (we don't want to serve any file that the client requests)
public_files = [ '/index.html', '/sdfUpload.html', '/select.html', '/style.css', '/script.js', '/sdf.js', '/select.js', '/display.html', '/display.js']

# Initialize the database
db = Database(reset=True)
db.create_tables()

class MyHandler(BaseHTTPRequestHandler):
    # declare global variable
    currDisplayMol = ""
    x = 0
    y = 0
    z = 0

    def do_GET(self):
        # check default files
        if self.path in public_files:
            self.send_response( 200 );  
            self.send_header( "Content-type", "text/html" )

            fp = open( self.path[1:] ); 

            site = fp.read()
            fp.close()

            self.send_header( "Content-length", len(site))
            self.end_headers()

            self.wfile.write( bytes( site, "utf-8" ) )

        elif (self.path == "/getMol"):
            # Read SQL Molecules Table
            molTable = db.getMolTableData()
            # convert to JSON data
            data = json.dumps(molTable)
            # send data back to JS server side
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(data.encode("utf-8"))

        elif(self.path == "/createMol"):
            self.send_response( 200 ) 
            self.send_header("Content-type", "image/svg+xml") 
            self.end_headers() 
            length = int(self.headers.get('Content-Length', 0)) 

            # create svg
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()
            name = MyHandler.currDisplayMol
            mol = db.load_mol(name)
            # get dimensions
            if (MyHandler.x != 0):
                mx = molecule.mx_wrapper(int(MyHandler.x), 0, 0)
                mol.xform( mx.xform_matrix )
            if (MyHandler.y != 0):
                mx = molecule.mx_wrapper(0, int(MyHandler.y), 0)
                mol.xform( mx.xform_matrix )
            if (MyHandler.z != 0):
                mx = molecule.mx_wrapper(0, 0, int(MyHandler.z))
                mol.xform( mx.xform_matrix )
            # sort
            mol.sort()
            # write svg
            self.wfile.write( bytes( mol.svg(), "utf-8" ) ) 

        else:
            # 404 Error
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

    def do_POST(self):
        if (self.path == "/elementHandler"):            
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            # get data from JS server side
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )

            # get values from js dictionary
            eNum = int(postvars['elementNum'][0])
            eCode = str(postvars['elementCode'][0])
            eName = str(postvars['elementName'][0])
            colOne = str(postvars['colOne'][0])[1:]
            colTwo = str(postvars['colTwo'][0])[1:]
            colThree = str(postvars['colThree'][0])[1:]
            radius = int(postvars['radius'][0])
            # save element to db
            db['Elements'] = (eNum, eCode, eName, colOne, colTwo, colThree, radius)

            # Send success output
            message = "Element saved"
            self.send_response( 200 ); 
            self.send_header( "Content-type", "text/plain" )
            self.send_header( "Content-length", len(message) )
            self.end_headers()

        elif (self.path == "/display"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            # get data from JS server side
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )
            # get molecule name
            name = str(postvars['name'][0])

            # save molecule name globally
            MyHandler.currDisplayMol = name

            # Send success output
            response_body = "Molecule saved"
            response_length = len(response_body.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", response_length)
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))

        elif (self.path == "/rotate"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            # get data from JS server side
            postvars = urllib.parse.parse_qs(body.decode('utf-8'))
            # get dimension that we are looking to rotate
            dimension = postvars['dimension'][0]
            # check which dimension is being rotated, then rotate
            if(dimension == 'y'):
                MyHandler.y = (MyHandler.y + 10) % 360
            elif(dimension == 'x'):
                MyHandler.x = (MyHandler.x + 10) % 360
            elif(dimension == 'z'):
                MyHandler.z = (MyHandler.z + 10) % 360

            # send success output
            response_body = "Molecule has been rotated"
            response_length = len(response_body.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", response_length)
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))

        elif (self.path == "/sdfUpload.html"):
            # get file
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            # retrieve data from file
            name = form['mol-name'].value
            sdf = form['sdf-file'].value

            # Check if file input was correct
            content = form['sdf-file'].headers['Content-Disposition']
            fName = cgi.parse_header(content)[1]['filename']
            ext = fName.split('.')[-1]
            # if a type .sdf was not inputted
            if ext != 'sdf':
                # Show Error output
                response_body = "Invalid SDF file"
                response_length = len(response_body.encode('utf-8'))
                self.send_response(400)
                self.send_header("Content-type", "text/plain")
                self.send_header("Content-length", response_length)
                self.end_headers()
                self.wfile.write(response_body.encode('utf-8'))
                return

            # Convert file type, Create molecule
            temp = io.BytesIO(sdf)
            file = io.TextIOWrapper(temp)

            # Add molecule into database
            db.add_molecule(name, file)

            # Send response to client
            response_body = "Molecule has been saved in db"
            response_length = len(response_body.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", response_length)
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))

    def do_DELETE(self):
        if (self.path == "/rmvElementHandler"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            # get data from JS server side
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )
            # get element to delete
            elementDel = str(postvars['elementDel'][0])

            # get element
            cursor = db.conn.cursor()
            cursor.execute("""SELECT * FROM Elements WHERE ELEMENT_NAME = ?""", (elementDel,))
            element = cursor.fetchall()

            # If element is found in database
            if(element):
                # remove from db
                cursor = db.conn.cursor()
                cursor.execute("""DELETE FROM Elements WHERE ELEMENT_NAME = ?""", (elementDel,))
                db.conn.commit()
                # send successs output
                message = f"{elementDel} has been deleted."
                self.send_response( 205 ); # OK
                self.send_header( "Content-type", "text/plain" )
                self.send_header( "Content-length", len(message) )
                self.end_headers()
                self.wfile.write(message.encode('utf-8'))
            # If element was not found
            else:
                # send Error output
                message = f"{elementDel} cannot be found."
                self.send_response(404); # OK
                self.send_header( "Content-type", "text/plain" )
                self.send_header( "Content-length", len(message) )
                self.end_headers()
                self.wfile.write(message.encode('utf-8'))

        else:
            # 404 error
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

httpd = HTTPServer(('localhost', int(sys.argv[1]) ), MyHandler)
httpd.serve_forever()