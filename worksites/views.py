from django.shortcuts import redirect, render

from django.db.models import Prefetch
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.template.defaultfilters import time
from django.contrib.auth.decorators import user_passes_test
from accounts.models import Profile
from worksites.serializers import WorksiteSerializer
from .models import Worksites

from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from django.db.models import Q
import json
import os
import requests
import csv
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django.http import HttpResponseBadRequest
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
from django.core.files import File
from django.conf import settings
from urllib.parse import unquote
from django.core.paginator import Paginator
from collections import defaultdict
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image



def compress_image(image_file, quality=85):
    """
    Compresses the provided image file and returns the compressed image.

    Parameters:
    - image_file: The image file object (uploaded file).
    - quality: The quality level of the compressed image (0 - 100). Default is 85.

    Returns:
    - The compressed image file object.
    """
    try:
        # Apri l'immagine utilizzando Pillow
        image = Image.open(image_file)

        # Comprimi l'immagine
        output_buffer = BytesIO()

        if image.format == 'JPEG':
            output_format = 'JPEG'
        elif image.format == 'PNG':
            output_format = 'PNG'
        else:
            # If it's neither JPEG nor PNG, you can choose a default format
            output_format = 'JPEG'

        image.save(output_buffer, format=output_format, quality=quality)

        # Crea un nuovo file temporaneo per l'immagine compressa
        compressed_image_file = ContentFile(output_buffer.getvalue(), name=image_file.name)

        return compressed_image_file

    except Exception as e:
        print(f"An error occurred while compressing the image: {e}")
        return None


# Create your views here.


from itertools import groupby


def admin_check(user):
   return user.is_superuser

def logged_check(user):
    return user.is_authenticated

@login_required(login_url='accounts:login')
def worksites_lists(request):
    return render(request, 'worksites-lists.html')

@login_required(login_url='accounts:login')
def worksites_list_api(request):
    order_by_field = request.GET.get('order_by', '-id')
    search_query = request.GET.get('search', '')

    worksites = Worksites.objects.all()

    # if request.user.is_superuser:
    #     if search_query:
    #         eventi = Evento.objects.filter(
    #             Q(data_da__icontains=search_query,is_fixed=False) |
    #             Q(data_a__icontains=search_query,is_fixed=False) |
    #             Q(nome__icontains=search_query,is_fixed=False)  |
    #             Q(luogo__nome__icontains=search_query,is_fixed=False) |
    #             Q(luogo__indirizzo__icontains=search_query,is_fixed=False) |
    #             Q(luogo__edificio__icontains=search_query,is_fixed=False) |
    #             Q(luogo__cap__icontains=search_query,is_fixed=False)             
    #         ).order_by(order_by_field)
    #     else:    
    #         eventi = Evento.objects.filter(is_fixed=False).order_by(order_by_field)
    
    #     #categorie_eventi = CategorieEvento.objects.select_related('evento', 'categoria').order_by('-evento__id')
    # else:
    #     if search_query:
    #         eventi = Evento.objects.filter(
    #             Q(data_da__icontains=search_query, author=request.user) |
    #             Q(data_a__icontains=search_query, author=request.user) |
    #             Q(nome__icontains=search_query, author=request.user) 
    #         ).order_by(order_by_field)
    #     else:    
    #         eventi = Evento.objects.filter(author=request.user).order_by(order_by_field)
        #categorie_eventi = CategorieEvento.objects.filter(evento__author=request.user).select_related('evento', 'categoria').order_by('-evento__id')

    paginator = Paginator(worksites, per_page=10)
    
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    serializer = WorksiteSerializer(page_obj, many=True)


    data = {
        'results': serializer.data,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'total_count': worksites.count()  # Adding the total count here
    }

    return JsonResponse(data)


@login_required(login_url='accounts:login')
def worksite_detail(request, id):
    
    worksite = Worksites.objects.get(id=id)

    context = {
        'worksite': worksite,
    }

    return render(request, 'worksite-detail.html', context)



@login_required(login_url='accounts:login')
def add_worksite(request):
    return render(request, 'new-worksite.html')


@login_required(login_url='accounts:login')
def add_new_worksite(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            address = request.POST.get('address')
            region = request.POST.get('region')
            image = request.FILES.get('image')
            # if image:
            #     compressed_copertina_file = compress_image(image)
            # else:
            #     default_image_url = request.POST.get('default_image')
            #     full_default_image_url = f"https://teramo-eventi.s3.nl-ams.scw.cloud/media/{default_image_url}"

            #     response = requests.get(full_default_image_url)

            #     if response.status_code == 200:
            #         compressed_copertina_file = ContentFile(response.content)
            #         desired_filename = 'default_event_image.jpg'
            #         compressed_copertina_file.name = desired_filename
            #     else:
            #         raise ValueError("Couldn't fetch the default image.")

            city = request.POST.get('city')
            date = request.POST.get('date')
            user = request.user
            profile = Profile.objects.get(user=user)

            
            Worksites.objects.create(
                name=name,
                address=address,
                region=region,
                image=image,
                city=city,
                date=date,
                user=profile
            )

            messages.success(request, "Cantiere inserito con successo")
            return redirect('worksites:worksites-lists')
        else:
            return print('negativo')
    except Exception as e:
        print(f"Adding worksite Error occurred: {e}")
        return HttpResponse(f"An error occurred: {e}", status=500)  # HTTP 500 Internal Server Error
    

@login_required(login_url='accounts:login')
def edit_worksite(request):
    try:
        worksite_id = request.POST.get('worksite_id')
        worksite = Worksites.objects.get(id=worksite_id)

        if request.method == "POST":
            worksite.name = request.POST.get('name')
            worksite.address = request.POST.get('address')
            worksite.region = request.POST.get('region')
            worksite.city = request.POST.get('city')
            worksite.date = request.POST.get('date')
            worksite.user = request.user.profile

            # Handle image upload
            image = request.FILES.get('image')
            if image:
                # Add your image processing logic here if necessary
                worksite.image = image
            # else:
            #     Handle default image logic here

            # Save updated fields
            worksite.save(update_fields=['name', 'address', 'region', 'image', 'city', 'date', 'user'])

            messages.success(request, "Cantiere modificato con successo")
            return redirect('worksites:worksites-lists')

    except Exception as e:
        print(f"Editing worksite Error occurred: {e}")
        return HttpResponse(f"An error occurred: {e}", status=500)


@login_required
def delete_worksite(request):
    id = request.GET.get('id')
    
    try:
        worksite = Worksites.objects.get(id=id)
    except Worksites.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))
    
    # Check if the user is a superuser or the author of the event
    if request.user.is_superuser:
        worksite.delete()  # Delete the event object
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))
    
    # Redirect back to the referring page or a default path
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))

# @login_required(login_url='accounts:login')
# def lista_eventi_da_approvare(request):
#     # Paginate results for better performance
#     page = request.GET.get('page', 1)
#     items_per_page = 1 # Or any number you find suitable

#     if request.user.is_superuser:
#         categorie_eventi = CategorieEvento.objects.filter(evento__approved=False).select_related('evento', 'categoria').order_by('-evento__id')
#     else:
#         categorie_eventi = CategorieEvento.objects.filter(evento__author=request.user, evento__approved=False).select_related('evento', 'categoria').order_by('-evento__id')

#     events_with_categories = defaultdict(list)

#     for ce in categorie_eventi:
#         events_with_categories[ce.evento].append(ce.categoria)


#     events_list = list(events_with_categories.items())
#     paginator = Paginator(events_list, items_per_page)
#     page = paginator.get_page(page)

#     context = {
#         'categorie': page,
#     }

#     return render(request, 'iniziative/eventi_da_approvare.html', context)


# @user_passes_test(admin_check)
# def lista_eventi_prossimi(request):

#     current_datetime = timezone.now()  # Here
#     current_date = current_datetime.strftime('%Y-%m-%d')

#     # Combine Q object with other filters using the bitwise OR operator |
#     eventi = Evento.objects.filter(
#         Q(
#             data_da__lte=current_date,
#             data_a__gte=current_date,
#         ) | Q(
#             data_a__isnull=True,
#             data_da__gte=current_date,
#         )
#     )

#     context = {
#         'eventi': eventi,
#     }
    
#     return render(request, 'iniziative/eventi_prossimi.html', context)

# @user_passes_test(admin_check)
# def lista_utenti(request):
#     profile = Profile.objects.filter().all()

#     context = {
#         'firebase': profile,
#     }
    

#     return render(request, 'iniziative/lista_firebase.html', context)


# # @login_required(login_url='accounts:login')
# # def nuovo_evento(request):
# #     provincia_choices = Luogo.PROVINCIA_CHOICES
    

# #     context = {
# #         'all_categories': all_categories,
# #         'all_categories_fixed': all_categories_fixed,
# #         'provincia_choices': provincia_choices,
# #         'orari': [],
# #         'categorie': [],
# #     }

#     return render(request, 'iniziative/nuovo-evento.html', context)

# @login_required
# def delete_event(request):
#     id = request.GET.get('id')
    
#     try:
#         event = Evento.objects.get(id=id)
#     except Evento.DoesNotExist:
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))
    
#     # Check if the user is a superuser or the author of the event
#     if request.user.is_superuser or request.user == event.author:
#         event.delete()  # Delete the event object
#     else:
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))
    
#     # Redirect back to the referring page or a default path
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))

# @login_required
# def decline_event(request):
#     id = request.GET.get('id')
#     comment = request.GET.get('comment')
    
#     try:
#         event = Evento.objects.get(id=id)
#     except Evento.DoesNotExist:
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))
    
#     # Check if the user is a superuser or the author of the event
#     if request.user.is_superuser:
#         event.denied = True
#         event.note =  comment 
#         event.save()
#     else:
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))
    
#     # Redirect back to the referring page or a default path
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))

# @login_required
# def approve_event(request):
#     id = request.GET.get('id')
#     comment = request.GET.get('comment')
    
#     try:
#         event = Evento.objects.get(id=id)
#     except Evento.DoesNotExist:
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))
    
#     # Check if the user is a superuser or the author of the event
#     if request.user.is_superuser:
#         event.approved = True
#         event.denied = False
#         event.note =  None
#         event.save()
#     else:
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))
    
#     # Redirect back to the referring page or a default path
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))


# @login_required(login_url='accounts:login')
# def dettaglio_evento(request, id):
#     evento=None
#     if request.user.is_superuser:
#         evento = Evento.objects.get(id=id)
#     else:
#         evento = Evento.objects.get(id=id, author=request.user)
        

#     # Group the orari queryset by orario_da and orario_a using Python loops and dictionaries
#     orari_grouped = {}
#     for orario in orari:
#         orario_da = orario.orario_da.strftime('%H:%M') if orario.orario_da else None
#         orario_a = orario.orario_a.strftime('%H:%M') if orario.orario_a else None
#         orario_key = (orario_da, orario_a)
#         if orario_key in orari_grouped:
#             orari_grouped[orario_key]['giorni'].append(orario.giorno)
#         else:
#             orari_grouped[orario_key] = {
#                 'evento': evento.id,
#                 'orario_da': orario_da,
#                 'orario_a': orario_a,
#                 'giorni': [orario.giorno],
#             }

#     # Convert the orari_grouped dictionary to a list
#     orari_grouped_list = [
#         {'model': 'orari.time', 'fields': orario_group}
#         for orario_group in orari_grouped.values()
#     ]

    
#     orari_json = json.dumps(orari_grouped_list)

#     all_categories = Categorie.objects.all()

#     categorie_ids = [cat.categoria.id for cat in categorie]
#     for category in all_categories:
#         category.selected = category.id in categorie_ids


#     context = {
#         'evento': evento,
#         'categorie': categorie,
#         'orari': orari_json,
#         'all_categories': all_categories,
#     }

#     return render(request, 'iniziative/dettaglio-evento.html', context)


# @login_required(login_url='accounts:login')
# def duplica_evento(request, id):
#     evento=None
#     if request.user.is_superuser:
#         evento = Evento.objects.get(id=id)
#     else:
#         evento = Evento.objects.get(id=id, author=request.user)

#     categorie = CategorieEvento.objects.filter(evento=evento)
#     orari = Time.objects.filter(evento=evento)
    

#     # Group the orari queryset by orario_da and orario_a using Python loops and dictionaries
#     orari_grouped = {}
#     for orario in orari:
#         orario_da = orario.orario_da.strftime('%H:%M') if orario.orario_da else None
#         orario_a = orario.orario_a.strftime('%H:%M') if orario.orario_a else None
#         orario_key = (orario_da, orario_a)
#         if orario_key in orari_grouped:
#             orari_grouped[orario_key]['giorni'].append(orario.giorno)
#         else:
#             orari_grouped[orario_key] = {
#                 'evento': evento.id,
#                 'orario_da': orario_da,
#                 'orario_a': orario_a,
#                 'giorni': [orario.giorno],
#             }

#     # Convert the orari_grouped dictionary to a list
#     orari_grouped_list = [
#         {'model': 'orari.time', 'fields': orario_group}
#         for orario_group in orari_grouped.values()
#     ]

    
#     orari_json = json.dumps(orari_grouped_list)

#     all_categories = Categorie.objects.all()

#     categorie_ids = [cat.categoria.id for cat in categorie]
#     for category in all_categories:
#         category.selected = category.id in categorie_ids


#     context = {
#         'evento': evento,
#         'categorie': categorie,
#         'orari': orari_json,
#         'all_categories': all_categories,
#     }

#     return render(request, 'iniziative/duplica-evento.html', context)



# def compress_image(image_file, quality=85):
#     """
#     Compresses the provided image file and returns the compressed image.

#     Parameters:
#     - image_file: The image file object (uploaded file).
#     - quality: The quality level of the compressed image (0 - 100). Default is 85.

#     Returns:
#     - The compressed image file object.
#     """
#     try:
#         # Apri l'immagine utilizzando Pillow
#         image = Image.open(image_file)

#         # Comprimi l'immagine
#         output_buffer = BytesIO()

#         if image.format == 'JPEG':
#             output_format = 'JPEG'
#         elif image.format == 'PNG':
#             output_format = 'PNG'
#         else:
#             # If it's neither JPEG nor PNG, you can choose a default format
#             output_format = 'JPEG'

#         image.save(output_buffer, format=output_format, quality=quality)

#         # Crea un nuovo file temporaneo per l'immagine compressa
#         compressed_image_file = ContentFile(output_buffer.getvalue(), name=image_file.name)

#         return compressed_image_file

#     except Exception as e:
#         print(f"An error occurred while compressing the image: {e}")
#         return None




# @login_required(login_url='accounts:login')
# def modifica_evento(request):
#     if request.method == "POST":
#         # Get event data from the form
#         id_evento = request.POST.get('id_evento')
#         nome = request.POST.get('nome')
#         website = request.POST.get('website')
#         descrizione = request.POST.get('descrizione')

#         copertina_file = request.FILES.get('copertina')  # get the file from FILES instead of POST
#         if copertina_file:
#             compressed_copertina_file = compress_image(copertina_file)

#         data_da = request.POST.get('data_da')
#         data_a = request.POST.get('data_a')
#         if data_a == '':
#             data_a = None

#         # Get luogo data from the form
#         id_luogo = request.POST.get('id_luogo')
#         nome_luogo = request.POST.get('nome_luogo')
#         indirizzo = request.POST.get('indirizzo')
#         edificio = request.POST.get('edificio')
#         cap = request.POST.get('cap')
#         provincia = request.POST.get('provincia')
#         is_fixed = request.POST.get('is_fixed') == 'on'

#         # Get categories data from the form (this will be a list of selected category IDs)
#         selected_categories = request.POST.getlist('new_categories')
#         selected_orari = request.POST.get('orari')
#         selected_orari = json.loads(selected_orari)


#         # Get or create the Luogo object
#         if cap == '' and indirizzo == '':
#             luogo_obj, luogo_created = Luogo.objects.get_or_create(
#                 id=id_luogo,
#                 defaults={
#                     'nome': nome_luogo,
#                     'indirizzo': indirizzo,
#                     'edificio': edificio,
#                     'cap': cap,
#                     'provincia': provincia
#                 }
#             )
#             if not luogo_created:
#                 luogo_obj.nome = nome_luogo
#                 luogo_obj.indirizzo = indirizzo
#                 luogo_obj.edificio= edificio
#                 luogo_obj.cap = cap
#                 luogo_obj.provincia= provincia
#                 luogo_obj.save()
                
#         elif indirizzo == '' or indirizzo == None:
#             luogo_obj, luogo_created = Luogo.objects.get_or_create(
#                 id=id_luogo,
#                 defaults={
#                     'nome': nome_luogo,
#                     'cap': cap,
#                     'provincia': provincia
#                 }
#             )
#             if not luogo_created:
#                 luogo_obj.nome = nome_luogo
#                 luogo_obj.cap = cap
#                 luogo_obj.provincia= provincia
#                 luogo_obj.save()
#         elif cap == '' or cap == None:
#             luogo_obj, luogo_created = Luogo.objects.get_or_create(
#                 id=id_luogo,
#                 defaults={
#                     'nome': nome_luogo,
#                     'indirizzo': indirizzo,
#                     'edificio': edificio,
#                     'provincia': provincia
#                 }
#             )
#             if not luogo_created:
#                 luogo_obj.nome = nome_luogo
#                 luogo_obj.indirizzo = indirizzo
#                 luogo_obj.edificio= edificio
#                 luogo_obj.provincia= provincia
#                 luogo_obj.save()
#         else:
#             luogo_obj, luogo_created = Luogo.objects.get_or_create(
#                 id=id_luogo,
#                 defaults={
#                     'nome': nome_luogo,
#                     'indirizzo': indirizzo,
#                     'edificio': edificio,
#                     'cap': cap,
#                     'provincia': provincia
#                 }
#             )
            
#             if not luogo_created:
#                 luogo_obj.nome = nome_luogo
#                 luogo_obj.indirizzo = indirizzo
#                 luogo_obj.edificio= edificio
#                 luogo_obj.cap = cap
#                 luogo_obj.provincia= provincia
#                 luogo_obj.save()
        
#         # Get or create the Evento object
#         if request.user.is_superuser:
#             evento, created = Evento.objects.get_or_create(
#                 id=id_evento,
#                 defaults={
#                     'nome': nome,
#                     'descrizione': descrizione,
#                     'copertina': compressed_copertina_file if copertina_file else None,  # set default copertina value
#                     'data_da': data_da,
#                     'data_a': data_a,
#                     'is_fixed': is_fixed,
#                     'website': website,
#                     'denied': False,
#                 }
#             )
#             if not created:
#                 evento.nome = nome
#                 evento.descrizione = descrizione
#                 if copertina_file:  # if a new file was uploaded, update copertina
#                     evento.copertina = compressed_copertina_file
#                 evento.data_da = data_da
#                 evento.data_a = data_a
#                 evento.is_fixed = is_fixed
#                 evento.website = website
#                 evento.denied = False

#             evento.save()
#         else:
#             evento, created = Evento.objects.get_or_create(
#                 id=id_evento, author=request.user,
#                 defaults={
#                     'nome': nome,
#                     'descrizione': descrizione,
#                     'copertina': compressed_copertina_file if copertina_file else None,  # set default copertina value
#                     'data_da': data_da,
#                     'data_a': data_a,
#                     'website': website,
#                     'approved': False,
#                     'denied': False,
#                 }
#             )
#             if not created:
#                 evento.nome = nome
#                 evento.descrizione = descrizione
#                 if copertina_file:  # if a new file was uploaded, update copertina
#                     evento.copertina = compressed_copertina_file
#                 evento.data_da = data_da
#                 evento.data_a = data_a
#                 evento.website = website
#                 evento.approved = False
#                 evento.denied = False
#                 evento.author = request.user
#             evento.save()

#         # Remove the current categories associated with the event
#         ##evento.categorieevento_set.clear()
#         categorie_evento_list = CategorieEvento.objects.filter(evento=evento)
#         categorie_evento_list.delete()

#         # Add the selected categories to the event
#         for category_id in selected_categories:
#             category = Categorie.objects.get(pk=category_id)
#             CategorieEvento.objects.create(categoria=category, evento=evento)

        
#         orari_evento_list = Time.objects.filter(evento=evento)
#         orari_evento_list.delete()

#         for orario in selected_orari:
#             if orario['fields']['giorni'] == []:
#                 if not orario['fields']['orario_a']:
#                     orario_new_obj = Time.objects.create(
#                         evento=evento, 
#                         orario_da=orario['fields']['orario_da'], 
#                     )
#                 else:
#                     orario_new_obj = Time.objects.create(
#                         evento=evento, 
#                         orario_da=orario['fields']['orario_da'],
#                         orario_a= orario['fields']['orario_a'],

#                     )
#             else:
#                 for giorno in orario['fields']['giorni']:
#                     if not orario['fields']['orario_a']:
#                         orario_new_obj = Time.objects.create(
#                             evento=evento, 
#                             orario_da=orario['fields']['orario_da'], 
#                             giorno=giorno
#                         )
#                     else:
#                         orario_new_obj = Time.objects.create(
#                             evento=evento, 
#                             orario_da=orario['fields']['orario_da'], 
#                             orario_a=orario['fields']['orario_a'],
#                             giorno=giorno
#                         )

#         evento = Evento.objects.get(id=id_evento)

#         if evento.is_fixed:
#             return redirect('iniziative:lista-eventi-ricorrenti')
#         else:
#             return redirect('iniziative:lista-eventi')
#     # If the request method is not POST, handle the GET request here if needed

#     return redirect('iniziative:lista-eventi')

# @login_required(login_url='accounts:login')
# def add_evento_csv(request):
#     if request.method == "POST":
#     #evento
#         nome = request.POST.get('nome')
#         descrizione = request.POST.get('descrizione')

#         copertina_file = request.FILES.get('copertina')
#         if copertina_file:
#             compressed_copertina_file = compress_image(copertina_file)
#         else:
#             default_image_url = request.POST.get('default_image')
#             full_default_image_url = f"https://teramo-eventi.s3.nl-ams.scw.cloud/media/{default_image_url}"

#             response = requests.get(full_default_image_url)

#             if response.status_code == 200:
#                 compressed_copertina_file = ContentFile(response.content)
#                 desired_filename = 'default_event_image.jpg'
#                 compressed_copertina_file.name = desired_filename
#             else:
#                 raise ValueError("Couldn't fetch the default image.")


#         website = request.POST.get('website')
#         data_da = request.POST.get('data_da')
#         categorie = request.POST.getlist('new_categories')
#         data_da = request.POST.get('data_da')
#         data_a = request.POST.get('data_a')
#         data_a = None if data_a == '' else data_a
#         user = request.user

#         selected_categories = request.POST.getlist('new_categories')
#         selected_orari = json.loads(request.POST.get('orari'))

#         luogo_args = {
#             'nome': request.POST.get('nome_luogo'),
#             'indirizzo': request.POST.get('indirizzo') or None,
#             'edificio': request.POST.get('edificio') or None,
#             'cap': request.POST.get('cap') or None,
#             'provincia': request.POST.get('provincia'),
#             'edificio': request.POST.get('edificio') or None
#         }

#         luogo_obj = Luogo.objects.create(**luogo_args)
        
#         evento_obj = Evento.objects.create(
#             nome=nome,
#             descrizione=descrizione,
#             luogo=luogo_obj,
#             copertina=compressed_copertina_file,
#             data_da=data_da,
#             data_a=data_a,
#             website=website,
#             author=user
#         )

#         for category_id in selected_categories:
#             category = Categorie.objects.get(pk=category_id)
#             CategorieEvento.objects.create(categoria=category, evento=evento_obj)

    
#         for orario in selected_orari:
#             orario_da = orario['fields']['orario_da']
#             orario_a = orario['fields']['orario_a']
#             giorni = orario['fields']['giorni']


#             if giorni == []:
#                 if not orario_a:
#                     orario_new_obj = Time.objects.create(
#                         evento=evento_obj, 
#                         orario_da=orario_da, 
#                     )
#                 else:
#                     orario_new_obj = Time.objects.create(
#                         evento=evento_obj, 
#                         orario_da=orario_da, 
#                         orario_a=orario_a, 
#                     )
#             else:
#                 for giorno in giorni:
#                     if not orario_a:
#                         orario_new_obj = Time.objects.create(
#                             evento=evento_obj, 
#                             orario_da=orario_da, 
#                             giorno=giorno
#                         )
#                     else:
#                         orario_new_obj = Time.objects.create(
#                             evento=evento_obj, 
#                             orario_da=orario_da, 
#                             orario_a=orario_a, 
#                             giorno=giorno
#                         )


#         # Handle other form fields as necessary

#         return redirect('iniziative:lista-eventi')
    
#     else:
#         return print('negativo')


# @login_required(login_url='accounts:login')
# def add_evento(request):
#     try:
#         if request.method == "POST":
#         #evento
#             nome = request.POST.get('nome')
#             descrizione = request.POST.get('descrizione')
#             copertina_file = request.FILES.get('copertina')
#             if copertina_file:
#                 compressed_copertina_file = compress_image(copertina_file)
#             else:
#                 default_image_url = request.POST.get('default_image')
#                 full_default_image_url = f"https://teramo-eventi.s3.nl-ams.scw.cloud/media/{default_image_url}"

#                 response = requests.get(full_default_image_url)

#                 if response.status_code == 200:
#                     compressed_copertina_file = ContentFile(response.content)
#                     desired_filename = 'default_event_image.jpg'
#                     compressed_copertina_file.name = desired_filename
#                 else:
#                     raise ValueError("Couldn't fetch the default image.")

#             website = request.POST.get('website')
#             data_da = request.POST.get('data_da')
#             categorie = request.POST.getlist('new_categories')
#             data_da = request.POST.get('data_da')
#             data_a = request.POST.get('data_a')
#             is_fixed = request.POST.get('is_fixed') == 'on'
#             data_a = None if data_a == '' else data_a
#             user = request.user

#             selected_categories = request.POST.getlist('new_categories')
#             selected_orari = json.loads(request.POST.get('orari'))

#             luogo_args = {
#                 'nome': request.POST.get('nome_luogo'),
#                 'indirizzo': request.POST.get('indirizzo') or None,
#                 'edificio': request.POST.get('edificio') or None,
#                 'cap': request.POST.get('cap') or None,
#                 'provincia': request.POST.get('provincia'),
#                 'edificio': request.POST.get('edificio') or None
#             }

#             luogo_obj = Luogo.objects.create(**luogo_args)
            
#             if request.user.is_superuser:
#                 evento_obj = Evento.objects.create(
#                     nome=nome,
#                     descrizione=descrizione,
#                     luogo=luogo_obj,
#                     copertina=compressed_copertina_file,
#                     data_da=data_da,
#                     data_a=data_a,
#                     is_fixed=is_fixed,
#                     website=website,
#                     author=user,
#                 )
#             else:
#                 evento_obj = Evento.objects.create(
#                     nome=nome,
#                     descrizione=descrizione,
#                     luogo=luogo_obj,
#                     copertina=compressed_copertina_file,
#                     data_da=data_da,
#                     data_a=data_a,
#                     is_fixed=is_fixed,
#                     website=website,
#                     author=user,
#                     approved=False
#                 )

#             for category_id in selected_categories:
#                 category = Categorie.objects.get(pk=category_id)
#                 CategorieEvento.objects.create(categoria=category, evento=evento_obj)

        
#             for orario in selected_orari:
#                 orario_da = orario['fields']['orario_da']
#                 orario_a = orario['fields']['orario_a']
#                 giorni = orario['fields']['giorni']


#                 if giorni == []:
#                     if not orario_a:
#                         orario_new_obj = Time.objects.create(
#                             evento=evento_obj, 
#                             orario_da=orario_da, 
#                         )
#                     else:
#                         orario_new_obj = Time.objects.create(
#                             evento=evento_obj, 
#                             orario_da=orario_da, 
#                             orario_a=orario_a, 
#                         )
#                 else:
#                     for giorno in giorni:
#                         if not orario_a:
#                             orario_new_obj = Time.objects.create(
#                                 evento=evento_obj, 
#                                 orario_da=orario_da, 
#                                 giorno=giorno
#                             )
#                         else:
#                             orario_new_obj = Time.objects.create(
#                                 evento=evento_obj, 
#                                 orario_da=orario_da, 
#                                 orario_a=orario_a, 
#                                 giorno=giorno
#                             )


#             # Handle other form fields as necessary
#             if is_fixed:
#                 return redirect('iniziative:lista-eventi-ricorrenti')
#             else:
#                 return redirect('iniziative:lista-eventi')
#         else:
#             return print('negativo')
#     except Exception as e:
#         print(f"ADD_EVENT Error occurred: {e}")
#         return HttpResponse(f"An error occurred: {e}", status=500)  # HTTP 500 Internal Server Error

# class EventiSegnalatiCreateView(APIView):
#     def post(self, request, format=None):
#         serializer = EventiSegnalatiSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class OrganizzatoriRichiesteCreateView(APIView):
#     def post(self, request, format=None):
#         serializer = OrganizzatoriRichiesteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# API_ENDPOINT = 'https://www.abruzzooggi.it/eventi/?orderby%5B0%5D=event_start_date&orderby%5B1%5D=event_start_time&orderby%5B2%5D=event_name&pagination=1&full=1&ajaxCalendar=1&mo=8&yr=2023&em_ajax=1'

# def modify_mo_param(url, new_mo_value, new_year_value):
#     # Parse the URL
#     parsed_url = urlparse(url)
    
#     # Extract and parse the query parameters
#     query_params = parse_qs(parsed_url.query)
    
#     # Update the 'mo' parameter value
#     query_params['mo'] = [new_mo_value]
#     query_params['yr'] = [new_year_value]
    
#     # Encode the query parameters back to a string
#     new_query_string = urlencode(query_params, doseq=True)
    
#     # Construct the new URL
#     modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment))
    
#     return modified_url

# @user_passes_test(admin_check)
# def scrape_ancora(request):
    
#     url=request.GET.get('link')
#     parsed_url = urlparse(url)
#     query_params = parse_qs(parsed_url.query)
#     query_params['pagination'] = [0]
#     new_query_string = urlencode(query_params, doseq=True)
#     link = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment))

#     response = requests.get(link)
#     soup = BeautifulSoup(response.content, "html.parser")

#     # Find the table containing event data
#     table = soup.find("table", class_="events-table")
#     tbody = table.find("tbody")

#     # Define CSV file name
#     csv_filename = "events.csv"

#     # Check if the CSV file already exists
#     if os.path.exists(csv_filename):
#         print(f"The file '{csv_filename}' already exists. Appending data.")
#         mode = "a"  # Append mode
#     else:
#         print(f"The file '{csv_filename}' does not exist. Creating new file.")
#         mode = "w"  # Write mode

#     with open(csv_filename, mode, newline="", encoding="utf-8") as csvfile:
#         csv_writer = csv.writer(csvfile)

#         # Write header only if it's a new file
#         if mode == "w":
#             csv_writer.writerow(["Date", "Event", "Link", "Image", "Date/Time", "Location", "Description", "Categories"])

#         # Iterate through each row in the table
#         for row in tbody.find_all("tr"):
#             columns = row.find_all("td")
            
#             date_string = columns[0].get_text(strip=True)
#             start_date_str = date_string[:10]
#             start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
#             formatted_date = start_date.strftime("%Y-%m-%d")



#             event_info = columns[1].get_text(strip=True)
#             event_link = columns[1].find("a")["href"]

#             if "<br>" in event_info:
#                 event, location = event_info.split("<br>")
#                 event = event.strip()
#                 location = location.strip("<i>").strip("</i>")
#             else:
#                 event = event_info.strip()
#                 location = ""  # Set location to empty if no delimiter is found
            
#             # Write the data to the CSV file
#             csv_writer.writerow([formatted_date, event, event_link, "", "", location, "", ""])

    
#     # Create a temporary list to hold the rows you want to keep
#     updated_rows = []

#     main_link = url.split('?')[0]

#     with open(csv_filename, "r", newline="", encoding="utf-8") as csvfile:
#         csv_reader = csv.reader(csvfile)
#         for row in csv_reader:
#             row_url = row[2]  # Assuming row[2] contains the URL
            
#             # Extract the main part of the row URL
#             main_row_link = row_url.split('?')[0]
            
#             if main_row_link != main_link:
#                 updated_rows.append(row)

#     # Rewrite the CSV file with the updated rows
#     with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
#         csv_writer = csv.writer(csvfile)
#         for row in updated_rows:
#             csv_writer.writerow(row)

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))

# def scrape_and_save_to_csv(new_mo_value, new_year_value):
#     new_url = modify_mo_param(API_ENDPOINT, new_mo_value, new_year_value)
    
#     response = requests.get(new_url)
    
#     if response.status_code != 200:
#         print("Error fetching data")
#         return
    
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Extract new event data
#     new_events = []
#     for td in soup.find_all("td", class_="eventful"):
#         day = td.a.string
#         for li in td.ul.find_all("li"):
#             title = li.a.string
#             link = li.a['href']
#             date_str = f"{new_year_value}/{new_mo_value}/{day}"  # concatenate year, month, and dayù

#             event_date = datetime.strptime(date_str, "%Y/%m/%d").date()
#             today = datetime.today().date()

#             if event_date >= today:
#                 formatted_date = event_date.strftime("%Y-%m-%d")  # format the date in the desired format
#                 new_events.append([formatted_date, title, link, '','','','', ''])

#     # If CSV exists, read the existing data
#     old_events = []
#     existing_keys = set()
#     if os.path.exists('events.csv'):
#         with open('events.csv', 'r') as csvfile:
#             csv_reader = csv.reader(csvfile)
#             # Skip the header row
#             next(csv_reader, None)
#             for row in csv_reader:
#                 existing_keys.add(row[0] + row[2])  # row[0] is date, row[2] is link
#                 print('key',row[0] + row[2])
#                 old_events.append(row)

#     unique_new_events = [event for event in new_events if event[0] + event[2] not in existing_keys]

#     # Write old and new data to CSV
#     with open('events.csv', 'w', newline='') as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(['Date', 'Event', 'Link', 'Image', 'Date/Time', 'Location', 'Description', 'Categories'])  # updated header
#         csv_writer.writerows(old_events)  # write old events
#         csv_writer.writerows(unique_new_events)  # write new events


# def scrape_view(request):
#     new_month_value = request.GET.get('month')
#     new_year_value = request.GET.get('year')
#     if not new_month_value:
#         return HttpResponseBadRequest("The 'month' parameter is required.")
    
#     if not new_year_value:
#         return HttpResponseBadRequest("The 'year' parameter is required.")
    
#     scrape_and_save_to_csv(new_month_value, new_year_value)
    
#     return HttpResponse("Data has been scraped and saved to events.csv")

# def read_csv_file():
#     data = []
#     with open('events.csv', 'r') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             data.append(row)
#     return data

# @user_passes_test(admin_check)
# def display_csv(request):
#     data = read_csv_file()
#     header = data[0]  # assuming the first row of CSV contains header
#     rows = data[1:]   # rest of the data

#     with open("links_file.txt", "r") as file:
#         saved_links = file.readlines()

#     # Add a flag in each row if the link exists in the saved_links
#     for row in rows:
#         link = row[2]
#         if link + "\n" in saved_links:
#             row.append(True)  # indicates the link exists
#         else:
#             row.append(False)

#     return render(request, 'csv_display.html', {'header': header, 'rows': rows})

# def read_csv_file_data():
#     data = []
#     with open('event_data.csv', 'r') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             data.append(row)
#     return data

# @user_passes_test(admin_check)
# def display_csv_data(request):
#     data = read_csv_file_data()
#     header = data[0]  # assuming the first row of CSV contains header
#     rows = data[1:]   # rest of the data
#     return render(request, 'csv_display_detail.html', {'header': header, 'rows': rows})


# def fetch_event_data_from_url(url):
#     response = requests.get(url)
#     response.raise_for_status()
#     html_content = response.text

#     soup = BeautifulSoup(html_content, 'html.parser')

#     img_tag = soup.find("div", class_="post-thumbnail")
#     image_url = img_tag.img["data-src"] if img_tag and img_tag.img else ""

#     data_time_elem = soup.find("strong", string="Data / Ora")
#     data_time = data_time_elem.find_next_sibling().get_text(strip=True) if data_time_elem and data_time_elem.find_next_sibling() else ""

#     location_elem = soup.find("strong", string="Luogo")
#     location = location_elem.find_next_sibling("a").get_text(strip=True) if location_elem and location_elem.find_next_sibling("a") else ""


#     # Find the event-categories div
#     event_categories = soup.find('ul', class_='event-categories')
#     categories = []

#     if event_categories:
#         for li in event_categories.find_all('li'):
#             category = li.get_text(strip=True)
#             categories.append(category)

#     # Format the categories into [cat1:cat2] format
#     formatted_categories = '' + ' - '.join(categories)


#     description = None

#     entry_content = soup.find('div', class_='entry-content')

#     if entry_content:

#         plain_text = entry_content.get_text(strip=True, separator=' ')
#         # Clean out any excessive whitespace
#         clean_text = ' '.join(plain_text.split())
#         try:
#             clean_text = clean_text.replace("Mappa non disponibile", "").strip()
#         except Exception as e:
#             pass


#         # Remove everything after 'Foto tratta'
#         cutoff_index = clean_text.find('Foto tratta')
#         if cutoff_index != -1:
#             clean_text = clean_text[:cutoff_index].strip()

#                 # Remove everything after 'Foto tratta'
#         cutoff_index = clean_text.find('Consulta il nostro Calendario Eventi')
#         if cutoff_index != -1:
#             clean_text = clean_text[:cutoff_index].strip()

#         description = clean_text

#     else:
#         print("entry-content class not found.")


#     if image_url:
#         image_response = requests.get(image_url, stream=True)
#         image_response.raise_for_status()

#         image_extension = os.path.splitext(image_url)[-1]  # Extract the file extension (e.g., .jpg, .png)
#         random_image_name = f"{uuid.uuid4()}{image_extension}"

#         # Save the file using Django's storage API
#         django_file = ContentFile(image_response.content)
#         image_path = default_storage.save("events_images/" + random_image_name, django_file)
#     else:
#         image_path = ""

#     return image_path, data_time, location, description, formatted_categories



# @user_passes_test(admin_check)
# def update_event(request):
#     if request.method == "POST":
#         date = request.POST.get("date")
#         link = request.POST.get("link")

#         image_path, data_time, location, description, categories = fetch_event_data_from_url(link)


#         # Read events from CSV
#         with open('events.csv', 'r') as csvfile:
#             csv_reader = csv.reader(csvfile)
#             events = [row for row in csv_reader]

#         # Update the specific event description
#         for event in events:
#             if event[0] == date and event[2] == link:
#                 event[3] = image_path  # Image
#                 event[4] = data_time   # Date/Time
#                 event[5] = location    # Location
#                 event[6] = description # Description
#                 event[7] = categories # Description
#                 break

#         # Write updated events back to CSV
#         with open('events.csv', 'w', newline='') as csvfile:
#             csv_writer = csv.writer(csvfile)
#             csv_writer.writerows(events)

#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))

# def save_link(request):
#     link = request.GET.get("link")
    
#     # Save the link to another file
#     if link:
#         with open("links_file.txt", "a") as file:
#             file.write(link + "\n")

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))


# def reset_event(request):
#     link_to_remove = request.GET.get("link", "")

#     if link_to_remove:
#         with open("links_file.txt", "r") as file:
#             lines = file.readlines()

#         # Remove the link
#         with open("links_file.txt", "w") as file:
#             for line in lines:
#                 # Check if the line contains the link and is not just a newline character
#                 if line.strip() != link_to_remove:
#                     file.write(line)

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))



# @user_passes_test(admin_check)
# def add_abr_oggi_event(request):
#     event_to_pass = None

#     if request.method == "POST":
#         date = request.POST.get("date")
#         link = request.POST.get("link")

        
#         with open('events.csv', 'r') as csvfile:
#             csv_reader = csv.reader(csvfile)
#             events = [row for row in csv_reader]

        
#         for event in events:
#             if event[0] == date and event[2] == link:
#                 event_to_pass = event
#                 break
 
#         all_categories = Categorie.objects.all()
    

#         if event_to_pass:
#             context = {
#                 'evento': event_to_pass,
#                 'all_categories': all_categories,
#                 'provinces': Luogo.PROVINCIA_CHOICES
#             }
        
#         return render(request, 'add-eventocsv.html',context)

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))

# @user_passes_test(admin_check)
# def display_links_file(request):
#     with open("links_file.txt", "r") as file:
#         content = file.read()
#     return HttpResponse(content, content_type="text/plain")

# @login_required(login_url='accounts:login')
# def search_eventi(request):
#     query = request.GET.get('q', '')
#     page_num = request.GET.get('page', 1)
#     items_per_page = 300  # You can adjust this as per your requirements

#     # Define the base queryset
#     base_query = CategorieEvento.objects.select_related('evento', 'categoria').order_by('-evento__id')

#     # Filter the events based on the user privileges
#     if not request.user.is_superuser:
#         base_query = base_query.filter(evento__author=request.user)

#     # If there's a search query, filter events based on it
#     if query:
#         base_query = base_query.filter(Q(evento__nome__icontains=query) | Q(categoria__name__icontains=query))

#     # Group events with their categories
#     events_with_categories = defaultdict(list)
#     for ce in base_query:
#         events_with_categories[ce.evento].append(ce.categoria)  # Append the category object

#     events_list = list(events_with_categories.items())
#     paginator = Paginator(events_list, items_per_page)
#     page = paginator.get_page(page_num)

#     # Format the data for DataTables
#     data = []
#     for event, categories in page:
#         categories_html = ""
#         for category in categories:
#             categories_html += f"<div style='display: inline-flex' class='border p-2 rounded'>"
#             if category.image:
#                 categories_html += f"<img src='{category.image.url}' alt='icon' class='category-icon'>"
#             categories_html += f"{category.name}</div> "
        
        

#         event_name_html = (
#             f"sito: {event.website}<br>"
#             f"<span class='event-name'><a href='dettaglio-evento/{event.id}'>{event.nome}</a></span><br>"
#         )

#         event_description = event.descrizione
        
#         event_image = (f"")

#         if event.copertina:
#             event_image = (
#                     f"<img src='{event.copertina.url}' alt='Copertina' class='img-thumbnail cover-img'>"
#             )

#         event_luogo = ("")
#         if event.luogo:
#             event_luogo = (
#                     f"{event.luogo.provincia}<br>"
#                     f"{event.luogo.edificio}<br>"
#                     f"{event.luogo.indirizzo}<br>"
#                     f"{event.luogo.cap}<br>"
#                     f"{event.luogo.nome}"
#             )

#         event_da = ("")
#         if event.data_da:
#             event_da = (
#                     f"{event.data_da}<br>"
#             )
    
#         data.append({
#             'event_id': event.id,
#             'event_copertina': event_image,
#             'event_name': event_name_html, 
#             'event_description': event_description, 
#             'categories': categories_html,
#             'event_luogo': event_luogo,
#             'event_da': event_da,
#             })


#     response = {
#         'data': data
#     }

#     return JsonResponse(response)

# @login_required(login_url='accounts:login')
# def lista_eventi_api(request):
#     order_by_field = request.GET.get('order_by', '-id')
#     search_query = request.GET.get('search', '')

#     if request.user.is_superuser:
#         if search_query:
#             eventi = Evento.objects.filter(
#                 Q(data_da__icontains=search_query,is_fixed=False) |
#                 Q(data_a__icontains=search_query,is_fixed=False) |
#                 Q(nome__icontains=search_query,is_fixed=False)  |
#                 Q(luogo__nome__icontains=search_query,is_fixed=False) |
#                 Q(luogo__indirizzo__icontains=search_query,is_fixed=False) |
#                 Q(luogo__edificio__icontains=search_query,is_fixed=False) |
#                 Q(luogo__cap__icontains=search_query,is_fixed=False)             
#             ).order_by(order_by_field)
#         else:    
#             eventi = Evento.objects.filter(is_fixed=False).order_by(order_by_field)
    
#         #categorie_eventi = CategorieEvento.objects.select_related('evento', 'categoria').order_by('-evento__id')
#     else:
#         if search_query:
#             eventi = Evento.objects.filter(
#                 Q(data_da__icontains=search_query, author=request.user) |
#                 Q(data_a__icontains=search_query, author=request.user) |
#                 Q(nome__icontains=search_query, author=request.user) 
#             ).order_by(order_by_field)
#         else:    
#             eventi = Evento.objects.filter(author=request.user).order_by(order_by_field)
#         #categorie_eventi = CategorieEvento.objects.filter(evento__author=request.user).select_related('evento', 'categoria').order_by('-evento__id')

#     paginator = Paginator(eventi, per_page=10)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)

#     serializer = EventoSerializer(page_obj, many=True)


#     data = {
#         'results': serializer.data,
#         'current_page': page_obj.number,
#         'total_pages': paginator.num_pages,
#         'has_previous': page_obj.has_previous(),
#         'has_next': page_obj.has_next(),
#         'total_count': eventi.count()  # Adding the total count here
#     }

#     return JsonResponse(data)

# @login_required(login_url='accounts:login')
# def lista_eventi_da_approvare_api(request):
#     order_by_field = request.GET.get('order_by', '-id')
#     search_query = request.GET.get('search', '')

#     if request.user.is_superuser:
#         if search_query:
#             eventi = Evento.objects.filter(
#                 Q(data_da__icontains=search_query,approved=False) |
#                 Q(data_a__icontains=search_query,approved=False) |
#                 Q(nome__icontains=search_query,approved=False)  |
#                 Q(luogo__nome__icontains=search_query,approved=False) |
#                 Q(luogo__indirizzo__icontains=search_query,approved=False) |
#                 Q(luogo__edificio__icontains=search_query,approved=False) |
#                 Q(luogo__cap__icontains=search_query,approved=False)             
#             ).order_by(order_by_field)
#         else:    
#             eventi = Evento.objects.filter(approved=False).order_by(order_by_field)
    
#         #categorie_eventi = CategorieEvento.objects.select_related('evento', 'categoria').order_by('-evento__id')
#     else:
#         if search_query:
#             eventi = Evento.objects.filter(
#                 Q(data_da__icontains=search_query, author=request.user) |
#                 Q(data_a__icontains=search_query, author=request.user) |
#                 Q(nome__icontains=search_query, author=request.user) 
#             ).order_by(order_by_field)
#         else:    
#             eventi = Evento.objects.filter(author=request.user).order_by(order_by_field)
#         #categorie_eventi = CategorieEvento.objects.filter(evento__author=request.user).select_related('evento', 'categoria').order_by('-evento__id')

#     paginator = Paginator(eventi, per_page=10)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)

#     serializer = EventoSerializer(page_obj, many=True)


#     data = {
#         'results': serializer.data,
#         'current_page': page_obj.number,
#         'total_pages': paginator.num_pages,
#         'has_previous': page_obj.has_previous(),
#         'has_next': page_obj.has_next(),
#         'total_count': eventi.count()  # Adding the total count here
#     }

#     return JsonResponse(data)

# @login_required(login_url='accounts:login')
# def lista_eventi_ricorenti_api(request):
#     order_by_field = request.GET.get('order_by', '-id')
#     search_query = request.GET.get('search', '')

#     if request.user.is_superuser:
#         if search_query:
#             eventi = Evento.objects.filter(
#                 Q(data_da__icontains=search_query, is_fixed=True) |
#                 Q(data_a__icontains=search_query,is_fixed=True) |
#                 Q(nome__icontains=search_query,is_fixed=True)  |
#                 Q(luogo__nome__icontains=search_query,is_fixed=True) |
#                 Q(luogo__indirizzo__icontains=search_query,is_fixed=True) |
#                 Q(luogo__edificio__icontains=search_query,is_fixed=True) |
#                 Q(luogo__cap__icontains=search_query,is_fixed=True)             
#             ).order_by(order_by_field)
#         else:    
#             eventi = Evento.objects.filter(is_fixed=True).order_by(order_by_field)
    
#         #categorie_eventi = CategorieEvento.objects.select_related('evento', 'categoria').order_by('-evento__id')
#     else:
#         if search_query:
#             eventi = Evento.objects.filter(
#                 Q(data_da__icontains=search_query, author=request.user) |
#                 Q(data_a__icontains=search_query, author=request.user) |
#                 Q(nome__icontains=search_query, author=request.user) 
#             ).order_by(order_by_field)
#         else:    
#             eventi = Evento.objects.filter(author=request.user).order_by(order_by_field)
#         #categorie_eventi = CategorieEvento.objects.filter(evento__author=request.user).select_related('evento', 'categoria').order_by('-evento__id')

#     paginator = Paginator(eventi, per_page=10)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)

#     serializer = EventoSerializer(page_obj, many=True)


#     data = {
#         'results': serializer.data,
#         'current_page': page_obj.number,
#         'total_pages': paginator.num_pages,
#         'has_previous': page_obj.has_previous(),
#         'has_next': page_obj.has_next(),
#         'total_count': eventi.count()  # Adding the total count here
#     }

#     return JsonResponse(data)