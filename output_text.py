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
    #for raw in thing_tags_list:
    #    print raw, thing_tags_list[raw]
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



#### method bellow is the correct one ####
sql_thing = 'SELECT thing.id, thing.url, thing.name FROM thing'
sql_desc = 'SELECT id, description FROM description'
sql_insc = 'SELECT id, instruction FROM instruction'
things = {}
def text_things_right():
    c = conn.cursor()
    sql = sql_thing
    c.execute(sql, ())
    for raw in c.fetchall():
        thing_id = raw[0]
        thing_url = raw[1]
        thing_title = raw[2]
        if not things.has_key(thing_id):
            things[thing_id] = {}
        things[thing_id]['thing_id'] = thing_id
        things[thing_id]['thing_url'] = thing_url
        things[thing_id]['thing_title'] = thing_title
    sql = sql_desc
    c.execute(sql, ())
    for raw in c.fetchall():
        thing_id = raw[0]
        desc = raw[1]
        things[thing_id]['thing_desc'] = desc
    sql = sql_insc
    c.execute(sql, ())
    for raw in c.fetchall():
        thing_id = raw[0]
        insc = raw[1]
        things[thing_id]['thing_insc'] = insc
    print len(things)
    thing_tags_list = text_tags()
    f = open("./texts/texts_all.txt", 'w')
    f.write('thing_id \tthing_url \tthing_title \tthing_tags \tthing_desc \tthing_instruction\n')
    for tid in things:
        thing_url = things[tid]['thing_url'].encode('utf-8')
        thing_title = things[tid]['thing_title'].encode('utf-8')
        if things[tid].has_key('thing_desc'):
            thing_desc = things[tid]['thing_desc'].encode('utf-8')
        else:
            thing_desc = ''
        if things[tid].has_key('thing_insc'):
            thing_insc = things[tid]['thing_insc'].encode('utf-8')
        else:
            thing_insc = ''
        if thing_url in thing_tags_list:
            thing_tags = thing_tags_list[thing_url].encode('utf-8')
        else:
            thing_tags = ''
        print tid
        f.write('%s\t%s\t%s\t%s\t%s\t%s\t\n'%(thing_id, thing_url, thing_title, thing_tags, thing_desc, thing_insc))
    f.close()
    c.close()
    
if __name__ == '__main__':
    text_things_right()
    
    
