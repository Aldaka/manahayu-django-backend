from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django import forms
from .models import Room, Booking, Package, Reservation, Contact

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'email', 'phone', 'check_in_date', 'check_in_time', 'room', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama depan Anda'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama belakang Anda'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Masukkan email Anda'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Masukkan nomor telepon Anda'}),
            'check_in_date': forms.DateInput(attrs={'placeholder': 'Pilih tanggal check-in', 'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'placeholder': 'Pilih waktu check-in', 'type' : 'time'}),
            'room': forms.CheckboxSelectMultiple(attrs={'placeholder': 'Pilih jenis kamar'}),  # Untuk memilih banyak kamar
            # 'room': forms.Select(attrs={'placeholder': 'Pilih jenis kamar'}),
            'message': forms.Textarea(attrs={'placeholder': 'Masukkan pesan Anda'}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'email', 'phone', 'package', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama depan Anda'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama belakang Anda'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Masukkan email Anda'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Masukkan nomor telepon Anda'}),
            # 'check_in_date': forms.DateInput(attrs={'placeholder': 'Pilih tanggal check-in'}),
            # 'check_in_time': forms.TimeInput(attrs={'placeholder': 'Pilih waktu check-in'}),
            'package': forms.CheckboxSelectMultiple(attrs={'placeholder': 'Pilih jenis paket'}),  # Untuk memilih banyak kamar
            # 'room': forms.Select(attrs={'placeholder': 'Pilih jenis kamar'}),
            'message': forms.Textarea(attrs={'placeholder': 'Masukkan pesan Anda'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama depan Anda'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama belakang Anda'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Masukkan email Anda'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Masukkan nomor telepon Anda'}),
            'message': forms.Textarea(attrs={'placeholder': 'Masukkan pesan Anda'}),
        }