from django.http import JsonResponse

def apple_app_site_association(request):
    data = {
        "applinks": {
            "apps": [],
            "details": [
                {
                    "appID": "8MD582JM2N.com.todo.app",
                    "paths": ["*"]
                }
            ]
        }
    }
    return JsonResponse(data, safe=False)
