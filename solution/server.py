from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs


ordenes_compra = []

class OrdenCompra:
    def __init__(self, tipo, productos=None, codigo_descarga=None, fecha_expiracion=None):
        self.id = len(ordenes_compra) + 1
        self.tipo = tipo
        self.productos = productos or []
        self.codigo_descarga = codigo_descarga
        self.fecha_expiracion = fecha_expiracion
        self.estado = "Pendiente"

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "productos": self.productos,
            "codigo_descarga": self.codigo_descarga,
            "fecha_expiracion": self.fecha_expiracion,
            "estado": self.estado
        }

class OrdenHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path == '/ordenes/fisicas':
            orden = OrdenCompra("Física", productos=["Camiseta", "Pantalón", "Zapatos"])
            ordenes_compra.append(orden)
            self._set_headers(201)
            self.wfile.write(json.dumps({"mensaje": "Orden de compra física creada exitosamente"}).encode('utf-8'))
        elif self.path == '/ordenes/digitales':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            codigo_descarga = data.get("codigo_descarga")
            fecha_expiracion = data.get("fecha_expiracion")
            orden = OrdenCompra("Digital", codigo_descarga=codigo_descarga, fecha_expiracion=fecha_expiracion)
            ordenes_compra.append(orden)
            self._set_headers(201)
            self.wfile.write(json.dumps({"mensaje": "Orden de compra digital creada exitosamente"}).encode('utf-8'))
        elif self.path == '/ordenes/licuadora-refrigeradora-lavadora':
            orden = OrdenCompra("Física", productos=["Licuadora", "Refrigeradora", "Lavadora"])
            ordenes_compra.append(orden)
            self._set_headers(201)
            self.wfile.write(json.dumps({"mensaje": "Orden de compra física creada exitosamente"}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(b"Ruta no encontrada")

    def do_GET(self):
        if self.path == '/ordenes':
            self._set_headers()
            self.wfile.write(json.dumps([orden.to_dict() for orden in ordenes_compra]).encode('utf-8'))
        elif self.path == '/ordenes/pendientes':
            self._set_headers()
            pendientes = [orden.to_dict() for orden in ordenes_compra if orden.estado == "Pendiente"]
            self.wfile.write(json.dumps(pendientes).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(b"Ruta no encontrada")

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        orden_id = int(parsed_path.path.split('/')[2])
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data.decode('utf-8'))
        
        for orden in ordenes_compra:
            if orden.id == orden_id:
                orden.estado = data.get("estado")
                self._set_headers()
                self.wfile.write(json.dumps({"mensaje": f"Estado de la orden {orden_id} actualizado correctamente a {orden.estado}"}).encode('utf-8'))
                return
        self._set_headers(404)
        self.wfile.write(json.dumps({"mensaje": "No se encontró la orden especificada"}).encode('utf-8'))

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        orden_id = int(parsed_path.path.split('/')[2])
        
        for orden in ordenes_compra:
            if orden.id == orden_id:
                ordenes_compra.remove(orden)
                self._set_headers()
                self.wfile.write(json.dumps({"mensaje": f"Orden {orden_id} eliminada correctamente"}).encode('utf-8'))
                return
        self._set_headers(404)
        self.wfile.write(json.dumps({"mensaje": "No se encontró la orden especificada"}).encode('utf-8'))

def main():
    try:
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, OrdenHandler)
        print('Iniciando servidor HTTP en puerto 8000...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Apagando servidor HTTP')
        httpd.socket.close()

if __name__ == '__main__':
    main()
