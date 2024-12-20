# from Student_app.models import Teacher, Branch, Subject, Program
# from django.shortcuts import get_object_or_404


# def get_all_subject():
#     """
#     Returns a queryset of all subject.
#     """
#     return Subject.objects.filter(status=1).all()

# def get_all_branches(filters=None):
#     branches = Branch.objects.all()
    
#     if filters:
#         branch_name = filters.get('branch_name')
#         if branch_name: 
#             branches = branches.filter(name__icontains=branch_name)
    
#     return branches

# def get_all_program():
#     program = Program.objects.all()    
#     return program


# def get_program(program_id=None):
#     """
#     Retrieve program(s) based on the provided program_id.
#     If program_id is None, return all programs.
#     """
#     if program_id:
#         return get_object_or_404(Program, id=program_id)
#     return Program.objects.all()


# def get_all_teachers():
#     """
#     Returns a queryset of all teacher.
#     """
#     return Teacher.objects.filter(status=1).all()

# def get_teacher(teacher_id=None):
#     """
#     Retrieve a teacher based on the provided teacher_id.
#     Returns a single Teacher instance or None if not found.
#     """
#     return Teacher.objects.filter(id=teacher_id).first()

from django.apps import apps
from django.shortcuts import get_object_or_404


def get_entries(model_name, filters=None, pk=None):
    """
    Retrieve entries from a specified model as dictionaries.

    Args:
        model_name (str): The name of the model (e.g., 'Program', 'Branch').
        filters (dict, optional): Filters for querying the model. Defaults to None.
        pk (int, optional): Primary key to fetch a single entry. Defaults to None.

    Returns:
        dict or list of dict: Returns a dictionary for a single instance or a list of dictionaries for multiple instances.
    """
    try:
        # Dynamically get the model class
        model = apps.get_model('Student_app', model_name)

        if pk:
            # Fetch a single instance and return it as a dictionary
            obj = get_object_or_404(model, pk=pk)
            return vars(obj)

        # Fetch all entries and return them as a list of dictionaries
        queryset = model.objects.filter(**filters) if filters else model.objects.all()
        return list(queryset.values())
    
    except LookupError:
        raise ValueError(f"Model '{model_name}' does not exist in the 'Student_app' app.")
