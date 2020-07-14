from django.contrib import admin
from .models import articles, Category, Plat_a_manger, booking, contact, author, happy_costumer

# Register your models here.

@admin.register(articles)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Category)
admin.site.register(Plat_a_manger)
admin.site.register(booking)
admin.site.register(contact)
admin.site.register(author)
admin.site.register(happy_costumer)