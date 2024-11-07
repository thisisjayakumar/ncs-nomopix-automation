from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
import logging

User = get_user_model() 

logger = logging.getLogger(__name__)


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username and email:
                username = email.split('@')[0]

            if not email or not password:
                return JsonResponse({"error": "Missing required fields."}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User with this email already exists."}, status=400)
            
            user = User.objects.create_user(username=username, email=email, password=password)
            
            return JsonResponse({"message": "User created successfully.", "user_id": user.id}, status=201)
        
        except json.JSONDecodeError:
            logger.exception("Invalid JSON input")
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        
        except Exception as e:
            logger.exception(f"Error occurred while creating user: {e}")
            return JsonResponse({"error": "Something went wrong."}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)
