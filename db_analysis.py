def test():
    print "hello db_analysis"

sql_derived_from_x_to_y = '''
SELECT 
  x.id, 
  x.x_url, 
  y.y_url
FROM 
(SELECT 
  derived_raw.id,
  thing.url AS x_url,
  thing.name
FROM derived_raw, thing
WHERE
  derived_raw.x_url = thing.url
) AS x,
(SELECT 
  derived_raw.id, 
  thing.url AS y_url, 
  thing.name
FROM derived_raw, thing
WHERE
  derived_raw.y_url = thing.url
) AS y
WHERE
  x.id = y.id
'''


'''
SELECT xy.x_url, xy.y_count, thing.name FROM thing,
(
SELECT x_url, COUNT(y_url) AS y_count
FROM derived_raw
GROUP BY x_url
) AS xy
WHERE thing.url = xy.x_url
ORDER BY y_count DESC
LIMIT 100
'''


sql_derived_from_x_to_y = '''
SELECT * from  
(
SELECT x_url, COUNT(y_url) AS y_count
FROM derived_raw
GROUP BY x_url
) AS derived
ORDER BY y_count DESC
LIMIT 100
'''
def derived_from_x_to_y():
    print "hello"
