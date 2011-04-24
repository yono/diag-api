#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import time
import os

import blockdiag as bd
import seqdiag.command as sd
import actdiag as ad

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
app = Flask(__name__)

def create_result(filename, diag_id):
    response = app.make_response(render_template('result.xml',
                                url=url_for('static', filename=filename),
                                diag_id=diag_id))
    response.headers['Content-Type'] = 'application/xml'
    return response

def delete_result():
    response = app.make_response(render_template('result.xml',url='None',
                                                diag_id=0))
    response.headers['Content-Type'] = 'application/xml'
    return response

def none_result():
    response = app.make_response(render_template('result.xml', url='None'))
    response.headers['Content-Type'] = 'application/xml'
    return response

def create_blockdiag(data, outfile):
    tree = bd.diagparser.parse(bd.diagparser.tokenize(data))
    diagram = bd.blockdiag.ScreenNodeBuilder.build(tree)
    draw = bd.DiagramDraw.DiagramDraw('PNG',diagram,'static/%s' % (outfile),
            font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)

    draw.draw()
    draw.save()


@app.route("/api/blockdiag", methods=['POST'])
def api_blockdiag_post():
    if 'src' in request.form:
        data = request.form['src']
    else:
        return none_result()

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = 'blockdiag%d.png' % (unixtime)

    create_blockdiag(data, outfile)

    return create_result(outfile, unixtime)

@app.route("/api/blockdiag/<int:diag_id>", methods=['PUT', 'DELETE'])
def api_blockdiag(diag_id):
    outfile = 'blockdiag%d.png' % (diag_id)

    if 'PUT' == request.method:
        if 'src' in request.form:
            data = request.form['src']
            create_blockdiag(data, outfile)

        return create_result(outfile, diag_id)

    elif 'DELETE' == request.method:
        os.remove('static/%s' % (outfile))
        return delete_result()

@app.route("/blockdiag", methods=['GET'])
def show_blockdiag():
    data = u"""
{
  a -> b -> c [style=dashed];
  b -> d -> e;
  a [style = dotted];
  b [color = pink];
  c [color = "#999999"];
  d [numbered = 20];
  e [label = "ゴール"];
}
    """;
    return render_template('index.html', data=data, diag="blockdiag")

def create_seqdiag(data, filename):
    tree = sd.diagparser.parse(sd.diagparser.tokenize(data))
    diagram = sd.ScreenNodeBuilder.build(tree)
    draw = sd.DiagramDraw('PNG', diagram, 'static/%s' % (filename),
            font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)
    draw.draw()
    draw.save()

@app.route("/seqdiag", methods=['GET'])
def show_seqdiag():
    data = u"""
{
  // simple notation
    browser  -> webserver [label = "GET /index.html"];
    browser <-- webserver;
}
    """;
    return render_template('index.html', data=data, diag="seqdiag")

@app.route("/api/seqdiag", methods=['POST'])
def api_seqdiag_post():
    if 'src' in request.form:
        data = request.form['src']
    else:
        return none_result()

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = 'seqdiag%d.png' % (unixtime)

    create_seqdiag(data, outfile)

    return create_result(outfile, unixtime)

@app.route("/api/seqdiag/<int:diag_id>", methods=['PUT', 'DELETE'])
def api_seqdiag(diag_id):
    outfile = 'seqdiag%d.png' % (diag_id)

    if 'PUT' == request.method:
        if 'src' in request.form:
            data = request.form['src']
            create_seqdiag(data, outfile)

        return create_result(outfile, diag_id)

    elif 'DELETE' == request.method:
        os.remove('static/%s' % (outfile))
        return delete_result()

def create_actdiag(data, outfile):
    tree = ad.diagparser.parse(ad.diagparser.tokenize(data))
    diagram = ad.actdiag.ScreenNodeBuilder.build(tree)
    draw = ad.DiagramDraw.DiagramDraw('PNG', diagram, 
            'static/%s' % (outfile),
            font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)

    draw.draw()
    draw.save()

@app.route("/actdiag", methods=['GET'])
def show_actdiag():
    data = u"""
diagram {
  A -> B -> C -> D;
  lane you {
    A; B; D;
  }
  lane me {
    C;
  }
}
    """;
    return render_template('index.html', data=data, diag="actdiag")

@app.route("/api/actdiag", methods=['POST'])
def api_actdiag_post():
    if 'src' in request.form:
        data = request.form['src']
    else:
        return none_result()

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = 'actdiag%d.png' % (unixtime)

    create_actdiag(data, outfile)

    return create_result(outfile, unixtime)

@app.route("/api/actdiag/<int:diag_id>", methods=['PUT', 'DELETE'])
def api_actdiag(diag_id):
    outfile = 'actdiag%d.png' % (diag_id)

    if 'PUT' == request.method:
        if 'src' in request.form:
            data = request.form['src']
            create_actdiag(data, outfile)

        return create_result(outfile, diag_id)
    elif 'DELETE' == request.method:
        os.remove('static/%s' % (outfile))
        return delete_result()


if __name__ == "__main__":
    app.debug = True
    app.run()

