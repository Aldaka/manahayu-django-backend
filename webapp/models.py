from django.db import models
import logging, os
from django.core.exceptions import ValidationError

class ImageWithFileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(image="").exclude(image__isnull=True)

# Model Kategori
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Model Menu
class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=16, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='menus', blank=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon class (e.g., fa-solid fa-bed)")

    
    def __str__(self):
        return self.name
    
class MenuImage(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='menu_gallery/', null=True, blank=True)
    objects = ImageWithFileManager()
    def __str__(self):
        return f"Image for {self.menu.name}"


    
class Facility(models.Model):
    name = models.CharField(max_length=100)  # Class FontAwesome untuk ikon
    icon_class = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name   

class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=16, decimal_places=2)
    facilities = models.ManyToManyField(Facility, related_name='rooms', blank=True)
    type = models.ManyToManyField(RoomType, related_name='type', blank=True)

    def __str__(self):
        return self.name

# Model untuk gambar Room
class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_gallery/', null=True, blank=True)
    objects = ImageWithFileManager()

    def __str__(self):
        return f"Image for {self.room.name}"

    


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    message = models.TextField()  # Additional message for the booking
    room = models.ManyToManyField(Room, related_name='bookings', blank=False,)  # Many-to-Many relation to Room
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Menampilkan nama pemesan dan kamar yang dipesan
        room_names = ', '.join([room.name for room in self.room.all()])  # Menampilkan nama kamar yang dipesan
        return f"Booking for {self.first_name} {self.last_name} in rooms: {room_names} on {self.check_in_date}"


class Review(models.Model):
    name = models.CharField(max_length=255)
    rating = models.IntegerField()
    content = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.rating}★)"
    
class ServiceFeature(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nama fitur layanan
    icon_class = models.CharField(max_length=50, blank=True, null=True,)

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=16, decimal_places=2)
    service = models.ManyToManyField(ServiceFeature, related_name='packages', blank=True)

    def __str__(self):
        return self.name

class PackageImage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='package_gallery/', null=True, blank=True)
    objects = ImageWithFileManager()
    def __str__(self):
        return f"Image for {self.package.name}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    # check_in_date = models.DateField(blank=True)
    # check_in_time = models.TimeField(blank=True)
    message = models.TextField()  # Additional message for the booking
    package = models.ManyToManyField(Package, related_name='reservations', blank=True)  # Many-to-Many relation to Room
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        package_names = ', '.join([package.name for package in self.package.all()])
        return f"Booking for {self.first_name} {self.last_name} with packages: {package_names}"



class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()  # Additional message for the booking  # Many-to-Many relation to Room
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.first_name} {self.last_name} ({self.email})"
    
class MainContact(models.Model):
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.phone
    
    def save(self, *args, **kwargs):
        # 1. Cek apakah sudah ada instans lain dari model KontakUtama di database.
        # 2. Cek apakah objek yang sedang mencoba disimpan ini adalah objek BARU (belum punya primary key/ID).
        if MainContact.objects.exists() and not self.pk:
            # Jika kedua kondisi terpenuhi, berarti ada upaya untuk MENAMBAHKAN data kedua/ketiga/dst.
            # Maka, kita lemparkan ValidationError.
            raise ValidationError("Anda hanya bisa menginputkan data ke model ini SATU KALI SAJA.")
        # Jika validasi lolos (ini adalah input pertama, atau ini adalah operasi UPDATE),
        # maka lanjutkan proses penyimpanan data ke database.
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Main Contact"
        verbose_name_plural = "Main Contact"