from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Trainer, Customer, User, CustomerTrainer, Category, Train, Schedule


class TrainerProfileInline(admin.StackedInline):
    model = Trainer
    can_delete = False


class CustomerProfileInline(admin.StackedInline):
    model = Customer
    can_delete = False


class ExtendedUserAdmin(UserAdmin):
    inlines = (TrainerProfileInline, CustomerProfileInline)
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Added Fields',
            {
                "fields":
                    (
                        "type",
                    )
            },
        ),
    )


admin.site.register(User, ExtendedUserAdmin)
admin.site.register(CustomerTrainer)
admin.site.register(Category)
admin.site.register(Train)
admin.site.register(Schedule)
