

from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, ListView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from .decorators import lecturer_required, student_required, admin_required
from course.models import Course

from app.models import Session, Semester
from .forms import StaffAddForm, StudentAddForm, ProfileUpdateForm, ParentAddForm
from .models import User, Student, Parent


def validate_username(request):
    username = request.GET.get("username", None)
    data = {
        "is_taken": User.objects.filter(username__iexact = username).exists()
    }
    return JsonResponse (data)


def register(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cuenta creada con éxito.')
        else:
            messages.error(request, f'Algo no es correcto, por favor complete todos los campos correctamente.')
    else:
        form = StudentAddForm(request.POST)
    return render(request, "registration/register.html", {'form': form})


@login_required
def profile(request):
    """ Mostrar el perfil de cualquier usuario que envíe la solicitud"""
    try:
        current_session = get_object_or_404(Session, is_current_session=True)
        current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
        
    except Semester.MultipleObjectsReturned and Semester.DoesNotExist and Session.DoesNotExist:
        raise Http404

    if request.user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(
            semester=current_semester)
        return render(request, 'accounts/profile.html', {
            'title': request.user.get_full_name,
            "courses": courses,
            'current_session': current_session,
            'current_semester': current_semester,
        })
    elif request.user.is_student:
        level = Student.objects.get(student__pk=request.user.id)
        try:
            parent = Parent.objects.get(student=level)
        except:
            parent = "no parent set"
        courses = TakenCourse.objects.filter(student__student__id=request.user.id, course__level=level.level)
        context = {
            'title': request.user.get_full_name,
            'parent': parent,
            'courses': courses,
            'level': level,
            'current_session': current_session,
            'current_semester': current_semester,
        }
        return render(request, 'accounts/profile.html', context)
    else:
        staff = User.objects.filter(is_lecturer=True)
        return render(request, 'accounts/profile.html', {
            'title': request.user.get_full_name,
            "staff": staff,
            'current_session': current_session,
            'current_semester': current_semester,
        })


@login_required
@admin_required
def profile_estado(request, id):
    """ Show profile of any selected user """
    if request.user.id == id:
        return redirect("/profile/")

    current_session = get_object_or_404(Session, is_current_session=True)
    current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
    user = User.objects.get(pk=id)
    if user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=id).filter(semester=current_semester)
        context = {
            'title': user.get_full_name,
            "user": user,
            "user_type": "Lecturer",
            "courses": courses,
            'current_session': current_session,
            'current_semester': current_semester,
        }
        return render(request, 'accounts/prifile_estado.html', context)
    elif user.is_student:
        student = Student.objects.get(student__pk=id)
        courses = TakenCourse.objects.filter(student__student__id=id, course__level=student.level)
        context = {
            'title': user.get_full_name,
            'user': user,
            "user_type": "student",
            'courses': courses,
            'student': student,
            'current_session': current_session,
            'current_semester': current_semester,
        }
        return render(request, 'accounts/profile_estado.html', context)
    else:
        context = {
            'title': user.get_full_name,
            "user": user,
            "user_type": "superuser",
            'current_session': current_session,
            'current_semester': current_semester,
        }
        return render(request, 'accounts/profile_estado.html', context)


@login_required
@admin_required
def admin_panel(request):
    return render(request, 'setting/admin_panel.html', {})
# ########################################################


# ########################################################
# Setting views
# ########################################################
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrija los siguientes errores.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'setting/profile_info_change.html', {
        'title': 'Setting | DjangoSMS',
        'form': form,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Su contraseña se actualizó con éxito!')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrija los siguientes errores. ')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'setting/password_change.html', {
        'form': form,
    })
# ########################################################

@login_required
@admin_required
def staff_add_view(request):
    if request.method == 'POST':
        form = StaffAddForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if form.is_valid():
            form.save()
            messages.success(request, "Account for lecturer " + first_name + ' ' + last_name + " has been created.")
            return redirect("estudiante_lista")
    else:
        form = StaffAddForm()

    context = {
        'title': 'Agregar tutores',
        'form': form,
    }

    return render(request, 'accounts/add_administrador.html', context)


@login_required
@admin_required
def edit_staff(request, pk):
    instance = get_object_or_404(User, is_lecturer=True, pk=pk)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, 'Estudiante ' + full_name + ' Ha sido actualizado.')
            return redirect('estudiante_lista')
        else:
            messages.error(request, 'Corrija el error a continuación.')
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(request, 'accounts/edit_estudiante.html', {
        'title': 'Editar Estudiante',
        'form': form,
    })


@method_decorator([login_required, admin_required], name='dispatch')
class LecturerListView(ListView):
    queryset = User.objects.filter(is_lecturer=True)
    template_name = "accounts/estudiante_lista.html"
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Estudiante"
        return context


# @login_required
# @lecturer_required
# def delete_staff(request, pk):
#     staff = get_object_or_404(User, pk=pk)
#     staff.delete()
#     return redirect('lecturer_list')

@login_required
@admin_required
def delete_staff(request, pk):
    lecturer = get_object_or_404(User, pk=pk)
    full_name = lecturer.get_full_name
    lecturer.delete()
    messages.success(request, 'Estudiante ' + full_name + ' Ha sido actualizado.')
    return redirect('estudiante_lista')
# ########################################################


# ########################################################
# Student views
# ########################################################
@login_required
@admin_required
def student_add_view(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta para' + first_name + ' ' + last_name + 'Ha sido creado.')
            return redirect('student_list')
        else:
            messages.error(request, 'Corrija los errores a continuación.')
    else:
        form = StudentAddForm()

    return render(request, 'accounts/add_student.html', {
        'title': "Agregar",
        'form': form
    })


@login_required
@admin_required
def edit_student(request, pk):
    # instance = User.objects.get(pk=pk)
    instance = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, ('Alumno ' + full_name + ' Ha sido actualizado.'))
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(request, 'accounts/edit_student.html', {
        'title': 'Edit-profile | DjangoSMS',
        'form': form,
    })


@method_decorator([login_required, admin_required], name='dispatch')
class StudentListView(ListView):
    template_name = "accounts/student_list.html"
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        queryset = Student.objects.all()
        query = self.request.GET.get('student_id')
        if query is not None:
            queryset = queryset.filter(Q(department=query))
        return queryset



@login_required
@admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # full_name = student.user.get_full_name
    student.delete()
    messages.success(request, 'Student has been deleted.')
    return redirect('student_list')
# ########################################################


class ParentAdd(CreateView):
    model = Parent
    form_class = ParentAddForm
    template_name = 'accounts/parent_form.html'


# def parent_add(request):
#     if request.method == 'POST':
#         form = ParentAddForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('student_list')
#     else:
#         form = ParentAddForm(request.POST)
