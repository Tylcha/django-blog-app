from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


DEFAULT = 'Yazilim'
Kategori = (
    ('Technology','Teknoloji'), 
    ('Sport','Spor'), 
    ('Science','Bilim'), 
    ('Cinema , Series','Sinema , Dizi'),
    ('Game','Oyun'),
    ('Software','Yazilim'),
)
class Category(models.Model):
    title = models.CharField(max_length=200) 
    slug = models.SlugField(max_length=200, default="")
    image = models.ImageField(null=True, blank=True, upload_to="category") #image istersek ekleriz diye

    def __str__(self):
        return self.title #admin title


class Post(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name='Kategori') #kategori silinirse postda silinsin

    user = models.ForeignKey('auth.User', related_name='post', on_delete=models.CASCADE,verbose_name='Yazar') #hazir user on_delete kullanici silinirse hepsi silinir
    title = models.CharField(max_length=120, verbose_name='Başlık') 
    content = models.TextField(verbose_name='İçerik')
    publishing_date = models.DateTimeField(verbose_name='Yayınlanma Tarihi', auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='post', verbose_name='Resim')
    slug = models.SlugField(editable=False, unique=True) #slug posta gore arama cubugunda olusan title kismi varya o

    def __str__(self):  # admin panelinde postun basligi gozukucek
        return self.title

    def get_absolute_url(self):
        return reverse('detail',kwargs={'slug': self.slug})

    def get_unique_slug(self): #slug olusturma
        slug = slugify(self.title.replace('ı', 'i')) #i lari i ile degistik ne olur ne olmaz
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs): #kaydetme islemi
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    class Meta: #siralama olcutu olusturulma zamani
        ordering = ['-publishing_date', 'id']

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, verbose_name='Ad Soyad')
    content = models.TextField(max_length=500, verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False) #admin kabul edene kadar false

    def approve(self): #admin true
        self.approved_comment = True
        self.save() #kayit

    def approved_comments(self):#onaylanmis comment
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.name