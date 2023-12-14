from django.db import models
from django.contrib.auth.models import User # Kullanıc ile ilgili tüm ulaşılabilecek bilgilerin oldugu kütüphane

# Create your models here.

class Blog(models.Model):
    user = models. ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    title=models.CharField(("Başlık)"),max_length=50)
    text= models.TextField(("Blog Yazisi"))
    image= models.ImageField(("Resim"), upload_to="blog")
    date_now = models.DateTimeField(("Tarih - Saat"), auto_now_add=True)
    likes=    models.ManyToManyField(User,related_name="user2", verbose_name=("Beğenen Kullanıcılar"), blank=True)
    comment_num = models.IntegerField(("Yorum Sayısı"), default=0)

    def __str__(self):
        return self.title # admin apane linde obje ismi gözükmesi için
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)    
    blog=models.ForeignKey(Blog, verbose_name=("Yorum Yapılan Blog"), on_delete=models.CASCADE)
    text = models.TextField(("Yorum"))
    date_now = models.DateTimeField(("Tarih - Saat "), auto_now_add=True)
    
    def __str__(self):
        return self.blog.title    
    
    