#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import time

from blockdiag import diagparser
from blockdiag import blockdiag
from blockdiag import DiagramDraw

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

    tree = diagparser.parse(diagparser.tokenize(data))
    diagram = blockdiag.ScreenNodeBuilder.build(tree)
    draw = DiagramDraw.DiagramDraw('PNG', diagram, 'static/%s' % (outfile),
            font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf', antialias=True)

    draw.draw()
    draw.save()

    return render_template('index.html', data=data, outfile=outfile)

if __name__ == "__main__":
    app.debug = True
    app.run()

