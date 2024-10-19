from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from .models import Order, Book
from django.utils.safestring import mark_safe

# Custom Actions for Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at')
    actions = ['mark_as_shipped']

    def mark_as_shipped(self, request, queryset):
        updated_count = queryset.update(status='shipped')
        self.message_user(request, f"{updated_count} orders marked as shipped.")
    mark_as_shipped.short_description = 'Mark selected orders as shipped'

# Custom Buttons for Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'custom_publish_button', 'custom_b', 'custom_field')
    readonly_fields = ('custom_publish_button', 'custom_b')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:book_id>/publish/', self.admin_site.admin_view(self.publish_book), name='publish-book'),
        ]
        return custom_urls + urls

    def publish_book(self, request, book_id):
        
        # Custom logic to mark a book as published
        book = self.get_object(request, book_id)
        book.is_published = True
        book.save()
        self.message_user(request, f"Book '{book.title}' has been published.")
        return redirect('admin:store_book_changelist')

    def custom_publish_button(self, obj):
        if obj and obj.id and not obj.is_published:
            publish_url = reverse('admin:publish-book', args=[obj.id])
            return mark_safe(f'''
                <a class="button" onclick="return confirm('Are you sure you want to publish this book?');" href="{publish_url}">Publish</a>
            ''')
        return "Already Published" if obj and obj.is_published else "Cannot publish an unsaved book"
    custom_publish_button.short_description = 'Publish Book'
    custom_publish_button.allow_tags = True

    def custom_field(self):
        print("FVGHBJNMKLJNHBGVHBJNMKJNH")
        return f"Calculated: {123}"

    def custom_b(self, obj):
        return  
    custom_b.short_description = 'just a button'

    def has_publish_permission(self, request):
        return request.user.has_perm('store.can_publish_books')

# Register the models and admin classes
admin.site.register(Order, OrderAdmin)
admin.site.register(Book, BookAdmin)
