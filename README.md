# Justificación

## Los endpoints de CRUD de cada tabla/modelo, deben ser obligatorios para tener un buen manejo de datos. Entre estos endpoints se comprenden:
- GET, POST: api/v1/room | GET, PUT, DELETE: api/v1/room/<id>
- GET, POST: api/v1/client | GET, PUT, DELETE: api/v1/client/<id>

## En el caso del CRUD de la ruta de reservación, se han automatizado algunos procesos, tales como:
#### GET, POST: api/v1/reservation  
- Al momento de crear una nueva reserva, si el monto pagado es igual al pago total que debe hacer el cliente (dias de instancia * costo de habitacion por dia) el estado de la reserva será "pagado" de forma automática, si el monto es menor al total el estado será "pendiente" de forma automática.
- Si se intenta realizar una reserva la cual tiene una habitación que tiene la disponibilidad en false, este retornará un mensaje indicando que la habitación ya está en uso, por lo cual no se podrá realizar dicha reserva.
- Si la reserva hecha ya ha sido pagada, la disponibilidad de la habitación pasará a ser false, debido a que se ha realizado el pago completo, de lo contrario la habitación seguirá disponible.

#### GET, PUT, DELETE: api/v1/reservation/<id>/
- Al igual que en el método CREATE, en el método UPDATE si el monto pagado es igual al total a pagar el estado de la reserva cambiará automáticamente de "pendiente" a "pagado" y la disponibilidad de la habitación pasará a ser false, de igual manera, si se le indica en el estado que ha sido "pagado" el monto pagado se actualizará de forma automática al total a pagar.
- Si la disponibilidad de la habitación es false, esta no se podrá asignar a través de una actualización tanto a otras reservas como a sí misma, debido a que no podría pasar de "pagado" a "pendiente", en cuanto al estado "eliminado" se ha creado otro endpoint que actualice el estado de la reserva de "pagado" a "eliminado" y libere la habitación.
- En cuanto al método DELETE/DESTROY, este solo cambiará la disponibilidad de la habitación a true siempre y cuando la reserva borrada tenga un estado de "pagado", debido a que se sobre entiende que al estar pagado el cliente actualmente tiene esa habitación ocupada.

##  Este endpoint muestra todas las rooms que se encuentran ocupadas o disponibles a través de un parámetro status al cual se le deben pasar los valores "occupied" = ocupadas O "available" = disponibles 
```
Método GET
api/v1/room/availability/<str:status>/
```

## Este filtro ha sido añadido para buscar aquellas habitaciones por su precio 
```
api/v1/room/?search=50.0
```

## Este endpoint está creado para filtrar todas las reservas que ha hecho un cliente, se mostrará una lista de todas las reservas a través del client_id
```
Método GET
api/v1/reservation/client/<int:client_id>/
```

## Este endpoint está creado para filtrar aquellas reservas a través de su estado, sea pendiente, pagado o eliminado, esto con el fin de tener un filtro del estado de las reservas. Al cual se le deberan pasar los valores "pending", "paid" O "removed".
```
Método GET
api/v1/reservation/status/<str:status>/
```

## Este endpoint está creado para filtrar todas las habitaciones que son parte de las reservas, a través del room_id
```
Método GET
api/v1/reservation/room/<int:room_id>/
```


## Este endpoint está creado para cancelar directamente una reserva a través del id, en caso de que el cliente desista de reservar la habitación (siempre y cuando el estado sea "pendiente" si el estado está en "eliminado" o "pagado" no será posible cancelarse).
```
Método PUT
api/v1/reservation-cancel/<int:pk>/
```


## Este endpoint está creado para remover una reserva que esta actualmente en uso. Cuando el estado de una reserva es "pagado" esta misma bloqueará la habitación en cuestión, haciendo que no sea posible crear o actualizar otra reserva a nombre de la misma habitación, a traves de este endpoint se puede remover aquella reserva y liberar dicha habitación. En el cual se debera insertar como parametro el id de la reserva a remover.
```
Método PUT
api/v1/reservation-remove/<int:pk>/
```



## Este endpoint borrará de la base de datos todos los datos cuyas reservas tengan de estado "pendientes" o "eliminadas", esto depende lo que se le indique en filter_value, donde "pending" borrará todas las reservas pendientes, y "removed" borrará todas las reservas eliminadas
```
Método DELETE
api/v1/reservation-delete/<str:filter_value>/
```

## Estos endpoints son para la documentación de las rutas/endpoints que tiene el proyecto 
```
swagger/ => Muestra los endpoints
swagger.json => Muestra un archivo .json con los datos
swagger.yaml => Descarga un archivo .yaml con los datos
```