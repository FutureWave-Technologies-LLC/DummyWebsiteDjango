from .models import *

class AbstractFactory:
    @staticmethod
    def create_post(request):
        data = request.data.copy()

        user = users.objects.filter(user_id=data.get('user_id')).first()

        my_post_info = posts(author = user,   
                             title = data.get('title'),
                             description = data.get('description'),
                             media = data.get('media'))
        my_post_info.save()  

    @staticmethod
    def create_comment(request):
        request_user_id = request.data.get("user_id")
        request_post_id = request.data.get("post_id")

        user = users.objects.filter(user_id= request_user_id).first()
        post = posts.objects.filter(post_id= request_post_id).first()
        comment_info = comments(author = user,
                                post = post,
                                comment = request.data.get("comment"))
        comment_info.save()

    @staticmethod
    def create_reply(request):
        request_user_id = request.data.get("user_id")
        request_comment_id = request.data.get("comment_id")
        request_reply_text = request.data.get("reply")

        user = users.objects.filter(user_id = request_user_id).first()
        comment = comments.objects.filter(comment_id = request_comment_id).first()
        
        replies.objects.create(author = user,
                                comment_id = comment.comment_id,
                                reply = request_reply_text)

    @staticmethod
    def create_like(request):
        request_user_id = request.data.get('user_id')
        request_post_id = request.data.get('post_id')

        user = users.objects.filter(user_id = request_user_id).first()
        post = posts.objects.filter(post_id = request_post_id).first()
        
        likes.objects.create(author = user,
                            post = post)

