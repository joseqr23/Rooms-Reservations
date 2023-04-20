from django.db import models

class Room(models.Model):
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=30, null=True)
    availability = models.BooleanField(default=True)
    description = models.CharField(max_length=100, null=True)
    price_per_day = models.FloatField(default=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.room_number}"	

    class Meta:
        db_table = "room"


class Client(models.Model):
    first_name  = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email = models.EmailField(max_length=25, null=True)
    phone = models.CharField(max_length=15)
    identification_document = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"		

    class Meta:
        db_table = "client"

    def delete(self, *args, **kwargs):
        try:
            reservation = Reservation.objects.get(client_id=self)
            room = reservation.room_id
            room.availability = True
            room.save()
        except Reservation.DoesNotExist:
            pass
        super(Client, self).delete(*args, **kwargs)		


        
class Reservation(models.Model):
    STATUS_CHOICES = (
        ("pending","PENDING"),    
        ("paid","PAID"),   
        ("removed","REMOVED"),   
    )

    PAY_METHOD_CHOICES = (
        ("credit_card","CREDIT_CARD"),    
        ("debit_card","DEBIT_CARD"),    
        ("cash","CASH"),   
        ("other","OTHER"),   
    )

    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_details = models.CharField(max_length=50)	
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    stay_days = models.IntegerField()
    billing_info = models.CharField(max_length=100)
    amount = models.FloatField()
    pay_method = models.CharField(max_length=11, choices=PAY_METHOD_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reservation"