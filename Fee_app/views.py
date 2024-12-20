from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.utils.timezone import now




def get_branches(request, program_id):
    branches = Branch.objects.filter(program_id=program_id).values("id", "name")
    semester = Program.objects.filter(id=program_id).values("semsters")
    return JsonResponse({"branches": list(branches), "semesters": list(semester)})

def get_students(request, branch_id, program_id, semester):
    students = Student.objects.filter(
        branch_id=branch_id,
        program_id=program_id,
        semester=semester
    ).values("id", "name")

    return JsonResponse({"students": list(students)})


def Add_Fee(request):
    if request.method == "POST":
        student_id = request.POST.get("student")
        program_id = request.POST.get("program")
        branch_id = request.POST.get("branch")
        semester = request.POST.get("semester")
        total_fee = request.POST.get("total_fee")
        payment_type = request.POST.get("payment_type")
        cash_notes = request.POST.get("cash_notes") 
        transaction_id = request.POST.get("transaction_id")
        screenshot = request.FILES.get("screenshot")
        payment_amount = request.POST.get("amount")
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            messages.error(request, "Student does not exist.")
            return redirect("Add_Fee")
        
        program = Program.objects.filter(id=program_id).first()
        branch = Branch.objects.filter(id=branch_id).first()

        if not program or not branch:
            messages.error(request, "Invalid program or branch selected.")
            return redirect("Add_Fee")

        if not semester or not semester.isdigit():
            messages.error(request, "Invalid semester.")
            return redirect("Add_Fee")

        # Handle cash or online payment validations
        if payment_type == "cash" and not cash_notes:
            messages.error(request, "Cash notes must be provided for cash payments.")
            return redirect("Add_Fee")

        if payment_type == "online" and not transaction_id:
            messages.error(request, "Transaction ID must be provided for online payments.")
            return redirect("Add_Fee")

        try:
            fee = Fee.objects.create(
                payment_amount=payment_amount,
                student=student,
                program=program,
                branch=branch,
                semester=int(semester),
                created_by=request.user.username,
                date=now().date(),
                total_fee=total_fee,
                payment_type=payment_type,
                cash_notes=cash_notes if payment_type == "cash" else None,
                transaction_id=transaction_id if payment_type == "online" else None,
                screenshot=screenshot if payment_type == "online" else None,
            )
            fee.save()
            
            messages.success(request, "Fee record added successfully.")
            return redirect("Add_Fee")

        except Exception as e:
            
            messages.error(request, f"Error saving fee record: {e}")
            return redirect("Add_Fee")

    # Fetch necessary data for the form
    students = Student.objects.all()
    programs = Program.objects.all()
    branches = Branch.objects.all()

    return render(request, "Fee/Add_Fee.html", {
        "students": students,
        "programs": programs,
        "branches": branches,
    })




def Std_Fees_List(request):
    # Get all programs and branches to populate the dropdowns
    programs = Program.objects.all()
    branches = Branch.objects.all()
    
    # Initialize payment_list as None
    payment_list = None

    if request.method == "POST":
        # Get selected values from the form
        program_id = request.POST.get("program_id")
        branch_id = request.POST.get("branch_id")
        semester = request.POST.get("semester")
        student_id = request.POST.get("student")  # Get student ID

        # Ensure all filters are selected
        if program_id and branch_id and semester:
            try:
                # Prepare filters for Fee query
                filters = {
                    'program_id': program_id,
                    'branch_id': branch_id,
                    'semester': semester,
                }

                # If a student is selected, add it to the filter
                if student_id:
                    filters['student_id'] = student_id

                # Filter Fee records based on selected program, branch, semester, and student
                payment_list = Fee.objects.filter(**filters).distinct()

                # Check if no payments were found
                if not payment_list:
                    messages.warning(request, "No payments found for the selected filters.")
                    
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                print("Error:", e)

    # Render the template with the filtered payment_list
    return render(request, 'Fee/Fee_List.html', {
        'programs': programs,
        'branches': branches,
        'payment_list': payment_list,
    })
