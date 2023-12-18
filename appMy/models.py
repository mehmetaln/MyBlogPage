from django.db import models
from django.contrib.auth.models import User # Kullanıc ile ilgili tüm ulaşılabilecek bilgilerin oldugu kütüphane

# Create your models here.

class Category(models.Model):
    title = models.CharField(("Kategori"), max_length=50)
    color = models.CharField(("Renk"), max_length=50, null =True)
    slug = models.SlugField(("Slug"))#türkçe karekterleri ingilzice karekterlere dönüştüren bir araç
    def __str__(self):
        return self.title
class Blog(models.Model):
    user = models. ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    category =models.ForeignKey(Category, verbose_name=("Kategori"), null = True, on_delete=models.CASCADE) # foreinkey bize seçici bir seçme özelliği verir
    title=models.CharField(("Başlık)"),max_length=50)
    text= models.TextField(("Blog Yazisi"))
    image= models.ImageField(("Resim"), upload_to="blog")
    date_now = models.DateTimeField(("Tarih - Saat"), auto_now_add=True)
    likes=    models.ManyToManyField(User,related_name="user2", verbose_name=("Beğenen Kullanıcılar"), blank=True)
    comment_num = models.IntegerField(("Yorum Sayısı"), default=0)
    # likes_num = models.IntegerField(("Begeni Sayısı"), default=0)

    def __str__(self):
        return self.title # admin apane linde obje ismi gözükmesi için
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)    
    blog=models.ForeignKey(Blog, verbose_name=("Yorum Yapılan Blog"), on_delete=models.CASCADE)
    text = models.TextField(("Yorum"))
    date_now = models.DateTimeField(("Tarih - Saat "), auto_now_add=True)
    
    def __str__(self):
        return self.blog.title    
    
    
    
class Contact(models.Model):
    title = models.CharField(("Konu"), max_length=50)
    text = models.TextField(("Mesaj"))
    email = models.CharField(("Email"), max_length=50)
    fullname = models.CharField(("Ad-Soyad"), max_length=50)
    
    def __str__(self):
        return self.title
    