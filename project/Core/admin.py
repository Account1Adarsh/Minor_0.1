from django.contrib import admin
from .models import Book, BookIssue, PasswordReset
from django.core.exceptions import ValidationError
from django.db import transaction
from datetime import date, timedelta

from django.contrib import admin
from .models import Book, BookIssue, PasswordReset
from django.db import transaction
from datetime import date
from django.contrib import admin
from django.db import transaction
from datetime import date
from .models import Book, BookIssue, PasswordReset

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'issue_date', 'due_date', 'returned', 'fine_display', 'active_issues')
    list_editable = ('returned',)
    actions = ['mark_as_returned']

    @admin.display(description="Active Issues")
    def active_issues(self, obj):
        return BookIssue.objects.filter(user=obj.user, returned=False).count()

    @admin.display(description="Fine")
    def fine_display(self, obj):
        if not obj.returned and (date.today() > obj.due_date):
            overdue_days = (date.today() - obj.due_date).days
            return f"{overdue_days * 2:.2f}"  # Fine is 2 per overdue day
        return obj.fine

    @admin.action(description="Mark selected books as returned")
    def mark_as_returned(self, request, queryset):
        with transaction.atomic():
            for issue in queryset:
                if not issue.returned:
                    issue.returned = True
                    issue.save()
        self.message_user(request, "Selected books marked as returned successfully.")

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if it's a new BookIssue
            # Automatically set the due date to 28 days after issue_date if not already set
            if not obj.due_date:
                obj.due_date = obj.issue_date + timedelta(days=28)
        super().save_model(request, obj, form, change)

# Other models
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'available_copies')

admin.site.register(PasswordReset)


# @admin.register(BookIssue)
# class BookIssueAdmin(admin.ModelAdmin):
#     list_display = ('user', 'book', 'issue_date', 'due_date', 'returned', 'fine_display', 'active_issues')
#     list_editable = ('returned',)
#     actions = ['mark_as_returned']

#     @admin.display(description="Active Issues")
#     def active_issues(self, obj):
#         return BookIssue.objects.filter(user=obj.user, returned=False).count()

#     @admin.display(description="Fine")
#     def fine_display(self, obj):
#         # If the book is not returned and the due date is passed, calculate the fine
#         if not obj.returned and (date.today() > obj.due_date):
#             overdue_days = (date.today() - obj.due_date).days
#             return f"{overdue_days * 2:.2f}"  # Fine is 2 points per overdue day
#         return f"{obj.fine:.2f}"  # Return the stored fine

#     @admin.action(description="Mark selected books as returned")
#     def mark_as_returned(self, request, queryset):
#         with transaction.atomic():
#             for issue in queryset:
#                 if not issue.returned:
#                     issue.returned = True
#                     issue.save()
#         self.message_user(request, "Selected books marked as returned successfully.")

#     def save_model(self, request, obj, form, change):
#         # Automatically set the due_date to 28 days from issue_date if not already set
#         if not obj.due_date:
#             obj.due_date = obj.issue_date + timedelta(days=28)
        
#         # Validation: Ensure the user hasn't exceeded the 5 active book limit
#         if not obj.pk:  # Only validate when creating a new book issue
#             if BookIssue.objects.filter(user=obj.user, returned=False).count() >= 5:
#                 raise ValidationError(f"{obj.user} already has 5 books issued and cannot issue more.")
        
#         # Ensure the book has available copies
#         if obj.book.available_copies <= 0:
#             raise ValidationError(f"No copies of '{obj.book}' are available for issuing.")
        
#         # Decrease the available copies of the book
#         if not change:
#             obj.book.available_copies -= 1
#             obj.book.save()

#         super().save_model(request, obj, form, change)

# # Other models
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'category', 'available_copies')

# admin.site.register(PasswordReset)
