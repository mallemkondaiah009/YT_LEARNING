from django.shortcuts import get_object_or_404, render, redirect
from .models import UserRegistrations, UserStreak
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


def Register_View(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Validation: Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        # Validation: Check if username is already taken
        if UserRegistrations.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'accounts/register.html')

        # Validation: Check if email is already taken
        if UserRegistrations.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return render(request, 'accounts/register.html')

        # Create the user if all validations pass
        try:
            # Use create_user() to securely hash the password
            user = UserRegistrations.objects.create(username=username, email=email, password=make_password(password),)
            user.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')  # Redirect to login page after successful registration
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'accounts/register.html')

    # Render the registration form for GET requests
    return render(request, 'accounts/register.html')

def Login_View(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        #fetch user from database
        try: 
            user = UserRegistrations.objects.get(email=email)
        except UserRegistrations.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
        
        #Validate password
        if not check_password(password, user.password):
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
        
        # set user session
        request.session['user_id'] = user.id
        request.session['email']  = user.email
        request.session['username'] = user.username
        messages.success(request, 'Login successful.')
        return redirect('landing_page') 
    
    return render(request, 'accounts/login.html')

def Logout_View(request):
    # Check if user is logged in (assuming you store user info in session)
    if 'user_id' in request.session:
        # Clear user-specific session data
        del request.session['user_id']
        messages.success(request, 'Logout successful.')
    else:
        messages.info(request, 'No active user session found.')
    return redirect('login')



def Profile_View(request):
    # Get session data
    custom_user_id = request.session.get('user_id')

    # Determine user based on authentication method
    if custom_user_id:
        user = get_object_or_404(UserRegistrations, id=custom_user_id)
    else:
        return render(request, 'accounts/profile.html', {'error': 'Please log in to view your profile'})

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


def Register_Category_View(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Validation: Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        # Validation: Check if username is already taken
        if UserRegistrations.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'accounts/register.html')

        # Validation: Check if email is already taken
        if UserRegistrations.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return render(request, 'accounts/register.html')

        # Create the user if all validations pass
        try:
            # Use create_user() to securely hash the password
            user = UserRegistrations.objects.create(username=username, email=email, password=make_password(password),)
            user.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login_category')  # Redirect to login page after successful registration
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'accounts/register.html')

    # Render the registration form for GET requests
    return render(request, 'accounts/register.html')


def Login_Category_View(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        #fetch user from database
        try: 
            user = UserRegistrations.objects.get(email=email)
        except UserRegistrations.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
        
        #Validate password
        if not check_password(password, user.password):
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
        
        # set user session
        request.session['user_id'] = user.id
        request.session['email']  = user.email
        request.session['username'] = user.username
        messages.success(request, 'Login successful.')
        #take category_id from the form and redirect to videos_by_category
        category_name=request.session.get('category_name')
        return redirect('videos_by_category', category_name=category_name)
    
    return render(request, 'accounts/login.html')


# accounts/views.py

# accounts/views.py
import time
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from .models import UserRegistrations
from .tokens import custom_token_generator

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserRegistrations.objects.get(email=email)
            token = custom_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
            
            print(f"Reset link: {reset_link}")  # Debug
            
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
            
        except UserRegistrations.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return redirect('forgot_password')
            
    return render(request, 'accounts/forgot_password.html')

def reset_password(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(f"Decoded UID: {uid}")  # Debug
        user = UserRegistrations.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserRegistrations.DoesNotExist) as e:
        print(f"UID decoding error: {str(e)}")  # Debug
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
        print(f"Token validation failed for user: {user}, token: {token}")  # Debug
        return redirect('forgot_password')