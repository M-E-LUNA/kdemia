from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de categoría")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del curso")
    slug = models.SlugField(unique=True, blank=True, help_text="Se genera solo, o puedes personalizarlo")
    badge_label = models.CharField(max_length=50, default="Curso TESOEM", verbose_name="Etiqueta superior (ej. Curso TESOEM)")
    partner = models.CharField(max_length=150, default="TESOEM", verbose_name="Aliado / Institución (ej. Microsoft, TESOEM)")
    description = models.TextField(verbose_name="Descripción breve (para la tarjeta)")
    cover_image = models.ImageField(upload_to='courses/covers/', verbose_name="Imagen de portada", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="courses", verbose_name="Categoría")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules", verbose_name="Curso")
    title = models.CharField(max_length=200, verbose_name="Título del módulo (ej. Módulo 1)")
    order = models.PositiveIntegerField(default=1, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons", verbose_name="Módulo")
    title = models.CharField(max_length=200, verbose_name="Título de la lección")
    order = models.PositiveIntegerField(default=1, verbose_name="Número u orden")
    
    # Soporta video directo desde tu PC O enlace web
    video_file = models.FileField(upload_to='courses/videos/', blank=True, null=True, verbose_name="Subir video o GIF desde tu PC")
    video_url = models.URLField(blank=True, null=True, verbose_name="O enlace de video (YouTube/Vimeo/etc.)")
    
    content = models.TextField(verbose_name="Contenido explicativo de la lección", help_text="Puedes escribir texto normal o código HTML")
    practical_example = models.TextField(blank=True, null=True, verbose_name="Caja de ejemplo práctico (Opcional)", help_text="Aparecerá en el bloque destacado abajo")

    class Meta:
        verbose_name = "Lección"
        verbose_name_plural = "Lecciones"
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} -> {self.title}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Progreso de Usuario"
        verbose_name_plural = "Progresos de Usuarios"
        unique_together = ('user', 'lesson')