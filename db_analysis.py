def test():
    print "hello db_analysis"

sql_derived_from_x_to_y = '''
SELECT 
  x.id, 
  x.thing_id, 
  x.url, 
  y.thing_id, 
  y.url
FROM 
(SELECT 
  derived.id,
  thing.id AS thing_id, 
  thing.url
FROM derived, thing
WHERE
  derived.thing_id = thing.id
) AS x,
(SELECT 
  derived.id, 
  thing.id AS thing_id, 
  thing.url
FROM derived, thing
WHERE
  derived.url = thing.url
) AS y
WHERE
  x.id = y.id
'''
def derived_from_x_to_y():
    print "hello"
