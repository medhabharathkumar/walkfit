from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

from django.shortcuts import render, redirect


from django.contrib import messages
from .models import Register

def register(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            password = request.POST.get('password')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            age = int(request.POST.get('age'))
            height = float(request.POST.get('height'))
            weight = float(request.POST.get('weight'))
            fitness_goal = request.POST.get('fitness_goal')

            # Basic validation
            if not name:
                messages.error(request, "Name is required!")
                return redirect('register')

            if gender not in ['M', 'F', 'O']:
                messages.error(request, "Please select a valid gender")
                return redirect('register')

            if age < 10 or age > 100:
                messages.error(request, "Please enter a realistic age")
                return redirect('register')

            if height < 100 or height > 250:
                messages.error(request, "Height should be between 100-250 cm")
                return redirect('register')

            if weight < 25 or weight > 300:
                messages.error(request, "Weight should be between 30-300 kg")
                return redirect('register')

            if not fitness_goal:
                messages.error(request, "Please select your fitness goal")
                return redirect('register')

            # Create the record
            Register.objects.create(
                name=name,
                password=password,
                gender=gender,
                email=email,
                phone=phone,
                age=age,
                height=height,
                weight=weight,
                fitness_goal=fitness_goal
            )

            messages.success(request, "Registration successful! Welcome! 💪")
            return redirect('index')  # or redirect to success page

        except ValueError:
            messages.error(request, "Please enter valid numbers for age/height/weight")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(name=name)
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('home')
            else:
                messages.error(request, "Wrong password")
        except Register.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'login.html')
from django.shortcuts import render, redirect
from .models import Register

def profile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')
    
    try:
        user = Register.objects.get(id=user_id)
    except Register.DoesNotExist:
        request.session.flush()
        return redirect('login')

    # Simple BMI calculation (safe & clean)
    bmi = None
    if user.height and user.height > 0:
        height_m = user.height / 100
        bmi = round(user.weight / (height_m ** 2), 1)

    return render(request, 'profile.html', {
        'user': user,
        'bmi': bmi,
    })

from django.shortcuts import render, redirect
from .models import Register
from django.contrib import messages

def editprofile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')
    
    try:
        user = Register.objects.get(id=user_id)
    except Register.DoesNotExist:
        request.session.flush()
        return redirect('login')

    if request.method == 'POST':
        # Update only allowed fields (simple version)
        user.age = request.POST.get('age', user.age)
        user.phone = request.POST.get('phone', user.phone)
        user.height = request.POST.get('height', user.height)
        user.weight = request.POST.get('weight', user.weight)
        user.fitness_goal = request.POST.get('fitness_goal', user.fitness_goal)
        
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {'user': user})

def logout(request):
    request.session.flush()
    return redirect('index')



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import FitnessVideo


def video_list(request):
    videos = FitnessVideo.objects.all().order_by('-created_at')
    return render(request, 'videolist.html', {'videos': videos})

def userlist(request):
    user = Register.objects.all().order_by('-created_at')
    return render(request, 'userlist.html', {'user': user})

def deleteuser(request,id):
    if request.method =="POST":
        user = Register.objects.get(id=id)
        user.delete()
        return redirect('userlist')
    return redirect('userlist')

def deletevideo(request,id):
    if request.method=="POST":
        video=FitnessVideo.objects.get(id=id)
        video.delete()
        return redirect('listvideo')
    return redirect('listvideo')


def video_add(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        video_file = request.FILES.get('video')
        thumbnail_file = request.FILES.get('thumbnail')

        if title and video_file:  # minimal required fields check
            video = FitnessVideo(
                title=title,
                description=description,
                video=video_file,
            )
            if thumbnail_file:
                video.thumbnail = thumbnail_file

            video.save()
            return redirect('listvideo')

    return render(request, 'addvideo.html')
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import FitnessRecord, Register

def fitness_tracker(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            distance = float(data.get("distance", 0))
            steps = int(data.get("steps", 0))
            calories = int(data.get("calories", 0))

            user = None
            if 'user_id' in request.session:
                user = Register.objects.get(id=request.session['user_id'])

            FitnessRecord.objects.create(
                user=user,
                distance_km=distance,
                steps=steps,
                calories=calories,
                session_id=request.session.session_key
            )
            return JsonResponse({"status": "saved"})

        except Exception:
            return JsonResponse({"error": "invalid"}, status=400)

    # GET - show the page
    return render(request, 'fitness.html')
def adminlogin(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Direct check for admin/admin
        if username == 'admin' and password == 'admin':
            return redirect('adhome')
        else:
            return render(request, 'adlogin.html', {'msg': 'Try again'})

    return render(request, 'adlogin.html')

def adhome(request):
    return render(request, 'adhome.html')

from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
import random

from .models import Reminder, Register


def manage_reminder(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = Register.objects.get(id=user_id)
    except Register.DoesNotExist:
        request.session.flush()
        return redirect('login')

    reminder, _ = Reminder.objects.get_or_create(
        user=user,
        defaults={
            'remind_water': True,
            'remind_exercise': True,
            'remind_diet': True,
            'remind_time': timezone.now().time().replace(hour=9, minute=0)
        }
    )

    if request.method == 'POST':
        reminder.remind_water    = 'remind_water'    in request.POST
        reminder.remind_exercise = 'remind_exercise' in request.POST
        reminder.remind_diet     = 'remind_diet'     in request.POST

        time_input = request.POST.get('remind_time')
        if time_input:
            try:
                h, m = map(int, time_input.split(':'))
                reminder.remind_time = timezone.now().time().replace(hour=h, minute=m)
            except:
                pass

        reminder.save()
        messages.success(request, "Reminders updated!")
        return redirect('home')

    context = {
        'reminder': reminder,
        'example_message': random.choice([
            "Hey 💕 Time to drink some water! 🌊",
            "Mini stretch or dance break! 💃",
            "Healthy food moment 🍓🥑",
            "Water + movement + good vibes 💖"
        ])
    }
    return render(request, 'manage.html', context)


from django.http import JsonResponse
from django.utils import timezone
from .models import Reminder, Register

def get_daily_reminder(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"error": "not_logged_in"}, status=403)

    try:
        user = Register.objects.get(id=user_id)
        reminder = Reminder.objects.get(user=user)
        enabled = reminder.remind_water or reminder.remind_exercise or reminder.remind_diet
        time_str = reminder.remind_time.strftime("%H:%M") if reminder.remind_time else None
        return JsonResponse({
            "enabled": enabled,
            "remind_time": time_str
        })
    except Reminder.DoesNotExist:
        return JsonResponse({"enabled": False})
    
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq
import os, json

from .models import Register  # adjust import path if needed


client = Groq(api_key="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")

BASE_PROMPT = """You are WalkFit – strict, direct, motivating fitness coach.
Short, aggressive answers. No fluff. Practical advice only.
Use this user info to personalize every reply:
- Height: {height} cm
- Weight: {weight} kg
- Goal: {goal}
Never ask for this info again."""
@csrf_exempt
def chatbot(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # or wherever your login is

    try:
        user = Register.objects.get(id=user_id)
        user_context = {
            'height': user.height,
            'weight': user.weight,
            'goal': user.get_fitness_goal_display()  # human-readable
        }
    except Register.DoesNotExist:
        return redirect('login')

    system_prompt = BASE_PROMPT.format(**user_context)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            msg = data.get("message", "").strip()
            if not msg:
                return JsonResponse({"error": "empty"}, status=400)

            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": msg}
                ],
                temperature=0.7,
                max_tokens=280
            )

            return JsonResponse({"reply": resp.choices[0].message.content.strip()})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET → show page
    return render(request, 'chatbot.html', {
        'icon_url': 'https://cdn3d.iconscout.com/3d/premium/thumb/orange-robot-lifting-weights-3d-icon-png-download-10975515.png'
    })
    
def spotify(request):
    return render(request, 'spotify.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback

def feedback(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        rating  = request.POST.get('rating')
        message = request.POST.get('message', '').strip()

        errors = []

        if not name:
            errors.append("Please enter your name.")
        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            errors.append("Please select a rating between 1 and 5.")
        if not message:
            errors.append("Please write your feedback.")

        if not errors:
            try:
                Feedback.objects.create(
                    name=name,
                    rating=int(rating),
                    message=message
                )
                messages.success(request, "Thank you! Your feedback was saved.")
                return redirect('feedback')
            except Exception:
                messages.error(request, "Something went wrong. Try again.")
        else:
            for err in errors:
                messages.error(request, err)

    # Show recent feedbacks (optional)
    recent = Feedback.objects.order_by('-created_at')[:5]

    return render(request, 'feedback.html', {
        'recent': recent,
    })




from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Feedback

def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')

    feedback_to_delete = None
    if 'delete' in request.GET:
        try:
            feedback_id = int(request.GET['delete'])
            feedback_to_delete = Feedback.objects.get(id=feedback_id)
        except (ValueError, Feedback.DoesNotExist):
            pass

    return render(request, 'feedbacklist.html', {
        'feedbacks': feedbacks,
        'feedback': feedback_to_delete,  
    })

def feedback_delete(request, id):  
    feedback = get_object_or_404(Feedback, id=id)

    if request.method == 'POST':
        name = feedback.name
        rating = feedback.rating
        feedback.delete()
        messages.success(request, f"Feedback from {name} ({rating}★) deleted.")
        return redirect('feedback_list')

    return redirect('feedback_list')