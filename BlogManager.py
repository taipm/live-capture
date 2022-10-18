from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

import collections
collections.Iterable = collections.abc.Iterable
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import collections
try:
    collectionsAbc = collections.abc
except AttributeError:
    collectionsAbc = collections

class BlogPost:
    def __init__(self, title, content, tags) -> None:
        self.title = title
        self.content = content
        self.tags = tags

    def update_to_blog(self):
        blog = Blog()
        blog.post(title=self.title,content=self.content, tags= self.tags)
        
#https://python-wordpress-xmlrpc.readthedocs.io/en/latest/examples/media.html#uploading-a-file
class Blog:
    def __init__(self) -> None:
        self.wp = Client('https://alphacodeclub.wordpress.com/xmlrpc.php', 'taipm.bidv@gmail.com', 'P@$$w0rdPMT')
        
    def get_posts(self):
        rs = self.wp.call(GetPosts())
        print(rs)

    def post(self, title, content, tags):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.terms_names = {
        'post_tag': tags,
        'category': ['Stocks', 'Query']
        }
        post.post_status = 'publish'
        self.wp.call(NewPost(post))

    def upload(self, file_path):
        # prepare metadata

        data = {
                'name': 'test.jpg',
                'type': 'image/png',  # mimetype
        }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(file_path, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

            response = self.wp.call(media.UploadFile(data))
            # response == {
            #       'id': 6,
            #       'file': 'picture.jpg'
            #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
            #       'type': 'image/jpeg',
            # }
            attachment_id = response['id']
    # def upload_thumbnail(self):
    #     post = WordPressPost()
    #     post.title = 'Picture of the Day'
    #     post.content = 'What a lovely picture today!'
    #     post.post_status = 'publish'
    #     post.thumbnail = attachment_id
    #     post.id = client.call(posts.NewPost(post))


# blog = Blog()
# blog.upload(file_path='./test.png')