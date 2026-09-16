from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),    
    path('package/', views.package, name='package'),    
    path('package/reservation-package/', views.reservation_package, name='reservation_package'),
    path('menu/', views.menu, name='menu'),
    path('room/', views.room, name='room'),
    path('room/book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('room/book-room/', views.book_room, name='book_room'),
    # path('room-list/', views.room_list, name='room_list'),
    # path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    # path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('reviews/', views.reviews_page, name='reviews_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)