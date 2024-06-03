# from django.shortcuts import redirect
# from django.urls import resolve

# class UserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
        
#         resolved_url = resolve(request.path_info)
#         print(resolved_url)
#         allowed_urls = ['additional', 'additional_fitness_goal', 'additional_activity_level', 'main', 'login']
        
#         if resolved_url.url_name in allowed_urls:
#             return response
        
#         if request.user.is_authenticated:
#             user = request.user
#             # 필수 필드가 모두 채워져 있는지 확인
#             if not user.height or not user.weight or not user.age or not user.gender:
#                 return redirect('user:additional')
#             if not user.fitness_goal:
#                 return redirect('user:additional_fitness_goal')
#             if not user.activity_level:
#                 return redirect('user:additional_activity_level')
#         return response
