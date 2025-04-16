from django.shortcuts import render
from django.http import JsonResponse
from .models import CodeGround
from django.views.decorators.http import require_GET

@require_GET
def CodeReels_View(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX request
        current_id = request.GET.get('current_id', None)
        direction = request.GET.get('direction', 'next')  # 'next' or 'prev'
        try:
            if current_id:
                current_id = int(current_id)
                if direction == 'next':
                    next_problem = CodeGround.objects.filter(id__gt=current_id).order_by('id').first()
                else:  # prev
                    next_problem = CodeGround.objects.filter(id__lt=current_id).order_by('-id').first()
            else:
                next_problem = CodeGround.objects.order_by('id').first()

            if not next_problem:
                return JsonResponse({'error': 'No more problems available'}, status=404)

            # Handle visible_testcases as a JSONField list
            visible_testcases = next_problem.visible_testcases or []  # Fallback to empty list
            if not isinstance(visible_testcases, list):
                visible_testcases = []

            # Format test cases for JSON response
            formatted_testcases = [
                {'input': str(tc['input']), 'output': str(tc['output'])}
                for tc in visible_testcases
                if isinstance(tc, dict) and 'input' in tc and 'output' in tc
            ]

            return JsonResponse({
                'id': next_problem.id,
                'question': next_problem.question,
                'visible_testcases': formatted_testcases,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Initial page load
        code_ground = CodeGround.objects.order_by('id').first()
        if not code_ground:
            return render(request, 'codeground/code_reels.html', {'error': 'No problems available'})
        context = {
            'code_ground': code_ground,
        }
        return render(request, 'codeground/code_reels.html', context)