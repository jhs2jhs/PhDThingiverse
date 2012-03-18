import httplib2
http = httplib2.Http()

import sqlite3
sqlite_file_path = './db/thingiver.db'
conn = sqlite3.connect(sqlite_file_path)

page_url_root = 'http://www.thingiverse.com/'

class page_dict_label:
    author_url = 'author_url'

    thing_name = 'thing_name'
    thing_created_time = 'thing_created_time'
    thing_status = 'thing_working_in_progress'
    thing_index = 'thing_index'

    description = 'thing_description'

    thing_images = 'thing_gallery_image'
    thing_image_url = 'url'
    thing_image_type = 'type'

    thing_files = 'thing_files'
    file_date = 'file_date'
    file_name = 'file_name'
    file_download = 'file_download'
    file_url = 'file_url'
    file_type = 'file_type'

    instruction = 'thing_instruction'

    thing_tags = 'thing_tags'
    tag_name = 'tag_name'

    thing_likes = 'thing_likes'
    follower_url = 'like_follower_url'

    thing_license = 'thing_license'

    thing_mades = 'thing_mades'
    made_url = 'thing_made_url'
    thing_deriveds = 'thing_deriveds'
    derived_url = 'thing_derived_url'
    
    
