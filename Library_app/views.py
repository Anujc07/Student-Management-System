from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


def Create_Book(request):
    if request.method == "POST":

        book_title = request.POST.get("book_title")
        author = request.POST.get("author")
        isbn = request.POST.get("isbn")
        genre = request.POST.get("genre")
        price = request.POST.get("price")
        published_date = request.POST.get("published_date")
        total_copies = request.POST.get("total_copies")
        available_copies = request.POST.get("available_copies")
        cover_image = request.FILES.get("cover_image")
        description = request.POST.get("description")


        if int(available_copies) > int(total_copies):
            messages.error(request, "Available copies cannot exceed total copies.")
            return redirect("./Add-Books")


        try:
            book = Book(
                book_title=book_title,
                author=author,
                isbn=isbn,
                genre=genre,
                price=price,
                published_date=published_date,
                total_copies=total_copies,
                available_copies=available_copies,
                cover_image=cover_image,
                description=description,
            )
            book.full_clean() 
            book.save()
            messages.success(request, "Book added successfully!")
            return redirect("./Add-Books")

        except ValidationError as e:
            messages.error(request, f"Error: {', '.join(e.messages)}")
            return redirect("./Add-Books")
    book_type = Book_Type.objects.all()
    return render(request, "Library/Add_Books.html", {"book_types":book_type})



def Assign_Book(request):
    if request.method == 'POST':
        program_id = request.POST.get('program_id')
        branch_id = request.POST.get('branch_id')
        semester = request.POST.get('semester')
        student_id = request.POST.get('student')
        book_id = request.POST.get('book')
        number_of_copies = request.POST.get('number_of_copies')
        date_of_submission = request.POST.get('date_of_submission')

        if not all([program_id, branch_id, semester, student_id, book_id, number_of_copies, date_of_submission]):
            messages.error(request, "All fields are required. Please fill in all the details.")
            return redirect('Assign_Book')

        try:
            # Convert semester and number_of_copies to integers
            semester = int(semester)
            number_of_copies = int(number_of_copies)

            # Fetch related objects
            program = Program.objects.get(id=program_id)
            branch = Branch.objects.get(id=branch_id)
            student = Student.objects.get(id=student_id)
            book = Book.objects.get(id=book_id)

            # Check if enough copies are available
            if book.available_copies < number_of_copies:
                messages.error(request, f"Only {book.available_copies} copies of the book '{book.book_title}' are available.")
                return redirect('./Assign-Book')

            # Atomic transaction to ensure consistency
            with transaction.atomic():
                # Create the book assignment
                book_assign = BookAssignment.objects.create(
                    program=program,
                    branch=branch,
                    semester=semester,
                    student=student,
                    book=book,
                    number_of_copies=number_of_copies,
                    date_of_submission=date_of_submission
                )
                book_assign.save()

                # Update the available copies
                book.available_copies -= number_of_copies
                book.save()

            messages.success(request, "Book successfully assigned!")
            return redirect('./Assign-Book')

        except ObjectDoesNotExist as e:
            messages.error(request, f"Invalid data: {e}")
        except ValueError:
            messages.error(request, "Invalid semester or number of copies. Ensure these are integers.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('./Assign-Book')

    # GET request
    programs = Program.objects.all()
    books = Book.objects.all()
    return render(request, 'Library/Assign_Book.html', {'programs': programs, 'books': books})




def Book_List(request):
    isbn = request.GET.get('isbn', '')
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    
    book_list = Book.objects.all()
    
    if isbn:
        book_list = book_list.filter(isbn__icontains=isbn)
    if title:
        book_list = book_list.filter(book_title__icontains=title)
    if author:
        book_list = book_list.filter(author__icontains=author)
    
    return render(request, 'Library/Library_Management.html', {'book_list': book_list})



