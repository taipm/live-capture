from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from pathlib import Path
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from pprint import pprint
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
        link = blog.post(title=self.title,content=self.content, tags= self.tags)
        return link
        
#https://python-wordpress-xmlrpc.readthedocs.io/en/latest/examples/media.html#uploading-a-file
import Config
class Blog:
    def __init__(self) -> None:
        self.wp = Client('https://alphacodeclub.wordpress.com/xmlrpc.php', Config.blog_user, Config.blog_pwd)
        self.url = self.wp.url
        self.id = self.wp.blog_id
        self.posts = self.get_posts(length_of_post=100)
        self.length = len(self.posts)
        self.last_post = self.posts[0]
        self.first_post = self.posts[self.length-1]
        
    def get_posts(self, length_of_post):
        rs = self.wp.call(GetPosts({'number': length_of_post}))
        return rs

    def get_post(self,id):
        # if(type(id) != str):
        #     #print(type(id))
        #     id = str(id)
        #     #xprint(type(id))
        print(id)
        print(type(id))
        
        print(self.posts[0].id)
        print(type(self.posts[0].id))

        for post in self.posts:
            if(post.id == id):
                pprint(post)
                return post
        

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
        #print(f'Id: {id} - Type: {type(id)}')
        # uploaded_post = self.last_post
        # print(f'Bài mới {uploaded_post}')
        # #print(f'Bài mới {uploaded_post.link}')
        blog = Blog()
        return blog.last_post.link
            

    def upload(self, file_path):
        data = {
                'name':  Path(file_path).name,
                'type': 'application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # mimetype
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
            return response['url']
    @property
    def summary(self):
        output = f'Blog: {self.url}'
        output += f'\nSố bài: {self.length}'
        output += f'\nBài đầu: {self.first_post.title} - {self.first_post.date} - {self.first_post.date_modified}'
        output += f'\nBài cuối:\n- {self.last_post.title} - {self.last_post.date} - {self.last_post.date_modified}'
        output += f'\n- Id: {self.last_post.id}'
        output += f'\n- Link: {self.last_post.link}'
        return output
    # def upload_thumbnail(self):
    #     post = WordPressPost()
    #     post.title = 'Picture of the Day'
    #     post.content = 'What a lovely picture today!'
    #     post.post_status = 'publish'
    #     post.thumbnail = attachment_id
    #     post.id = client.call(posts.NewPost(post))


# blog = Blog()
# blog.upload(file_path='./test.png')

# blog = Blog()
# # pprint(blog.last_post)
# # print(blog.summary)

# link = blog.post('TEST','TEST','TEST')
# print('Bài mới: ' + link)

# blog = Blog()
# x = blog.get_post(id='1696')
# print("Bài mới: " + x.link)
# print(blog.summary)