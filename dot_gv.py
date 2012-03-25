from myutil import conn
from datetime import datetime
from gexf import Gexf

def test():
    print "hello dot gv"


sql_derived_x_to_y_basic = '''
SELECT * FROM 
derived_raw
'''
sql_derived_x_to_y_created_time = '''
SELECT 
  x.id, 
  x.x_url,
  y.y_url,
  x.x_ctime, 
  y.y_ctime
FROM
(SELECT 
  derived_raw.id,
  derived_raw.x_url AS x_url,
  thing.created_time AS x_ctime
FROM derived_raw, thing
WHERE 
  derived_raw.x_url = thing.url
) AS x, 
(SELECT 
  derived_raw.id,
  derived_raw.y_url AS y_url,
  thing.created_time AS y_ctime
FROM derived_raw, thing
WHERE 
  derived_raw.y_url = thing.url
) AS y
WHERE x.id = y.id
ORDER BY x.x_url, y.y_url
'''
def derived_x_to_y():
    txt = open('./dot/derived_x_to_y.gv', 'w')
    txt.write('//%s\n'%(str(datetime.now())))
    txt.write('digraph graphname {\n')
    gexf = Gexf('Jianhua Shao', 'Thingiver derivation mapping')
    graph = gexf.addGraph('directed', 'static', 'derivation_x_y')
    #attr_node = graph.addNodeAttribute('url', '', 'string')
    attr_edge = graph.addEdgeAttribute('c_days', '', 'string')
    #sql = sql_derived_x_to_y
    sql = sql_derived_x_to_y_created_time
    param = ()
    c = conn.cursor()
    c.execute(sql, param)
    for r in c.fetchall():
        print r
        x = r[1]
        y = r[2]
        x_ctime = r[3]
        y_ctime = r[4]
        x = x.strip('\n\t/thing:')
        #x = int(x)
        y = y.strip('\n\t/thing:')
        #y = int(y)
        #print type(x), type(y)
        #print x, y
        x_ctime = datetime.strptime(x_ctime, '%b %d, %Y')
        y_ctime = datetime.strptime(y_ctime, '%b %d, %Y')
        duration = (y_ctime - x_ctime).days
        #print duration
        dot_line = '\t{%s} -> {%s} [label=%s];\n'%(x, y, str(duration))
        print dot_line
        txt.write(dot_line)
        n_x = graph.addNode(str(x), str(x))
        n_y = graph.addNode(str(y), str(y))
        #n_x.addAttribute(attr_node, 'string')
        #n_y.addAttribute(attr_node, 'string')
        e = graph.addEdge('%s_%s'%(str(x), str(y)), x, y)
        e.addAttribute(attr_edge, str(duration))
        #print e
    c.close()
    txt.write('}')
    txt.close()
    gexf_file = open('./dot/derived_x_to_y.gexf', 'w')
    gexf.write(gexf_file)
    print "finish"
