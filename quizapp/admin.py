from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Choice, Question, Category, PersonalCare,
QuizModal, Customer, Hydration, Concerns, Products)

"""
@admin.register(Choice)
class ChoiceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'choice_text', 'marks')
    list_filter = ['choice_text']
    search_fields = ['choice_text']
"""


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    # fk_name = "question"
    # fieldsets = [
    #    (None, {'fields': ['choice_text', 'marks']}),
    # ]
    exclude = ('votes',)
    can_delete = True


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'category', 'pc_name')
    list_filter = ['pub_date', 'category']
    search_fields = ['name', 'category__name', 'category__personalcare__name']
    list_display_links = ['name']
    ordering = ('code',)
    # list_editable = ['code', ]
    # prepopulated_fields = {"name": ("name",)}

    fieldsets = [
        ('Question Information', {'fields': [('code', 'name', 'category')]}),
        # ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    def pc_name(self, obj):
        """return choice question"""
        return obj.category.personalcare.name


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'code', 'name', 'personalcare')
    list_filter = ['name']
    search_fields = ['personalcare']
    list_display_links = ['code', 'name']
    ordering = ('code',)


@admin.register(QuizModal)
class QuizModalAdmin(ImportExportModelAdmin):
    list_display = ('question_code', 'question', 'choice', 'marks', 'customer', 'pub_date')
    list_filter = ['customer']
    search_fields = ['choice', 'customer__name']

    def question(self, obj):
        """return choice question"""
        return obj.choice.question
    
    def question_code(self, obj):
        """return choice question"""
        return obj.choice.question.code

    def marks(self, obj):
        """return user email"""
        return obj.choice.marks


@admin.register(PersonalCare)
class PersonalCareAdmin(ImportExportModelAdmin):
    list_display = ('id', 'code', 'name')
    list_filter = ['name']
    list_display_links = ['code', 'name']
    search_fields = ['name']
    ordering = ('code',)


@admin.register(Customer)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('employee_id', 'name', 'gender', 'age', 'location')
    list_filter = ['name']
    search_fields = ['employee_id', 'name']


@admin.register(Hydration)
class HydrationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'customer', 'weight','physical_activity', 'water_intake', 'status')
    list_filter = ['customer', 'status']
    list_display_links = ['customer', 'status']
    search_fields =  ['customer', 'status']


@admin.register(Concerns)
class ConcernsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'customer', 'is_primary')
    list_filter = ['customer']
    list_display_links = ['customer']
    search_fields =  ['customer']


@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    list_display = ('code', 'title', 'cleanser', 'moisturizer', 'serum')
    list_filter = ['title']
    list_display_links = ['code', 'title']
    search_fields = ['code', 'title', 'cleanser', 'moisturizer', 'serum']
