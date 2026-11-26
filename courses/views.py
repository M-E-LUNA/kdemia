import json
import ssl
import urllib.request
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Course, Module, Lesson, UserProgress

def course_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.prefetch_related('lessons').all()
    all_lessons = list(Lesson.objects.filter(module__course=course).order_by('module__order', 'order'))
    total_lessons = len(all_lessons)
    
    completed_ids = []
    unlocked_ids = []
    progress_percent = 0

    if request.user.is_authenticated:
        completed_ids = list(UserProgress.objects.filter(
            user=request.user,
            lesson__module__course=course,
            completed=True
        ).values_list('lesson_id', flat=True))
        
        if total_lessons > 0:
            progress_percent = int((len(completed_ids) / total_lessons) * 100)

        if request.user.is_staff or request.user.is_superuser:
            unlocked_ids = [l.id for l in all_lessons]
        else:
            if all_lessons:
                unlocked_ids.append(all_lessons[0].id)
                for i in range(1, len(all_lessons)):
                    if all_lessons[i-1].id in completed_ids:
                        unlocked_ids.append(all_lessons[i].id)
                    else:
                        break
    else:
        if all_lessons:
            unlocked_ids.append(all_lessons[0].id)

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'total_lessons': total_lessons,
        'completed_ids': completed_ids,
        'unlocked_ids': unlocked_ids,
        'progress_percent': progress_percent,
    })

def lesson_detail(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    modules = course.modules.prefetch_related('lessons').all()
    
    all_lessons = list(Lesson.objects.filter(module__course=course).order_by('module__order', 'order'))
    current_index = all_lessons.index(lesson)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    if not request.user.is_authenticated and current_index > 0:
        return redirect('login')

    if request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser):
        if current_index > 0:
            prev_completed = UserProgress.objects.filter(
                user=request.user, 
                lesson=all_lessons[current_index - 1], 
                completed=True
            ).exists()
            
            if not prev_completed:
                messages.warning(request, f'La lección "{lesson.title}" está bloqueada. Debes completar las lecciones anteriores primero.')
                return redirect('course_detail', slug=course_slug)

    is_completed = False
    if request.user.is_authenticated:
        is_completed = UserProgress.objects.filter(user=request.user, lesson=lesson, completed=True).exists()

    is_quiz = any(k in lesson.title.lower() for k in ['cuestionario', 'evaluación', 'evaluacion', 'examen', 'quiz'])

    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'modules': modules,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'is_completed': is_completed,
        'is_quiz': is_quiz,
    })

def toggle_lesson_completed(request, course_slug, lesson_id):
    if not request.user.is_authenticated:
        return redirect('login')

    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, _ = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.completed = True
    progress.save()

    all_lessons = list(Lesson.objects.filter(module__course__slug=course_slug).order_by('module__order', 'order'))
    current_index = all_lessons.index(lesson)
    
    if current_index < len(all_lessons) - 1:
        next_lesson = all_lessons[current_index + 1]
        return redirect('lesson_detail', course_slug=course_slug, lesson_id=next_lesson.id)
    else:
        return redirect('course_certificate', slug=course_slug)

def course_certificate(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    course = get_object_or_404(Course, slug=slug)
    all_lessons = list(Lesson.objects.filter(module__course=course))
    total_lessons = len(all_lessons)

    completed_count = UserProgress.objects.filter(
        user=request.user,
        lesson__module__course=course,
        completed=True
    ).count()

    if not (request.user.is_staff or request.user.is_superuser):
        if total_lessons == 0 or completed_count < total_lessons:
            messages.warning(request, "Aún no has completado el 100% del programa para emitir tu certificado.")
            return redirect('course_detail', slug=slug)

    cert_code = f"KD-{datetime.now().year}-{request.user.id:04d}-{course.id:03d}"

    return render(request, 'courses/certificate.html', {
        'course': course,
        'student_name': request.user.get_full_name() or request.user.username,
        'cert_code': cert_code,
        'completion_date': datetime.now(),
    })

@csrf_exempt
def ask_tuzy(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        lesson_id = data.get('lesson_id')

        if not user_message:
            return JsonResponse({'reply': '¡Hola! Escríbeme tu duda para que pueda ayudarte ✨.'})

        lesson = Lesson.objects.filter(id=lesson_id).first()
        course_title = lesson.module.course.title if lesson else "Kdemia"
        category_name = lesson.module.course.category.name if lesson and lesson.module.course.category else "Tecnología"
        lesson_title = lesson.title if lesson else "Clase"
        lesson_content = lesson.content if lesson else "Contenido"

        api_key = getattr(settings, 'GEMINI_API_KEY', '').strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"

        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        payload = {
            "contents": [{
                "parts": [{"text": f"Eres Tuzy, tutora en Kdemia. Responde con cariño y brevedad a la duda de este curso '{course_title}' sobre la lección '{lesson_title}': {user_message}"}]
            }]
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        )

        with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            tuzy_reply = result['candidates'][0]['content']['parts'][0]['text']

        return JsonResponse({'reply': tuzy_reply, 'status': 'ok'})
    except Exception as e:
        return JsonResponse({'reply': 'Lo siento, no puedo responderte en este momento ✨.'})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('course_list')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de username ya está registrado.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('course_list')
    return render(request, 'courses/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('course_list')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'course_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'courses/login.html')

def logout_view(request):
    logout(request)
    return redirect('course_list')

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def kdemia_admin_dashboard(request):
    
    return render(request, 'courses/admin_dashboard.html')