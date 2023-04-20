from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"room", views.RoomViewSet, basename="room")
router.register("client", views.ClientViewSet, basename="client")
router.register("reservation", views.ReservationViewSet, basename="reservation")

urlpatterns = [
	path('room/availability/<str:status>/', views.RoomsAvailableAPIView.as_view(), name="rooms-availability"),
	path('reservation/<str:filter_type>/<str:filter_value>/', views.ReservationsAPIView.as_view(), name="reservation-data"),
	path('reservation-cancel/<int:pk>/', views.CancelPendingReservationAPIView.as_view(), name="cancel-reservation"),
	path('reservation-remove/<int:pk>/', views.RemoveActiveReservationAPIView.as_view(), name="remove-reservation"),
	path('reservation-delete/<str:filter_value>/', views.DeletePendingOrRemovedReservationsAPIView.as_view(), name="delete-pending-reservation"),
]

urlpatterns += router.urls