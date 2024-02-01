from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Apartments
from .serializers import WorksiteApartmentsSerializer
from django.contrib.auth.decorators import login_required


# # Create your views here.
# @login_required(login_url='accounts:login')
# def apartments_api(request):
#     apartments = Apartments.objects.all()
#     serializer = WorksiteApartmentsSerializer(apartments, many=True)

#     data = {
#     'results': serializer.data,
#     }

#     return JsonResponse(data)


# def new_apartment(request, id):
#     context = {
#         'worksite_id': id,
#     }
#     return render(request, 'new-apartment.html',context)


# @login_required(login_url='accounts:login')
# def add_apartment(request):
#     try:
#         if request.method == "POST":
#             worksite_id = request.POST.get('worksite_id')
#             name = request.POST.get('name')
#             surface = request.POST.get('surface')
#             owner = request.POST.get('owner')
            
#             Apartments.objects.create(
#                 worksite=worksite_id,
#                 name=name,
#                 surface=surface,
#                 owner=owner,
#             )

#             messages.success(request, "Cantiere inserito con successo")
#             return redirect('worksites:worksites-lists')
#         else:
#             return print('negativo')
#     except Exception as e:
#         print(f"Adding worksite Error occurred: {e}")
#         return HttpResponse(f"An error occurred: {e}", status=500)  # HTTP 500 Internal Server Error