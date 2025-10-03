from django.contrib import admin
from .models import Hotel, Room, Booking, Staff

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating')
    search_fields = ('name', 'location')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_number', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('hotel', 'room_type', 'is_available')
    search_fields = ('room_number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'guest_name', 'check_in_date', 'check_out_date', 'total_price')
    list_filter = ('check_in_date', 'check_out_date')
    search_fields = ('guest_name',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'name', 'position', 'salary')
    list_filter = ('hotel', 'position')
    search_fields = ('name', 'position')
