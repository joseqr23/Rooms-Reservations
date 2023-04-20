# CLIENTS

### Endpoint: /api/v1/client/ (GET)
### Endpoint: /api/v1/client/int:id/ (GET)

### Endpoint: /api/v1/client/ (POST)
Crear un nuevo cliente
```
{
    "first_name": "Juan",
    "last_name": "Maldonado",
    "email": "juamal@gmail.com",
    "phone": "54545454",
    "identification_document": "3434343"
}
```

## Endpoint: /api/v1/client/int:id/ (UPDATE)
Actualizar un cliente
```
{
    "first_name": "Juana",
    "last_name": "Garcia",
    "email": "juagar@gmail.com",
    "phone": "21212121",
    "identification_document": "656565565"
}
```

## Endpoint: /api/v1/client/int:id/ (DELETE)
Eliminar un cliente


# ROOMS

### Endpoint: /api/v1/room/ (GET)
### Endpoint: /api/v1/room/int:id/ (GET)

### Endpoint: /api/v1/room/ (POST)
Crear una nueva habitación
```
{
    "room_number": 100,
    "room_type": "Mediano",
    "description": "Cuarto con dos baños, etc",
    "price_per_day": 25
}
```

## Endpoint: /api/v1/client/int:id/ (UPDATE)
Actualizar una habitación
```
{
    "room_number": 115,
    "room_type": "Habitación grande",
    "availability": true,
    "description": "Cuarto con un baño",
    "price_per_day": 20.0
}
```

## Endpoint: /api/v1/client/int:id/ (DELETE)
Eliminar una habitación

## Endpoint: /api/v1/room/availability/str:status/ (GET)
Buscar por disponibilidad
```
http://127.0.0.1:8000/api/v1/room/availability/occupied/

http://127.0.0.1:8000/api/v1/room/availability/availible/
```

## Endpoint: /api/v1/room/?search=50.0 (GET)
Filtrar por precio
```
http://127.0.0.1:8000/api/v1/room/?search=50.0
```


# RESERVATIONS

### Endpoint: /api/v1/reservation/ (GET)
### Endpoint: /api/v1/reservation/int:id/ (GET)

### Endpoint: /api/v1/reservation/ (POST)
Crear una nueva reserva
```
PENDIENTE
{
    "client_id": 2,
    "room_id": 2,
    "stay_days": 2,
    "amount": 50.0,
    "pay_method": "cash"
}

PAGADA
{
    "client_id": 5,
    "room_id": 3,
    "stay_days": 2,
    "amount": 100.0,
    "pay_method": "cash"
}
```
Output
```bash
{
    "id": 120,
    "client_id": 5,
    "room_id": 3,
    "room_details": {
        "id": 3,
        "room_number": 23,
        "room_type": "23",
        "availability": false,
        "description": "32",
        "price_per_day": 50.0,
        "created_at": "2023-04-20T00:42:54.596410Z",
        "updated_at": "2023-04-20T20:36:14.591481Z"
    },
    "status": "paid",
    "stay_days": 2,
    "billing_info": "Client: Leandro Reyes, ID: 5, Payment made: 100.0, Total to pay: 100.0",
    "amount": 100.0,
    "pay_method": "cash"
}
```


## Endpoint: /api/v1/reservation/int:id/ (UPDATE)
Actualizar estado de reserva
```
{
    "client_id": 2,
    "room_id": 2,
    "status": "paid"
}
```

## Endpoint: /api/v1/reservation/int:id/ (DELETE)
Eliminar una reserva 


## Endpoint: api/v1/reservation/client/<int:client_id> (GET)
Mostrar reservas por cliente (client_id)

## Endpoint: api/v1/reservation/status/<str:status> (GET)
Mostrar reservas por estado (pending, paid, removed)
```
http://127.0.0.1:8000/api/v1/reservation/status/pending
http://127.0.0.1:8000/api/v1/reservation/status/paid
http://127.0.0.1:8000/api/v1/reservation/status/removed
```

## Endpoint: api/v1/reservation/room/<int:room_id> (GET)
Mostrar las habitaciones que tienen reservas registradas (room_id)


## Endpoint: api/v1/reservation-cancel/<int:pk>/ (PUT)
Cancela las reservas pendientes por id de reserva


## Endpoint: api/v1/reservation-remove/<int:pk>/ (PUT)
Cambia el estado de la reserva de "pagado" a "eliminado"


## Endpoint: api/v1/reservation-delete/<str:filter_value>/ (DELETE)
Elimina los registros de la base de datos dependiendo el estado que se le pase (pendiente/ eliminado)
```
http://127.0.0.1:8000/api/v1/reservation-delete/removed/
http://127.0.0.1:8000/api/v1/reservation-delete/pending/
```

# Documentación en web de postman
https://documenter.getpostman.com/view/24367860/2s93Y3ufyH
