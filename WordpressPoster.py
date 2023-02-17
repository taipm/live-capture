from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import Config

class WordPressPoster:
    def __init__(self, site_url, username, password):
        self.site_url = 'https://alphacodeclub.wordpress.com/xmlrpc.php'
        self.username = Config.blog_user,
        self.password = Config.blog_pwd

        # Tạo client để kết nối với trang WordPress
        self.client = Client(site_url + '/xmlrpc.php', username, password)

    def post(self, title, content):
        # Tạo đối tượng bài viết
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'publish'

        # Đăng bài viết lên trang WordPress
        post_id = self.client.call(posts.NewPost(post))

        if post_id:
            print(f'Bài viết đã được đăng thành công với ID là {post_id}')
        else:
            print('Đăng bài viết không thành công')
