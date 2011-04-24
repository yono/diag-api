#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import time

import blockdiag as bd
import seqdiag.command as sd
import actdiag as ad

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
app = Flask(__name__)

@app.route("/api/blockdiag", methods=['POST'])
def api_blockdiag():
    if 'src' in request.form:
        data = request.form['src']
    else:
        response = app.make_response(render_template('result.xml',url='None'))
        response.headers['Content-Type'] = 'application/xml'
        return response

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = 'blockdiag%d.png' % (unixtime)


    tree = bd.diagparser.parse(bd.diagparser.tokenize(data))
    diagram = bd.blockdiag.ScreenNodeBuilder.build(tree)
    draw = bd.DiagramDraw.DiagramDraw('PNG',diagram,'static/%s' % (outfile),
            font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)

    draw.draw()
    draw.save()

    response = app.make_response(render_template('result.xml', url=url_for('static', filename=outfile)))
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route("/blockdiag", methods=['POST', 'GET'])
def show_blockdiag():
    if 'aaa' in request.form:
        data = request.form['aaa']
    else:
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

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = 'blockdiag%d.png' % (unixtime)

    tree = bd.diagparser.parse(bd.diagparser.tokenize(data))
    diagram = bd.blockdiag.ScreenNodeBuilder.build(tree)
    draw = bd.DiagramDraw.DiagramDraw('PNG',diagram,'static/%s' % (outfile),
            font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)

    draw.draw()
    draw.save()

    return render_template('index.html', data=data, outfile=outfile, 
                           diag="blockdiag")

@app.route("/seqdiag", methods=['POST', 'GET'])
def show_seqdiag():
    if 'aaa' in request.form:
        data = request.form['aaa']
    else:
        data = u"""
{
  // simple notation
    browser  -> webserver [label = "GET /index.html"];
    browser <-- webserver;
}
        """;

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = 'seqdiag%d.png' % (unixtime)

    tree = sd.diagparser.parse(sd.diagparser.tokenize(data))
    diagram = sd.ScreenNodeBuilder.build(tree)
    draw = sd.DiagramDraw('PNG', diagram, 'static/%s' % (outfile),
            font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)

    draw.draw()
    draw.save()

    return render_template('index.html', data=data, outfile=outfile, 
                           diag="seqdiag")

@app.route("/actdiag", methods=['POST', 'GET'])
def show_actdiag():
    if 'aaa' in request.form:
        data = request.form['aaa']
    else:
        data = u"""
diagram {
  A -> B -> C;
  lane you {
    A; B;
  }
  lane me {
    C;
  }
}
        """;

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = 'actdiag%d.png' % (unixtime)

    tree = ad.diagparser.parse(ad.diagparser.tokenize(data))
    diagram = ad.actdiag.ScreenNodeBuilder.build(tree)
    draw = ad.DiagramDraw.DiagramDraw('PNG', diagram, 'static/%s' % (outfile),font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)

    draw.draw()
    draw.save()

    return render_template('index.html', data=data, outfile=outfile, 
                           diag="actdiag")


if __name__ == "__main__":
    app.debug = True
    app.run()

