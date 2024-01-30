from django.shortcuts import render
from board.models import Boards
from falone.decorators import check_staff
from django.core.paginator import Paginator
from worksites.models import Worksites
from worksites.serializers import WorksiteSerializer

@check_staff
def admin(request):
    worksites = Worksites.objects.all()
    boards = Boards.objects.all()

    context = {
        'total_count': worksites.count(),
        'boards':boards,
        'total_count_board': boards.count()
    }
    return render(request,'index.html', context)


@check_staff
def worksites(request):
    worksites = Worksites.objects.filter(is_open=True)

    context = {
        'total_count': worksites.count(), 
        'worksites':worksites,
    }
    return render(request, 'cantieri.html', context)
