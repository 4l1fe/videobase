# coding: utf-8
from apps.contents.models import Comments
from Levenshtein import distance

#Нахождение похожих комментариев, с помощью растояния Левинштейна
#Возвращает список id контентов под которым есть похожий комментарий
def clean_comments():
    comments = Comments.objects.order_by("content_id")
    comments_list = []
    content_id = comments[0].content_id
    text = comments[0].text
    for comment in comments:
        if comment.content_id == content_id and not(comment.id == content_id):
            dis = distance(text, comment.text)
            len1 = len(text)
            len2 = len(comment.text)
            len_text = (len1+len2)/2
            count = float(dis)/len_text
            if count < 0.5:
                comments_list.append(comment.content_id)
            text = comment.text
        else:
            content_id = comment.content_id
            text = comment.text

    return comments_list
