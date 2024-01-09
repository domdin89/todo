from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

app_name = 'worksites'
urlpatterns = [
        path('', views.worksites_lists, name='worksites-lists'),
        path('worksites-lists-api/', views.worksites_list_api, name='worksites-lists-api'),
        path('worksite-detail/<int:id>', views.worksite_detail, name='worksite-detail'),
        path('add-worksite/', views.add_worksite, name='add-worksite'),
        path('add-new-worksite/', views.add_new_worksite, name='add-new-worksite'),
        path('delete_worksite/', views.delete_worksite, name='delete-worksite'),
        # path('lista-eventi-ricorrenti/', views.lista_eventi_ricorrenti, name='lista-eventi-ricorrenti'),
        # path('lista-eventi-da-approvare/', views.lista_eventi_da_approvare, name='lista-eventi-da-approvare'),
        # path('lista-eventi-prossimi/', views.lista_eventi_prossimi, name='lista-eventi-prossimi'),
        # path('dettaglio-evento/<int:id>', views.dettaglio_evento, name='dettaglio-evento'),
        # path('duplica-evento/<int:id>', views.duplica_evento, name='duplica-evento'),
        # path('modifica-evento/', views.modifica_evento, name='modifica-evento'),
        # path('nuovo-evento/', views.nuovo_evento, name='nuovo-evento'),
        # path('crea-nuovo-evento/', views.add_evento, name='crea-nuovo-evento'),
        # path('crea-nuovo-evento-csv/', views.add_evento_csv, name='crea-nuovo-evento-csv'),

        # path('lista-utenti/', views.lista_utenti, name='lista-utenti'),



        # path('delete_event/', views.delete_event, name='delete-event'),
        # path('decline_event/', views.decline_event, name='decline-event'),
        # path('approve_event/', views.approve_event, name='approve-event'),

        # path('scrape/', views.scrape_view),
        # path('scrape_ancora/', views.scrape_ancora),
        # path('display_csv/', views.display_csv, name='display-csv'),

        # path('update_event/', views.update_event),
        
        
        # path('display_csv_data/', views.display_csv_data),
        # path('save_link/', views.save_link, name="save_link"),
        # path('reset_event/', views.reset_event),

        # path('add_abr_oggi_event/', views.add_abr_oggi_event),

        # path('links-txt/', views.display_links_file, name='display-links-file'),

        # path('search_eventi/', views.search_eventi),

        # path('api/lista_eventi/', views.lista_eventi_api, name='lista_eventi_api'),
        # path('api/lista_eventi_da_approvare/', views.lista_eventi_da_approvare_api, name='lista_eventi_api'),
        # path('api/lista_eventi_ricorrenti/', views.lista_eventi_ricorenti_api, name='lista_eventi_ricorrenti_api'),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
