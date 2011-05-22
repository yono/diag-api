#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import time
import os

import psycopg2

import blockdiag.command as bd
import blockdiag.builder as bd_builder
import blockdiag.elements as bd_elements

import seqdiag.command as sd
import seqdiag.builder as sd_builder
import seqdiag.elements as sd_elements

import actdiag.command as ad
import actdiag.builder as ad_builder
import actdiag.elements as ad_elements

import nwdiag.command as nd
import nwdiag.builder as nd_builder
import nwdiag.elements as nd_elements

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
app = Flask(__name__)

font='/Library/Fonts/ヒラギノ明朝 Pro W3.otf'

dbname = 'diagapi_development'
username = 'postgres'
conn = psycopg2.connect('dbname=%s user=%s' % (dbname, username))
cur = conn.cursor()

def create_result(filename, diag_id, src):
    response = app.make_response(render_template('result.xml',
                                url=url_for('static', filename=filename),
                                diag_id=diag_id, src=src))
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

def all_result(rows):
    response = app.make_response(render_template('all.xml', diags=rows))
    response.headers['Content-Type'] = 'application/xml'
    return response

def create_diag_image(diagtype, diagsrc, outfile):
    diags = {'blockdiag': [bd, bd_builder, bd_elements],
             'seqdiag': [sd, sd_builder, sd_elements],
             'actdiag': [ad, ad_builder, ad_elements],
             'nwdiag': [nd, nd_builder, nd_elements]}

    diag, diagobj, diagelements = diags[diagtype]
    try:
        diagelements.DiagramNode.clear()
        diagelements.DiagramEdge.clear()
        diagelements.NodeGroup.clear()
        tree = diag.diagparser.parse(diag.diagparser.tokenize(diagsrc))
        diagram = diagobj.ScreenNodeBuilder.build(tree)
        draw = diag.DiagramDraw.DiagramDraw('PNG',diagram,
                'static/%s' % (outfile),
                font=font, 
                antialias=True)

        draw.draw()
        draw.save()
        return True
    except Exception, e:
        return False

@app.route("/api/<string:diag>", methods=['GET','POST'])
def api_diag_post(diag):

    cur.execute("SELECT id FROM diagtype WHERE name = %s", [diag])
    diag_row = cur.fetchone()
    if diag_row is None:
        return none_result()
    diagtype_id = diag_row[0]

    if 'GET' == request.method:
        cur.execute("""
          SELECT 
            d.id, 
            d.src, 
            d.imgpath,
            dt.name
          FROM diag as d
          INNER JOIN diagtype as dt
          ON d.diagtype_id = dt.id
          WHERE d.diagtype_id = %s
        """, (str(diagtype_id)))
        rows = []
        for row in cur.fetchall():
            rows.append(row)
        return all_result(rows)
    elif 'POST' == request.method:
        if 'src' in request.form:
            data = request.form['src']
        else:
            return none_result()

        is_saved = True
        if 'save' in request.form:
            if request.form['save'] == 'true':
                is_saved = True
            elif request.form['false'] == 'false':
                is_saved = False

        unixtime = int(time.mktime(datetime.datetime.now().timetuple()))
        outfile = '%s%d.png' % (diag, unixtime)

        if create_diag_image(diag, data, outfile):
            if is_saved:
                cur.execute("""
                INSERT INTO diag (src, imgpath, diagtype_id) 
                VALUES (%s, %s, %s)
                """, (data, outfile, str(diagtype_id)))
            conn.commit()
            return create_result(outfile, unixtime, data)
        else:
            return none_result()
    
@app.route("/api/<string:diag>/<int:diag_id>", methods=['GET', 'PUT', 'DELETE'])
def api_diag(diag, diag_id):
    outfile = '%s%d.png' % (diag, diag_id)

    if 'GET' == request.method:
        cur.execute("""
        select imgpath, src from diag where id = %s
        """, (str(diag_id)))
        row = cur.fetchone()
        outfile = row[0]
        src = row[1]
        return create_result(outfile, outfile.replace(diag,'').replace('.png',''), src)
    elif 'PUT' == request.method:
        if 'src' in request.form:
            data = request.form['src']
            if create_diag_image(diag, data, outfile):
                cur.execute("UPDATE diag SET src = %s WHERE imgpath = %s", (data, outfile))
                conn.commit()
                return create_result(outfile, diag_id, data)
            else:
                return none_result()
    elif 'DELETE' == request.method:
        os.remove('static/%s' % (outfile))
        cur.execute("DELETE FROM diag WHERE imgpath = %s", (imgpath))
        conn.commit()
        return delete_result()

diag_srcs = {
    'blockdiag': u"""
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
    """,
    'seqdiag': u"""
{
  // simple notation
    browser  -> webserver [label = "GET /index.html"];
    browser <-- webserver;
}
    """,
    'actdiag': u"""
diagram {
  A -> B -> C -> D;
  lane you {
    A; B; D;
  }
  lane me {
    C;
  }
}
    """,
    'nwdiag': u"""
diagram {
  network dmz {
    address = "210.x.x.x/24" web01; web02;
  }
  network internal {
    address = "172.x.x.x/24" db01; db02;
  }
}
    """
}


@app.route("/", methods=['GET'])
def show_list():
    return render_template('list.html') 

@app.route("/<string:diag>", methods=['GET'])
def show_diag_list(diag):
    return render_template('list.html', diag=diag)

@app.route("/<string:diag>/new", methods=['GET'])
def show_diag(diag):
    if diag in diag_srcs:
        return render_template('index.html', data=diag_srcs[diag],diag=diag)
    else:
        return none_result()

@app.route("/<string:diag>/<int:diag_id>", methods=['GET'])
def show_blockdiag_edit(diag, diag_id):
    return render_template('edit.html', diag=diag, diag_id=diag_id)


if __name__ == "__main__":
    app.debug = True
    app.run()

