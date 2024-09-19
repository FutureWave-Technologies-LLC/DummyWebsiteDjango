from django.db import models

class users(models.Model):
    user_id = models.IntegerField(primary_key=True, null=False)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=45)
    status = models.BooleanField()

    def __str__(self):
        return self.user_id

class personal_pages(models.Model):
    page_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(users, on_delete=models.CASCADE)

    def __str__(self):
        return self.page_id

class posts(models.Model):
    post_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    media = models.CharField(max_length=255)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.post_id

class comments(models.Model):
    comment_id = models.IntegerField(primary_key=True, null=False)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.comment_id

class replies(models.Model):
    reply_id = models.IntegerField(primary_key=True, null=False)
    comment = models.ForeignKey(comments, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.reply_id

class messages(models.Model):
    message_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    reciever_id = models.IntegerField(null=False)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.message_id