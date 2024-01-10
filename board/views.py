from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Boards
from worksites.models import Worksites
from apartments.models import Apartments
from .serializers import BoardSerializer
from apartments.serializers import WorksiteApartmentsSerializer
from django.http import JsonResponse



# Create your views here.
@login_required(login_url='accounts:login')
def board_lists(request):
    return render(request, 'board-lists.html')


@login_required(login_url='accounts:login')
def board_list_api(request):
    order_by_field = request.GET.get('order_by', '-id')
    search_query = request.GET.get('search', '')

    worksites = Boards.objects.all()

    paginator = Paginator(worksites, per_page=10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    serializer = BoardSerializer(page_obj, many=True)


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
def add_board(request):
    apartments = Apartments.objects.all()
    serializer = WorksiteApartmentsSerializer(apartments, many=True)

    context = {
        'apartments': serializer.data

    }
    return render(request, 'new-board.html', context)


@login_required(login_url='accounts:login')
def add_new_board(request):
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
