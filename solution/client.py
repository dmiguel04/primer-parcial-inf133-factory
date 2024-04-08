import requests

# Definimos la URL del servicio de órdenes de compra
url_ordenes = "http://localhost:8000/ordenes"

# Definimos los encabezados HTTP que vamos a enviar con la petición
headers = {"Content-Type": "application/json"}

# 1. Crear una orden de compra de tipo Física con los siguientes productos: Camiseta, Pantalón y Zapatos
response = requests.post(url_ordenes + "/fisicas", headers=headers)
print("1. Crear orden de compra física:", response.text)

# 2. Crear una orden de compra Digital con el código de descarga ABC123 y fecha de expiración 2022-12-31
data_digital = {"codigo_descarga": "ABC123", "fecha_expiracion": "2022-12-31"}
response = requests.post(url_ordenes + "/digitales", json=data_digital, headers=headers)
print("2. Crear orden de compra digital:", response.text)

# 3. Listar todas las órdenes de compra
response = requests.get(url_ordenes, headers=headers)
print("3. Listar todas las órdenes de compra:", response.json())

# 4. Listar todos los pedidos en estado Pendiente
response = requests.get(url_ordenes + "/pendientes", headers=headers)
print("4. Listar órdenes pendientes:", response.json())

# 5. Actualizar el estado de una orden de compra por su ID (suponiendo que la orden con ID 1 está en estado Pendiente)
data_update = {"estado": "Entregada"}
response = requests.put(url_ordenes + "/1", json=data_update, headers=headers)
print("5. Actualizar estado de la orden:", response.text)

# 6. Eliminar una orden de compra por su ID (suponiendo que la orden con ID 2 existe)
response = requests.delete(url_ordenes + "/2", headers=headers)
print("6. Eliminar orden de compra:", response.text)

# 7. Crear una orden de tipo Física con los siguientes productos: Licuadora, Refrigeradora y Lavadora
response = requests.post(url_ordenes + "/licuadora-refrigeradora-lavadora", headers=headers)
print("7. Crear orden de compra física personalizada:", response.text)
