from Student_app.models import Subject, Branch, Program, Teacher
from django.db.models import Q
from ..Services import get_entries


def get_filtered_subjects(subject_name=None, semester=None, subject_code=None, branch_id=None):
    """
    Retrieves the list of subjects filtered by subject name, semester, subject code, and branch.
    """
    subjects = Subject.objects.all()

    if subject_name:
        subjects = subjects.filter(name__icontains=subject_name)

    if semester:
        subjects = subjects.filter(semester=semester)

    if subject_code:
        subjects = subjects.filter(code__icontains=subject_code)

    if branch_id:
        subjects = subjects.filter(branch__id=branch_id)

    return subjects


def edit_subject(subject_id, data):
    """
    Updates a subject's details based on the provided data dictionary.
    """
    try:
        subject = Subject.objects.get(id=subject_id)
        subject.name = data.get('name', subject.name)
        subject.code = data.get('code', subject.code)
        subject.description = data.get('description', subject.description)
        subject.semester = data.get('semester', subject.semester)
        subject.credits = data.get('credits', subject.credits)
        subject.is_elective = data.get('is_elective', subject.is_elective)
        subject.branch_id = data.get('branch', subject.branch_id)
        subject.teachers_id = data.get('teachers', subject.teachers_id)

        subject.save()
        return subject
    except Subject.DoesNotExist:
        return None


def add_subject(data):
    """
    Adds a new subject based on the provided data.
    """
    try:
        branch = get_entries('Branch', pk=data['branch'])
        program = get_entries('Program', pk=data['program'])
        teacher = get_entries('Teacher', pk=data['teachers'])
        semester = int(data['semester'])
        credits = int(data['credits'])
        is_elective = data['is_elective'] == 'True'
        
        Subject.objects.create(
            name=data['name'],
            code=data['code'],
            description=data.get('description', ''),
            branch=branch,
            program=program,
            semester=semester,
            credits=credits,
            is_elective=is_elective,
            teachers=teacher
        )
        return True, 'Subject added successfully!'
    except Branch.DoesNotExist:
        return False, 'Branch not found.'
    except Program.DoesNotExist:
        return False, 'Program not found.'
    except Teacher.DoesNotExist:
        return False, 'Teacher not found.'
    except Exception as e:
        return False, f'An error occurred: {str(e)}'