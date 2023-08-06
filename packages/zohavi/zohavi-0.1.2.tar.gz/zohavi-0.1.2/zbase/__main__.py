import sys
sys.path.insert(0, '../')


from flask import Flask, Blueprint, jsonify

import zohavi_base
from zohavi_base.routes import BaseView
# from zohavi_procs import 

app = Flask(__name__)
BaseView.register( zohavi_base.bp  )
app.register_blueprint( zohavi_base.bp )

# breakpoint();

@app.route("/")
def hello_world():
	return "<p>Hello, World!</p>"

@app.route("/routes", methods=["GET"])
def getRoutes():
    routes = {}
    for r in app.url_map._rules:
        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["methods"] = list(r.methods)

    routes.pop("/static/<path:filename>")

    return jsonify(routes)



if __name__ == "__main__":
	# setup_args()
	app.run('0.0.0.0', debug=True, port=1112)