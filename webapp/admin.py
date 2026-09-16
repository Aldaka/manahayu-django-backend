from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from django import forms
from django.db import models
from .models import (Menu, MenuImage, Category, Room, 
                     Booking, Facility, RoomImage, RoomType, 
                     Review, ServiceFeature, Package, PackageImage,
                     Reservation, Contact,MainContact
                     )
from unfold.admin import ModelAdmin
from django.templatetags.static import static
from unfold.widgets import UnfoldAdminTextInputWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportMixin, ExportActionMixin, ImportExportModelAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin



class MenuImageForm(forms.ModelForm):
    class Meta:
        model = MenuImage
        fields = '__all__'

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            # If image is cleared, set it to None (this allows for image removal)
            return None
        return image

class MenuImageInline(admin.TabularInline):
    model = MenuImage  # Model gambar terkait Menu
    extra = 1  # Menambahkan satu baris kosong untuk menambah gambar baru
    fields = ('image', 'image_tag')  # Menampilkan field gambar dan tag untuk preview
    readonly_fields = ('image_tag',)  # Membuat gambar hanya bisa dilihat (readonly)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')  # Menampilkan gambar sebagai preview
        return "No image"
    image_tag.short_description = 'Image Preview'

class MenuAdmin(ModelAdmin):
    filter_horizontal = ('categories',)
    list_display = ('name', 'price', 'image_tag')  # Menampilkan gambar di daftar menu
    search_fields = ('name',)
    inlines = [MenuImageInline]  # Menambahkan inline untuk gambar menu

    def image_tag(self, obj):
        # Mengakses gambar pertama dari MenuImage terkait dengan menu
        if obj.images.exists() and obj.images.first().image:
            return mark_safe(f'<img src="{obj.images.first().image.url}" width="100" />')  # Menampilkan gambar pertama
        return "No image"  # Menampilkan pesan jika tidak ada gambar
    image_tag.short_description = 'Image'

    def image_tag_large(self, obj):
        # Mengakses gambar pertama dari MenuImage untuk menampilkan gambar besar di form edit
        if obj.images.exists():
            return mark_safe(f'<img src="{obj.images.first().image.url}" width="500" />')  # Gambar besar untuk form edit
        return "No image"
    image_tag_large.short_description = 'Image'

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'categories')
        }),
        ('Images', {
            'fields': ('image_tag_large',)  # Menampilkan gambar besar di form edit
        }),
    )
    readonly_fields = ('image_tag_large',)  # Membuat image_tag_large hanya bisa dilihat (readonly)
    
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)  # Menampilkan nama kategori di daftar kategori
    search_fields = ('name',)  # Memungkinkan pencarian kategori berdasarkan nama

class FacilityAdminForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'
        widgets = {
            'icon_class': UnfoldAdminTextInputWidget(attrs={
                'placeholder': 'Contoh: fa-solid fa-wifi',
            }),
        }
        help_texts = {
            'icon_class': "Font Awesome icon class (contoh : fa-solid fa-bed)",
        }

# class FacilityAdminForm(forms.ModelForm):
#     icon_class = forms.CharField(
#         max_length=50,
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'e.g., fa-solid fa-bed'}),
#         help_text="Font Awesome icon class (e.g., fa-solid fa-bed)"
#     )
#     class Meta:
#         model = Facility
#         fields = '__all__'

class FacilityAdmin(ModelAdmin):
    form = FacilityAdminForm # Gunakan form kustom di sini
    list_display = ('name', 'icon_class_display')
    search_fields = ('name', 'icon_class')
    
    # fieldsets atau fields bisa tetap di sini untuk mengatur layout form
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'icon_class',)
    #     }),
    # )

    # Fungsi untuk menampilkan ikon di halaman daftar admin
    def icon_class_display(self, obj):
        if obj.icon_class:
            return mark_safe(f'<i class="{obj.icon_class}" style="font-size: 24px;"></i> {obj.icon_class}')
        return "No Icon"
    icon_class_display.short_description = 'Icon'

class RoomTypeAdmin(ModelAdmin):
    list_display = ('name',)  # Menampilkan nama room type di daftar admin
    search_fields = ('name',)  # Memungkinkan pencarian berdasarkan nama

        
class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImage
        fields = '__all__'

    # Customisasi widget untuk 'ImageField'
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))


class RoomImageInline(admin.TabularInline):
    model = RoomImage  # Model gambar terkait Room
    extra = 1  # Menambahkan satu baris kosong untuk menambah gambar baru
    fields = ('image', 'image_tag')  # Menampilkan field gambar dan tag untuk preview
    readonly_fields = ('image_tag',)  # Membuat gambar hanya bisa dilihat (readonly)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')  # Menampilkan gambar sebagai preview
        return "No image"
    image_tag.short_description = 'Image Preview'



class RoomAdmin(ModelAdmin):
    filter_horizontal = ('facilities', 'type')
    list_display = ('name', 'price', 'room_types','image_tag',)  # Use image_tag method for displaying image preview in the admin list view
    search_fields = ('name',)
    inlines = [RoomImageInline]

    # Function for displaying image in the list view (small size)
    def image_tag(self, obj):
        # Access the first related RoomImage for the room
        room_image = obj.images.first()  # Get the first related image
        if room_image and room_image.image:
            return mark_safe(f'<img src="{room_image.image.url}" width="100" />')  # Image preview in the admin list view
        return "No image"  # Display "No image" if no related image is found
    image_tag.short_description = 'Image Preview'

    # Function for displaying image in the form edit view (large size)
    def image_tag_large(self, obj):
        room_image = obj.images.first()  # Get the first related image
        if room_image and room_image.image:
            return mark_safe(f'<img src="{room_image.image.url}" width="500" />')  # Larger size for form edit view
        return "No image"
    image_tag_large.short_description = 'Image'

    def room_types(self, obj):
        return ", ".join([room_type.name for room_type in obj.type.all()])
    room_types.short_description = 'Room Types'

    # Customize the form and include the image preview
    fieldsets = (
        ('Room', {
            'fields': ('name', 'description', 'price', 'type', 'facilities')
        }),
    )
    readonly_fields = ('image_tag_large',)  # Making image_tag_large readonly in the form view

class BookingAdmin(ModelAdmin):
    filter_horizontal = ('room',)
    list_display = ('first_name', 'last_name', 'status', 'created_at')  # Kolom yang ditampilkan di daftar pemesanan
    list_filter = ('status',)  # Anda hanya dapat memfilter berdasarkan status
    search_fields = ('first_name', 'last_name', 'phone', 'rooms__name')  # Memungkinkan pencarian berdasarkan nama kamar

class UnfoldImportExportAdmin(ExportActionMixin, UnfoldModelAdmin):
    pass
class UnfoldImportExportAdmin(ImportExportModelAdmin, UnfoldModelAdmin):
    pass
class ReviewResources(resources.ModelResource):
    class Meta:
        model = Review

class ReviewAdmin(UnfoldImportExportAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    actions = ["export_admin_action"]
    resource_class = ReviewResources
    list_display = ('name', 'rating', 'content',)





































# Package Admin
# class ServiceFeatureAdminForm(forms.ModelForm):
#     icon_class = forms.CharField(
#         max_length=50,
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'e.g., fa-solid fa-wifi'}),
#         help_text="Font Awesome icon class"
#     )

#     class Meta:
#         model = ServiceFeature
#         fields = '__all__'

# class ServiceFeatureAdmin(ModelAdmin):
#     form = ServiceFeatureAdminForm
#     list_display = ('name', 'icon_class')
#     search_fields = ('name', 'icon_class')

#     def icon_class_display(self, obj):
#         if obj.icon_class:
#             return mark_safe(f'<i class="{obj.icon_class}" style="font-size: 20px;"></i> {obj.icon_class}')
#         return "-"
#     icon_class_display.short_description = 'Icon Preview'


# class ServiceAdmin(ModelAdmin):
#     form = ServiceFeatureAdminForm # Gunakan form kustom di sini
#     list_display = ('name', 'icon_class_display')
#     search_fields = ('name', 'icon_class')
    
#     # fieldsets atau fields bisa tetap di sini untuk mengatur layout form
#     # fieldsets = (
#     #     (None, {
#     #         'fields': ('name', 'icon_class',)
#     #     }),
#     # )

#     # Fungsi untuk menampilkan ikon di halaman daftar admin
#     def icon_class_display(self, obj):
#         if obj.icon_class:
#             return mark_safe(f'<i class="{obj.icon_class}" style="font-size: 24px;"></i> {obj.icon_class}')
#         return "No Icon"
#     icon_class_display.short_description = 'Icon'

# class PackageImageForm(forms.ModelForm):
#     class Meta:
#         model = RoomImage
#         fields = '__all__'
#     # Customisasi widget untuk 'ImageField'
#     image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))

# class PackageImageInline(admin.TabularInline):
#     model = PackageImage
#     extra = 1
#     fields = ('image', 'preview')
#     readonly_fields = ('preview',)

#     def preview(self, obj):
#         if obj.image:
#             return mark_safe(f'<img src="{obj.image.url}" width="100" />')
#         return "No image"
#     preview.short_description = 'Preview'

# class PackageAdmin(ModelAdmin):
#     filter_horizontal = ('service',)    
#     list_display = ('name', 'price', 'image_tag')  # Use image_tag method for displaying image preview in the admin list view
#     search_fields = ('name',)
#     inlines = [PackageImageInline]

#     # Function for displaying image in the list view (small size

#     # Customize the form and include the image preview
#     fieldsets = (
#         ('Room', {
#             'fields': ('name', 'description', 'price', 'packages')
#         }),
#     )
#     readonly_fields = ('image_tag_large',)  # Making image_tag_large readonly in the form view



class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "No image"
    preview.short_description = 'Preview'


class PackageAdmin(ModelAdmin):
    filter_horizontal = ('service',)
    list_display = ('name', 'price','image_tag')
    search_fields = ('name', 'price',)
    inlines = [PackageImageInline]

    def image_tag(self, obj):
        # Access the first related RoomImage for the room
        room_image = obj.images.first()  # Get the first related image
        if room_image and room_image.image:
            return mark_safe(f'<img src="{room_image.image.url}" width="100" />')  # Image preview in the admin list view
        return "No image"  # Display "No image" if no related image is found
    image_tag.short_description = 'Image Preview'

# Jangan Hapus Backup
# class ServiceFeatureAdminForm(forms.ModelForm):
#     icon_class = forms.CharField(
#         max_length=50,
#         required=False,
#         widget =forms.TextInput(attrs={'placeholder': 'e.g., fa-solid fa-wifi'}),
#     )
#     class Meta:
#         model = ServiceFeature
#         fields = '__all__'

class ServiceFeatureAdminForm(forms.ModelForm):
    class Meta:
        model = ServiceFeature
        fields = '__all__'
        widgets = {
            'icon_class': UnfoldAdminTextInputWidget(attrs={
                'placeholder': 'Contoh: fa-solid fa-wifi',
            }),
        }
        help_texts = {
            'icon_class': "Font Awesome icon class (contoh : fa-solid fa-bed)",
        }

class ServiceFeatureAdmin(ModelAdmin):
    form = ServiceFeatureAdminForm
    list_display = ('name', 'icon_class')
    search_fields = ('name','icon_class',)


class ReservationAdmin(ModelAdmin):
    filter_horizontal = ('package',)
    list_display = ('first_name', 'last_name', 'status', 'created_at')  # Kolom yang ditampilkan di daftar pemesanan
    list_filter = ('status','created_at')  # Anda hanya dapat memfilter berdasarkan status
    search_fields = ('first_name', 'last_name', 'phone', 'packages__name')  # Memungkinkan pencarian berdasarkan nama kamar


class MainContactAdminForm(forms.ModelForm):
    class Meta:
        model = MainContact
        fields = '__all__' # Atau tentukan field yang ingin Anda tampilkan, misal ['phone']
        widgets = {
            'phone': UnfoldAdminTextInputWidget(attrs={ # <<< Gunakan widget Unfold
                'placeholder': 'Contoh: 6281234567890 (tanpa +)',
                # Unfold widget seringkali otomatis menangani lebar yang responsif,
                # jadi 'size' mungkin tidak diperlukan lagi atau bekerja secara berbeda.
                # Namun, Anda bisa mencobanya jika diperlukan, misal: 'data-size': 'xl'
            }),
            }


class MainContactAdmin(admin.ModelAdmin):
    form = MainContactAdminForm
    list_display = ('phone',)

    def has_add_permission(self, request):
        return not MainContact.objects.exists()
    
    def changelist_view(self, request, extra_context=None):
        if MainContact.objects.exists():
            obj = MainContact.objects.first()
            return self.change_view(request, str(obj.pk))
        return super().changelist_view(request, extra_context)
    
class ContactAdmin(ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'phone', 'message',]
    list_display = ['first_name','last_name', 'phone']
    readonly_fields = ['created_at', ]

admin.site.register(Menu, MenuAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(ServiceFeature, ServiceFeatureAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(MainContact,MainContactAdmin)

