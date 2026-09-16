from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_object_or_404
from .models import Menu, Room, Booking, Category, MainContact
from .forms import BookingForm, ReservationForm, ContactForm
from .models import * 
from django.http import HttpResponse, HttpResponseRedirect 
from urllib.parse import quote
import re, html






def home(request): 
    menus = Menu.objects.all()[:4]
    reviews = Review.objects.all().order_by('-id')[:8]
    for review in reviews:
        review.stars_full = [1] * review.rating  # List for full stars
        review.stars_empty = [1] * (5 - review.rating)  # List for empty stars
    rooms = Room.objects.all()[:7]
    context = {
        'menus': menus,
        'title': 'Manahayu Holistic Farm – Home | Sustainable Lifestyle Experience',
        'reviews' : reviews,
        'rooms': rooms,
    }
    return render(request, 'home.html', context)  # Mengarahkan ke template home.html di folder templates/

def about_us(request):
    context = {
        'title': 'Tentang Kami – Manahayu Holistic Farm | Filosofi & Cerita Kami'
    }
    return render(request, 'aboutus.html',context)  # Mengarahkan ke template aboutus.html

# Jangan habus base Func Room
# def room(request):
#     rooms = Room.objects.all()
#     cleaned_rooms = []
#     for room_obj in rooms:
#         if room_obj.description:
#             cleaned_description = html.unescape(room_obj.description)
#             try:
#                 cleaned_description = cleaned_description.encode('latin1').decode('unicode_escape')
#             except UnicodeDecodeError:
#                 pass
#             except Exception as e:
#                 # Tangani error lain jika terjadi selama proses unescape
#                 print(f"Error decoding unicode escape sequence for room {room_obj.id}: {e}")
#             cleaned_description = re.sub(r'\s+', ' ', cleaned_description).strip()

#             # Assign kembali deskripsi yang sudah bersih ke objek room
#             room_obj.description = cleaned_description

#         cleaned_rooms.append(room_obj)

#     context = { 
#         'rooms': cleaned_rooms,
#         'title': 'Manahayu Holistic Farm | Room'
#     }
#     return render(request, 'room/room.html', context)






def room(request):
    rooms = Room.objects.all() # Ambil semua objek Room untuk paginator
    paginator = Paginator(rooms, 4)  # 4 item per halaman, Anda bisa sesuaikan
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # cleaned_rooms = []
    # for room_obj in page_obj: # Ubah `rooms` menjadi `page_obj` di sini
    #     if room_obj.description:
    #         cleaned_description = html.unescape(room_obj.description) #
    #         try:
    #             cleaned_description = cleaned_description.encode('latin1').decode('unicode_escape') #
    #         except UnicodeDecodeError:
    #             pass
    #         except Exception as e:
    #             print(f"Error decoding unicode escape sequence for room {room_obj.id}: {e}") #
    #         cleaned_description = re.sub(r'\s+', ' ', cleaned_description).strip() #
    #         room_obj.description = cleaned_description #
    #     cleaned_rooms.append(room_obj) #
    context = {
        # 'rooms': cleaned_rooms, # Ini tetap 'cleaned_rooms' seperti yang Anda inginkan
        'rooms': rooms, # Ini tetap 'cleaned_rooms' seperti yang Anda inginkan
        'page_obj': page_obj,  # --- TAMBAHKAN INI KE CONTEXT ---
        'title': 'Manahayu Holistic Farm | Room' #
    }
    return render(request, 'room/room.html', context) #






def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
        'title': 'Manahayu Holistic Farm | Daftar Kamar'
    }
    return render(request, 'room/room_list.html', context)

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)  # Mendapatkan detail kamar berdasarkan ID
    return render(request, 'room/room_detail.html', {'room': room}) 

# def book_room(request, room_id):
#     room = get_object_or_404(Room, id=room_id)  # Dapatkan data kamar yang dipilih
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)  # Jangan simpan dulu
#             booking.save()  # Simpan objek booking
#             booking.room.add(room)  # Tambahkan kamar ke booking
#             booking.save()  # Simpan kembali setelah menambahkan room
#             return redirect('thank_you')  # Ganti dengan halaman yang sesuai
#     else:
#         # Pre-fill room dalam form
#         form = BookingForm(initial={'room': room})  # Isi dengan room yang dipilih

#     return render(request, 'room/booking.html', {'form': form, 'room': room})



def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            try:
                booking.save()
            except ValidationError as e:
                form.add_error(None, e.message)
                all_rooms = Room.objects.prefetch_related('images', 'type', 'facilities').all()
                context = {
                    'form': form,
                    'all_rooms': all_rooms,
                    'title': 'Manahayu Holistic Farm - Booking Kamar'
                }
                return render(request, 'room/booking.html', context)

            rooms = form.cleaned_data['room']
            booking.room.set(rooms)
            booking.save()

            phone_number = None
            try:
                main_contact = MainContact.objects.first()
                if main_contact:
                    phone_number = main_contact.phone
                else:
                    phone_number = "62895397661277"
            except Exception:
                phone_number = "62895397661277"

            if phone_number:
                message = (
                    f"Halo Admin Manahayu! 😊 \n\n"
                    f"Nama saya {booking.first_name} {booking.last_name}, saya ingin mengonfirmasi pemesanan kamar saya:\n\n"
                    f"📅 Tanggal Check-in : {booking.check_in_date} jam {booking.check_in_time}\n"
                    f"🏨 Kamar : " + ", ".join([room.name for room in booking.room.all()]) + "\n"
                    f"📞 Nomor Telepon : {booking.phone}\n\n"
                    f"{booking.message}\n\n"
                )
                encoded_message = quote(message)
                whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"
                return redirect(whatsapp_url)
            else:
                form.add_error(None, "Maaf, nomor kontak admin tidak tersedia untuk WhatsApp. Silakan coba lagi nanti.")
                all_rooms = Room.objects.prefetch_related('images', 'type', 'facilities').all()
                context = {
                    'form': form,
                    'all_rooms': all_rooms,
                    'title': 'Manahayu Holistic Farm - Booking Kamar'
                }
                return render(request, 'room/booking.html', context)

        else:
            all_rooms = Room.objects.prefetch_related('images', 'type', 'facilities').all()
            context = {
                'form': form,
                'all_rooms': all_rooms,
                'title': 'Manahayu Holistic Farm - Booking Kamar'
            }
            return render(request, 'room/booking.html', context)

    else:
        form = BookingForm()

    all_rooms = Room.objects.prefetch_related('images', 'type', 'facilities').all()
    context = {
        'form': form,
        'all_rooms': all_rooms,
        'title': 'Manahayu Holistic Farm - Booking Kamar'
    }
    return render(request, 'room/booking.html', context)




def menu(request):
    menus = Menu.objects.all()
    paginator = Paginator(menus, 8)  # 8 item per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'menus': page_obj,
        'title': 'Manahayu Holistic Farm | Menu'
    }

    # query = request.GET.get('q', '')
    # category_id = request.GET.get('category', '')  # Mengambil ID kategori dari query string
    # if query:
    #     menu_items = Menu.objects.filter(name__icontains=query)
    # else:
    #     menu_items = Menu.objects.all()
        
    # # Jika ada kategori yang dipilih, filter menu berdasarkan kategori tersebut
    # if category_id:
    #     menu_items = menu_items.filter(categories__id=category_id)
    
    # categories = Category.objects.all()  # Ambil semua kategori untuk dropdown
    
    # paginator = Paginator(menu_items, 10)  # Menampilkan 10 menu per halaman
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    
    return render(request, 'menu/menu.html',  context)

def package(request):
    packages = Package.objects.all()
    paginator = Paginator(packages, 4) # 4 item per halaman (sesuaikan jumlahnya)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'packages': page_obj,
        'title':'Menu Kopi & Kuliner – Manahayu Holistic Farm | Nikmati Cita Rasa Alami'
    }
    return render(request, 'package/package.html', context)  # Mengarahkan ke template contact.html

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        contact = form.save()
        phone_number = None
        try:
            main_contact = MainContact.objects.first()
            if main_contact:
                phone_number = main_contact.phone
            else:
                phone_number = "62895397661277"  # Nomor fallback default
        except Exception:
            phone_number = "62895397661277"
        message = (
            f"Halo Admin Manahayu! 😊\n\n"
            f"Nama saya {contact.first_name} {contact.last_name}, berikut detail kontak saya:\n\n"
            f"📞 Nomor Telepon : {contact.phone}\n"
            f"📧 Email : {contact.email}\n\n"
            f"{contact.message}"
        )
        encoded_message = quote(message)
        whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"
        return redirect(whatsapp_url)
    context = {
        'title': 'Pesan Ruangan – Manahayu Holistic Farm',
        'form': form,
    }
    return render(request, 'contact.html', context)


def reservation_package(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.save()
            
            packages = form.cleaned_data['package']
            reservation.package.set(packages)
            reservation.save()

            # --- Ambil nomor dari MainContact, fallback ke default ---
            phone_number = None
            try:
                main_contact = MainContact.objects.first()
                if main_contact:
                    phone_number = main_contact.phone
                else:
                    phone_number = "62895397661277"  # Nomor fallback default
            except Exception:
                phone_number = "62895397661277"

            if phone_number:
                message = (
                    f"Halo Admin Manahayu! 😊 \n\n"
                    f"Nama saya {reservation.first_name} {reservation.last_name}, saya ingin mengonfirmasi pemesanan Paket saya:\n\n"
                    f"🎉 Paket : " + ", ".join([package.name for package in reservation.package.all()]) + "\n"
                    f"📞 Nomor Telepon : {reservation.phone}\n\n"
                    f"{reservation.message}\n\n"
                )
                encoded_message = quote(message)
                whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"
                return redirect(whatsapp_url)

            else:
                form.add_error(None, "Nomor kontak admin tidak tersedia. Silakan coba lagi nanti.")

    else:
        form = ReservationForm()
    all_packages = Package.objects.all()
    for package in all_packages:
        package.services_preview = package.service.all()[:3]  # Slice di views

    context = {
        'form': form,
        'all_packages': all_packages,
        'title': 'Reservasi Paket - Manahayu Holistic Farm'
    }

    return render(request, 'package/reservasi.html', context)

def reviews_page(request):
    reviews = Review.objects.all().order_by('-id')  # atau pakai .latest() jika ingin review terbaru
    return render(request, 'home.html', {'reviews': reviews})


