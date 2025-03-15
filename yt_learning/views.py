from django.shortcuts import render, get_object_or_404
from .models import Category, Videos, Bashalu,VideoProgress
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
    request.session['category_id'] = category.id
    
    # Get selected language name from POST request or session
    selected_language_name = request.POST.get('language')
    if selected_language_name is not None:
        request.session['selected_language_name'] = selected_language_name
    else:
        selected_language_name = request.session.get('selected_language_name')
    
    # Retrieve videos for the category
    videos = Videos.objects.filter(category=category)
    
    # Filter videos by selected language name if provided
    if selected_language_name:
        try:
            language_obj = Bashalu.objects.get(lang_name=selected_language_name)
            videos = videos.filter(bhashalu=language_obj)
        except Bashalu.DoesNotExist:
            videos = Videos.objects.none()
    
    # Retrieve saved video IDs, progress, and calculate overall progress
    saved_video_ids = []
    video_progress = {}
    overall_progress = 0.0
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserRegistrations.objects.get(id=user_id)
            saved_video_ids = save_watch_later.objects.filter(user=user).values_list('video_id', flat=True)
            progress_records = VideoProgress.objects.filter(user=user, video__in=videos).values('video_id', 'progress')
            video_progress = {record['video_id']: record['progress'] for record in progress_records}
            
            # Calculate overall progress
            total_videos = videos.count()
            if total_videos > 0:
                completed_progress = sum(video_progress.get(video.id, 0.0) for video in videos)
                overall_progress = (completed_progress / (total_videos * 100.0)) * 100.0
        except UserRegistrations.DoesNotExist:
            saved_video_ids = []
            video_progress = {}
            overall_progress = 0.0
    
    # Handle POST request
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
        
        user = UserRegistrations.objects.get(id=user_id)
        action = request.POST.get('action')
        
        if action == 'save':
            video_id = request.POST.get('video_id')
            video = get_object_or_404(Videos, id=video_id)
            if not save_watch_later.objects.filter(video=video, user=user).exists():
                save_watch_later.objects.create(video=video, user=user)
                return JsonResponse({'status': 'success', 'message': 'Video saved for later'})
            else:
                return JsonResponse({'status': 'info', 'message': 'Video already saved'})
        
        elif action == 'language':
            return JsonResponse({'status': 'success', 'message': 'Language changed'})
        
        elif action == 'update_progress':
            video_id = request.POST.get('video_id')
            completed = request.POST.get('completed') == 'true'
            
            try:
                video = Videos.objects.get(id=video_id)
                VideoProgress.objects.update_or_create(
                    user=user,
                    video=video,
                    defaults={'progress': 100.0 if completed else 0.0}
                )
                # Recalculate overall progress after update
                progress_records = VideoProgress.objects.filter(user=user, video__in=videos).values('video_id', 'progress')
                video_progress = {record['video_id']: record['progress'] for record in progress_records}
                total_videos = videos.count()
                if total_videos > 0:
                    completed_progress = sum(video_progress.get(video.id, 0.0) for video in videos)
                    overall_progress = (completed_progress / (total_videos * 100.0)) * 100.0
                return JsonResponse({
                    'status': 'success',
                    'message': 'Progress updated',
                    'overall_progress': overall_progress
                })
            except Videos.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Video not found'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
    
    # Prepare context
    context = {
        'category': category,
        'languages': languages,
        'videos': videos,
        'saved_video_ids': list(saved_video_ids),
        'selected_language': selected_language_name,
        'video_progress': video_progress,
        'overall_progress': overall_progress,  # Add overall progress to context
    }
    
    return render(request, 'yt_learning/videos_by_category.html', context)