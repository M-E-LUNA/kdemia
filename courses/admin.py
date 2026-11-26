from django.contrib import admin
from .models import Category, Course, Module, Lesson, UserProgress

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'partner', 'category', 'created_at')
    search_fields = ('title', 'partner', 'description')
    list_filter = ('category',)
    inlines = [ModuleInline]

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    list_filter = ('module__course', 'module')
    search_fields = ('title', 'content')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'updated_at')