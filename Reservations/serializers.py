from rest_framework import serializers
from .models import Room, Client, Reservation

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

class ReservationSerializer(serializers.ModelSerializer):      
    room_details = RoomSerializer(source='room_id', read_only=True)
    class Meta:
        model = Reservation
        fields = ('id','client_id', 'room_id', 'room_details', 'status', 'stay_days', 'billing_info', 'amount', 'pay_method')