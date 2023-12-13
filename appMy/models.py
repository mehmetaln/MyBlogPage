from django.db import models
from django.contrib.auth.models import User # Kullanıc ile ilgili tüm ulaşılabilecek bilgilerin oldugu kütüphane

# Create your models here.

class Blog(models.Model):
    user = models. ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    title=models.CharField(("Başlık)"),max_length=50)
    text= models.TextField(("Blog Yazisi"))
    image= models.ImageField(("Resim"), upload_to="blog")
    date_now = models.DateTimeField(("Tarih - Saat"), auto_now_add=False)
    likes=    models.ManyToManyField(User,related_name="user2", verbose_name=("Beğenen Kullanıcılar"))
    
 
 
 
 
    def __str__(self):
        return self.title # admin apanelinde obje ismi gözükmesi için