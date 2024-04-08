import requests


url_ordenes = "http://localhost:8000/ordenes"

 
headers = {"Content-Type": "application/json"}

# 1. 
response = requests.post(url_ordenes + "/fisicas", headers=headers)
print("1. Crear orden de compra física:", response.text)

# 2. 
data_digital = {"codigo_descarga": "ABC123", "fecha_expiracion": "2022-12-31"}
response = requests.post(url_ordenes + "/digitales", json=data_digital, headers=headers)
print("2. Crear orden de compra digital:", response.text)

# 3. 
response = requests.get(url_ordenes, headers=headers)
print("3. Listar todas las órdenes de compra:", response.json())

# 4. 
response = requests.get(url_ordenes + "/pendientes", headers=headers)
print("4. Listar órdenes pendientes:", response.json())

# 5. 
data_update = {"estado": "Entregada"}
response = requests.put(url_ordenes + "/1", json=data_update, headers=headers)
print("5. Actualizar estado de la orden:", response.text)

# 6. 
response = requests.delete(url_ordenes + "/2", headers=headers)
print("6. Eliminar orden de compra:", response.text)

# 7. 
response = requests.post(url_ordenes + "/licuadora-refrigeradora-lavadora", headers=headers)
print("7. Crear orden de compra física personalizada:", response.text)
