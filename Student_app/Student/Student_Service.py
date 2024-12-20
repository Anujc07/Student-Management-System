from django.contrib import messages
from Student_app.models import Student, Program, Branch

def create_student(request):
    """Method to create a new student"""
    name = request.POST['name']
    class_name = request.POST['class_name']
    roll_no = request.POST['roll_no']
    dob = request.POST['dob']
    parent_contact = request.POST['parent_contact']
    adhaar_no = request.POST['adhaar_no']
    father_name = request.POST['father_name']
    address = request.POST['address']
    program_id = request.POST['program']
    branch_id = request.POST['branch']
    tenth_marksheet = request.FILES.get('tenth_marksheet')
    twelfth_marksheet = request.FILES.get('twelfth_marksheet')

    try:
        program = Program.objects.get(id=program_id)
        branch = Branch.objects.get(id=branch_id)
        student = Student.objects.create(
            name=name,
            class_name=class_name,
            roll_no=roll_no,
            dob=dob,
            parent_contact=parent_contact,
            adhaar_no=adhaar_no,
            father_name=father_name,
            address=address,
            tenth_marksheet=tenth_marksheet,
            twelfth_marksheet=twelfth_marksheet,
            program=program,
            branch=branch
        )
        student.save()
        return "Student added successfully!"
    except Program.DoesNotExist:
        return "Program not found."
    except Branch.DoesNotExist:
        return "Branch not found."
    except Exception as e:
        return f"Error adding student: {e}"

def edit_student(request, student_id):
    """Method to edit an existing student"""

    try:
        student = Student.objects.get(id=student_id)
        student.name = request.POST.get('name', student.name)
        student.class_name = request.POST.get('class_name', student.class_name)
        student.roll_no = request.POST.get('roll_no', student.roll_no)
        student.dob = request.POST.get('dob', student.dob)
        student.parent_contact = request.POST.get('parent_contact', student.parent_contact)
        student.adhaar_no = request.POST.get('adhaar_no', student.adhaar_no)
        student.father_name = request.POST.get('father_name', student.father_name)
        student.address = request.POST.get('address', student.address)
        program_id = request.POST.get('program', None)
        branch_id = request.POST.get('branch', None)
        
        if program_id:
            student.program = Program.objects.get(id=program_id)
        if branch_id:
            student.branch = Branch.objects.get(id=branch_id)
        
        student.tenth_marksheet = request.FILES.get('tenth_marksheet', student.tenth_marksheet)
        student.twelfth_marksheet = request.FILES.get('twelfth_marksheet', student.twelfth_marksheet)
        
        student.save()
        return "Student updated successfully!"
    except Student.DoesNotExist:
        return "Student not found."
    except Program.DoesNotExist:
        return "Program not found."
    except Branch.DoesNotExist:
        return "Branch not found."
    except Exception as e:
        return f"Error updating student: {e}"

def delete_student(student_id):
    """Method to delete a student"""
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return "Student deleted successfully!"
    except Student.DoesNotExist:
        return "Student not found."
    except Exception as e:
        return f"Error deleting student: {e}"


def filter_students(student_name=None, program_name=None, branch_name=None):
    """
    Filters students based on the provided criteria.
    :param student_name: Filter by student name (partial match).
    :param program_name: Filter by program name (partial match).
    :param branch_name: Filter by branch name (partial match).
    :return: Queryset of filtered students.
    """
    students = Student.objects.all()
    if student_name:
        students = students.filter(name__icontains=student_name)
    if program_name:
        students = students.filter(program__name__icontains=program_name)
    if branch_name:
        students = students.filter(branch__name__icontains=branch_name)
    return students