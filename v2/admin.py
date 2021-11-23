from django.contrib import admin
from v2.models import Post, Category, Comments

# Register your models here.

@admin.register(Post) #decorator olarak yazdik admin klasi turettik
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publishing_date', 'category','slug'] #admin paneli gozukme
    list_display_links = ['title','publishing_date']    #link olarak tiklanabilir
    list_filter = ['publishing_date']   #sag zaman filtre
    search_fields = ['title']   #arama cubugu titlea gore

    class Meta:
        model = Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} #oncelikli olarak gorunucek alan
    list_display_links = ['title','pk']
    list_display = (
        "pk", #primarykey id
        "title",
        "slug",
    )

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comments