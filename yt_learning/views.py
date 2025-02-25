from django.shortcuts import render, get_object_or_404
from .models import Category, Videos, Bashalu
from accounts.models import UserRegistrations
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Videos, Category, save_watch_later

# Landing page view
def landing_page(request):
    return render(request, 'yt_learning/landing_page.html')

# Categories page view
def categories_page(request):
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'yt_learning/category.html', {'categories': categories})


def videos_by_category(request, category_id):
    # Retrieve category
    category = get_object_or_404(Category, id=category_id)
    languages = Bashalu.objects.all()
    
    # Retrieve videos for the category
    videos = Videos.objects.filter(category=category)
    
    # Retrieve saved video IDs using session
    saved_video_ids = []
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserRegistrations.objects.get(id=user_id)
            saved_video_ids = save_watch_later.objects.filter(user=user).values_list('video_id', flat=True)
        except user.DoesNotExist:
            # Handle case where user does not exist
            saved_video_ids = []
    
    # Handle POST request for saving a video
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
        
        video_id = request.POST.get('video_id')
        video = get_object_or_404(Videos, id=video_id)
        user = UserRegistrations.objects.get(id=user_id)
        
        # Check if already saved
        if not save_watch_later.objects.filter(video=video, user=user).exists():
            save_watch_later.objects.create(video=video, user=user)
            return JsonResponse({'status': 'success', 'message': 'Video saved for later'})
        else:
            return JsonResponse({'status': 'info', 'message': 'Video already saved'})
    
    # Render the page for GET requests
    context = {
        'category': category,
        'languages': languages,
        'videos': videos,
        'saved_video_ids': list(saved_video_ids),
    }
    return render(request, 'yt_learning/videos_by_category.html', context)

