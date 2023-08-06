from flask import Flask, render_template, make_response,  Response
from argparse import ArgumentParser
from cellcube_xml_page_builder.cellcube_xml_builder import CellcubeXmlPageBuilder, Document

# Get command line arguments to start server
def get_args():
    parser = ArgumentParser(description='Handset simulator')
    parser.add_argument("command")

    parser.add_argument("-s", "--host", dest="server_host", default="127.0.0.1",
                        help="Sever listening adress. Use 0.0.0.0 to listen on all interfaces")
    parser.add_argument("-p", "--port", dest="server_port", default=3333,                    
                        help="Server default port"),
    parser.add_argument("-x", "--debug", dest="server_debug", default=False,                   
                        help="Enable server debug mode")
    parser.add_argument("-d", "--directory", dest="app_directory",                    
                        help="XML App root directory. The simuator will look for a home.xml file")
    
    return parser.parse_args()


def get_flask_app() -> Flask:

    app = Flask(__name__)

    @app.route("/xml/sample/one")
    def xml_sample_one():
        xml = ('<?xml version="1.0" encoding="UTF-8"?>'
        '<!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">'
        '<pages><page tag="page1">it\'s ok<a href="#1">line 1</a><a href="#2">line 2</a></page><page>Nouvelle page ajoutée.</page><page>New page at the specified index</page></pages>'
        )
        resp = make_response(xml, 200)
        resp.headers['Content-Type'] = 'application/xml'
        return resp

    @app.route("/hello")
    def hello_world():
        return "<p>Hello, World!</p>" 

    @app.route("/")
    def index():
        return render_template('home.html', name="name")

    return app


def start_server(host, port, debug=False) -> Flask:    
    app = get_flask_app()
    print(f"app.template_folder ===>{app.template_folder}")
    print(f"app.instance_path ===>{app.instance_path}")
    print(f"app.root_path  ===>{app.root_path}")

    
    
    app.run(host=host,port=port, debug=debug)    
    return app


def run():
    args = get_args()
    if str(args.command).lower() == "start":
        #if __name__ == "__main__":
        debug=str(args.server_debug).capitalize() == "True"
        return start_server(host=args.server_host,port=args.server_port, debug=debug)
    else:
        print(f"Unknow command {args.command}. Did you mean 'start' ?")
        exit()

if __name__ == "__main__":
    run()
    

    









"""
xml = ('<?xml version="1.0" encoding="UTF-8"?>'
        '<!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">'
        '<pages><page tag="page1">it\'s ok<a href="#1">line 1</a><a href="#2">line 2</a></page><page>Nouvelle page ajoutée.</page><page>New page at the specified index</page></pages>'
        )

cellcube_xml_builder = CellcubeXmlPageBuilder()

print()
print(":::::::::::")
xml_doc = Document(xml_input=xml) # OK
xml_doc = cellcube_xml_builder.parse_xml_document(xml) # OK
print(xml_doc.xml(True)) # OK
print(":::::::::::")
print()
"""



"""
click        8.1.2
Flask        2.1.1
itsdangerous 2.1.2
Jinja2       3.1.1
MarkupSafe   2.1.1
pip          22.0.4
setuptools   58.1.0
Werkzeug     2.1.1
"""
