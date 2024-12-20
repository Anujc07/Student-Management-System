from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Q
import json
from django.utils.timezone import now
from django.db import IntegrityError
from django.core.serializers.json import DjangoJSONEncoder
from .Branch.Branch_Service import get_branch_by_id, update_branch, delete_branch
from .Program.Program_Service import add_program, edit_program, delete_program, search_programs
from .Student.Student_Service import edit_student, create_student, delete_student, filter_students
# from .Services import get_all_branches, get_all_subject, get_program, get_all_teachers, get_teacher, get_all_program
from .Services import get_entries
from .Teacher.Teacher_Service import list_teachers, create_teacher, update_teacher
from .Subject.Subject_Service import add_subject, get_filtered_subjects, edit_subject   
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            request.session['username'] = user.username
            request.session['is_staff'] = user.is_staff
            teacher = getattr(user, 'teacher_profile', None)
            if teacher:
                request.session['teacher_id'] = teacher.id
                if teacher.assigned_branch:
                    request.session['branch_id'] = teacher.assigned_branch.id
                else:
                    request.session['branch_id'] = None 
            login(request, user)
            return redirect('./Add-Program') 
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('./login')

def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('create_user')

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "User created successfully.")
            return redirect('login')
        except  Exception as e:
            messages.error(request, "An error occurred while creating the user.")
            return redirect('create_user')

    return render(request, 'create_user.html')


# def Add_Program(request):
#     if request.method == 'POST':
#         program_name = request.POST.get('program_name')
#         duration = request.POST.get('duration')
#         semsters = request.POST.get('semsters')

#         if not program_name or not duration:
#             messages.error(request, 'All fields are required.')
#             return redirect('Add-Program')

#         try:
#             duration = Decimal(duration)
#             Program.objects.create(name=program_name, duration=duration, semsters=semsters)
#             messages.success(request, 'Program added successfully!')
#         except ValueError:
#             messages.error(request, 'Duration must be a valid number.')
#         except Exception as e:
#             messages.error(request, f'Error adding program: {e}')

#         return redirect('/student/Add-Program')
#     return render(request, "Masters/Add_Program.html" )

# This is program methods
def Add_Program(request):
    if request.method == 'POST':
        program_name = request.POST.get('program_name')
        duration = request.POST.get('duration')
        semsters = request.POST.get('semsters')

        if not program_name or not duration:
            messages.error(request, 'All fields are required.')
            return redirect('Add-Program')

        try:
            duration = float(duration)
            add_program(name=program_name, duration=duration, semsters=semsters)
            messages.success(request, 'Program added successfully!')
        except ValueError:
            messages.error(request, 'Duration must be a valid number.')
        except Exception as e:
            messages.error(request, f'Error adding program: {e}')

        return redirect('Add-Program')
    return render(request, "Masters/Add_Program.html")


def Edit_Program(request, program_id):
    program = get_object_or_404(Program, id=program_id)

    if request.method == 'POST':
        program_name = request.POST.get('name')
        duration = request.POST.get('duration')
        semsters = request.POST.get('semsters')

        if not program_name or not duration:
            messages.error(request, 'All fields are required.')
            return redirect('Program_List')

        try:
            duration = float(duration)
            edit_program(program_id=program_id, name=program_name, duration=duration, semsters=semsters)
            messages.success(request, 'Program updated successfully!')
        except ValueError:
            messages.error(request, 'Duration must be a valid number.')
        except Exception as e:
            messages.error(request, f'Error editing program: {e}')

        return redirect('Program_List')
    return render(request, "Masters/Edit_Program.html", {'program': program})


def Delete_Program(request, program_id):
    try:
        delete_program(program_id=program_id)
        messages.success(request, 'Program deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting program: {e}')
    return redirect('Program-List')


def Program_List(request):
    name = request.GET.get('name')
    duration = request.GET.get('duration')
    semsters = request.GET.get('semesters')
    programs = search_programs(name=name, duration=duration, semsters=semsters)
    return render(request, "Masters/Program_List.html", {'programs': programs})



# This is student methods

# def Add_Student(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         class_name = request.POST['class_name']
#         roll_no = request.POST['roll_no']
#         dob = request.POST['dob']
#         parent_contact = request.POST['parent_contact']
#         adhaar_no = request.POST['adhaar_no']
#         father_name = request.POST['father_name']
#         address = request.POST['address']
#         program_id = request.POST['program']
#         branch_id = request.POST['branch']
#         tenth_marksheet = request.FILES.get('tenth_marksheet')
#         twelfth_marksheet = request.FILES.get('twelfth_marksheet')

#         try:
#             program = Program.objects.get(id=program_id)
#             branch = Branch.objects.get(id=branch_id)
#             student = Student.objects.create(
#                 name=name,
#                 class_name=class_name,
#                 roll_no=roll_no,
#                 dob=dob,
#                 parent_contact=parent_contact,
#                 adhaar_no=adhaar_no,
#                 father_name=father_name,
#                 address=address,
#                 tenth_marksheet=tenth_marksheet,
#                 twelfth_marksheet=twelfth_marksheet,
#                 program=program,
#                 branch=branch
#             )
            
#             student.save()
#             messages.success(request, "Student added successfully!")
#             return redirect('add_student')
#         except Program.DoesNotExist:
#             messages.error(request, "Program not found.")
#         except Branch.DoesNotExist:
#             messages.error(request, "Branch not found.")
#         except Exception as e:
            
#             messages.error(request, f"Error adding student: {e}")
        
#     programs = Program.objects.all()
#     branches = Branch.objects.all()
#     return render(request, 'Masters/Add_Student.html', {'programs': programs, 'branches': branches})



# def Student_List(request):
#     student = Student.objects.all()

#     return render(request, 'Masters/Student_List.html', {"students":student})


def Add_Student(request):
    """View to add a student"""
    if request.method == 'POST':
        result = create_student(request)
        if "successfully" in result:
            messages.success(request, result)
            return redirect('add_student')
        else:
            messages.error(request, result)

    programs = get_entries('Program')
    branches = get_entries('Branch')
    return render(request, 'Masters/Add_Student.html', {'programs': programs, 'branches': branches})


def Student_List(request):
    """
    View to list students with optional filtering by name, program, and branch.
    """
    student_name = request.GET.get('student_name', '')
    program_name = request.GET.get('program_name', '')
    branch_name = request.GET.get('branch_name', '')

    students = filter_students(student_name, program_name, branch_name)
    programs = Program.objects.all()
    branches = Branch.objects.all()

    return render(request, 'Masters/Student_List.html', {
        "students": students,
        "programs": programs,
        "branches": branches,
        "filters": {
            "student_name": student_name,
            "program_name": program_name,
            "branch_name": branch_name,
        },
    })


def Edit_Student(request, student_id):
    """View to edit an existing student"""
    if request.method == 'POST':
        result = edit_student(request, student_id)
        if "updated successfully" in result:
            messages.success(request, result)
            return redirect('Student_List')
        else:
            messages.error(request, result)
    student = Student.objects.get(id=student_id)
    programs = Program.objects.all()
    branches = Branch.objects.all()
    return render(request, 'Masters/Edit_Student.html', {'student': student, 'programs': programs, 'branches': branches})


def Delete_Student(request, student_id):
    """View to delete a student"""
    result = delete_student(student_id)
    if "deleted successfully" in result:
        messages.success(request, result)
    else:
        messages.error(request, result)
    return redirect('Student_List')


# This is branch methods

def Add_Branch(request):
    if request.method == 'POST':
        branch_name = request.POST.get('branch_name')
        program_id = request.POST.get('program')
        
        if not branch_name or not program_id:
            messages.error(request, "All fields are required.")
            return redirect('Add_Branch')
        
        try:
            program =  get_entries('Program', pk=program_id)
            Branch.objects.create(name=branch_name, program=program)
            messages.success(request, "Branch added successfully!")
        except Program.DoesNotExist:
            messages.error(request, "Invalid program selected.")
        except Exception as e:
            messages.error(request, f"Error adding branch: {e}")
        
        return redirect('Add_Branch')
    
    programs = Program.objects.all()
    return render(request, 'Masters/Add_Branch.html', {'programs': programs})



def Branch_List(request):
    filters = {
        'branch_name': request.GET.get('branch_name'),
        'program': request.GET.get('program'),
        'head_of_branch': request.GET.get('head_of_branch'),
    }

    # Remove empty filter keys
    filters = {key: value for key, value in filters.items() if value}

    # Use the generic method to fetch branches
    branches = get_entries('Branch', filters=filters)
    programs = get_entries('Program')
    
    return render(request, 'Masters/Branch_List.html', {'branches': branches, 'programs':programs})



def edit_branch(request, branch_id):
    branch = get_entries('Branch', pk=branch_id)
    if request.method == 'POST':
        update_branch(branch, request.POST)
        messages.success(request, f'Branch "{branch.name}" was successfully updated.')
        return redirect('Branch_List')
    messages.error(request, 'Invalid request.')
    return redirect('Branch_List')



def delete_branch_view(request, branch_id):
    delete_branch(branch_id)
    return redirect('Branch_List')


def Program_List(request):
    program = get_entries('Program')
    return render(request, 'Masters/Program_List.html', {'programs': program})





# def Add_Teacher(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         name = request.POST['name']
#         email = request.POST['email']
#         contact_number = request.POST['contact_number']
#         subject = request.POST['subject']
#         hire_date = request.POST['hire_date']
#         qualification = request.POST.get('qualification', '')
#         assigned_branch_id = request.POST.get('assigned_branch', None)
#         address = request.POST.get('address', '')

#         try:
#             # Create user in auth_user
#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.is_staff = True  # Mark as staff
#             user.save()

#             # Fetch assigned branch
#             assigned_branch = Branch.objects.get(id=assigned_branch_id) if assigned_branch_id else None

#             # Create teacher in Teacher table
#             Teacher.objects.create(
#                 user=user,
#                 name=name,
#                 email=email,
#                 contact_number=contact_number,
#                 subject=subject,
#                 hire_date=hire_date,
#                 address=address,
#                 qualification=qualification,
#                 assigned_branch=assigned_branch,
#             )

#             messages.success(request, "Teacher added successfully!")
#             return redirect('Add_Teacher')

#         except Exception as e:
#             messages.error(request, f"Error: {str(e)}")
#             return redirect('Add_Teacher')

#     branches = Branch.objects.all()
#     return render(request, 'Masters/Add_Teacher.html', {'branches': branches})

def Add_Teacher(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        subject = request.POST['subject']
        hire_date = request.POST['hire_date']
        qualification = request.POST.get('qualification', '')
        assigned_branch_id = request.POST.get('assigned_branch', None)
        address = request.POST.get('address', '')

        try:
            # Call the service method to create a teacher
            create_teacher(
                username=username,
                password=password,
                name=name,
                email=email,
                contact_number=contact_number,
                subject=subject,
                hire_date=hire_date,
                qualification=qualification,
                assigned_branch_id=assigned_branch_id,
                address=address
            )

            messages.success(request, "Teacher added successfully!")
            return redirect('Add_Teacher')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('Add_Teacher')

    # Fetch branches for the dropdown
    branches = get_entries('Branch')
    return render(request, 'Masters/Add_Teacher.html', {'branches': branches})

def Teacher_List(request):
    # Get filter values from request
    teacher_name = request.GET.get('teacher_name', '')
    subject = request.GET.get('subject', '')
    branch_id = request.GET.get('branch', '')

    # Fetch filtered teachers using the service method
    teachers = list_teachers(teacher_name=teacher_name, subject=subject, branch_id=branch_id)

    # Fetch branches for the filter dropdown
    branches = get_entries('Branch')
    subject_list = get_entries('Student')
    # Pass filters back to the template for form value persistence
    return render(request, 'Masters/Teacher_List.html', {
        'teachers': teachers,
        'branches': branches,
        'subject_list': subject_list,
        'filters': {
            'teacher_name': teacher_name,
            'subject': subject,
            'branch': branch_id,
        },
    })


def edit_teacher(request, teacher_id):
    if request.method == "POST":
        try:
            update_teacher(request.POST)
            messages.success(request, "Teacher updated successfully!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return redirect('Teacher_List')




def Add_Subject(request):
    if request.method == 'POST':
        data = request.POST.dict()  # Convert QueryDict to a regular dictionary
        success, message = add_subject(data)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('Add_Subject')

    branches = get_entries('Branch')
    programs = get_entries('Program')
    teachers = get_entries('Teacher')
    return render(request, 'Masters/Add_Subject.html', {'branches': branches, 'programs': programs, 'teachers': teachers})

def subject_list(request):
    """
    View to display the list of subjects with filters.
    """
    name = request.GET.get('name')
    semester = request.GET.get('semester')
    code = request.GET.get('code')
    branch = request.GET.get('branch')

    branches = Branch.objects.all()
    subjects = get_filtered_subjects(name, semester, code, branch)
    teachers = get_entries("Teacher")
    context = {
        'subjects': subjects,
        'branches': branches,
        'teachers': teachers,
        'filters': {
            'name': name,
            'semester': semester,
            'code': code,
            'branch': branch
        }
    }
    return render(request, 'Masters/Subject_List.html', context)

def edit_subject_view(request, subject_id):
    if request.method == 'POST':
        print("====id", subject_id)
        data = {
            'name': request.POST.get('name'),
            'code': request.POST.get('code'),
            'description': request.POST.get('description'),
            'branch': request.POST.get('branch'),
            'semester': request.POST.get('semester'),
            'credits': request.POST.get('credits'),
            'is_elective': request.POST.get('is_elective') == 'True',
            'teachers': request.POST.get('teachers'),
        }
        # Pass subject_id correctly
        success = edit_subject(subject_id=subject_id, data=data)
        if success:
            messages.success(request, 'Subject updated successfully!')
        else:
            messages.error(request, 'Error updating subject.')
        return redirect('subject_list')

    branches = get_entries("Branch")
    teachers = get_entries("Teacher")
    subject = get_entries("Subject")
    context = {
        'subject': subject,
        'branches': branches,
        'teachers': teachers
    }
    return render(request, 'Masters/Add_Subject.html', context)

# def Add_Subject(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         code = request.POST['code']
#         description = request.POST.get('description', '')
#         branch = Branch.objects.get(id=request.POST['branch'])
#         program = Program.objects.get(id=request.POST['program'])
#         semester = int(request.POST['semester'])
#         credits = int(request.POST['credits'])
#         is_elective = request.POST['is_elective'] == 'True'
#         teacher = Teacher.objects.get(id=request.POST['teachers'])
#         Subject.objects.create(
#             name=name, code=code, description=description, 
#             branch=branch, program=program, semester=semester, 
#             credits=credits, is_elective=is_elective,
#             teachers=teacher
#         )
#         messages.success(request, 'Subject added successfully!')
#         return redirect('Add_Subject')

#     branches = get_entries('Branch')
#     programs = get_entries('Program')
#     teacher = get_entries('Teacher')
#     return render(request, 'Masters/Add_Subject.html', {'branches': branches, 'programs': programs, 'teachers':teacher})



def Get_Students(request):
    teacher_id = request.session.get('teacher_id', None)
    teacher_branch = request.session.get('branch_id', None)
    subjects = Subject.objects.filter(teachers_id=teacher_id)
    students = None
    selected_subject_name = None
    attendance_data = {}

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        if subject_id:
            subject = Subject.objects.filter(id=subject_id).first()
            if subject:
                students = Student.objects.filter(Q(semester=subject.semester) & Q(branch_id=teacher_branch))
                request.session['program_id'] = subject.program_id
                request.session['subject_id'] = subject.id
                selected_subject_name = subject.name 
                attendance_record = Attendance.objects.filter(
                    subject_id=subject_id,
                    branch_id=teacher_branch,
                    date=now().day,
                    month=now().month,
                    year=now().year
                ).first()
                if attendance_record:
                    attendance_data = json.loads(
                        attendance_record.student_data
                    )
                    attendance_data = {record["student_id"]: record for record in attendance_data}
    return render(request, 'Attendance/Mark_Attendance.html', {
        "subjects": subjects,
        "students": students,
        "selected_subject_name":selected_subject_name,
          "attendance_data": attendance_data
    })







def Save_Attendance(request):
    if request.method == 'POST':
        attendance_data = []
        student_ids = request.POST.getlist('student_ids') 

        for student_id in student_ids:
            status = request.POST.get(f"status_{student_id}", "not_marked")
            attendance_data.append({
                "student_id": student_id,
                "status": status,
            })
        
        teacher_id = request.session.get('teacher_id')
        program_id = request.session.get('program_id')
        subject_id = request.session.get('subject_id')
        teacher_branch = request.session.get('branch_id')

        # Validation
        if not program_id or not subject_id or not teacher_branch:
            messages.error(request, "Required session data is missing. Please select the subject again.")
            return redirect('Get_Students')

        try:
            attendance_record = Attendance(
                student_data=json.dumps(attendance_data),
                date=now().day,
                month=now().month,
                year=now().year,
                marked_by_id=teacher_id,
                program_id=program_id,
                branch_id=teacher_branch,
                subject_id=subject_id
            )
            attendance_record.save()
            messages.success(request, "Attendance successfully marked.")
        except IntegrityError:
            messages.error(request, "Attendance for this date, subject, and branch has already been marked.")

        return redirect('Get_Students')
    
    
def Add_Book_Type(request):
    programs = Program.objects.all()
    if request.method == "POST":
        program_id = request.POST.get("program") 
        branch_id = request.POST.get("branch")
        book_type = request.POST.get("book_type")
        subject = request.POST.get("subject")

        if program_id and branch_id and book_type and subject:
            program = Program.objects.get(id=program_id)
            branch = Branch.objects.get(id=branch_id)
            book = Book_Type.objects.create(
                program=program,
                branch=branch,
                book_type=book_type,
                subject=subject
            )
            book.save()
            messages.success(request, "Book added successfully!")
            return redirect("Add-Book-Type")
        else:
            messages.error(request, "All fields are required!")

    return render(request, "Masters/Add_Book_Type.html", {"programs": programs})