from flask_frozen import Freezer
from app import app 


freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()

    @freezer.register_generator
    def post_url_generator():
    # Yield the URL for every dynamic page you want to freeze
        for post in app.get_all_posts():
            yield {'id': post.id}