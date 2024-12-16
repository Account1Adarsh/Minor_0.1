from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid
from django.utils.timezone import now

class LoginStreak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    consecutive_days = models.PositiveIntegerField(default=1)

    def update_streak(self):
        """
        Update the consecutive streak count based on the user's last login.
        """
        last_login = LoginStreak.objects.filter(
            user=self.user
        ).order_by('-date').first()

        if last_login and (self.date - last_login.date == timedelta(days=1)):
            # Increment the streak if last login was the day before
            self.consecutive_days = last_login.consecutive_days + 1
        else:
            # Reset streak if there's no login for the previous day
            self.consecutive_days = 1

    def save(self, *args, **kwargs):
        self.update_streak()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date} - Streak: {self.consecutive_days}"


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
    
from datetime import timedelta, date
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    available_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from datetime import date

from datetime import timedelta

from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from datetime import date

from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from datetime import date
from datetime import timedelta

from datetime import timedelta
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from datetime import date

# class BookIssue(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     issue_date = models.DateField(auto_now_add=True)
#     due_date = models.DateField()
#     returned = models.BooleanField(default=False)
#     fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

#     def clean(self):
#     # Ensure that due_date and issue_date are not None and due_date is later than issue_date
#         if self.issue_date and self.due_date:
#             if self.due_date <= self.issue_date:
#                 raise ValidationError({
#                     'due_date': _("Due date must be later than the issue date.")
#                 })

#     def save(self, *args, **kwargs):
#         # Use a transaction to ensure atomic updates
#         with transaction.atomic():
#             if not self.pk:  # Only validate on new issues
#                 # Automatically set due_date to 28 days from issue_date if not set
#                 if not self.due_date:
#                     self.due_date = self.issue_date + timedelta(days=28)
                
#                 # Check if the user has already issued 5 books
#                 active_issues = BookIssue.objects.filter(user=self.user, returned=False).count()
#                 if active_issues >= 5:
#                     raise ValidationError(_(f"{self.user} already has 5 books issued and cannot issue more."))

#                 # Check if the book has available copies
#                 if self.book.available_copies > 0:
#                     self.book.available_copies -= 1  # Decrease available copies
#                     self.book.save()
#                 else:
#                     raise ValidationError(_(f"No copies of '{self.book}' are available for issuing."))

#             elif self.returned:  # Handle book return
#                 # Update fine if overdue
#                 overdue_days = (date.today() - self.due_date).days
#                 if overdue_days > 0:
#                     self.fine = overdue_days * 2  # Fine is 2 points per overdue day

#                 # Update book availability if not already returned
#                 if not BookIssue.objects.filter(pk=self.pk, returned=True).exists():
#                     self.book.available_copies += 1  # Increase available copies
#                     self.book.save()

#             super().save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         # Handle deletion of an unreturned book issue
#         with transaction.atomic():
#             if not self.returned:
#                 self.book.available_copies += 1
#                 self.book.save()
#             super().delete(*args, **kwargs)

#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(due_date__gt=models.F('issue_date')),
#                 name='check_due_date_after_issue_date'
#             )
#         ]

from datetime import timedelta
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BookIssue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Automatically set due_date to 28 days from issue_date if not set
        if not self.pk:  # Only on new BookIssue
            if not self.due_date:
                self.due_date = self.issue_date + timedelta(days=28)

            # Check if the user has already issued 5 books
            active_issues = BookIssue.objects.filter(user=self.user, returned=False).count()
            if active_issues >= 5:
                raise ValidationError(_(f"{self.user} already has 5 books issued and cannot issue more."))

            # Check if the book has available copies
            if self.book.available_copies > 0:
                self.book.available_copies -= 1  # Decrease available copies
                self.book.save()
            else:
                raise ValidationError(_(f"No copies of '{self.book}' are available for issuing."))

        elif self.returned:  # Handle book return
            # Update fine if overdue
            overdue_days = (date.today() - self.due_date).days
            if overdue_days > 0:
                self.fine = overdue_days * 2  # Fine is 2 points per overdue day

            # Update book availability if not already returned
            if not BookIssue.objects.filter(pk=self.pk, returned=True).exists():
                self.book.available_copies += 1  # Increase available copies
                self.book.save()

        super().save(*args, **kwargs)

    # def clean(self):
    #     # Ensure that due_date and issue_date are not None and due_date is later than issue_date
    #     if self.issue_date and self.due_date:
    #         if self.due_date <= self.issue_date:
    #             raise ValidationError({
    #                 'due_date': _("Due date must be later than the issue date.")
    #             })

    def days_left(self):
        if self.returned:
            return 0
        return (self.due_date - date.today()).days

    def delete(self, *args, **kwargs):
        # Handle deletion of an unreturned book issue
        if not self.returned:
            self.book.available_copies += 1
            self.book.save()
        super().delete(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(due_date__gt=models.F('issue_date')),
                name='check_due_date_after_issue_date'
            )
        ]


# class BookIssue(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     issue_date = models.DateField(auto_now_add=True)
#     due_date = models.DateField()
#     returned = models.BooleanField(default=False)
#     fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

#     def save(self, *args, **kwargs):
#         if not self.pk:  # Only validate on new issues
#             # Check if the user has already issued 5 books
#             active_issues = BookIssue.objects.filter(user=self.user, returned=False).count()
#             if active_issues >= 5:
#                 raise ValidationError(f"{self.user} already has 5 books issued and cannot issue more.")
            
#             # Check if the book has available copies
#             if self.book.available_copies > 0:
#                 self.book.available_copies -= 1  # Decrease available copies
#                 self.book.save()
#             else:
#                 raise ValidationError(f"No copies of '{self.book}' are available for issuing.")
        
#         elif self.returned:  # Handle book return
#             if not BookIssue.objects.filter(pk=self.pk, returned=True).exists():
#                 self.book.available_copies += 1  # Increase available copies
#                 self.book.save()

#         super().save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         if not self.returned:  # Return a copy if deleting an unreturned issue
#             self.book.available_copies += 1
#             self.book.save()
#         super().delete(*args, **kwargs)


# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     category = models.CharField(max_length=100)
#     available_copies = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return self.title


# class BookIssue(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     issue_date = models.DateField(auto_now_add=True)
#     due_date = models.DateField(default=date.today() + timedelta(days=28))
#     returned = models.BooleanField(default=False)

#     def days_left(self):
#         if self.returned:
#             return 0
#         return max((self.due_date - date.today()).days, 0)

#     def fine(self):
#         overdue_days = max((date.today() - self.due_date).days, 0)
#         return overdue_days * 2
    
#     def issue_book(self):
#         if self.book.available_copies > 0:
#             self.book.available_copies -= 1
#             self.book.save()
#         else:
#             raise ValueError("No available copies to issue the book.")
    
#     def return_book(self):
#         self.returned = True
#         self.book.available_copies += 1
#         self.book.save()
#         self.save() 


