#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import time
import os

import blockdiag as bd
import seqdiag.command as sd
import seqdiag.elements as sd_elements
import actdiag as ad
import netdiag as nd

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

def create_diag_image(diagtype, diagsrc, outfile):
    diags = {'blockdiag': [bd, bd.blockdiag],
             'seqdiag': [sd, ''],
             'actdiag': [ad, ad.actdiag],
             'netdiag': [nd, nd.netdiag]}

    if diagtype == 'seqdiag':
        try:
            sd_elements.DiagramNode.clear()
            sd_elements.DiagramEdge.clear()
            sd_elements.NodeGroup.clear()
            tree = sd.diagparser.parse(sd.diagparser.tokenize(diagsrc))
            diagram = sd.ScreenNodeBuilder.build(tree)
            draw = sd.DiagramDraw('PNG', diagram, 'static/%s' % (outfile),
                    font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', 
                    antialias=True)
            draw.draw()
            draw.save()
            return True
        except Exception, e:
            return False
    else:
        diag, diagobj = diags[diagtype]
        try:
            diag.elements.DiagramNode.clear()
            diag.elements.DiagramEdge.clear()
            diag.elements.NodeGroup.clear()
            tree = diag.diagparser.parse(diag.diagparser.tokenize(diagsrc))
            diagram = diagobj.ScreenNodeBuilder.build(tree)
            draw = diag.DiagramDraw.DiagramDraw('PNG',diagram,
                    'static/%s' % (outfile),
                    font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', 
                    antialias=True)

            draw.draw()
            draw.save()
            return True
        except Exception, e:
            return False

@app.route("/api/<string:diag>", methods=['POST'])
def api_diag_post(diag):
    if 'src' in request.form:
        data = request.form['src']
    else:
        return none_result()

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = '%s%d.png' % (diag, unixtime)

    if create_diag_image(diag, data, outfile):
        return create_result(outfile, unixtime)
    else:
        return none_result()
    

@app.route("/api/blockdiag/<int:diag_id>", methods=['PUT', 'DELETE'])
def api_blockdiag(diag_id):
    outfile = 'blockdiag%d.png' % (diag_id)

    if 'PUT' == request.method:
        if 'src' in request.form:
            data = request.form['src']
            if create_diag_image('blockdiag', data, outfile):
                return create_result(outfile, diag_id)
            else:
                return none_result()
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
  group {
    color=yellow;
    label="テスト";
    c; d; e;
  }
}
    """;
    return render_template('index.html', data=data, diag="blockdiag")

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


@app.route("/api/seqdiag/<int:diag_id>", methods=['PUT', 'DELETE'])
def api_seqdiag(diag_id):
    outfile = 'seqdiag%d.png' % (diag_id)

    if 'PUT' == request.method:
        if 'src' in request.form:
            data = request.form['src']
            if create_diag_image('seqdiag', data, outfile):
                return create_result(outfile, diag_id)
            else:
                return none_result()
    elif 'DELETE' == request.method:
        os.remove('static/%s' % (outfile))
        return delete_result()


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


@app.route("/api/actdiag/<int:diag_id>", methods=['PUT', 'DELETE'])
def api_actdiag(diag_id):
    outfile = 'actdiag%d.png' % (diag_id)

    if 'PUT' == request.method:
        if 'src' in request.form:
            data = request.form['src']
            if create_diag_image('actdiag', data, outfile):
                return create_result(outfile, diag_id)
            else:
                return none_result()
    elif 'DELETE' == request.method:
        os.remove('static/%s' % (outfile))
        return delete_result()


@app.route("/netdiag", methods=['GET'])
def show_netdiag():
    data = u"""
diagram {
  network dmz {
    address = "210.x.x.x/24" web01; web02;
  }
  network internal {
    address = "172.x.x.x/24" db01; db02;
  }
  dmz -- internal;
}
    """;
    return render_template('index.html', data=data, diag="netdiag")


@app.route("/api/netdiag/<int:diag_id>", methods=['PUT', 'DELETE'])
def api_netdiag(diag_id):
    outfile = 'netdiag%d.png' % (diag_id)

    if 'PUT' == request.method:
        if 'src' in request.form:
            data = request.form['src']
            if create_diag_image('netdiag', data, outfile):
                return create_result(outfile, diag_id)
            else:
                return none_result()
    elif 'DELETE' == request.method:
        os.remove('static/%s' % (outfile))
        return delete_result()

if __name__ == "__main__":
    app.debug = True
    app.run()

