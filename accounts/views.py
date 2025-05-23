from django.shortcuts import get_object_or_404, render, redirect
from .models import UserStreak
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from yt_learning.models import save_watch_later
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import time
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password, check_password
from .tokens import custom_token_generator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
#from django.contrib.auth.decorators import login_required
from .decorators import custom_login_required
from django.contrib.auth import authenticate, login


def Register_View(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Validation: Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        # Validation: Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'accounts/register.html')

        # Validation: Check if email is already taken
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return render(request, 'accounts/register.html')

        # Create the user using create_user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password  # create_user hashes the password automatically
            )
            user.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')  # Redirect to login page
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'accounts/register.html')

    return render(request, 'accounts/register.html')

def Login_View(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)  # Use custom backend or username=email
        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully sined in as, {user.username}!")
            return redirect('landing_page')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')

def Logout_View(request):
    # Log out the user using Django's built-in logout function
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login')



@custom_login_required
def Profile_View(request):
    # Use request.user for the authenticated user
    user = request.user

    # Check if user is admin (staff or superuser)
    if user.is_staff or user.is_superuser:
        return redirect('login')  # Redirect to login page

    # Handle POST requests for AJAX
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        action = request.POST.get('action')
        if action == 'remove':
            video_id = request.POST.get('video_id')
            try:
                saved_video = save_watch_later.objects.get(user=user, video_id=video_id)
                saved_video.delete()
                return JsonResponse({'status': 'success', 'message': 'Video removed from watch later'})
            except save_watch_later.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Video not found in watch later'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

    # Get or create streak
    try:
        streak = UserStreak.objects.get(user=user)
    except UserStreak.DoesNotExist:
        streak = UserStreak.objects.create(user=user)
    
    # Update streak
    streak.update_streak()

    # Retrieve saved videos
    saved_videos = (
        save_watch_later.objects
        .filter(user=user)
        .select_related('video')
        .order_by('date')
    )
    
    # Prepare context
    context = {
        'user': user,
        'saved_videos': saved_videos,
        'current_streak': streak.streak_count,
        'longest_streak': streak.longest_streak,
        'last_visit': streak.last_visit,
    }

    return render(request, 'accounts/profile.html', context)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        try:
            user = User.objects.get(email__iexact=email)
            token = custom_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
            
            subject = 'Password Reset Request'
            message = render_to_string('emails/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            
            send_mail(
                subject,
                message,
                'hexacodesrepley@gmail.com',
                [email],
                fail_silently=False,
                html_message=message
            )
            
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('forgot_password')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return redirect('forgot_password')
        except User.MultipleObjectsReturned:
            messages.error(request, 'Multiple accounts found with this email.')
            return redirect('forgot_password')     
    return render(request, 'accounts/forgot_password.html')

def reset_password(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and custom_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            
            if password != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('reset_password', uidb64=uidb64, token=token)
                
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('reset_password', uidb64=uidb64, token=token)
                
            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully.')
            return redirect('login')
            
        return render(request, 'accounts/reset_password.html')
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('forgot_password')