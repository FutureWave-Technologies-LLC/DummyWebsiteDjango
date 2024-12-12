from .models import *
import hashlib

class UserFactory:
    @staticmethod
    def create_user(request):
        data = request.data

        # Check if user already exists
        if users.objects.filter(username=data.get('username')).first():
            # Return JSON that username is taken
            json_data = {"response": "Username already exists.", "error": True}
            return JsonResponse(json_data, safe=False)

        # Validate password length
        if len(data.get('password')) < 4:
            # Return JSON that invalid password
            json_data = {"response": "Password must be more than 4 characters long.", "error": True}
            return JsonResponse(json_data, safe=False)

        # Hash password
        data['password'] = hashlib.sha256(str(data.get('password')).encode()).hexdigest()
    
        # Create user
        new_user_info = users(username=data.get('username'),
                              password=data.get('password'),
                              first_name=data.get('first_name'),
                              last_name=data.get('last_name'),
                              profile_image="",
                              token_id=-1)
        new_user_info.save()