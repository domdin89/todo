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
    return render(request, 'new-board.html')