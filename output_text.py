from myutil import conn
import re

sql_all = '''
SELECT
  thing.id AS thing_id, thing.url AS thing_url, thing.name AS thing_title,
  description.description AS thing_desc, 
  instruction.instruction AS thing_inst
FROM thing, description, instruction
WHERE
  thing.id = description.thing_id AND
  thing.id = instruction.thing_id 
'''

sql_tags = '''
SELECT 
  thing.id AS thing_id, thing.url AS thing_url, tag.name AS thing_t
FROM thing, thing_tag, tag
WHERE
  thing.id = thing_tag.thing_id
  AND thing_tag.tag_id = tag.id
'''


def text_tags():
    thing_tags_list = {}
    c = conn.cursor()
    param = ()
    sql = sql_tags
    c.execute(sql, param)
    for raw in c.fetchall():
        thing_id = raw[0]
        thing_url = raw[1]
        thing_tag = raw[2].strip().replace('/tag:', '')
        #print thing_id, thing_tag
        if thing_url in thing_tags_list:
            #print thing_id, "ininiinininini"
            thing_tags_list[thing_url] = thing_tags_list.pop(thing_url)+", "+thing_tag
        else:
            thing_tags_list[thing_url] = thing_tag
        #print thing_id, thing_tags_list[thing_id] 
    c.close()
    for raw in thing_tags_list:
        print raw, thing_tags_list[raw]
    return thing_tags_list
        
def text_things():
    thing_tags_list = text_tags()
    f = open("./texts/texts_all.txt", 'w')
    f.write('thing_id \tthing_url \tthing_title \tthing_tags \tthing_desc \tthing_instruction\n')
    c = conn.cursor()
    param = ()
    sql = sql_all
    c.execute(sql, param)
    for raw in c.fetchall():
        thing_id = raw[0]
        thing_url = raw[1]
        thing_title = raw[2].strip().encode('ascii', 'ignore').replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ')
        thing_desc = raw[3].strip().encode('ascii', 'ignore').replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ')
        thing_instruction = raw[4].strip().encode('ascii', 'ignore').replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ')
        #print thing_desc
        if thing_url in thing_tags_list:
            thing_tags = thing_tags_list[thing_url]
        else:
            thing_tags = ''
            #print thing_url, "==========", raw
        if thing_id == 15152 or thing_id == 15153: # be careful this line, I can not format and clean it, so be aware to manually delete it. 
            print thing_desc
            print thing_instruction
            print "======"
        f.write('%s\t%s\t%s\t%s\t%s\t%s\t\n'%(thing_id, thing_url, thing_title, thing_tags, thing_desc, thing_instruction))
    f.close()
    c.close()
    
