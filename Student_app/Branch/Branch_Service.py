from django.shortcuts import get_object_or_404
from Student_app.models import Branch, Program

# def get_all_branches(filters=None):
#     branches = Branch.objects.all()
    
#     if filters:
#         branch_name = filters.get('branch_name')
#         if branch_name: 
#             branches = branches.filter(name__icontains=branch_name)
    
#     return branches



def get_branch_by_id(branch_id):
    """
    Retrieve a single branch by its ID.
    """
    return get_object_or_404(Branch, id=branch_id)


def update_branch(branch, data):
    """
    Update a branch instance with the provided data.
    """
    branch.name = data.get('name', branch.name)
    branch.program_id = data.get('program', branch.program_id)
    # branch.head_of_branch = data.get('head_of_branch', branch.head_of_branch)
    # branch.contact = data.get('contact', branch.contact)
    branch.save()

def delete_branch(branch_id):
    """
    Delete a branch by its ID.
    """
    branch = get_object_or_404(Branch, id=branch_id)
    branch.delete()

# def get_program(program_id=None):
#     """
#     Retrieve program(s) based on the provided program_id.
#     If program_id is None, return all programs.
#     """
#     if program_id:
#         return get_object_or_404(Program, id=program_id)
#     return Program.objects.all()