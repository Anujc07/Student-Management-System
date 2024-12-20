from Student_app.models import Teacher, Branch
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404



def list_teachers(teacher_name=None, subject=None, branch_id=None):
    """
    Returns a queryset of teachers filtered by teacher_name, subject, and branch.
    """
    teachers = Teacher.objects.all()

    if teacher_name:
        teachers = teachers.filter(name__icontains=teacher_name)
    if subject:
        teachers = teachers.filter(subject__icontains=subject)
    if branch_id:
        teachers = teachers.filter(assigned_branch_id=branch_id)

    return teachers


def create_teacher(username, password, name, email, contact_number, subject, hire_date, qualification, assigned_branch_id, address):
    """
    Creates a teacher with the provided details and returns the created teacher.
    """
    try:
        # Create user in auth_user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True  # Mark as staff
        user.save()

        # Fetch assigned branch
        assigned_branch = Branch.objects.get(id=assigned_branch_id) if assigned_branch_id else None

        # Create teacher in Teacher table
        teacher = Teacher.objects.create(
            user=user,
            name=name,
            email=email,
            contact_number=contact_number,
            subject=subject,
            hire_date=hire_date,
            address=address,
            qualification=qualification,
            assigned_branch=assigned_branch,
        )
        teacher.save()
        return teacher
    except Exception as e:
        raise e


def update_teacher(data):
    teacher_id = data.get('teacher_id')
    teacher = get_object_or_404(Teacher, id=teacher_id)

    teacher.name = data.get('name')
    teacher.email = data.get('email')
    teacher.contact_number = data.get('contact_number')
    teacher.subject = data.get('subject')
    teacher.hire_date = data.get('hire_date')
    teacher.assigned_branch = Branch.objects.get(id=data.get('assigned_branch')) if data.get('assigned_branch') else None

    teacher.save()
    return teacher