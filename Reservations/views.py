from rest_framework import viewsets, filters, status
from rest_framework.generics import ListAPIView 
from rest_framework.views import APIView 
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db import transaction

from .serializers import RoomSerializer, ClientSerializer, ReservationSerializer
from .models import Room, Client, Reservation


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['price_per_day']

class RoomsAvailableAPIView(ListAPIView):
    serializer_class = RoomSerializer
    def get_queryset(self):
        status = self.kwargs.get('status', None)
    
        if status == 'available':
            queryset = Room.objects.filter(availability = True)
        elif status == 'occupied':
            queryset = Room.objects.filter(availability = False)
        else:
            return Response({'ok': False, 'error': 'Invalid Parameter'})
        return queryset
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()    
        serializer = self.get_serializer(queryset, many = True)
        return Response({'ok': True, 'data':serializer.data})


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def validate_required_fields(self, data, fields):
        for field in fields:
            if field not in data or data[field] == '':
                return Response({"error": f"The {field} field is required and must have a value"}, status = status.HTTP_400_BAD_REQUEST)

    def update_room_availability(self, room_id, status):
        room = Room.objects.get(id=room_id)
        if status == 'paid':
            room.availability = False
            room.save()        
        else:
            room.availability = True
            room.save()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        reservation_data = request.data.copy()

        
        required_fields = ['amount', 'stay_days', 'room_id']
        validation_error = self.validate_required_fields(reservation_data, required_fields)
        if validation_error:
            return validation_error

        amount = float(reservation_data.get('amount'))
        stay_days = float(reservation_data.get('stay_days'))
        room_id = reservation_data.get('room_id')
        client_id = reservation_data.get('client_id')        

        room = Room.objects.get(id=room_id)
        client = Client.objects.get(id=client_id)
        
        price_per_day = room.price_per_day
        total = price_per_day * stay_days
        reservation_data['billing_info'] = f"Client: {client}, ID: {client_id}, Payment made: {amount}, Total to pay: {total}"

        if amount <= total or amount <= 0:
            reservation_data['status'] = 'pending'
        if amount >= total and amount > 0:
            reservation_data['status'] = 'paid'

        if not room.availability:
            return Response({"ok": False, "message": "The room is not available"}, status=status.HTTP_400_BAD_REQUEST)

        if reservation_data['status']  == "paid":
            self.update_room_availability(room_id, 'paid')
        
        serializer = self.get_serializer(data=reservation_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status = status.HTTP_201_CREATED)        

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        reservation_data = request.data.copy()
        reservation_status = reservation_data.get('status')
        
        if instance.status == "removed":
            return Response({"ok": False, "message": "You cannot modify a removed reservation"}, status=status.HTTP_400_BAD_REQUEST)
    
        amount = float(request.data['amount']) if 'amount' in request.data else instance.amount
        stay_days = float(request.data['stay_days']) if 'stay_days' in request.data else instance.stay_days
        
        room_id = reservation_data.get('room_id')
        client_id = reservation_data.get('client_id')    
           
        room = Room.objects.get(id=room_id)
        client = Client.objects.get(id=client_id)
        
        price_per_day = room.price_per_day
        total = price_per_day * stay_days
        reservation_data['billing_info'] = f"Client: {client}, ID: {client_id}, Payment made: {amount}, Total to pay: {total}"

        if amount >= total and reservation_status in ('paid', 'pending'):
            reservation_data['status'] = 'paid'
        elif amount >= total and reservation_status == "removed":
            reservation_data['status'] = 'removed'

        if not room.availability:
            return Response({"ok": False, "message": "The room is not available"}, status=status.HTTP_400_BAD_REQUEST)

        if reservation_data['status'] == "paid":
            reservation_data['amount'] = total
            reservation_data['billing_info'] = f"Client: {client}, ID: {client_id}, Payment made: {total}, Total to pay: {total}"
            self.update_room_availability(room_id, "paid")
        elif reservation_data['status'] == "removed":
            self.update_room_availability(room_id, "removed")
        else:                        
            self.update_room_availability(room_id, "pending")

        serializer = self.get_serializer(instance, data=reservation_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"ok": True, "message": "the reservation has been updated", 'data': serializer.data}, status=status.HTTP_200_OK)


    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        reservation_status = instance.status
        room_id = instance.room_id.id
        
        if reservation_status == "paid":
            self.update_room_availability(room_id, 'removed')
        
        self.perform_destroy(instance)
        return Response({"ok": True, "message": "the reservation has been removed"}, status=status.HTTP_204_NO_CONTENT)

class ReservationsAPIView(ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    
    ERROR_INVALID_FILTER = 'Invalid Filter'
    ERROR_NO_DATA = 'No data to Show'

    def get(self, request, *args, **kwargs):
        filter_type = kwargs.get('filter_type', None)
        filter_value = kwargs.get('filter_value', None)
        reservations = self.queryset
        
        if filter_type == 'client':
            reservations = reservations.filter(client_id=filter_value)
        elif filter_type == 'status':
            reservations = reservations.filter(status=filter_value)
        elif filter_type == 'room':
            reservations = reservations.filter(room_id=filter_value)
        else:
            return Response({'ok': False, 'error': self.ERROR_INVALID_FILTER}, status=status.HTTP_400_BAD_REQUEST)
        
        if not reservations.exists():
            return Response({'ok': False, 'message': self.ERROR_NO_DATA}, status= status.HTTP_404_NOT_FOUND)

        serialized_reservations = self.serializer_class(reservations, many=True)
        return Response({'ok': True, 'data':serialized_reservations.data}, status=status.HTTP_200_OK)


class CancelPendingReservationAPIView(APIView):
    def put(self, request, pk, *args, **kwargs):
        reservation = get_object_or_404(Reservation, pk=pk)

        if reservation.status in ("removed","paid"): 
            return Response({'ok': False, 'message': 'the status of this reservation has already been deleted or paid'}, status=status.HTTP_400_BAD_REQUEST)

        reservation.status = "removed"
        reservation.billing_info = "this client has canceled his reservation"
        reservation.amount = 0
        reservation.stay_days = 0
        reservation.save()
        return Response({'ok': True, 'message': 'this reservation has been canceled'}, status=status.HTTP_200_OK)


class RemoveActiveReservationAPIView(APIView):
    def put(self, request, pk, *args, **kwargs):
        reservation = get_object_or_404(Reservation, pk=pk)

        if not reservation.status == "paid":
            return Response({'ok': False, 'message': 'this reservation has not been paid or has already been removed'}, status=status.HTTP_400_BAD_REQUEST)
        
        room_id = reservation.room_id.id
        room = get_object_or_404(Room, pk=room_id)        
        room.availability = True
        reservation.status = "removed"
        reservation.save()
        room.save()
        return Response({'ok': True, 'message': 'this reservation has been removed'}, status= status.HTTP_200_OK)        


class DeletePendingOrRemovedReservationsAPIView(APIView):
    def delete(self, request, filter_value ,*args, **kwargs):
        
        if filter_value not in ["pending", "removed"]:
            return Response({'ok': False, 'message': 'Invalid filter value'}, status=400)

        reservations_to_delete = Reservation.objects.filter(status=filter_value)
        if not reservations_to_delete:
            return Response({'ok': False, 'message': f'No {filter_value} reservations found'})
            
        reservations_to_delete.delete()
        return Response({'ok': True, 'message': f'All {filter_value} reservations have been removed'})
    