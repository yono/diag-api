#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import time

import blockdiag as bd
import seqdiag.command as sd
import actdiag as ad
import netdiag as nd

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
app = Flask(__name__)

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

@app.route("/netdiag", methods=['POST', 'GET'])
def show_netdiag():
    if 'aaa' in request.form:
        data = request.form['aaa']
    else:
        data = u"""
diagram {
  network dmz {
      address = "210.x.x.x/24"

      web01 [address = "210.x.x.1"];
      web02 [address = "210.x.x.2"];
      web03 [address = "210.x.x.3"];
  }
  network internal {
      address = "172.x.x.x/24";

      db01;
      db02;
      app01;
      app02;
  }

  dmz -- internal
}
        """;

    unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
    outfile = 'netdiag%d.png' % (unixtime)

    tree = nd.diagparser.parse(nd.diagparser.tokenize(data))
    diagram = nd.netdiag.ScreenNodeBuilder.build(tree)
    draw = nd.DiagramDraw.DiagramDraw('PNG', diagram, 'static/%s' % (outfile),font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)

    draw.draw()
    draw.save()

    return render_template('index.html', data=data, outfile=outfile, 
                           diag="netdiag")

if __name__ == "__main__":
    app.debug = True
    app.run()

