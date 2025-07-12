from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import RegisterForm
from .models import User
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from django.shortcuts import render

from django.http import JsonResponse

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("conform_password")
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        user = User.objects.create_user(
        f_name=first_name,
        l_name=last_name,
        email=email,
        password=password1
)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")
    print("Register not successfull")
    return render(request, "register1.html")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("dashboard")  # Redirect to a dashboard page
            else:
                messages.error(request, "Invalid email or password")

    else:
        form = LoginForm()

    return render(request, "login1.html", {"form": form})

def index_view(request):
    return render(request, "index.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # Redirect to login page after logou

def dashboard(request):
    return render(request, 'dashboard.html')



# Google Service Account Credentials
SERVICE_ACCOUNT_FILE = ""
SCOPES = ["https://www.googleapis.com/auth/drive"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)


def upload_to_drive(file_path, file_name, folder_id, description=""):
    """Uploads a file to Google Drive in the selected folder with an optional description."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    drive_service = build("drive", "v3", credentials=credentials)

    file_metadata = {
        "name": file_name,
        "parents": [folder_id],  # ✅ Upload file to the selected folder
        "description": description  # ✅ Attach file description
    }
    media = MediaFileUpload(file_path, resumable=True)

    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()

    return file.get("webViewLink")  # ✅ Return the file link


def upload_note(request):
    """Handles file upload from user and uploads to the selected Google Drive folder with a description."""
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        selected_folder = request.POST.get("folder")  # ✅ Get selected folder ID
        file_description = request.POST.get("description", "")  # ✅ Get file description (optional)

        if not selected_folder:
            return JsonResponse({"error": "Please select a folder."})

        # ✅ Save file temporarily
        upload_dir = "uploads/"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, uploaded_file.name)

        with open(file_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # ✅ Upload to Google Drive in the selected folder with description
        drive_link = upload_to_drive(file_path, uploaded_file.name, selected_folder, file_description)

        # ✅ Remove local file after uploading
        os.remove(file_path)

        return JsonResponse({
            "message": "File uploaded successfully!",
            "drive_link": drive_link
        })

    return render(request, "upload.html")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)

# Dictionary to store folder names and their IDs
FOLDER_CHOICES = {
    "": "CSE",
    "": "AI and ML",
    "": "ECE",
    "": "Cybersecurity",
    "": "Data Science",
    "": "EEE",
    "": "Information Science",
    "": "Mathematics",
    "": "Medical Electronics",
    "": "Physics",
    "": "Civil",
    "": "Mechanical Engineering",
}

# Default Folder ID (CSE)
DEFAULT_FOLDER_ID = ""

def view_uploaded_files(request):
    """Fetches and displays files from a selected Google Drive folder"""

    # Get selected folder from request (empty if none selected)
    folder_id = request.GET.get("folder", "")

    files = []  # Default to empty files list

    if folder_id:  # Fetch only if a folder is selected
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents",
            fields="files(id, name, webViewLink, description)"
        ).execute()

        files = results.get("files", [])

    # Prepare file list with descriptions (tags/comments)
    file_list = [
        {
            "name": file["name"],
            "webViewLink": file["webViewLink"],
            "description": file.get("description", "No Tags/Comments")
        }
        for file in files
    ]

    return render(request, "view_files.html", {
        "files": file_list,
        "folders": FOLDER_CHOICES,
        "selected_folder": folder_id  # Pass selected folder for dropdown persistence
    })

    
# ✅ Your Google Drive API credentials

def list_drive_files(request):
    """Lists files from the selected Google Drive folder."""
    
    # ✅ Get the selected folder from the request
    folder_id = request.GET.get("folder", "")  # Default to CSE if not selected

    # ✅ Authenticate with Google Drive API
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive_service = build("drive", "v3", credentials=credentials)

    # ✅ Query files from the selected folder
    query = f"'{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name, webViewLink, description)").execute()
    
    files = results.get("files", [])

    return render(request, "uploaded_files.html", {"files": files})

def contact(request):
    return render(request, 'contact.html')

def whatsapp(request):
    return render(request, 'whatsapp.html')

def about(request):
    return render(request, 'about.html')