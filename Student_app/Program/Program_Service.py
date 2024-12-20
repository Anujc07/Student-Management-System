from Student_app.models import Program

def add_program(name, duration, semsters=None):
    """Adds a new program."""
    return Program.objects.create(name=name, duration=duration, semsters=semsters)

def edit_program(program_id, name, duration, semsters=None):
    """Edits an existing program."""
    program = Program.objects.get(id=program_id)
    program.name = name
    program.duration = duration
    program.semsters = semsters
    program.save()
    return program

def delete_program(program_id):
    """Deletes a program by ID."""
    program = Program.objects.get(id=program_id)
    program.delete()

    
def search_programs(name=None, duration=None, semsters=None):
    """Filters programs based on the provided criteria."""
    filters = {}
    if name:
        filters['name__icontains'] = name
    if duration:
        filters['duration'] = duration
    if semsters:
        filters['semsters'] = semsters
    return Program.objects.filter(**filters)