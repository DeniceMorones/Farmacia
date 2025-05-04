import tkinter as tk
from tkinter import font as tkfont
from tkinter import END, messagebox, ttk
import psycopg2
import datetime
import re
from psycopg2 import Error
iva = 16 #al final este no lo utilice

class DBManager:
    
    def __init__(self):
        self.user = "postgres"  # Usuario de PostgreSQL
        self.password = "12345"  
        self.database = "farmacia"  # Nombre de la base de datos
        self.host = "localhost"  
        self.port = "5432"  
        self.conn = None
        self.cursor = None
        self.open()
          
    def open(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print("Conexión exitosa a PostgreSQL")
        except psycopg2.Error as e:
            print(f"Error al conectar a PostgreSQL: {e}")
    
    #USUARIOS
    #################################################################
    
    def search_user_by_username(self, username):
        query = "SELECT * FROM usuarios WHERE nombre = %s"
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchone()
        return user

    def search_user_by_id(self, user_id):
        query = "SELECT * FROM usuarios WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        user = self.cursor.fetchone()
        return user
    
    def update_user(self, user):
        query = "UPDATE usuarios SET nombre=%s, password=%s, perfil=%s WHERE user_id=%s"
        values = (user['nombre'], user['password'], user['perfil'], user['user_id'])
        self.cursor.execute(query, values)
        self.conn.commit()
        
    def delete_user(self, user_id):
        query = "DELETE FROM usuarios WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()
    
    def save_user(self, user):
        query = "INSERT INTO usuarios (nombre, password, perfil) VALUES (%s, %s, %s)"
        values = (user['name'], user['password'], user['profile'])
        self.cursor.execute(query, values)
        self.conn.commit()
        
    def get_next_user_id(self):
        query = "SELECT MAX(user_id) FROM usuarios"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    #CLIENTES
    #################################################################
    
    def search_customer_by_id(self, customer_id):
        query = "SELECT * FROM clientes WHERE cliente_id = %s"
        self.cursor.execute(query, (customer_id,))
        customer = self.cursor.fetchone()
        return customer

    def search_customer_by_name(self, customer_name):
        query = "SELECT * FROM clientes WHERE nombre = %s"
        self.cursor.execute(query, (customer_name,))
        customer = self.cursor.fetchone()
        return customer
    
    def update_customer(self, customer):
        query = "UPDATE clientes SET nombre=%s, telefono=%s, rfc=%s, user_id=%s WHERE cliente_id=%s"
        values = (customer['nombre'], customer['telefono'], customer['rfc'], customer['user_id'], customer['cliente_id'])
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_customer(self, customer_id):
        query = "DELETE FROM clientes WHERE cliente_id = %s"
        self.cursor.execute(query, (customer_id,))
        self.conn.commit()
    
    def save_customer(self, customer):
        puntos = 0
        query = "INSERT INTO clientes (cliente_id, user_id, nombre, telefono, rfc, puntos ) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (customer['cliente_id'], customer['user_id'], customer['nombre'], customer['telefono'],  customer['rfc'], puntos)
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def get_next_customer_id(self):
        query = "SELECT MAX(cliente_id) FROM clientes"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
    
    def get_customer_name_by_id(self, cliente_id):
        query = "SELECT nombre FROM clientes WHERE cliente_id = %s"
        self.cursor.execute(query, (cliente_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    def get_all_clientes(self):
        try:
            query = "SELECT * FROM clientes"
            self.cursor.execute(query)
            cliente = self.cursor.fetchall()
            return cliente
        except Exception as e:
            print("Error while fetching all clientes:", e)
            return None
    
    def update_cliente_puntos(self, cliente_name, puntos):
        cliente_id = self.search_customer_by_name(cliente_name)
        query = "SELECT puntos FROM clientes WHERE cliente_id = %s" 
        self.cursor.execute(query, (cliente_id[0],))
        result = self.cursor.fetchone()
        puntos_actuales = int(result[0])
        puntos = puntos_actuales + puntos
                
        query2 = "UPDATE clientes SET puntos = %s WHERE cliente_id = %s"
        values2 = (puntos, cliente_id[0])
        self.cursor.execute(query2, values2)
        self.conn.commit()
        
    def get_cliente_puntos(self, cliente_id):
        query = "SELECT puntos FROM clientes WHERE cliente_id = %s"
        self.cursor.execute(query, (cliente_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    #PROVEEDOR
    #################################################################
    
    def search_proveedor_by_id(self, proveedor_id):
        query = "SELECT * FROM proveedor WHERE proveedor_id = %s"
        self.cursor.execute(query, (proveedor_id,))
        proveedor = self.cursor.fetchone()
        return proveedor

    def search_proveedor_by_name(self, proveedor_name):
        query = "SELECT * FROM proveedor WHERE nombre = %s"
        self.cursor.execute(query, (proveedor_name,))
        proveedor = self.cursor.fetchone()
        return proveedor
    
    def update_proveedor(self, proveedor):
        query = "UPDATE proveedor SET nombre=%s, empresa=%s, direccion=%s, telefono=%s WHERE proveedor_id=%s"
        values = (proveedor['nombre'], proveedor['empresa'], proveedor['direccion'], proveedor['telefono'], proveedor['proveedor_id'])
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_proveedor(self, proveedor_id):
        query = "DELETE FROM proveedor WHERE proveedor_id = %s"
        self.cursor.execute(query, (proveedor_id,))
        self.conn.commit()
    
    def save_proveedor(self, proveedor):
        query = "INSERT INTO proveedor (proveedor_id, nombre, empresa, direccion, telefono ) VALUES (%s, %s, %s, %s, %s)"
        values = (proveedor['proveedor_id'], proveedor['nombre'], proveedor['empresa'], proveedor['direccion'],  proveedor['telefono'])
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def get_next_proveedor_id(self):
        query = "SELECT MAX(proveedor_id) FROM proveedor"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
    
    def get_all_proveedores(self):
        try:
            query = "SELECT * FROM proveedor"
            self.cursor.execute(query)
            proveedor = self.cursor.fetchall()
            return proveedor
        except Exception as e:
            print("Error while fetching all proveedores:", e)
            return None
    
    def get_proveedor_id_by_description(self, nombre):
        query = "SELECT proveedor_id FROM proveedor WHERE nombre = %s"
        self.cursor.execute(query, (nombre,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    #ARTICULOS
    #################################################################

    def search_articulo_by_id(self, articulo_id):
        query = "SELECT * FROM articulos WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        articulo = self.cursor.fetchone()
        return articulo

    def search_articulo_by_name(self, articulo_name):
        query = "SELECT * FROM articulos WHERE descripcion = %s"
        self.cursor.execute(query, (articulo_name,))
        articulo = self.cursor.fetchone()
        return articulo
    
    def update_articulo_in_articulos(self, articulo, articuloDetail):
        query = "UPDATE articulos SET descripcion=%s, precio_unitario=%s, precio_venta=%s, puntos=%s WHERE articulo_id=%s"
        values = (articulo['descripcion'], articulo['precio_unitario'], articulo['precio_venta'], articulo['puntos'], articulo['articulo_id'])
        self.cursor.execute(query, values)
        self.conn.commit()
        
        if articuloDetail:
            proveedor_id = self.get_proveedor_id_by_description(articuloDetail['proveedor_id'])
            query2 = "UPDATE det_articulo SET proveedor_id = %s, precio = %s, existencia = %s WHERE articulo_id = %s"
            values2 = (proveedor_id, articuloDetail['precio'], articuloDetail['existencia'], articuloDetail['articulo_id'])
            self.cursor.execute(query2, values2)
            self.conn.commit()
    
    def delete_articulo(self, articulo_id):
        query = "DELETE FROM articulos WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        self.conn.commit()
    
    def save_articulo(self, articulo):
        #valor = articulo['descuento'].strip()
        #descuento = int(valor) if valor else None
        query = "INSERT INTO articulos (articulo_id, descripcion, precio_unitario, precio_venta, puntos, descuento ) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (articulo['articulo_id'], articulo['descripcion'], articulo['precio_unitario'], articulo['precio_venta'], articulo['puntos'], articulo['descuento'])
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def get_next_articulo_id(self):
        query = "SELECT MAX(articulo_id) FROM articulos"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
    
    def add_articulo_detalle(self, articuloDetail):
        proveedor_id = self.get_proveedor_id_by_description(articuloDetail['proveedor_id'])
        stock = int(articuloDetail['existencia'])
        query = "INSERT INTO det_articulo (proveedor_id, articulo_id, precio, existencia) VALUES (%s, %s, %s, %s) RETURNING det_id_articulo;"
        values = (proveedor_id, articuloDetail['articulo_id'], articuloDetail['precio'], articuloDetail['existencia'])      
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_articulo_details(self, articulo_id):
        query = "SELECT proveedor_id, existencia FROM det_articulo WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        articuloDetail = self.cursor.fetchone()
        return articuloDetail
    
    def get_articulo_name_by_id(self, articulo_id):
        query = "SELECT descripcion FROM articulos WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    def get_articulo_stock_by_id(self, articulo_id):
        query = "SELECT existencia FROM det_articulo WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        result = self.cursor.fetchone()
        if result:
            return result 
        else:
            return None
        
    def get_articulo_compra_stock_by_id(self, articulo_id):
        query = "SELECT cantidad FROM det_compra WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        result = self.cursor.fetchall()
        
        return result 
        
    
    def update_articulo_stock(self, articulo_id, difference):
        print(f"Cantidad aqui en update stock: {difference}")
        current_stock = self.get_articulo_stock_by_id(articulo_id)
        print("STOCK ACTUAL DEL ARTICULO", current_stock)

        #current_stock = int(current_stock) if current_stock is not None else 0

        new_stock = current_stock[0] - difference

        if new_stock < 1:
            messagebox.showerror("Error", "No hay suficientes piezas en stock.")
            return

        query = "UPDATE det_articulo SET existencia=%s WHERE articulo_id=%s"
        values = (new_stock, articulo_id)
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def search_articulo_venta_stock_by_id(self, articulo_id):
        query = "SELECT cantidad FROM articulo_stock WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        result = self.cursor.fetchone()
        print("RESULTADO DE LA BUSQUEDA", result)
        
        if result:
            return result
        else:
            return None
    
    def save_articulo_stock_venta(self, articulo_id, difference):
        articulo_existente = self.search_articulo_venta_stock_by_id(articulo_id)
        print(f"Articulo existente: {articulo_existente}")
        print(f"Diferencia aqui en save stock: {difference}")
        
        query = "INSERT INTO articulo_stock (articulo_id, cantidad) VALUES (%s, %s)"
        values = (articulo_id, difference)
        self.cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Éxito", "Stock insertado con éxito.")
          
    def update_articulo_venta_stock(self, articulo_id, difference):
        
        query = "UPDATE articulo_stock SET cantidad = cantidad - %s WHERE articulo_id = %s"
        values = (difference, articulo_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Éxito", "Stock actualizado con éxito.")
    
    def update_articulo_venta_stock_delete(self, articulo_id, difference):
        
        query = "UPDATE articulo_stock SET cantidad = cantidad + %s WHERE articulo_id = %s"
        values = (difference, articulo_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Éxito", "Stock actualizado con éxito.")
        
    def delete_articulo_venta_stock(self, articulo_id):
        query = "DELETE FROM articulo_stock WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        self.conn.commit()
    
    def get_articulo_by_proveedor(self, name):
        proveedor_id = self.get_proveedor_id_by_description(name)
    
        query = "SELECT articulo_id FROM det_articulo WHERE proveedor_id = %s"
        self.cursor.execute(query, (proveedor_id,))
        result = self.cursor.fetchall()
        
        articulo_ids = [r[0] for r in result]  
        
        if not articulo_ids:
            return [] 
        
        placeholders = ','.join(['%s'] * len(articulo_ids))
        query2 = f"SELECT descripcion FROM articulos WHERE articulo_id IN ({placeholders})"
        
        self.cursor.execute(query2, articulo_ids)
        real_result = self.cursor.fetchall()
        
        return real_result
    
    def get_all_articulo(self):
    
        query = "SELECT * FROM articulos"
        self.cursor.execute(query,)
        result = self.cursor.fetchall()
        
        return result
        

    
    #VENTAS
    #################################################################

    def search_venta_by_id(self, venta_id):
        query = "SELECT * FROM ventas WHERE folio_venta = %s"
        self.cursor.execute(query, (venta_id,))
        venta = self.cursor.fetchone()
        return venta

    def search_articulo_by_name(self, articulo_name):
        query = "SELECT * FROM articulos WHERE descripcion = %s"
        self.cursor.execute(query, (articulo_name,))
        articulo = self.cursor.fetchone()
        return articulo
    
    def update_articulo(self, articulo, articuloDetail):
        query = "UPDATE articulos SET descripcion=%s, precio_unitario=%s, precio_venta=%s, descuento=%s, puntos=%s WHERE articulo_id=%s"
        values = (articulo['descripcion'], articulo['precio_unitario'], articulo['precio_venta'], articulo['descuento'], articulo['puntos'], articulo['articulo_id'])
        self.cursor.execute(query, values)
        self.conn.commit()
        
        if articuloDetail:
            proveedor_id = self.get_proveedor_id_by_description(articuloDetail['proveedor_id'])
            query2 = "UPDATE det_articulo SET proveedor_id = %s, precio = %s, existencia = %s WHERE articulo_id = %s"
            values2 = (proveedor_id, articuloDetail['precio'], articuloDetail['existencia'], articuloDetail['articulo_id'])
            self.cursor.execute(query2, values2)
            self.conn.commit()
    
    def delete_articulo(self, articulo_id):
        query = "DELETE FROM articulos WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        self.conn.commit()
    
    def save_venta(self, venta):
        #valor = articulo['descuento'].strip()
        #descuento = int(valor) if valor else None
        print("TOTAL DE LA VENTA",venta["total"])   
        user_id = self.search_user_by_username(venta['usuario'])
        query = "INSERT INTO ventas (folio_venta, user_id, fecha, total) VALUES (%s, %s, %s, %s)"
        values = (venta['venta_id'], user_id[0], venta['fecha'], venta['total'])
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_venta(self, folio_venta):
        query = "DELETE FROM ventas WHERE folio_venta = %s"
        self.cursor.execute(query, (folio_venta,))
        self.conn.commit()
    
    def update_venta(self, venta, ventaDetail, actual_stock):
        articulo_id = self.search_articulo_by_name(ventaDetail['articulo'])
        print("ARTICULO ID",articulo_id[0])
        query0 = "SELECT * FROM det_venta WHERE articulo_id = %s AND folio_venta = %s"
        self.cursor.execute(query0, (articulo_id[0], venta['folio_venta']))
        detalle_compra = self.cursor.fetchone()
        print(detalle_compra)       
        
        user_id = self.search_user_by_username(venta['usuario'])
        query = "UPDATE ventas SET user_id=%s, fecha=%s, total=%s WHERE folio_venta=%s"
        values = (user_id[0], venta['fecha'], venta['total'], venta['folio_venta'])
        self.cursor.execute(query, values)
        self.conn.commit()
        
        if ventaDetail:
            cantidad_nueva = int(ventaDetail['cantidad'])    
            cantidad_existente = actual_stock
            print("Cantidad existente", cantidad_existente)
            
            print("Cantidad nueva", cantidad_nueva)
            
            #CHECAR QUE SEA EN EL STOCK DE VENTAS
                        
            if cantidad_nueva > cantidad_existente:  
                diferencia = cantidad_nueva - cantidad_existente
                self.update_articulo_venta_stock(articulo_id[0], diferencia)
            elif cantidad_nueva < cantidad_existente:
                diferencia = cantidad_existente - cantidad_nueva
                self.update_articulo_venta_stock(articulo_id[0], -diferencia)
            print(diferencia)
            
            print(f'Cantidad existente: {cantidad_existente}, Cantidad nueva: {cantidad_nueva}, Diferencia: {diferencia}') 
            
            query2 = "UPDATE det_venta SET articulo_id = %s, cantidad = %s WHERE det_id_venta = %s AND folio_venta = %s"
            values2 = (articulo_id[0], ventaDetail['cantidad'], ventaDetail['det_id_venta'], ventaDetail['venta_id'])
            self.cursor.execute(query2, values2)
            self.conn.commit()
            
            #cantidad = int(compraDetail['cantidad'])
            
            #self.update_articulo_stock(articulo_id[0], cantidad)  
    
    def get_next_venta_id(self):
        query = "SELECT MAX(folio_venta) FROM ventas"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
        

    
    def add_venta_detalle(self, ventaDetail):
        articulo_name = self.get_articulo_name_by_id(ventaDetail['articulo_id'])
        cliente_name = self.get_customer_name_by_id(ventaDetail['cliente_id'])
        cantidad = int(ventaDetail['cantidad'])
        
        query = "INSERT INTO det_venta (folio_venta, articulo_id, cantidad, cliente_id, puntos) VALUES (%s, %s, %s, %s, %s) RETURNING det_id_venta;"
        values = (ventaDetail['folio_venta'], ventaDetail['articulo_id'], cantidad, ventaDetail['cliente_id'], ventaDetail['puntos'])      
        self.cursor.execute(query, values)
        self.conn.commit()
        
        venta_id = self.cursor.fetchone()[0]
        
        print(f"Diferencia aqui en update stock: {cantidad}")
        
        stock = self.get_articulo_compra_stock_by_id(ventaDetail['articulo_id'])
        
        articulo_existente = self.search_articulo_venta_stock_by_id(ventaDetail['articulo_id'])
        print("ARTICULO EXISTENTE", articulo_existente)
        
        if articulo_existente:
            cantidad_existente = articulo_existente[0]
            print("Cantidad existente", cantidad_existente)
            nuevo_stock = cantidad_existente - cantidad
            query = "UPDATE articulo_stock SET cantidad = %s WHERE articulo_id = %s"
            values = (nuevo_stock, ventaDetail['articulo_id'])
            self.cursor.execute(query, values)
            messagebox.showinfo("Éxito", "Stock actualizado con éxito.")      

        return {
            'folio_venta': venta_id,
            'articulo_name': articulo_name,
            'cantidad': cantidad,
            'cliente_name': cliente_name,
            'puntos': ventaDetail['puntos']   
        }
    
    def search_venta_detalle_by_id(self, venta_id, articulo_id):
        query = "SELECT * FROM det_venta WHERE folio_venta = %s AND articulo_id = %s"
        self.cursor.execute(query, (venta_id, articulo_id))
        detalle = self.cursor.fetchone()
        print("DETALLE DE LA VENTA", detalle)
        return detalle
        
    def get_venta_detalle(self, folio_venta):
        query = "SELECT * FROM det_venta WHERE folio_venta = %s"
        self.cursor.execute(query, (folio_venta,))
        ventaDetail = self.cursor.fetchall()
        return ventaDetail
    
    def get_venta_detalle_by_articulo(self, articulo_id):
        query = "SELECT * FROM det_venta WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        ventaDetail = self.cursor.fetchone()
        return ventaDetail
      
    def delete_venta_detalle(self, folio_venta, articulo_id, cantidad, cliente_id, puntos):
        query = "DELETE FROM det_venta WHERE folio_venta = %s AND articulo_id = %s AND cantidad = %s AND cliente_id = %s AND puntos = %s RETURNING *;"
        self.cursor.execute(query, (folio_venta, articulo_id, cantidad, cliente_id, puntos))
        deleted_details = self.cursor.fetchall()
        self.conn.commit()
        return deleted_details
        
    def get_articulo_details(self, articulo_id):
        query = "SELECT proveedor_id, existencia FROM det_articulo WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        articuloDetail = self.cursor.fetchone()
        return articuloDetail
    
    def update_venta_detalle(self, venta_id, articulo_id, cantidad, cliente_id, puntos):    
        query = "UPDATE det_venta SET cantidad = %s WHERE folio_venta = %s AND articulo_id = %s AND cliente_id = %s AND puntos = %s"
        values = (cantidad, venta_id, articulo_id, cliente_id, puntos)
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_all_detalles_venta(self, folio_venta):
        query = "DELETE FROM det_venta WHERE folio_venta = %s"
        self.cursor.execute(query, (folio_venta,))
        self.conn.commit()
    
    def search_cliente_by_venta(self, cliente_name):
        cliente_id = self.search_customer_by_name(cliente_name)
        query = "SELECT * FROM clientes WHERE cliente_id = %s"
        self.cursor.execute(query, (cliente_id[0],))
        cliente = self.cursor.fetchone()
        return cliente

    def update_total_in_venta(self, venta_id, total):
        query = "UPDATE ventas SET total = %s WHERE folio_venta = %s"
        values = (total, venta_id)
        self.cursor.execute(query, values)
        self.conn.commit()

    #COMPRAS
    #################################################################
    
    def get_compra_detalle(self, folio_compra):
        query = "SELECT * FROM det_compra WHERE folio_compra = %s"
        self.cursor.execute(query, (folio_compra,))
        compraDetail = self.cursor.fetchall()
        return compraDetail
       
    def search_compra_by_id(self, compra_id):
        query = "SELECT * FROM compras WHERE folio_compra = %s"
        self.cursor.execute(query, (compra_id,))
        compra = self.cursor.fetchone()
        return compra
    
    def update_compra(self, compra, compraDetail, actual_stock):
        articulo_id = self.search_articulo_by_name(compraDetail['articulo'])
        query0 = "SELECT * FROM det_compra WHERE articulo_id = %s AND folio_compra = %s"
        self.cursor.execute(query0, (articulo_id[0], compra['compra_id']))
        detalle_compra = self.cursor.fetchone()
        print(detalle_compra)       
        
        user_id = self.search_user_by_username(compra['usuario'])
        query = "UPDATE compras SET user_id=%s, fecha=%s, total=%s WHERE folio_compra=%s"
        values = (user_id[0], compra['fecha'], compra['total'], compra['compra_id'])
        self.cursor.execute(query, values)
        self.conn.commit()
        
        if compraDetail:
            cantidad_nueva = int(compraDetail['cantidad'])    
            cantidad_existente = actual_stock
            print("Cantidad existente", cantidad_existente)
            
            print("Cantidad nueva", cantidad_nueva)
                        
            if cantidad_nueva > cantidad_existente:  
                diferencia = cantidad_nueva - cantidad_existente
                self.update_articulo_stock(articulo_id[0], diferencia)
            elif cantidad_nueva < cantidad_existente:
                diferencia = cantidad_existente - cantidad_nueva
                self.update_articulo_stock(articulo_id[0], -diferencia)
            print(diferencia)
            
            print(f'Cantidad existente: {cantidad_existente}, Cantidad nueva: {cantidad_nueva}, Diferencia: {diferencia}') 
            
            query2 = "UPDATE det_compra SET articulo_id = %s, cantidad = %s WHERE det_id_compra = %s AND folio_compra = %s"
            values2 = (articulo_id[0], compraDetail['cantidad'], compraDetail['det_id_compra'], compraDetail['compra_id'])
            self.cursor.execute(query2, values2)
            self.conn.commit()
            
            #cantidad = int(compraDetail['cantidad'])
            
            #self.update_articulo_stock(articulo_id[0], cantidad)  

    def update_total_in_compra(self, compra_id, total):
        query = "UPDATE compras SET total = %s WHERE folio_compra = %s"
        values = (total, compra_id)
        self.cursor.execute(query, values)
        self.conn.commit()       
    
    def delete_compra(self, folio_compra):
        query = "DELETE FROM compras WHERE folio_compra = %s"
        self.cursor.execute(query, (folio_compra,))
        self.conn.commit()
    
    def save_compra(self, compra):
        #valor = articulo['descuento'].strip()
        #descuento = int(valor) if valor else None
        user_id = self.search_user_by_username(compra['usuario'])
        query = "INSERT INTO compras (folio_compra, user_id, fecha, total) VALUES (%s, %s, %s, %s)"
        values = (compra['compra_id'], user_id[0], compra['fecha'], compra['total'])
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def get_next_compra_id(self):
        query = "SELECT MAX(folio_compra) FROM compras"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
    
    def add_compra_detalle(self, compraDetail):
        articulo_name = self.get_articulo_name_by_id(compraDetail['articulo_id'])
        cantidad = int(compraDetail['cantidad'])
        
        query = "INSERT INTO det_compra (folio_compra, articulo_id, cantidad) VALUES (%s, %s, %s) RETURNING det_id_compra;"
        values = (compraDetail['folio_compra'], compraDetail['articulo_id'], cantidad)      
        self.cursor.execute(query, values)
        self.conn.commit()
        compra_id = self.cursor.fetchone()
        
        venta_stock = self.search_articulo_venta_stock_by_id(compraDetail['articulo_id'])
        print("ARTICULO EXISTENTE", venta_stock)
        if venta_stock:
            cantidad_existente = venta_stock[0]
            print("Cantidad existente", cantidad_existente)
            nuevo_stock = cantidad_existente + cantidad
            query = "UPDATE articulo_stock SET cantidad = %s WHERE articulo_id = %s"
            values = (nuevo_stock, compraDetail['articulo_id'])
            self.cursor.execute(query, values)
            messagebox.showinfo("Éxito", "Stock actualizado con éxito.")
        else:
            stock = self.get_articulo_compra_stock_by_id(compraDetail['articulo_id'])
            
            current_stock = sum(int(row[0]) for row in stock) if stock else 0
            print("STOCK ACTUAL DEL ARTICULO", current_stock)
            
            new_stock = current_stock + cantidad
            
            self.save_articulo_stock_venta(compraDetail["articulo_id"], new_stock)

            if new_stock < 0:
                messagebox.showerror("Error", "No hay suficientes piezas en stock.")
                return
        
        
        print(f"cantidad a comprar: {cantidad}")
        self.update_articulo_stock(compraDetail['articulo_id'], cantidad)  

        return {
            'folio_compra': compra_id,
            'articulo_name': articulo_name,
            'cantidad': cantidad, 
        }
      
    def delete_compra_detalle(self, det_id_compra, articulo_id, cantidad):
        query = "DELETE FROM det_compra WHERE det_id_compra = %s AND articulo_id = %s AND cantidad = %s RETURNING *;"
        self.cursor.execute(query, (det_id_compra, articulo_id, cantidad))
        deleted_details = self.cursor.fetchall()
        print("Detalles eliminados:", deleted_details)
        self.conn.commit()
        return deleted_details
    
    def delete_all_detalles(self, folio_compra):
        query = "DELETE FROM det_compra WHERE folio_compra = %s"
        self.cursor.execute(query, (folio_compra,))
        self.conn.commit()
        
    def get_one_detalle(self, folio_compra):
            folio_compra_int = int(folio_compra)
            print(folio_compra_int)
            query = "SELECT * FROM det_compra WHERE folio_compra = %s"
            self.cursor.execute(query, (folio_compra_int,))
            compraDetail = self.cursor.fetchall()
            print(compraDetail)
            return compraDetail
    
    def search_compra_detalle_by_id(self, compra_id, articulo_id):
        query = "SELECT * FROM det_compra WHERE folio_compra = %s AND articulo_id = %s"
        self.cursor.execute(query, (compra_id, articulo_id))
        detalle = self.cursor.fetchone()
        return detalle
    
    def update_compra_detalle(self, compra_id, articulo_id, cantidad):
        query = "UPDATE det_compra SET cantidad = %s WHERE folio_compra = %s AND articulo_id = %s"
        values = (cantidad, compra_id, articulo_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        
        cantidad_nueva = int(cantidad)
        
        venta_stock = self.search_articulo_venta_stock_by_id(articulo_id)
        print("ARTICULO EXISTENTE EN UPDATE", venta_stock)
        if venta_stock:
            cantidad_existente = venta_stock[0]
            print("Cantidad existente en update", cantidad_existente)
            diferencia = cantidad_nueva - cantidad_existente
            print("Cantidad existente en update", cantidad_existente)
            nuevo_stock = diferencia + cantidad_existente
            print("Nuevo stock en update", nuevo_stock)
            query = "UPDATE articulo_stock SET cantidad = %s WHERE articulo_id = %s"
            values = (nuevo_stock, articulo_id)
            self.cursor.execute(query, values)
            messagebox.showinfo("Éxito", "Stock actualizado con éxito en update.")
        
    def search_compra_detalle_by_folio(self, folio_compra):
        query = "SELECT * FROM det_compra WHERE folio_compra = %s"
        self.cursor.execute(query, (folio_compra,))
        detalle = self.cursor.fetchall()
        return detalle
        
class App:
    def __init__(self, root, username=None):    
        self.root = root
        self.root.title("Usuarios")
        self.db = DBManager()
        self.current_user_id = None
        self.username = username

        self.root.configure(bg="#ffffff")
        self.font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        
        self.lbl_search_id = tk.Label(root, text="Buscar ID:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_search_id.place(x=20, y=2)  
        self.ent_search_id = tk.Entry(root, font=self.font)
        self.ent_search_id.place(x=180, y=2)
        
        self.btn_search = tk.Button(
            root, 
            text="Buscar", 
            command=self.search, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_search.place(x=450, y=2) 

        self.lbl_user_id = tk.Label(root, text="ID de Usuario:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_user_id.place(x=20, y=40)  
        self.ent_user_id = tk.Entry(root, font=self.font, state="readonly")
        self.ent_user_id.place(x=180, y=40)  

        self.lbl_name = tk.Label(root, text="Nombre:", font=self.font, bg="#ffffff",fg="#03012C")
        self.lbl_name.place(x=20, y=80)  
        self.ent_name = tk.Entry(root, font=self.font, state="disabled")
        self.ent_name.place(x=180, y=80)   

        self.lbl_password = tk.Label(root, text="Contraseña:", font=self.font, bg="#ffffff",fg="#03012C")
        self.lbl_password.place(x=20, y=120)  
        self.ent_password = tk.Entry(root, show="*", font=self.font, state="disabled")
        self.ent_password.place(x=180, y=120)  

        self.lbl_profile = tk.Label(root, text="Perfil:", font=self.font, bg="#ffffff",fg="#03012C")
        self.lbl_profile.place(x=20, y=160)  
        self.ent_profile = ttk.Combobox(root, values=["admin", "cajero", "gerente"], font=self.font, state="disabled")
        self.ent_profile.place(x=180, y=160)  

        self.btn_insert = tk.Button(
            root, 
            text="Guardar", 
            command=self.insert, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_insert.place(x=20, y=210) 

        self.btn_cancel = tk.Button(
            root, 
            text="Cancelar", 
            command=self.cancel, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_cancel.place(x=140, y=210) 

        self.btn_new = tk.Button(
            root, 
            text="Nuevo", 
            command=self.new_user, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_new.place(x=260, y=210)  

         

        self.btn_edit = tk.Button(
            root, 
            text="Editar", 
            command=self.edit, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_edit.place(x=360, y=210)  

        self.btn_delete = tk.Button(
            root, 
            text="Eliminar", 
            command=self.delete, 
            font=self.button_font, 
            bg="#33658A", 
            fg="white", 
            state="disabled"
        )
        self.btn_delete.place(x=460, y=210)  

         
        
        self.setup_buttons()
        
    def validate_name(self, name):
        """Valida que el nombre solo contenga letras y espacios"""
        if not name.strip():  
            return False
        return name.replace(" ", "").isalpha()  
    
    def setup_buttons(self):
        if self.username in ["cajero", "gerente"]:
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")

        self.btn_new.config(state="normal")
        self.btn_search.config(state="normal")
        self.btn_insert.config(state="normal")
        self.btn_cancel.config(state="normal")


    def new_user(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])

        self.current_user_id = self.db.get_next_user_id()
        self.ent_user_id.insert(0, self.current_user_id)
        self.ent_user_id["state"] = "readonly"
        self.ent_user_id["state"] = "disabled"    

    def insert(self):
        if not self.validate_fields():
            return
        user = {
            'user_id': self.ent_user_id.get(),
            'name': self.ent_name.get(),
            'password': self.ent_password.get(),
            'profile': self.ent_profile.get()
        }
        self.db.save_user(user)
        messagebox.showinfo("Éxito", "Usuario insertado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search(self):
        user_id = self.ent_search_id.get()
        
        if not user_id or not user_id.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número válido.")
            return
        
        user = self.db.search_user_by_id(user_id)
        if user:
            self.ent_user_id.delete(0, END)
            self.ent_name.delete(0, END)
            self.ent_password.delete(0, END)
            self.ent_profile.set("")

            #asi es para no se pongan doble los datos en el entry    
            self.ent_user_id["state"] = "normal"
            self.ent_name["state"] = "normal"
            self.ent_password["state"] = "normal"
            self.ent_profile["state"] = "normal"

            self.ent_user_id.insert(0, user[0])
            
            #self.ent_user_id["state"] = "disabled" 
            
            self.ent_name.insert(0, user[1])
            self.ent_password.insert(0, user[2])
            self.ent_profile.set(user[3])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            self.ent_user_id["state"] = "readonly"
            
            self.btn_edit["state"] = "normal"
        else:
            messagebox.showinfo("Error", "Usuario no encontrado.")

    def edit(self):
        if not self.validate_fields():
            return
        
        user = {
            'user_id': self.ent_user_id.get(),
            'name': self.ent_name.get(),
            'password': self.ent_password.get(),
            'profile': self.ent_profile.get()
        }
        self.db.update_user(user)
        messagebox.showinfo("Éxito", "Usuario actualizado con éxito.")
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()

    def delete(self):
        if not self.ent_user_id.get():
            messagebox.showerror("Error", "Debe ingresar un ID de usuario.")
            return

        user_id = self.ent_user_id.get()
        
        if messagebox.askyesno("Confirmación", "¿Estás seguro de que desea eliminar este usuario y todos los datos asociados?"):
            self.db.delete_user(user_id)
            messagebox.showinfo("Éxito", "Usuario y datos asociados eliminados con éxito.")
            self.clear_entries()
            self.disable_entries()
            self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
            self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_user_id.get()
            or not self.ent_name.get()
           #or not self.ent_username.get()
            or not self.ent_password.get()
            or not self.ent_profile.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        
        if not self.validate_name(self.ent_name.get()):
            messagebox.showerror("Error", "El nombre solo puede contener letras y espacios.")
            return False

        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_user_id.delete(0, END)
        self.ent_name.delete(0, END)
        self.ent_password.delete(0, END)
        self.ent_profile.set("")

    def enable_entries(self):
        self.ent_user_id["state"] = "normal"
        self.ent_name["state"] = "normal"
        self.ent_password["state"] = "normal"
        self.ent_profile["state"] = "normal"

    def disable_entries(self):
        self.ent_user_id["state"] = "disabled"
        self.ent_name["state"] = "disabled"
        self.ent_password["state"] = "disabled"
        self.ent_profile["state"] = "disabled"

class CustomerApp:
    def __init__(self, root, db, user_id, username=None):
        self.root = root
        self.root.title("Clientes")
        self.db = db
        self.current_customer_id = None
        self.user_id = user_id
        self.username = username  

        self.root.configure(bg="#ffffff")
        self.font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        
        self.lbl_search_id = tk.Label(root, text="Buscar ID:", font=self.font, bg="#ffffff")
        self.lbl_search_id.place(x=20, y=2)  
        self.ent_search_id = tk.Entry(root, font=self.font)
        self.ent_search_id.place(x=180, y=2)
        
        self.btn_search = tk.Button(
            root, 
            text="Buscar", 
            command=self.search_customer, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_search.place(x=450, y=2)

        self.lbl_customer_id = tk.Label(root, text="ID de Cliente:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_customer_id.place(x=20, y=40)  
        self.ent_customer_id = tk.Entry(root, font=self.font, state="readonly")
        self.ent_customer_id.place(x=180, y=40) 

        self.lbl_name = tk.Label(root, text="Nombre:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_name.place(x=20, y=80) 
        self.ent_name = tk.Entry(root, font=self.font, state="disabled")
        self.ent_name.place(x=180, y=80)  

        self.lbl_phone = tk.Label(root, text="Teléfono:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_phone.place(x=20, y=120)  
        self.ent_phone = tk.Entry(root, font=self.font, state="disabled")
        self.ent_phone.place(x=180, y=120)
        
        self.lbl_username = tk.Label(root, text="Nombre de usuario:", font=self.font, bg="#ffffff")
        self.lbl_username.place(x=20, y=200)  
        self.ent_username = tk.Entry(root, font=self.font, state="normal")
        self.ent_username.place(x=220, y=200)  
        self.ent_username.insert(0, self.username) 

        self.lbl_user_id = tk.Label(root, text="ID de Usuario:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_user_id.place(x=20, y=160)  
        self.ent_user_id = tk.Entry(root, font=self.font, state="normal")
        self.ent_user_id.place(x=180, y=160)  
        self.ent_user_id.insert(0, self.user_id)
        
        self.lbl_rfc = tk.Label(root, text="RFC:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_rfc.place(x=20, y=240)  
        self.ent_rfc = tk.Entry(root, font=self.font, state="normal")
        self.ent_rfc.place(x=180, y=240)  

        self.btn_insert = tk.Button(
            root, 
            text="Guardar", 
            command=self.insert, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_insert.place(x=20, y=280)  

        self.btn_cancel = tk.Button(
            root, 
            text="Cancelar", 
            command=self.cancel, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_cancel.place(x=140, y=280) 

        self.btn_new = tk.Button(
            root, 
            text="Nuevo", 
            command=self.new_customer, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_new.place(x=260, y=280)    

        self.btn_edit = tk.Button(
            root, 
            text="Editar", 
            command=self.edit, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_edit.place(x=360, y=280)  

        self.btn_delete = tk.Button(
            root, 
            text="Eliminar", 
            command=self.delete, 
            font=self.button_font, 
            bg="#33658A", 
            fg="white", 
            state="disabled"
        )
        self.btn_delete.place(x=460, y=280)  

        

        self.setup_buttons()  
    
    def validate_name(self, name):
        """Valida que el nombre solo contenga letras y espacios"""
        if not name.strip():  
            return False
        return name.replace(" ", "").isalpha()  
    
    def setup_buttons(self):
        print("user", self.username)
        user = self.db.search_user_by_username(self.username)
        print("user", user[3])
        if user[3] == "cajero":
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")
            #self.btn_cancel.config(state="disabled")

        self.btn_new.config(state="normal")
        self.btn_search.config(state="normal")
        self.btn_insert.config(state="normal")
        self.btn_cancel.config(state="normal")

    def new_customer(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])

        self.current_customer_id = self.db.get_next_customer_id()
        self.ent_customer_id.insert(0, self.current_customer_id)
        self.ent_customer_id["state"] = "readonly"
        self.ent_customer_id["state"] = "disabled"  

    def insert(self):
        if not self.validate_fields():
            return

        user_id = self.ent_user_id.get()
        if not self.db.search_user_by_id(user_id):
            messagebox.showerror("Error", f"El usuario con ID {user_id} no está registrado.")
            return

        customer_name = self.ent_name.get()
        existing_customer = self.db.search_customer_by_name(customer_name)
        if existing_customer and existing_customer[3] != user_id:  
            messagebox.showerror("Error", "Este cliente ya fue registrado por otro usuario.")
            return

        customer = {
            'cliente_id': self.ent_customer_id.get(),
            'user_id': user_id,
            'nombre': customer_name,
            'telefono': self.ent_phone.get(),            
            'rfc': self.ent_rfc.get()
        }
        self.db.save_customer(customer)
        messagebox.showinfo("Éxito", "Cliente insertado con éxito.")
        self.clear_entries()
        self.disable_entries()
        user = self.db.search_user_by_username(self.username)
        print("user", user[3])
        if user[3] == "cajero":
            print("cajero")
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")
            self.disable_buttons([self.btn_insert, self.btn_cancel])            
                #self.btn_cancel.config(state="disabled")
        else:
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])  
            self.enable_entries()
            
        #self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search_customer(self):
        customer_id_or_name = self.ent_search_id.get()
        if customer_id_or_name.isdigit():  
            customer = self.db.search_customer_by_id(customer_id_or_name)
        else:  
            customer = self.db.search_customer_by_name(customer_id_or_name)
        
        if customer:
            self.ent_customer_id.delete(0, END)
            self.ent_name.delete(0, END)
            self.ent_phone.delete(0, END)
            self.ent_user_id.delete(0, END)
            self.ent_rfc.delete(0, END)
            
            self.ent_customer_id["state"] = "normal"
            self.ent_name["state"] = "normal"
            self.ent_phone["state"] = "normal"
            self.ent_user_id["state"] = "normal"
            self.ent_rfc["state"] = "normal"

            self.ent_customer_id.insert(0, customer[0])
            self.ent_name.insert(0, customer[2])
            self.ent_phone.insert(0, customer[3])
            self.ent_user_id.insert(0, customer[1])
            self.ent_rfc.insert(0, customer[4])

            self.disable_buttons([self.btn_new, self.btn_insert])
            
            user = self.db.search_user_by_username(self.username)
            print("user", user[3])
            if user[3] == "cajero":
                print("cajero")
                self.btn_edit.config(state="disabled")
                self.btn_delete.config(state="disabled")
                #self.btn_cancel.config(state="disabled")
            else:
                self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])  
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            self.ent_customer_id["state"] = "readonly"
            
            #self.btn_edit["state"] = "normal"
        else:
            messagebox.showinfo("Error", "Cliente no encontrado.")

    def edit(self):
        if not self.validate_fields():
            return
        
        customer = {
            'cliente_id': self.ent_customer_id.get(),
            'user_id': self.ent_user_id.get(),
            'nombre': self.ent_name.get(),
            'telefono': self.ent_phone.get(),
            'rfc': self.ent_rfc.get()
            
        }
        self.db.update_customer(customer)
        messagebox.showinfo("Éxito", "Cliente actualizado con éxito.")
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()

    def delete(self):
        if not self.ent_customer_id.get():
            messagebox.showerror("Error", "Debe ingresar un ID de cliente.")
            return
        customer_id = self.ent_customer_id.get()
        self.db.delete_customer(customer_id)
        messagebox.showinfo("Éxito", "Cliente eliminado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_customer_id.get()
            or not self.ent_name.get()
            or not self.ent_phone.get()
            or not self.ent_user_id.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        if (
            not self.ent_phone.get().isdigit()
        ):
            messagebox.showerror("Error, ingrese solo numeros")
            return False
        
        if not self.validate_name(self.ent_name.get()):
            messagebox.showerror("Error", "El nombre solo puede contener letras y espacios.")
            return False
        
        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_customer_id.delete(0, END)
        self.ent_name.delete(0, END)
        self.ent_phone.delete(0, END)
        self.ent_rfc.delete(0, END)
        #self.ent_user_id.delete(0, END)

    def enable_entries(self):
        self.ent_customer_id["state"] = "normal"
        self.ent_name["state"] = "normal"
        self.ent_phone["state"] = "normal"
        self.ent_user_id["state"] = "normal"

    def disable_entries(self):
        self.ent_customer_id["state"] = "disabled"
        self.ent_name["state"] = "disabled"
        self.ent_phone["state"] = "disabled"
        self.ent_user_id["state"] = "disabled"

    def open_customer_menu(self):
            customer_window = tk.Tk()
            customer_window.title("Menú de Clientes")
            customer_window.geometry("600x400")
            customer_app = CustomerApp(customer_window, self.db, self.user_id, self.username)
            
            customer_window.mainloop()

class ProveedorApp:
    def __init__(self, root, db, user_id, username):
        self.root = root
        self.root.title("Proveedores")
        self.db = db
        self.current_proveedor_id = None
        self.username = username   

        self.root.configure(bg="#ffffff")
        self.font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        
        self.lbl_search_id = tk.Label(root, text="Buscar ID:", font=self.font, bg="#ffffff")
        self.lbl_search_id.place(x=20, y=2)  
        self.ent_search_id = tk.Entry(root, font=self.font)
        self.ent_search_id.place(x=180, y=2)
        
        self.btn_search = tk.Button(
            root, 
            text="Buscar", 
            command=self.search_proveedor, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_search.place(x=450, y=2)

        self.lbl_proveedor_id = tk.Label(root, text="ID Proveedor:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_proveedor_id.place(x=20, y=40)  
        self.ent_proveedor_id = tk.Entry(root, font=self.font, state="readonly")
        self.ent_proveedor_id.place(x=180, y=40) 

        self.lbl_name = tk.Label(root, text="Nombre:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_name.place(x=20, y=80) 
        self.ent_name = tk.Entry(root, font=self.font, state="disabled")
        self.ent_name.place(x=180, y=80)  

        self.lbl_phone = tk.Label(root, text="Teléfono:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_phone.place(x=20, y=120)  
        self.ent_phone = tk.Entry(root, font=self.font, state="disabled")
        self.ent_phone.place(x=180, y=120)
        
        self.lbl_empresa = tk.Label(root, text="Empresa:", font=self.font, bg="#ffffff")
        self.lbl_empresa.place(x=20, y=200)  
        self.ent_empresa = tk.Entry(root, font=self.font, state="normal")
        self.ent_empresa.place(x=180, y=200)   

        self.lbl_direccion = tk.Label(root, text="Direccion:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_direccion.place(x=20, y=160)  
        self.ent_direccion = tk.Entry(root, font=self.font, state="normal")
        self.ent_direccion.place(x=180, y=160)  

        self.btn_insert = tk.Button(
            root, 
            text="Guardar", 
            command=self.insert, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_insert.place(x=20, y=280)  

        self.btn_cancel = tk.Button(
            root, 
            text="Cancelar", 
            command=self.cancel, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_cancel.place(x=140, y=280) 

        self.btn_new = tk.Button(
            root, 
            text="Nuevo", 
            command=self.new_proveedor, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_new.place(x=260, y=280)    

        self.btn_edit = tk.Button(
            root, 
            text="Editar", 
            command=self.edit, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_edit.place(x=360, y=280)  

        self.btn_delete = tk.Button(
            root, 
            text="Eliminar", 
            command=self.delete, 
            font=self.button_font, 
            bg="#33658A", 
            fg="white", 
            state="disabled"
        )
        self.btn_delete.place(x=460, y=280)  

        

        self.setup_buttons()  
    
    def validate_name(self, name):
        """Valida que el nombre solo contenga letras y espacios"""
        if not name.strip():  
            return False
        return name.replace(" ", "").isalpha()  
    
    def setup_buttons(self):
        if self.username in ["Secre", "Mecanico"]:
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")

        self.btn_new.config(state="normal")
        self.btn_search.config(state="normal")
        self.btn_insert.config(state="normal")
        self.btn_cancel.config(state="normal")


    def new_proveedor(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])

        self.current_proveedor_id = self.db.get_next_proveedor_id()
        self.ent_proveedor_id.insert(0, self.current_proveedor_id)
        self.ent_proveedor_id["state"] = "readonly"
        self.ent_proveedor_id["state"] = "disabled"

    def insert(self):
        if not self.validate_fields():
            return

        proveedor = {
            'proveedor_id': self.ent_proveedor_id.get(),
            'nombre': self.ent_name.get(),
            'empresa': self.ent_empresa.get(),
            'direccion': self.ent_direccion.get(),           
            'telefono': self.ent_phone.get(),            
        }
        self.db.save_proveedor(proveedor)
        messagebox.showinfo("Éxito", "Proveedor insertado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search_proveedor(self):
        proveedor_id_or_name = self.ent_search_id.get()
        if proveedor_id_or_name.isdigit():  
            proveedor = self.db.search_proveedor_by_id(proveedor_id_or_name)
        else:  
            proveedor = self.db.search_proveedor_by_name(proveedor_id_or_name)
        
        if proveedor:
            self.ent_proveedor_id.delete(0, END)
            self.ent_name.delete(0, END)
            self.ent_empresa.delete(0, END)
            self.ent_direccion.delete(0, END)
            self.ent_phone.delete(0, END)
            
            self.ent_proveedor_id["state"] = "normal"
            self.ent_name["state"] = "normal"
            self.ent_empresa["state"] = "normal"
            self.ent_direccion["state"] = "normal"
            self.ent_phone["state"] = "normal"

            self.ent_proveedor_id.insert(0, proveedor[0])
            self.ent_name.insert(0, proveedor[1])
            self.ent_empresa.insert(0, proveedor[2])
            self.ent_direccion.insert(0, proveedor[3])
            self.ent_phone.insert(0, proveedor[4])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])  
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            self.ent_proveedor_id["state"] = "readonly"
            
            self.btn_edit["state"] = "normal"
        else:
            messagebox.showinfo("Error", "Proveedor no encontrado.")

    def edit(self):
        if not self.validate_fields():
            return
        
        proveedor = {
            'proveedor_id': self.ent_proveedor_id.get(),
            'nombre': self.ent_name.get(),
            'empresa': self.ent_empresa.get(),
            'direccion': self.ent_direccion.get(),           
            'telefono': self.ent_phone.get(),            
        }
        
        self.db.update_proveedor(proveedor)
        messagebox.showinfo("Éxito", "Proveedor actualizado con éxito.")
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()

    def delete(self):
        if not self.ent_proveedor_id.get():
            messagebox.showerror("Error", "Debe ingresar un ID de proveedor.")
            return
        proveedor_id = self.ent_proveedor_id.get()
        self.db.delete_proveedor(proveedor_id)
        messagebox.showinfo("Éxito", "Proveedor eliminado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_proveedor_id.get()
            or not self.ent_name.get()
            or not self.ent_empresa.get()
            or not self.ent_empresa.get()
            or not self.ent_phone.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        if (
            not self.ent_phone.get().isdigit()
        ):
            messagebox.showerror("Error, ingrese solo numeros")
            return False
        
        if not self.validate_name(self.ent_name.get()):
            messagebox.showerror("Error", "El nombre solo puede contener letras y espacios.")
            return False
        
        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_proveedor_id.delete(0, END)
        self.ent_name.delete(0, END)
        self.ent_empresa.delete(0, END)
        self.ent_direccion.delete(0, END)
        self.ent_phone.delete(0, END)
        #self.ent_user_id.delete(0, END)

    def enable_entries(self):
        self.ent_proveedor_id["state"] = "normal"
        self.ent_name["state"] = "normal"
        self.ent_empresa["state"] = "normal"
        self.ent_direccion["state"] = "normal"       
        self.ent_phone["state"] = "normal"

    def disable_entries(self):
        self.ent_proveedor_id["state"] = "disabled"
        self.ent_name["state"] = "disabled"
        self.ent_empresa["state"] = "disabled"
        self.ent_direccion["state"] = "disabled"       
        self.ent_phone["state"] = "disabled"

    def open_proveedor_menu(self):
            customer_window = tk.Tk()
            customer_window.title("Menú de Proveedor")
            customer_window.geometry("600x400")
            customer_app = ProveedorApp(customer_window, self.db, self.user_id, self.username)
            
            customer_window.mainloop()

class ArticuloApp:
    def __init__(self, root, db, user_id, username):
        self.root = root
        self.root.title("Articulos")
        self.db = db
        self.current_customer_id = None
        self.user_id = user_id
        self.username = username  

        self.root.configure(bg="#ffffff")
        self.font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        
        self.lbl_search_id = tk.Label(root, text="Buscar ID:", font=self.font, bg="#ffffff")
        self.lbl_search_id.place(x=20, y=2)  
        self.ent_search_id = tk.Entry(root, font=self.font)
        self.ent_search_id.place(x=180, y=2)
        
        self.btn_search = tk.Button(
            root, 
            text="Buscar", 
            command=self.search_articulo, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_search.place(x=450, y=2)

        self.lbl_articulo_id = tk.Label(root, text="Articulo ID:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_articulo_id.place(x=20, y=40)  
        self.ent_articulo_id = tk.Entry(root, font=self.font, state="readonly")
        self.ent_articulo_id.place(x=180, y=40) 

        #name ahora sera descripcion
        self.lbl_descripcion = tk.Label(root, text="Descripcion:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_descripcion.place(x=20, y=80) 
        self.ent_descripcion = tk.Entry(root, font=self.font, state="disabled")
        self.ent_descripcion.place(x=180, y=80)  

        #phone ahora sera precio unitario
        self.lbl_preciouni = tk.Label(root, text="Precio unitario:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_preciouni.place(x=20, y=120)  
        self.ent_preciouni = tk.Entry(root, font=self.font, state="disabled")
        self.ent_preciouni.place(x=180, y=120)
        
        self.lbl_precioven = tk.Label(root, text="Precio venta:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_precioven.place(x=20, y=160)  
        self.ent_precioven = tk.Entry(root, font=self.font, state="disabled")
        self.ent_precioven.place(x=180, y=160)
        
        #username como nombre del proveedor
        self.lbl_username = tk.Label(root, text="Seleccione un proveedor", font=self.font, bg="#ffffff")
        self.lbl_username.place(x=20, y=200)  
        self.combo_username = ttk.Combobox(root, font=self.font)
        self.combo_username.place(x=280, y=200)
        
        self.load_proveedor_data()

        #como ID del proveedor
        #self.lbl_user_id = tk.Label(root, text="ID proveedor:", font=self.font, bg="#ffffff", fg="#03012C")
        #self.lbl_user_id.place(x=20, y=240)  
        #self.ent_user_id = tk.Entry(root, font=self.font, state="normal")
        #self.ent_user_id.place(x=180, y=240)  
        #self.ent_user_id.insert(0, self.user_id)
        
        #rfc ahora sera descuento
        self.lbl_descuento = tk.Label(root, text="Descuento:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_descuento.place(x=20, y=240)  
        self.ent_descuento = tk.Entry(root, font=self.font, state="normal")
        self.ent_descuento.place(x=180, y=240)
        
        #NUEVO
        self.lbl_puntos = tk.Label(root, text="Puntos:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_puntos.place(x=20, y=280)  
        self.ent_puntos= tk.Entry(root, font=self.font, state="normal")
        self.ent_puntos.place(x=180, y=280)
        
        self.lbl_stock = tk.Label(root, text="Stock:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_stock.place(x=20, y=320)  
        self.ent_stock = tk.Entry(root, font=self.font)
        self.ent_stock.place(x=180, y=320)    

        self.btn_insert = tk.Button(
            root, 
            text="Guardar", 
            command=self.insert, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_insert.place(x=20, y=360)  

        self.btn_cancel = tk.Button(
            root, 
            text="Cancelar", 
            command=self.cancel, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_cancel.place(x=140, y=360) 

        self.btn_new = tk.Button(
            root, 
            text="Nuevo", 
            command=self.new_articulo, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_new.place(x=260, y=360)    

        self.btn_edit = tk.Button(
            root, 
            text="Editar", 
            command=self.edit, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_edit.place(x=360, y=360)  

        self.btn_delete = tk.Button(
            root, 
            text="Eliminar", 
            command=self.delete, 
            font=self.button_font, 
            bg="#33658A", 
            fg="white", 
            state="disabled"
        )
        self.btn_delete.place(x=460, y=360)  

        self.btn_limpiar = tk.Button(
                    root, 
                    text="Limpiar", 
                    command=self.clear_all_entries, 
                    font=self.button_font, 
                    bg="#86BBD8", 
                    fg="white"
                )
        self.btn_limpiar.place(x=450, y=300)

        self.setup_buttons()  
    
    def validate_name(self, name):
        """Valida que el nombre solo contenga letras y espacios"""
        if not name.strip():  
            return False
        return name.replace(" ", "").isalpha()  
    
    def setup_buttons(self):
        if self.username in ["Secre", "Mecanico"]:
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")

        self.btn_new.config(state="normal")
        self.btn_search.config(state="normal")
        self.btn_insert.config(state="normal")
        self.btn_cancel.config(state="normal")

    def new_articulo(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])

        self.current_articulo_id = self.db.get_next_articulo_id()
        self.ent_articulo_id.insert(0, self.current_articulo_id)
        self.ent_articulo_id["state"] = "readonly"
        self.ent_articulo_id["state"] = "disabled"

    def insert(self):
        if not self.validate_fields():
            return

        articulo = {
            'articulo_id': self.ent_articulo_id.get(),
            'descripcion': self.ent_descripcion.get(),
            'precio_unitario': self.ent_preciouni.get(),
            'precio_venta': self.ent_precioven.get(),            
            'puntos': self.ent_puntos.get(),
            'descuento': self.ent_descuento.get()
        }
        
        if not re.match(r'^\d+$', articulo['precio_unitario']):
            messagebox.showerror("Error", "El precio unitario debe ser un número positivo.")
            return
        
        if not re.match(r'^\d+$', articulo['precio_venta']):
            messagebox.showerror("Error", "El precio de venta debe ser un número positivo.")
            return
        
        if not re.match(r'^\d+$', articulo['puntos']):
            messagebox.showerror("Error", "Los puntos deben de ser un número positivo.")
            return
        
        existing_articulo = self.db.search_articulo_by_id(articulo['articulo_id'])
        
        if not existing_articulo:
            self.db.save_articulo(articulo)
            messagebox.showinfo("Éxito", "Articulo insertado con éxito.")
            
        articuloDetail = {            
            'proveedor_id':self.combo_username.get(),
            'articulo_id':self.ent_articulo_id.get(),
            'precio':self.ent_precioven.get(),
            'existencia':self.ent_stock.get()
        }
        
        self.db.add_articulo_detalle(articuloDetail)
        messagebox.showinfo("Éxito", "Articulo y detalle insertados con éxito.")
    
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search_articulo(self):
        articulo_id_or_name = self.ent_search_id.get()
        if articulo_id_or_name.isdigit():  
            articulo = self.db.search_articulo_by_id(articulo_id_or_name)
        else:  
            articulo = self.db.search_articulo_by_name(articulo_id_or_name)
        
        if articulo:
            self.ent_articulo_id.delete(0, END)
            self.ent_descripcion.delete(0, END)
            self.ent_preciouni.delete(0, END)
            self.ent_precioven.delete(0, END)
            self.ent_descuento.delete(0, END)
            self.ent_puntos.delete(0, END)
            
            self.ent_articulo_id["state"] = "normal"
            self.ent_descripcion["state"] = "normal"    
            self.ent_preciouni["state"] = "normal"
            self.ent_precioven["state"] = "normal"
            self.ent_descuento["state"] = "normal"
            self.ent_puntos["state"] = "normal"

            self.ent_articulo_id.insert(0, articulo[0])
            self.ent_descripcion.insert(0, articulo[1])
            self.ent_preciouni.insert(0, articulo[2])
            self.ent_precioven.insert(0, articulo[3])
            self.ent_descuento.insert(0, articulo[4])
            self.ent_puntos.insert(0, articulo[5])

            details = self.db.get_articulo_details(articulo[0])
            proveedor_id = self.db.search_proveedor_by_id(details[0])
            
            self.combo_username.insert(0, proveedor_id[1])
            self.ent_stock.insert(0, details[1])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])  
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            self.ent_articulo_id["state"] = "readonly"
            
            self.btn_edit["state"] = "normal"
        else:
            messagebox.showinfo("Error", "Articulo no encontrado.")

    def edit(self):
        if not self.validate_fields():
            return
        
        articulo = {
            'articulo_id': self.ent_articulo_id.get(),
            'descripcion': self.ent_descripcion.get(),
            'precio_unitario': self.ent_preciouni.get(),
            'precio_venta': self.ent_precioven.get(),
            'descuento': self.ent_descuento.get(),
            'puntos':self.ent_puntos.get()
            
        }
        
        articuloDetail = {            
            'proveedor_id':self.combo_username.get(),
            'articulo_id':self.ent_articulo_id.get(),
            'precio':self.ent_precioven.get(),
            'existencia':self.ent_stock.get()
        }
        
        self.db.update_articulo_in_articulos(articulo, articuloDetail)
        messagebox.showinfo("Éxito", "Articulo actualizado con éxito.")
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()

    def delete(self):
        if not self.ent_articulo_id.get():
            messagebox.showerror("Error", "Debe ingresar un ID de articulo.")
            return
        articulo_id = self.ent_articulo_id.get()
        self.db.delete_articulo(articulo_id)
        messagebox.showinfo("Éxito", "Articulo eliminado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_articulo_id.get()
            or not self.ent_descripcion.get()
            or not self.ent_preciouni.get()
            or not self.ent_precioven.get()
            #or not self.ent_descuento.get()
            or not self.ent_puntos.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        if (
            not self.ent_preciouni.get().isdigit()
            or not self.ent_precioven.get().isdigit()
            #or not self.ent_descuento.get().isdigit()
            or not self.ent_puntos.get().isdigit()
        ):
            messagebox.showerror("Error, ingrese solo numeros")
            return False
        
        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_articulo_id.delete(0, END)
        self.ent_descripcion.delete(0, END)
        self.ent_preciouni.delete(0, END)
        self.ent_precioven.delete(0, END)
        #self.ent_user_id.delete(0, END)
        self.combo_username.delete(0, END)
        self.ent_descuento.delete(0, END)
        self.ent_puntos.delete(0, END)
        self.ent_stock.delete(0, END)
        #self.ent_user_id.delete(0, END)

    def clear_all_entries(self):
        self.ent_articulo_id["state"] = "normal"    
        self.ent_articulo_id.delete(0, END)
        self.ent_articulo_id["state"] = "disabled"
        self.ent_descripcion.delete(0, END)
        self.ent_preciouni.delete(0, END)
        self.ent_precioven.delete(0, END)
        #self.ent_user_id.delete(0, END)
        self.combo_username.delete(0, END)
        self.ent_descuento.delete(0, END)
        self.ent_puntos.delete(0, END)
        self.ent_stock.delete(0, END)

    def enable_entries(self):
        self.ent_articulo_id["state"] = "normal"
        self.ent_descripcion["state"] = "normal"
        self.ent_preciouni["state"] = "normal"
        self.ent_precioven["state"] = "normal"
        #self.ent_user_id["state"] = "normal"
        self.ent_descuento["state"] = "normal"
        self.ent_puntos["state"] = "normal"
        self.ent_stock["state"] = "normal"

    def disable_entries(self):
        self.ent_articulo_id["state"] = "disabled"
        self.ent_descripcion["state"] = "disabled"
        self.ent_preciouni["state"] = "disabled"
        self.ent_precioven["state"] = "disabled"
        #self.ent_user_id["state"] = "disabled"
        self.ent_descuento["state"] = "disabled"
        self.ent_puntos["state"] = "disabled"
        self.ent_stock["state"] = "disabled"

    def open_articulo_menu(self):
            articulo_window = tk.Tk()
            articulo_window.title("Menú de Articulos")
            articulo_window.geometry("600x600")
            articulo_app = ArticuloApp(articulo_window, self.db, self.user_id, self.username)
            
            articulo_window.mainloop()
    
    def load_proveedor_data(self):
        proveedores = self.db.get_all_proveedores()
        proveedores_names = [proveedor[1] for proveedor in proveedores]
        self.combo_username['values'] = proveedores_names
        
class VentaApp:
    def __init__(self, root, db, user_id, username):
        self.root = root
        self.root.title("Ventas")
        self.db = db
        self.current_customer_id = None
        self.user_id = user_id
        self.username = username
        self.selected_articulos = []
        self.actual_stock = None
        self.cantidad_actual = None
        self.precios = []
        
        print(self.username)  

        self.root.configure(bg="#ffffff")
        self.font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        
        self.lbl_search_id = tk.Label(root, text="Buscar venta (ID):", font=self.font, bg="#ffffff")
        self.lbl_search_id.place(x=20, y=2)  
        self.ent_search_id = tk.Entry(root, font=self.font)
        self.ent_search_id.place(x=200, y=2)
        
        self.btn_search = tk.Button(
            root, 
            text="Buscar", 
            command=self.search_venta, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_search.place(x=450, y=2)

        self.lbl_venta_id = tk.Label(root, text="Venta ID:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_venta_id.place(x=20, y=40)  
        self.ent_venta_id = tk.Entry(root, font=self.font, state="readonly")
        self.ent_venta_id.place(x=180, y=40) 

        self.lbl_cliente = tk.Label(root, text="Cliente:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_cliente.place(x=20, y=80) 
        self.combo_cliente = ttk.Combobox(root, font=self.font)
        self.combo_cliente.place(x=180, y=80) 

        self.lbl_usuario = tk.Label(root, text="Usuario:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_usuario.place(x=20, y=120)  
        self.ent_usuario = tk.Entry(root, font=self.font, state="normal")
        self.ent_usuario.place(x=180, y=120)
        self.ent_usuario.insert(0, self.username)
        
        '''self.lbl_proveedor = tk.Label(root, text="Proveedor:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_proveedor.place(x=20, y=160) 
        self.combo_proveedor = ttk.Combobox(root, font=self.font)
        self.combo_proveedor.place(x=180, y=160)
        self.combo_proveedor.bind("<<ComboboxSelected>>", lambda e: self.load_articulo_data())'''
               
        self.lbl_articulo= tk.Label(root, text="Articulo:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_articulo.place(x=20, y=200)  
        self.combo_articulo = ttk.Combobox(root, font=self.font)
        self.combo_articulo.place(x=180, y=200) 
        
        self.lbl_cantidad = tk.Label(root, text="Cantidad", font=self.font, bg="#ffffff")
        self.lbl_cantidad.place(x=20, y=240)  
        self.ent_cantidad = tk.Entry(root, font=self.font, state="disabled")
        self.ent_cantidad.place(x=180, y=240)
        
        self.lbl_fecha = tk.Label(root, text="Fecha", font=self.font, bg="#ffffff")
        self.lbl_fecha.place(x=20, y=280)  
        self.ent_fecha = tk.Entry(root, font=self.font, state="disabled")
        self.ent_fecha.place(x=180, y=280)
        
        self.load_cliente_data()
        #self.load_proveedor_data()
        self.load_articulo_data()

        #como ID del proveedor
        #self.lbl_user_id = tk.Label(root, text="ID proveedor:", font=self.font, bg="#ffffff", fg="#03012C")
        #self.lbl_user_id.place(x=20, y=240)  
        #self.ent_user_id = tk.Entry(root, font=self.font, state="normal")
        #self.ent_user_id.place(x=180, y=240)  
        #self.ent_user_id.insert(0, self.user_id)
        
        self.lbl_subtotal = tk.Label(root, text="Subtotal:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_subtotal.place(x=20, y=320)  
        self.ent_subtotal = tk.Entry(root, font=self.font, state="disabled")
        self.ent_subtotal.place(x=180, y=320)
        
        self.lbl_total = tk.Label(root, text="Total:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_total.place(x=20, y=360)  
        self.ent_total = tk.Entry(root, font=self.font, state="disabled")
        self.ent_total.place(x=180, y=360)
        
        self.lbl_iva = tk.Label(root, text="IVA:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_iva.place(x=20, y=400)  
        self.ent_iva= tk.Entry(root, font=self.font, state="disabled")
        self.ent_iva.place(x=180, y=400)
        
           

        self.btn_insert = tk.Button(
            root, 
            text="Guardar", 
            command=self.insert, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_insert.place(x=20, y=440)  

        self.btn_cancel = tk.Button(
            root, 
            text="Cancelar", 
            command=self.cancel, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_cancel.place(x=140, y=440) 

        self.btn_new = tk.Button(
            root, 
            text="Nuevo", 
            command=self.new_venta, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_new.place(x=260, y=440)    

        self.btn_edit = tk.Button(
            root, 
            text="Editar", 
            command=self.edit, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_edit.place(x=360, y=440)  

        self.btn_delete = tk.Button(
            root, 
            text="Eliminar", 
            command=self.delete, 
            font=self.button_font, 
            bg="#33658A", 
            fg="white", 
            state="disabled"
        )
        self.btn_delete.place(x=460, y=440)  

        self.lbl_carrito_articulos=tk.Listbox(root, font=self.font, width=45)
        self.lbl_carrito_articulos.place(x=20, y=520)
        self.btn_agregar_articulo = tk.Button(
            root, 
            text="Agregar", 
            command=self.insert, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_agregar_articulo.place(x=20, y=800)
        
        self.btn_quitar_articulo = tk.Button(
            root, 
            text="Quitar", 
            command=self.quitar_detalle, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_quitar_articulo.place(x=120, y=800)
        
        self.btn_limpiar = tk.Button(
                    root, 
                    text="Limpiar", 
                    command=self.clear_all_entries, 
                    font=self.button_font, 
                    bg="#86BBD8", 
                    fg="white"
                )
        self.btn_limpiar.place(x=450, y=350) 
        
        self.setup_buttons()  
    
    def validate_name(self, name):
        """Valida que el nombre solo contenga letras y espacios"""
        if not name.strip():  
            return False
        return name.replace(" ", "").isalpha()  
    
    def setup_buttons(self):
        print("user perfil", self.username)
        user = self.db.search_user_by_username(self.username)
        print("user", user[3])
        if user[3] == "cajero":
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")

        self.btn_new.config(state="normal")
        self.btn_search.config(state="normal")
        self.btn_insert.config(state="normal")
        self.btn_cancel.config(state="normal")

    def new_venta(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])
        
        self.current_venta_id = self.db.get_next_venta_id()
        self.ent_venta_id.insert(0, self.current_venta_id)
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.ent_fecha.delete(0, END)
        self.ent_fecha.insert(0, today)
        self.ent_fecha.config(state="disabled")

    def insert_detalle(self):
        articulo_nombre = self.combo_articulo.get()
        articulo = self.db.search_articulo_by_name(articulo_nombre)
        precio_venta = int(articulo[3])
        cliente_name = self.combo_cliente.get()
        cantidad = int(self.ent_cantidad.get())
        cliente_existente = self.db.search_cliente_by_venta(cliente_name)
        
        if cliente_existente:
            puntos_cliente = cliente_existente[5]
            if puntos_cliente >= 100:
                descuento = precio_venta * (articulo[5] / 100)
                subtotal_articulo = precio_venta - descuento
            
        if not articulo:
            messagebox.showerror("Error", "Articulo no encontrado.")
            return
        
        subtotal_articulo = precio_venta * cantidad
        self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
        
        puntos_articulo = self.db.search_articulo_by_id(self.combo_articulo.get())
        
        ventaDetail = {            
            'folio_venta':self.ent_venta_id.get(),
            'articulo_id':self.combo_articulo.get(),
            'cantidad':self.ent_cantidad.get(),
            'cliente_id':self.combo_cliente.get(),
            'puntos': puntos_articulo[5] * int(self.ent_cantidad.get())
        }
        
        ventaResponse = self.db.add_venta_detalle(ventaDetail)
        self.selected_articulos.append((ventaResponse['folio_venta'], ventaResponse['articulo_name'], ventaResponse['cantidad'], ventaResponse['cliente_name'], ventaResponse['puntos']))
        self.lbl_carrito_articulos.insert(tk.END, f"{"Folio:", ventaResponse['folio_venta']} {"Articulo:", ventaResponse['articulo_name']} {"Cantidad:", ventaResponse['cantidad']} {"Cliente:", ventaResponse['cliente_name']} {"Puntos:", ventaResponse['puntos']}")
        
        self.calculate_total()

    def calculate_total(self):
        subtotal_total = sum(item['subtotal'] for item in self.precios)
        iva = subtotal_total * 0.16
        total = subtotal_total + iva
        
        print(f"Subtotal: {subtotal_total}, IVA: {iva}, Total: {total}")
        
        venta_id = self.ent_venta_id.get()
        
        self.ent_subtotal.config(state="normal")
        self.ent_total.config(state="normal")
        self.ent_iva.config(state="normal")

        self.ent_subtotal.delete(0, tk.END)
        self.ent_subtotal.insert(0, f"{subtotal_total:.2f}")

        self.ent_iva.delete(0, tk.END)
        self.ent_iva.insert(0, f"{iva:.2f}")

        self.ent_total.delete(0, tk.END)
        self.ent_total.insert(0, f"{total:.2f}")
        
        self.db.update_total_in_venta(venta_id, total)

        self.ent_subtotal.config(state="disabled")
        self.ent_iva.config(state="disabled")
        self.ent_total.config(state="disabled")

    def quitar_detalle(self):
        if not self.selected_articulos:
            messagebox.showwarning("No hay articulos para quitar.")
            return
        
        try:
            last_detail = self.selected_articulos[-1]
            print("Ultimo detalle:", last_detail)
            #articulo_id = self.db.search_articulo_by_name(last_detail[2])
            #print("Articulo ID:", articulo_id[0])
            
            total_existente = self.db.search_compra_detalle_by_id(self.ent_compra_id.get(), last_detail[2])
            print("Total existente:", total_existente[3])
            
            success = self.db.delete_compra_detalle(
                last_detail[0],  # folio_compra
                last_detail[2],  # articulo_id
                last_detail[3],  # cantidad
            )
            
            precio_unitario = self.db.search_articulo_by_id(last_detail[2])
            subtotal_total = precio_unitario[3] * last_detail[3]
            iva = subtotal_total * 0.16
            total = subtotal_total + iva
            
            total_actualizado = total_existente[3] - total
            print("Total actualizado:", total_actualizado)
            
            self.db.update_total_in_compra(self.ent_compra_id.get(), total_actualizado)
            
            self.ent_total.config(state="normal")
            self.ent_total.delete(0, tk.END)
            self.ent_total.insert(0, f"{total_actualizado:.2f}")
            self.ent_total.config(state="disabled")             
            
            if success:
                self.selected_articulos.pop()
                self.lbl_carrito_articulos.delete(tk.END)
                
                self.db.update_articulo_stock(last_detail[2], -last_detail[3])
                self.db.update_articulo_venta_stock_delete(last_detail[2], last_detail[3])
                              
                messagebox.showinfo("Éxito", "Detalle eliminado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el detalle de la BD")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
            print(f"Error al eliminar detalle: {e}")
    
    def insert(self):
        if not self.validate_fields():
            return
        
        if not re.match(r'^\d+$', self.ent_cantidad.get()):
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return
        
        

        articulo_nombre = self.combo_articulo.get()
        articulo = self.db.search_articulo_by_name(articulo_nombre)
        precio_venta = int(articulo[3])
        cliente_name = self.combo_cliente.get()
        cantidad = int(self.ent_cantidad.get())
        cliente_existente = self.db.search_cliente_by_venta(cliente_name)      
         
        articulo_id = articulo[0]
        stock_actual = self.db.search_articulo_venta_stock_by_id(articulo_id)
        stock_disponible = stock_actual[0]

        #cantidad = int(self.ent_cantidad.get())

        if stock_disponible < cantidad:
            messagebox.showerror("Stock insuficiente", "No hay suficiente stock para esta venta.")
            return
        
        total_existente = self.db.search_venta_detalle_by_id(self.ent_venta_id.get(), articulo[0])
                           
        if total_existente:
            if cliente_existente:
                puntos_cliente = cliente_existente[5]
                if puntos_cliente >= 100:
                        descuento = precio_venta * (articulo[5] / 100)
                        #subtotal_articulo = precio_venta - descuento 
                        cantidad_existente = total_existente[3]
                        cantidad = int(self.ent_cantidad.get())
                        diferencia = cantidad - cantidad_existente
                        subtotal_articulo = (precio_venta * diferencia) - descuento
                        self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
                    
                        self.calculate_total()
                else:
                    cantidad_existente = total_existente[3]
                    cantidad = int(self.ent_cantidad.get())
                    diferencia = cantidad - cantidad_existente
                    subtotal_articulo = precio_venta * diferencia
                    self.precios.append({'subtotal': subtotal_articulo})
                    
                    self.calculate_total()
            else:                
                cantidad_existente = total_existente[3]
                cantidad = int(self.ent_cantidad.get())
                diferencia = cantidad - cantidad_existente
                subtotal_articulo = precio_venta * diferencia
                self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
            
                self.calculate_total()
        else:
            
            if cliente_existente:
                puntos_cliente = cliente_existente[5]
                if puntos_cliente >= 100:
                    descuento = precio_venta * (articulo[5] / 100)
                    cantidad = int(self.ent_cantidad.get())
                    subtotal_articulo = (precio_venta * cantidad) - descuento
                    self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
                
                    self.calculate_total()
                else:
                    cantidad = int(self.ent_cantidad.get())
                    subtotal_articulo = precio_venta * cantidad
                    self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
                    
                    self.calculate_total()
            else:        
                cantidad = int(self.ent_cantidad.get())
                subtotal_articulo = precio_venta * cantidad
                self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
            
                self.calculate_total()

        venta = {
            'venta_id': self.ent_venta_id.get(),
            'cliente': self.combo_cliente.get(),
            'usuario': self.ent_usuario.get(),
            'articulo': self.combo_articulo.get(),            
            'cantidad': self.ent_cantidad.get(),
            'fecha': self.ent_fecha.get(),
            'total': self.ent_total.get()
        }
        
        existing_venta = self.db.search_venta_by_id(venta['venta_id'])
  
        if not existing_venta:
            self.db.save_venta(venta)
            messagebox.showinfo("Éxito", "Venta realizada con éxito.")
    
        if not articulo:
            messagebox.showerror("Error", "Articulo no encontrado.")
            return

        
        
        articulo_id = self.db.search_articulo_by_name(articulo_nombre)
        puntos_articulo = self.db.search_articulo_by_id(articulo_id[0])
        cliente_id = self.db.search_customer_by_name(cliente_name)
        
        ventaDetail = {            
            'folio_venta':self.ent_venta_id.get(),
            'articulo_id':articulo_id[0],
            'cantidad':self.ent_cantidad.get(),
            'cliente_id':cliente_id[0],
            'puntos': puntos_articulo[5] * int(self.ent_cantidad.get())
        }
        
        ventaDetail_existente = self.db.search_venta_detalle_by_id(ventaDetail['folio_venta'], articulo_id[0])
        if ventaDetail_existente:
            self.db.update_venta_detalle(ventaDetail["folio_venta"],ventaDetail["articulo_id"], ventaDetail['cantidad'], ventaDetail['cliente_id'], ventaDetail['puntos'])
        else:
            ventaResponse = self.db.add_venta_detalle(ventaDetail)
            self.selected_articulos.append((ventaResponse['folio_venta'], ventaResponse['articulo_name'], ventaResponse['cantidad'], ventaResponse['cliente_name'], ventaResponse['puntos']))
            self.lbl_carrito_articulos.insert(tk.END, f"{"Folio detalle:", ventaResponse['folio_venta']} {"Folio venta:", venta['venta_id']} {"Articulo:", ventaDetail['articulo_id']} {"Cantidad:", ventaResponse['cantidad']} {"Cliente:", ventaDetail['cliente_id']} {"Puntos:", ventaResponse['puntos']}")
        
        articulo_carrito = self.db.get_venta_detalle(venta['venta_id'])
        
        if not articulo_carrito:
            messagebox.showerror("Error", "No hay articulos en el carrito.")
            return
        
        total_puntos = int(0)
        puntos_articulo = self.db.get_venta_detalle(venta['venta_id'])
        total_puntos = sum(punto[5] for punto in puntos_articulo)
            
        self.db.update_cliente_puntos(venta['cliente'], total_puntos)
        #self.db.add_venta_detalle(ventaDetail)
    
        #self.clear_entries()
        #self.disable_entries()
        #self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

    def cancel(self):
        venta_id = self.ent_venta_id.get()
        saved_venta = self.db.search_venta_by_id(venta_id)
        
        if not venta_id:
            messagebox.showerror("Error", "Debe ingresar un ID de venta.")
            return
            
        if saved_venta:
            detalles_venta = self.db.get_venta_detalle(venta_id)  

            if detalles_venta:
                for detalle in detalles_venta:
                    articulo_id = detalle[2]  
                    cantidad_vendida = detalle[3]
                    print("Cantidad vendida", cantidad_vendida) 
                    self.db.update_articulo_venta_stock_delete(articulo_id, -cantidad_vendida)
                    
            self.db.delete_venta(saved_venta[0])
            self.db.delete_all_detalles_venta(venta_id)
        
        messagebox.showinfo("Éxito", "Venta cancelada con éxito.")
        
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search_venta(self):
        venta_id = self.ent_search_id.get()
        self.clear_folio_entry()
        
        venta = self.db.search_venta_by_id(venta_id)
        if not venta:
            messagebox.showinfo("Error", "Venta no encontrada.")
            return
        cliente_id = self.db.get_venta_detalle(venta[0])
        print("DETALLE DE VENTA:", cliente_id)
        print("CLIENTE ID:", cliente_id[0][4])
        cliente_name = self.db.search_customer_by_id(cliente_id[0][4])  
        user_name = self.db.search_user_by_id(venta[1])
        
        if venta:
            self.current_venta_id = venta[0]  
            
            self.ent_venta_id["state"] = "normal"
            self.combo_cliente["state"] = "normal"
            self.ent_usuario["state"] = "normal"
            self.combo_articulo["state"] = "normal"
            #self.combo_proveedor["state"] = "normal"
            #self.ent_user_id["state"] = "normal"
            self.ent_fecha["state"] = "normal"
            #self.ent_cantidad["state"] = "normal"
            #self.ent_subtotal["state"] = "disabled"
            self.ent_total["state"] = "normal"
            #self.ent_iva['state'] = "disabled"

            self.ent_venta_id.delete(0, END)
            self.ent_usuario.delete(0, END)
            self.combo_cliente.delete(0, END)
            #self.combo_proveedor.delete(0, END) 
            self.combo_articulo.delete(0, END)
            self.ent_fecha.delete(0, END)
            self.ent_cantidad.delete(0, END)
            self.ent_subtotal.delete(0, END)
            self.ent_total.delete(0, END)
            self.ent_iva.delete(0, END)
            
            self.ent_venta_id.insert(0, venta[0])  # venta_id
            self.ent_usuario.insert(0, user_name[1])   # usuario
            self.combo_cliente.insert(0, cliente_name[2])  # cliente
            self.ent_fecha.insert(0, venta[2]) # fecha
            self.ent_total.insert(0, venta[3]) # total
        
            self.lbl_carrito_articulos.delete(0, END)

            details = self.db.get_venta_detalle(venta[0]) 
            for detail in details:
                print("Detalle obtenido:", detail) 
                self.selected_articulos.append(detail)  
                self.lbl_carrito_articulos.insert(tk.END, f"{"Folio detalle:", detail[0]} {"Compra ID:", detail[1]} {"Articulo ID:", detail[2]} {"Cantidad:", detail[3]} {"Cliente ID:", detail[4]} {"Puntos:", detail[5]}")
            
            print("Detalles seleccionados:", self.lbl_carrito_articulos.get(0, tk.END))
            self.lbl_carrito_articulos.bind('<<ListboxSelect>>', self.on_listbox_select)
            
            print("user perfil", self.username)
            user = self.db.search_user_by_username(self.username)
            print("user", user[3])
            if user[3] == "cajero":
                self.btn_edit.config(state="disabled")
                self.btn_delete.config(state="disabled")
                self.btn_cancel.config(state="disabled")
            else:
                self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])

            self.disable_buttons([ self.btn_insert])
            self.ent_venta_id.config(state="normal")
            
            self.enable_entries()
            self.ent_venta_id.config(state="readonly")
        else:
            messagebox.showinfo("Error", "Venta no encontrada.")
    
    def on_listbox_select(self, event):
        self.combo_articulo.delete(0, END)
        #self.combo_proveedor.delete(0, END)
        self.ent_cantidad.delete(0, END)
        
        #CHECAR QUE AQUI EN VENTAS LO INDICES SEAN LOS CORRECTOS
        seleccion_detalle = self.lbl_carrito_articulos.curselection()
        print("Seleccionado:", seleccion_detalle)
        if seleccion_detalle:
            print("Seleccionado:", seleccion_detalle)
            index = seleccion_detalle[0]
            print(index)  
            detail = self.selected_articulos[index] 
            print("Detalle  folio venta:", detail[1])
            articulo_id = detail[2]  
            print("Articulo_id: ",articulo_id)
            proveedor = self.db.get_articulo_details(articulo_id)
            det_id = self.db.get_venta_detalle(detail[1])
            print(det_id[0][0])
            self.current_det_id = det_id[0][0]
            proveedor_data = self.db.search_proveedor_by_id(proveedor[0])
            #self.combo_proveedor.insert(0, proveedor_data[1])  
            articulo_name = self.db.search_articulo_by_id(articulo_id)
            self.combo_articulo.insert(0, articulo_name[1])  
            self.ent_cantidad.insert(0, detail[3])
            
            venta_id = self.ent_venta_id.get()
            cantidad = detail[3]
            self.cantidad_actual = cantidad
            
            stock = self.db.search_venta_detalle_by_id(venta_id, articulo_id)
            print("Stock encontrado:", stock)
            self.actual_stock = stock[3]
            detail = None 


    def edit(self):
        if not self.validate_fields():
            return
               
        articulo_nombre = self.combo_articulo.get()
        articulo = self.db.search_articulo_by_name(articulo_nombre)
        cliente_name = self.combo_cliente.get()
        cliente_id = self.db.search_customer_by_name(cliente_name)
        venta_id = self.ent_venta_id.get()
        precio_venta = int(articulo[3])
        
        articulo_id = articulo[0]
        stock_actual = self.db.search_articulo_venta_stock_by_id(articulo_id)
        stock_disponible = stock_actual[0]
       
        cantidad_actual = int(self.ent_cantidad.get())
        
        if stock_disponible < cantidad_actual:
            messagebox.showerror("Stock insuficiente", "No hay suficiente stock para esta venta.")
            return
        
        print("Cantidad actual:", cantidad_actual)
        detalle_encontrado = self.db.get_venta_detalle_by_articulo(articulo[0])
        print("Detalle encontrado:", detalle_encontrado)
        cantidad_en_bd = detalle_encontrado[3]
        print("Cantidad en bd:", cantidad_en_bd)
        diferencia_cantidades = 0
        
        if cantidad_actual > cantidad_en_bd:
            diferencia_cantidades = cantidad_actual - cantidad_en_bd
            #self.db.update_articulo_stock(articulo[0], -diferencia_cantidades)
            print("Diferencia de cantidades si cantidad actual es mayor:", diferencia_cantidades)
            #self.db.update_articulo_stock(articulo[0], diferencia_cantidades)
        #diferencia_cantidades = cantidad_actual - cantidad_en_bd
               
        total_existente = self.db.search_venta_by_id(self.ent_venta_id.get())
        print("Total devuelto de compras:", total_existente)
        if total_existente:
            total = total_existente[3]
            print("Total existente:", total)            
            if cantidad_actual < cantidad_en_bd:
                diferencia_cantidades = cantidad_en_bd - cantidad_actual
                print("Diferencia de cantidades si cantidad actual es menor:", diferencia_cantidades)
                subtotal_articulo = total - (precio_venta * (-1 * diferencia_cantidades))
                print("Subtotal articulo:", subtotal_articulo)
                self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
                  
                self.calculate_total() 
            else:            
                subtotal_articulo = total + (precio_venta * diferencia_cantidades)
                self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
                print("Subtotal articulo en else:", subtotal_articulo)  
                self.calculate_total()
        else:
            subtotal_articulo = precio_venta * cantidad_actual
            self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO            
            self.calculate_total()
        
        venta = {
            'folio_venta': self.ent_venta_id.get(),
            'usuario': self.ent_usuario.get(),
            'articulo': self.combo_articulo.get(),            
            'cantidad': self.ent_cantidad.get(),
            'fecha': self.ent_fecha.get(),
            'total': self.ent_total.get()
        }
        
        ventaDetail = {
            'det_id_venta': self.current_det_id,
            'venta_id': self.ent_venta_id.get(),
            'articulo': self.combo_articulo.get(),
            'cantidad': self.ent_cantidad.get(),
            'cliente': cliente_id[0],
            'puntos': articulo[5] * int(self.ent_cantidad.get())    
        }
        
        articulo_id = self.db.search_articulo_by_name(ventaDetail["articulo"])
        ventaDetail_existente = self.db.search_venta_detalle_by_id(ventaDetail["venta_id"], articulo_id[0])
        if ventaDetail_existente:
            self.db.update_venta_detalle(ventaDetail["venta_id"], articulo_id[0], ventaDetail['cantidad'], ventaDetail['cliente'], ventaDetail['puntos'])
        
        self.db.update_venta(venta, ventaDetail, self.actual_stock)
        
        #CHECAR ESTOS EN UN FUTURO POR SI LLEGA A DAR ERROR
        self.precios = []
        self.actual_stock = None
        self.cantidad_actual = None
               
        messagebox.showinfo("Éxito", "Compra actualizada con éxito.")
        self.current_det_id = None
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()

    def delete(self):
        venta_id = self.ent_venta_id.get()
        if not venta_id:
            messagebox.showerror("Error", "Debe ingresar un ID de venta.")
            return

        detalles_venta = self.db.get_venta_detalle(venta_id)  

        if detalles_venta:
            for detalle in detalles_venta:
                articulo_id = detalle[2]  
                cantidad_vendida = detalle[3] 
                self.db.update_articulo_venta_stock_delete(articulo_id, cantidad_vendida)

        self.db.delete_venta(venta_id)
        self.db.delete_all_detalles_venta(venta_id)

        messagebox.showinfo("Éxito", "Venta y sus detalles eliminados con éxito.")
        
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_venta_id.get()
            or not self.combo_cliente.get()
            or not self.ent_usuario.get()
            #or not self.combo_proveedor.get()
            or not self.combo_articulo.get()
            or not self.ent_cantidad.get()
            or not self.ent_fecha.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        if (
            not self.ent_cantidad.get().isdigit()
        ):
            messagebox.showerror("Error, ingrese solo numeros")
            return False
        
        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_venta_id.delete(0, END)
        self.combo_cliente.delete(0, END)
        #self.ent_usuario.delete(0, END)
        self.combo_articulo.delete(0, END)
        #self.ent_user_id.delete(0, END)
        #self.combo_proveedor.delete(0, END)
        self.ent_fecha.delete(0, END)
        self.ent_cantidad.delete(0, END)
        self.ent_subtotal.delete(0, END)
        self.ent_total.delete(0, END)
        self.ent_iva.delete(0, END)
        #self.ent_user_id.delete(0, END)
    
    def clear_all_entries(self):
        self.ent_venta_id["state"] = "normal"
        self.ent_venta_id.delete(0, END)
        self.ent_venta_id["state"] = "readonly"
        self.combo_cliente.delete(0, END)
        self.ent_usuario.delete(0, END)
        self.combo_articulo.delete(0, END)
        #self.ent_user_id.delete(0, END)
        #self.combo_proveedor.delete(0, END)
        self.ent_fecha.delete(0, END)
        self.ent_cantidad.delete(0, END)
        self.ent_subtotal.delete(0, END)
        self.ent_total["state"] = "normal"        
        self.ent_total.delete(0, END)
        self.ent_iva["state"] = "disabled"
        self.ent_iva.delete(0, END)
        #self.ent_user_id.delete(0, END)
        self.lbl_carrito_articulos.delete(0, END)
        self.selected_articulos.clear()

    def enable_entries(self):
        self.ent_venta_id["state"] = "normal"
        self.combo_cliente["state"] = "normal"
        self.ent_usuario["state"] = "normal"
        self.combo_articulo["state"] = "normal"
        #self.ent_user_id["state"] = "normal"
        self.ent_fecha["state"] = "normal"
        self.ent_cantidad["state"] = "normal"
        self.ent_subtotal["state"] = "disabled"
        self.ent_total["state"] = "disabled"
        self.ent_iva['state'] = "disabled"

    def disable_entries(self):
        self.ent_venta_id["state"] = "disabled"
        self.combo_cliente["state"] = "disabled"
        self.ent_usuario["state"] = "disabled"
        self.combo_articulo["state"] = "disabled"
        #self.ent_user_id["state"] = "disabled"
        self.ent_cantidad["state"] = "disabled"
        self.ent_subtotal["state"] = "disabled"
        self.ent_total["state"] = "disabled"
        self.ent_iva['state'] = "disabled"
    
    def clear_folio_entry(self):
        #self.clear_folio_entry()
        self.ent_venta_id.config(state="normal")

        self.ent_venta_id.delete(0, END)
        self.ent_venta_id.config(state="readonly")

    def open_venta_menu(self):
            venta_window = tk.Tk()
            venta_window.title("Menú de Ventas")
            venta_window.geometry("600x600")
            venta_app = VentaApp(venta_window, self.db, self.user_id, self.username)
            
            venta_window.mainloop()
    
    def load_cliente_data(self):
        clientes = self.db.get_all_clientes()
        clientes_names = [cliente[2] for cliente in clientes]
        self.combo_cliente['values'] = clientes_names
    
    '''def load_proveedor_data(self):
        proveedores = self.db.get_all_proveedores()
        proveedores_names = [proveedor[1] for proveedor in proveedores]
        self.combo_proveedor['values'] = proveedores_names'''
        
    def load_articulo_data(self):
        
        #proveedor = self.combo_proveedor.get()
        #print(proveedor)
        articulos = self.db.get_all_articulo()
        articulos_names = [articulo[1] for articulo in articulos]
        self.combo_articulo['values'] = articulos_names

class CompraApp:
    def __init__(self, root, db, user_id, username):
        self.root = root
        self.root.title("Compras")
        self.db = db
        self.current_customer_id = None
        self.user_id = user_id
        self.username = username
        self.current_det_id = None
        self.actual_stock = None
        self.cantidad_actual = None
        self.selected_articulos = []
        self.precios = []
        
        print(self.username)  

        self.root.configure(bg="#ffffff")
        self.font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        
        self.lbl_search_id = tk.Label(root, text="Buscar compra (ID):", font=self.font, bg="#ffffff")
        self.lbl_search_id.place(x=20, y=2)  
        self.ent_search_id = tk.Entry(root, font=self.font)
        self.ent_search_id.place(x=200, y=2)
        
        self.btn_search = tk.Button(
            root, 
            text="Buscar", 
            command=self.search_compra, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_search.place(x=450, y=2)

        self.lbl_compra_id = tk.Label(root, text="Compra ID:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_compra_id.place(x=20, y=40)  
        self.ent_compra_id = tk.Entry(root, font=self.font, state="readonly")
        self.ent_compra_id.place(x=180, y=40)  

        self.lbl_usuario = tk.Label(root, text="Usuario:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_usuario.place(x=20, y=80)  
        self.ent_usuario = tk.Entry(root, font=self.font, state="normal")
        self.ent_usuario.place(x=180, y=80)
        self.ent_usuario.insert(0, self.username)
        
        self.lbl_proveedor = tk.Label(root, text="Proveedor:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_proveedor.place(x=20, y=120) 
        self.combo_proveedor = ttk.Combobox(root, font=self.font)
        self.combo_proveedor.place(x=180, y=120)
        self.combo_proveedor.bind("<<ComboboxSelected>>", lambda e: self.load_articulo_data())
               
        self.lbl_articulo= tk.Label(root, text="Articulo:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_articulo.place(x=20, y=160)  
        self.combo_articulo = ttk.Combobox(root, font=self.font)
        self.combo_articulo.place(x=180, y=160) 
        
        self.lbl_cantidad = tk.Label(root, text="Cantidad", font=self.font, bg="#ffffff")
        self.lbl_cantidad.place(x=20, y=200)  
        self.ent_cantidad = tk.Entry(root, font=self.font, state="disabled")
        self.ent_cantidad.place(x=180, y=200)
        
        self.lbl_fecha = tk.Label(root, text="Fecha", font=self.font, bg="#ffffff")
        self.lbl_fecha.place(x=20, y=240)  
        self.ent_fecha = tk.Entry(root, font=self.font, state="disabled")
        self.ent_fecha.place(x=180, y=240)
        
        self.load_proveedor_data()
        #self.load_articulo_data()

        #como ID del proveedor
        #self.lbl_user_id = tk.Label(root, text="ID proveedor:", font=self.font, bg="#ffffff", fg="#03012C")
        #self.lbl_user_id.place(x=20, y=240)  
        #self.ent_user_id = tk.Entry(root, font=self.font, state="normal")
        #self.ent_user_id.place(x=180, y=240)  
        #self.ent_user_id.insert(0, self.user_id)
        
        self.lbl_subtotal = tk.Label(root, text="Subtotal:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_subtotal.place(x=20, y=320)  
        self.ent_subtotal = tk.Entry(root, font=self.font, state="disabled")
        self.ent_subtotal.place(x=180, y=320)
        
        self.lbl_total = tk.Label(root, text="Total:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_total.place(x=20, y=360)  
        self.ent_total = tk.Entry(root, font=self.font, state="disabled")
        self.ent_total.place(x=180, y=360)
        
        self.lbl_iva = tk.Label(root, text="IVA:", font=self.font, bg="#ffffff", fg="#03012C")
        self.lbl_iva.place(x=20, y=400)  
        self.ent_iva= tk.Entry(root, font=self.font, state="disabled")
        self.ent_iva.place(x=180, y=400)    

        self.btn_insert = tk.Button(
            root, 
            text="Guardar", 
            command=self.insert, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_insert.place(x=20, y=440)  

        self.btn_cancel = tk.Button(
            root, 
            text="Cancelar", 
            command=self.cancel, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_cancel.place(x=140, y=440) 

        self.btn_new = tk.Button(
            root, 
            text="Nuevo", 
            command=self.new_compra, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_new.place(x=260, y=440)    

        self.btn_edit = tk.Button(
            root, 
            text="Editar", 
            command=self.edit, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            state="disabled"
        )
        self.btn_edit.place(x=360, y=440)  

        self.btn_delete = tk.Button(
            root, 
            text="Eliminar", 
            command=self.delete, 
            font=self.button_font, 
            bg="#33658A", 
            fg="white", 
            state="disabled"
        )
        self.btn_delete.place(x=460, y=440)  

        self.lbl_carrito_articulos=tk.Listbox(root, font=self.font, width=45)
        self.lbl_carrito_articulos.place(x=20, y=520)
        self.btn_agregar_articulo = tk.Button(
            root, 
            text="Agregar", 
            command=self.insert, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_agregar_articulo.place(x=20, y=800)
        self.btn_quitar_articulo = tk.Button(
            root, 
            text="Quitar", 
            command=self.quitar_detalle, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white"
        )
        self.btn_quitar_articulo.place(x=120, y=800)

        self.btn_limpiar = tk.Button(
                    root, 
                    text="Limpiar", 
                    command=self.clear_all_entries, 
                    font=self.button_font, 
                    bg="#86BBD8", 
                    fg="white"
                )
        self.btn_limpiar.place(x=450, y=350) 

        self.setup_buttons()  
    
    def validate_name(self, name):
        """Valida que el nombre solo contenga letras y espacios"""
        if not name.strip():  
            return False
        return name.replace(" ", "").isalpha()  
    
    def setup_buttons(self):
        if self.username in ["gerente", "cajero"]:
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")

        self.btn_new.config(state="normal")
        self.btn_search.config(state="normal")
        self.btn_insert.config(state="normal")
        self.btn_cancel.config(state="normal")

    def new_compra(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])
        
        self.current_compra_id = self.db.get_next_compra_id()
        self.ent_compra_id.insert(0, self.current_compra_id)
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.ent_fecha.delete(0, END)
        self.ent_fecha.insert(0, today)
        self.ent_fecha.config(state="disabled")

    def insert_detalle(self):
        articulo_nombre = self.combo_articulo.get()
        articulo = self.db.search_articulo_by_name(articulo_nombre)
        precio_unitario = int(articulo[3])
        cantidad = int(self.ent_cantidad.get())
            
            
        if not articulo:
            messagebox.showerror("Error", "Articulo no encontrado.")
            return
        
        subtotal_articulo = precio_unitario * cantidad
        self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
                
        compraDetail = {            
            'folio_compra':self.ent_compra_id.get(),
            'articulo_id':articulo[0],
            'cantidad':self.ent_cantidad.get()
        }
        
        compraResponse = self.db.add_compra_detalle(compraDetail)
        self.selected_articulos.append((compraResponse['folio_compra'], compraResponse['articulo_name'], compraResponse['cantidad']))
        self.lbl_carrito_articulos.insert(tk.END, f"{"Folio:", compraResponse['folio_venta']} {"Articulo:", compraResponse['articulo_name']} {"Cantidad:", compraResponse['cantidad']}")
        
        self.calculate_total()
         
    def quitar_detalle(self):
        if not self.selected_articulos:
            messagebox.showwarning("No hay articulos para quitar.")
            return
        
        try:
            last_detail = self.selected_articulos[-1]
            print("Ultimo detalle:", last_detail)
            #articulo_id = self.db.search_articulo_by_name(last_detail[2])
            #print("Articulo ID:", articulo_id[0])
            
            total_existente = self.db.search_compra_detalle_by_id(self.ent_compra_id.get(), last_detail[2])
            print("Total existente:", total_existente[3])
            
            success = self.db.delete_compra_detalle(
                last_detail[0],  # folio_compra
                last_detail[2],  # articulo_id
                last_detail[3],  # cantidad
            )
            
            precio_unitario = self.db.search_articulo_by_id(last_detail[2])
            subtotal_total = precio_unitario[2] * last_detail[3]
            iva = subtotal_total * 0.16
            total = subtotal_total + iva
            
            total_actualizado = total_existente[3] - total
            print("Total actualizado:", total_actualizado)
            
            self.db.update_total_in_compra(self.ent_compra_id.get(), total_actualizado)
            
            self.ent_total.config(state="normal")
            self.ent_total.delete(0, tk.END)
            self.ent_total.insert(0, f"{total_actualizado:.2f}")
            self.ent_total.config(state="disabled")             
            
            if success:
                self.selected_articulos.pop()
                self.lbl_carrito_articulos.delete(tk.END)
                
                self.db.update_articulo_stock(last_detail[2], -last_detail[3])
                self.db.update_articulo_venta_stock_delete(last_detail[2], -last_detail[3])
                              
                messagebox.showinfo("Éxito", "Detalle eliminado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el detalle de la BD")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
            print(f"Error al eliminar detalle: {e}")

    def insert(self):
        if not self.validate_fields():
            return
 
        if not re.match(r'^\d+$', self.ent_cantidad.get()):
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return
                
        articulo_nombre = self.combo_articulo.get()
        articulo = self.db.search_articulo_by_name(articulo_nombre)
        precio_unitario = int(articulo[2])
        
        articulo_id = articulo[0]
        stock_actual = self.db.get_articulo_stock_by_id(articulo_id)
        stock_disponible = stock_actual[0] 

        cantidad = int(self.ent_cantidad.get())

        # Verificar stock
        if stock_disponible < cantidad:
            messagebox.showerror("Stock insuficiente", "No hay suficiente stock para esta venta.")
            return       
        
        total_existente = self.db.search_compra_detalle_by_id(self.ent_compra_id.get(), articulo[0])
        if total_existente:
            cantidad_existente = total_existente[3]
            cantidad = int(self.ent_cantidad.get())
            diferencia = cantidad - cantidad_existente
            subtotal_articulo = precio_unitario * diferencia
            print("Subtotal articulo:", subtotal_articulo)
            self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
        
            self.calculate_total()
        #ME QUEDE AQUI PARA ARREGLAR CUANDO SE BUSCA Y SE AÑADE UN ARTICULO NUEVO EL PRECIO SEA LA SUMA DEL TOTAL QUE YA HABIA
        #INTENTAR HACERLO BUSCANDO SI YA HAY UNA COMPRA GUARDADA CON ESE ID Y EXTRAER EL TOTAL
        else: 
            compra_existente = self.db.search_compra_by_id(self.ent_compra_id.get())
            if compra_existente:
                total_existente = compra_existente[3]
                subtotal_articulo = total_existente + (precio_unitario * cantidad)
                print("Subtotal articulo:", subtotal_articulo)
                self.precios.append({'subtotal': subtotal_articulo})
                
                self.calculate_total()
            else:
                cantidad = int(self.ent_cantidad.get())
                subtotal_articulo = precio_unitario * cantidad
                self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
            
                self.calculate_total()
        
        compra = {
            'compra_id': self.ent_compra_id.get(),
            'usuario': self.ent_usuario.get(),
            'articulo': self.combo_articulo.get(),            
            'cantidad': self.ent_cantidad.get(),
            'fecha': self.ent_fecha.get(),
            'total': self.ent_total.get()
        }
        
        existing_compra = self.db.search_compra_by_id(compra['compra_id'])
  
        if not existing_compra:
            self.db.save_compra(compra)
            messagebox.showinfo("Éxito", "Compra realizada con éxito.")
            
        if not articulo:
            messagebox.showerror("Error", "Articulo no encontrado.")
            return
               
        compraDetail = {            
            'folio_compra':self.ent_compra_id.get(),
            'articulo_id':articulo[0],
            'cantidad':self.ent_cantidad.get()
        }
        
        compraDetail_existente = self.db.search_compra_detalle_by_id(compraDetail['folio_compra'], compraDetail['articulo_id'])
        if compraDetail_existente:
            self.db.update_compra_detalle(compraDetail["folio_compra"],compraDetail["articulo_id"], compraDetail['cantidad'])
        else:
            compraResponse = self.db.add_compra_detalle(compraDetail)
            self.selected_articulos.append((compraResponse['folio_compra'], compraResponse['articulo_name'], compraResponse['cantidad']))
            self.lbl_carrito_articulos.insert(tk.END, f"{"Folio:", compraResponse['folio_compra']} {"Compra ID:", compra['compra_id']} {"Articulo ID:", compraDetail['articulo_id']} {"Cantidad:", compraResponse['cantidad']}")
        
        #self.clear_entries()
        #self.disable_entries()
        #self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
    
    def calculate_total(self):
        subtotal_total = sum(item['subtotal'] for item in self.precios)
        iva = subtotal_total * 0.16
        total = subtotal_total + iva
        
        compra_id = self.ent_compra_id.get()
        
        self.ent_subtotal.config(state="normal")
        self.ent_total.config(state="normal")
        self.ent_iva.config(state="normal")

        self.ent_subtotal.delete(0, tk.END)
        self.ent_subtotal.insert(0, f"{subtotal_total:.2f}")

        self.ent_iva.delete(0, tk.END)
        self.ent_iva.insert(0, f"{iva:.2f}")

        self.ent_total.delete(0, tk.END)
        self.ent_total.insert(0, f"{total:.2f}")
        
        self.db.update_total_in_compra(compra_id, total)

        self.ent_subtotal.config(state="disabled")
        self.ent_iva.config(state="disabled")
        self.ent_total.config(state="disabled")

    def cancel(self):
        compra_id = self.ent_compra_id.get()
        saved_compra = self.db.search_compra_by_id(compra_id)
        if saved_compra:
            detalles_compra = self.db.get_compra_detalle(compra_id)
            for detalle in detalles_compra:
                articulo_id = detalle[2]  
                cantidad_vendida = detalle[3] 
                self.db.update_articulo_stock(articulo_id, -cantidad_vendida)
                cantidad_articulo_venta = self.db.search_articulo_venta_stock_by_id(articulo_id)    
                if cantidad_articulo_venta:
                    self.db.update_articulo_venta_stock_delete(articulo_id, -cantidad_vendida)
            
            self.db.delete_compra(saved_compra[0])
            self.db.delete_all_detalles(compra_id)
            messagebox.showinfo("Éxito", "Compra cancelada con éxito.")
                   
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search_compra(self):
        compra_id = self.ent_search_id.get()
        self.clear_folio_entry()
        
        compra = self.db.search_compra_by_id(compra_id)
        
        user_name = self.db.search_user_by_id(compra[1])
        
        if compra:
            self.current_compra_id = compra[0]  
            
            self.ent_compra_id["state"] = "normal"
            self.ent_usuario["state"] = "normal"
            self.combo_articulo["state"] = "normal"
            self.combo_proveedor["state"] = "normal"
            #self.ent_user_id["state"] = "normal"
            self.ent_fecha["state"] = "normal"
            #self.ent_cantidad["state"] = "normal"
            #self.ent_subtotal["state"] = "disabled"
            self.ent_total["state"] = "normal"
            #self.ent_iva['state'] = "disabled"

            self.ent_compra_id.delete(0, END)
            self.ent_usuario.delete(0, END)
            self.combo_proveedor.delete(0, END) 
            self.combo_articulo.delete(0, END)
            self.ent_fecha.delete(0, END)
            self.ent_cantidad.delete(0, END)
            self.ent_subtotal.delete(0, END)
            self.ent_total.delete(0, END)
            self.ent_iva.delete(0, END)
            
            self.ent_compra_id.insert(0, compra[0])  # compra_id
            self.ent_usuario.insert(0, user_name[1])   # usuario
            self.ent_fecha.insert(0, compra[2]) # fecha
            self.ent_total.insert(0, compra[3]) # total
        
            self.lbl_carrito_articulos.delete(0, END)

            details = self.db.get_compra_detalle(compra[0]) 
            for detail in details:
                print("Detalle obtenido:", detail) 
                self.selected_articulos.append(detail)  
                self.lbl_carrito_articulos.insert(tk.END, f"{"Folio:", detail[0]} {"Compra ID:", detail[1]} {"Articulo ID:", detail[2]} {"Cantidad:", detail[3]}")
            
            print("Detalles seleccionados:", self.lbl_carrito_articulos.get(0, tk.END))
            self.lbl_carrito_articulos.bind('<<ListboxSelect>>', self.on_listbox_select)
            
            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])
            self.ent_compra_id.config(state="normal")
            
            self.enable_entries()
            self.ent_compra_id.config(state="readonly")
        else:
            messagebox.showinfo("Error", "Compra no encontrada.")
    
    def on_listbox_select(self, event):
        self.combo_articulo.delete(0, END)
        self.combo_proveedor.delete(0, END)
        self.ent_cantidad.delete(0, END)
        

        seleccion_detalle = self.lbl_carrito_articulos.curselection()
        print("Seleccionado:", seleccion_detalle)
        if seleccion_detalle:
            print("Seleccionado:", seleccion_detalle)
            index = seleccion_detalle[0]
            print(index)  
            detail = self.selected_articulos[index] 
            print("Detalle seleccionado:", detail)
            articulo_id = detail[2]  
            print("Articulo_id: ",articulo_id)
            proveedor = self.db.get_articulo_details(articulo_id)
            det_id = self.db.get_compra_detalle(detail[1])
            print(det_id[0][0])
            self.current_det_id = det_id[0][0]
            proveedor_data = self.db.search_proveedor_by_id(proveedor[0])
            self.combo_proveedor.insert(0, proveedor_data[1])  
            articulo_name = self.db.search_articulo_by_id(articulo_id)
            self.combo_articulo.insert(0, articulo_name[1])  
            self.ent_cantidad.insert(0, detail[3])
            
            compra_id = self.ent_compra_id.get()
            cantidad = detail[3]
            self.cantidad_actual = cantidad
            
            stock = self.db.search_compra_detalle_by_id(compra_id, articulo_id)
            self.actual_stock = stock[3] 

    def edit(self):
        if not self.validate_fields():
            return
               
        articulo_nombre = self.combo_articulo.get()
        articulo = self.db.search_articulo_by_name(articulo_nombre)
        compra_id = self.ent_compra_id.get()
        precio_unitario = int(articulo[2])
        
        
        articulo_id = articulo[0]
        stock_actual = self.db.get_articulo_stock_by_id(articulo_id)
        stock_disponible = stock_actual[0] if stock_actual else 0
        
        cantidad_actual = int(self.ent_cantidad.get())

        # Verificar stock
        if stock_disponible < cantidad_actual:
            messagebox.showerror("Stock insuficiente", "No hay suficiente stock para esta venta.")
            return
        
        print("Cantidad actual:", cantidad_actual)
        detalle_encontrado = self.db.search_compra_detalle_by_id(compra_id, articulo[0])
        cantidad_en_bd = detalle_encontrado[3]
        print("Cantidad en bd:", cantidad_en_bd)
        diferencia_cantidades = 0
        
        if cantidad_actual > cantidad_en_bd:
            diferencia_cantidades = cantidad_actual - cantidad_en_bd
            #self.db.update_articulo_stock(articulo[0], -diferencia_cantidades)
            print("Diferencia de cantidades si cantidad actual es mayor:", diferencia_cantidades)
            #self.db.update_articulo_stock(articulo[0], diferencia_cantidades)
        #diferencia_cantidades = cantidad_actual - cantidad_en_bd
        
        
        total_existente = self.db.search_compra_by_id(self.ent_compra_id.get())
        print("Total devuelto de compras:", total_existente)
        if total_existente:
            total = total_existente[3]
            print("Total existente:", total)            
            if cantidad_actual < cantidad_en_bd:
                diferencia_cantidades = cantidad_en_bd - cantidad_actual
                subtotal_articulo = total - (precio_unitario * (-1 * diferencia_cantidades))
                print("Subtotal articulo:", subtotal_articulo)
                self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO  
                self.calculate_total() 
            else:            
                subtotal_articulo = total + (precio_unitario * diferencia_cantidades)
                self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO
                print("Subtotal articulo en else:", subtotal_articulo)  
                self.calculate_total()
        else:
            subtotal_articulo = precio_unitario * cantidad_actual
            self.precios.append({'subtotal': subtotal_articulo})#HACER OTRO ARREGLO            
            self.calculate_total()
        
        compra = {
            'compra_id': self.ent_compra_id.get(),
            'usuario': self.ent_usuario.get(),
            'articulo': self.combo_articulo.get(),            
            'cantidad': self.ent_cantidad.get(),
            'fecha': self.ent_fecha.get(),
            'total': self.ent_total.get()
        }
        
        compraDetail = {
            'det_id_compra': self.current_det_id,
            'compra_id': self.ent_compra_id.get(),
            'articulo': self.combo_articulo.get(),
            'cantidad': self.ent_cantidad.get() 
        }
        
        articulo_id = self.db.search_articulo_by_name(compraDetail["articulo"])
        compraDetail_existente = self.db.search_compra_detalle_by_id(compraDetail["compra_id"], articulo_id[0])
        if compraDetail_existente:
            self.db.update_compra_detalle(compraDetail["compra_id"], articulo_id[0], compraDetail['cantidad'] )
        
        self.db.update_compra(compra, compraDetail, self.actual_stock)
        
        #CHECAR ESTOS EN UN FUTURO POR SI LLEGA A DAR ERROR
        self.precios = []
        self.actual_stock = None
        self.cantidad_actual = None
               
        messagebox.showinfo("Éxito", "Compra actualizada con éxito.")
        self.current_det_id = None
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()
        

    def delete(self):
        if not self.ent_compra_id.get():
            messagebox.showerror("Error", "Debe ingresar un ID de compra.")
            return
        compra_id = self.ent_compra_id.get()
        detalles_compra = self.db.get_compra_detalle(compra_id)
        for detalle in detalles_compra:
            articulo_id = detalle[2]  
            cantidad_vendida = detalle[3] 
            self.db.update_articulo_stock(articulo_id, -cantidad_vendida)
        
        self.db.delete_articulo_venta_stock(articulo_id)
        self.db.delete_compra(compra_id)
        messagebox.showinfo("Éxito", "Compra eliminada con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_compra_id.get()
            or not self.ent_usuario.get()
            or not self.combo_proveedor.get()
            or not self.combo_articulo.get()
            or not self.ent_fecha.get()
            or not self.ent_cantidad.get()    
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        if (
            not self.ent_cantidad.get().isdigit()
        ):
            messagebox.showerror("Error, ingrese solo numeros")
            return False
        
        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_compra_id.delete(0, END)
        #self.ent_usuario.delete(0, END)
        self.combo_articulo.delete(0, END)
        #self.ent_user_id.delete(0, END)
        self.ent_fecha.delete(0, END)
        self.ent_cantidad.delete(0, END)
        self.ent_subtotal.delete(0, END)
        self.ent_total.delete(0, END)
        self.ent_iva.delete(0, END)
        #self.ent_user_id.delete(0, END)

    def enable_entries(self):
        self.ent_compra_id["state"] = "normal"
        self.ent_usuario["state"] = "normal"
        self.combo_articulo["state"] = "normal"
        #self.ent_user_id["state"] = "normal"
        self.ent_fecha["state"] = "normal"
        self.ent_cantidad["state"] = "normal"
        self.ent_subtotal["state"] = "disabled"
        self.ent_total["state"] = "disabled"
        self.ent_iva['state'] = "disabled"

    def disable_entries(self):
        self.ent_compra_id["state"] = "disabled"
        self.ent_usuario["state"] = "disabled"
        self.combo_articulo["state"] = "disabled"
        #self.ent_user_id["state"] = "disabled"
        self.ent_cantidad["state"] = "disabled"
        self.ent_subtotal["state"] = "disabled"
        self.ent_total["state"] = "disabled"
        self.ent_iva['state'] = "disabled"
    
    def clear_all_entries(self):
        self.ent_compra_id["state"] = "normal"
        self.ent_compra_id.delete(0, END)
        self.ent_compra_id["state"] = "readonly"
        self.ent_usuario.delete(0, END)
        self.combo_proveedor.delete(0, END)
        self.combo_articulo.delete(0, END)
        #self.ent_user_id.delete(0, END)
        #self.combo_proveedor.delete(0, END)
        self.ent_fecha.delete(0, END)
        self.ent_cantidad.delete(0, END)
        self.ent_subtotal["state"] = "normal"
        self.ent_subtotal.delete(0, END)
        self.ent_subtotal["state"] = "disabled"
        self.ent_total["state"] = "normal"        
        self.ent_total.delete(0, END)
        self.ent_total["state"] = "disabled"
        self.ent_iva["state"] = "normal"
        self.ent_iva.delete(0, END)
        self.ent_iva["state"] = "disabled"      
        #self.ent_user_id.delete(0, END)
        self.lbl_carrito_articulos.delete(0, END)
        self.selected_articulos.clear()
    
    def clear_folio_entry(self):
        #self.clear_folio_entry()
        self.ent_compra_id.config(state="normal")

        self.ent_compra_id.delete(0, END)
        self.ent_compra_id.config(state="readonly")

    def open_compra_menu(self):
            compra_window = tk.Tk()
            compra_window.title("Menú de Compras")
            compra_window.geometry("600x600")
            compra_app = CompraApp(compra_window, self.db, self.user_id, self.username)
            
            compra_window.mainloop()
    
    def load_proveedor_data(self):
        proveedores = self.db.get_all_proveedores()
        proveedores_names = [proveedor[1] for proveedor in proveedores]
        self.combo_proveedor['values'] = proveedores_names
        
    def load_articulo_data(self):
        proveedor = self.combo_proveedor.get()
        print(proveedor)
        articulos = self.db.get_articulo_by_proveedor(proveedor)
        articulos_names = [articulo[0] for articulo in articulos]
        self.combo_articulo['values'] = articulos_names
        
class LoginWindow:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Farmacia")
        self.db = db
        self.user_db = None
        self.username = None
        self.user_id = None

        self.root.configure(bg="#daf1fa")
        self.font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        

        self.main_frame = tk.Frame(root, bg="#ffffff")
        self.main_frame.pack(pady=(70,0), padx=20)
        
        self.label_title = tk.Label(self.main_frame, text="BIENVENIDO A TU FARMACIA", font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#03012C", anchor="center", justify="center")
        self.label_title.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky="ew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.label_username = tk.Label(self.main_frame, text="Usuario:", font=self.font, bg="#ffffff")
        self.label_username.grid(row=5, column=0, pady=5, padx=5, sticky="w")
        self.entry_username = tk.Entry(self.main_frame, font=self.font, bd=2, relief="flat")
        self.entry_username.grid(row=5, column=1, pady=5, padx=5)

        self.label_password = tk.Label(self.main_frame, text="Contraseña:", font=self.font, bg="#ffffff")
        self.label_password.grid(row=6, column=0, pady=5, padx=5, sticky="w")
        self.entry_password = tk.Entry(self.main_frame, show="*", font=self.font, bd=2, relief="flat")
        self.entry_password.grid(row=6, column=1, pady=5, padx=5)

        self.button_login = tk.Button(
            self.main_frame, 
            text="Iniciar sesión", 
            command=self.login, 
            font=self.button_font, 
            bg="#86BBD8", 
            fg="white", 
            bd=0, 
            padx=20, 
            pady=10
        )
        self.button_login.grid(row=7, column=0, columnspan=2, pady=10)

    def login(self):
        
        username = self.entry_username.get()
        password = self.entry_password.get()
              
        user = self.db.search_user_by_username(username)
        if user and user[2] == password:
            self.user_id = user[0]
            self.username = user[1]
            if user[3] == "admin":
                messagebox.showinfo("Login Exitoso", "Bienvenido, {}!".format(username))
                self.root.destroy()
                self.open_menu_user(user)
            elif user[3] == "cajero":
                messagebox.showinfo("Login Exitoso", "Bienvenido cajero, {}!".format(username))
                self.root.destroy()
                self.open_cajero_menu()
            elif user[3] == "gerente":
                messagebox.showinfo("Login Exitoso", "Bienvenido gerente, {}!".format(username))
                self.root.destroy()
                self.open_gerente_menu()
                    
        else:
            messagebox.showerror("Datos incorrectos.")

    def open_menu(self):
        
        menu_window = tk.Tk()
        menu_window.title("Menú Principal")
        menu_window.geometry("400x350")
        menu_window.configure(bg="#f0f0f0")

        button_font = tkfont.Font(family="Helvetica", size=12)

        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0, font=button_font, bg="#f0f0f0", fg="#333333")
        file_menu.add_command(label="Users", command=self.open_user_menu)
        file_menu.add_command(label="Customers", command=self.open_customer_menu)
        file_menu.add_command(label="Cars", command=self.open_cars_menu)
        file_menu.add_command(label="Pieces", command=self.open_pice_menu)
        file_menu.add_command(label="Repairs", command=self.open_repair_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=menu_window.destroy)
        menu_bar.add_cascade(label="Menú", menu=file_menu)

        login_button = tk.Button(
            menu_window, 
            text="Regresar a Login", 
            command=self.show_login_window, 
            font=button_font, 
            bg="#007BFF", 
            fg="white", 
            padx=20, 
            pady=10, 
            bd=0, 
            relief="flat"
        )
        login_button.pack(pady=20)

        menu_window.mainloop()

    def show_login_window(self, current_window):
            current_window.destroy()  
            login_window = tk.Tk()
            login_app = LoginWindow(login_window, self.db)
            login_window.geometry("600x400")
            login_window.mainloop()
    
    def open_menu_user(self, user):
        
        menu_window = tk.Tk()
        menu_window.title("Farmacia Usuario")
        menu_window.geometry("800x550")
        menu_window.configure(bg="#ffffff")
        username = self.username

        button_font = tkfont.Font(family="Helvetica", size=12)

        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)
        
        button_frame = tk.Frame(menu_window, bg="#ffffff")
        button_frame.pack(pady=20)    
            
        if(username == "admin"):
            
            
            usuario_button = tk.Button(
                button_frame, 
                text="Usuarios", 
                command=self.open_user_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
            usuario_button.pack(side="left", pady=2)
            
            cliente_button = tk.Button(
                button_frame, 
                text="Clientes", 
                command=self.open_customer_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
            cliente_button.pack(side="left", pady=2)
            
            venta_button = tk.Button(
                button_frame, 
                text="Ventas", 
                command=self.open_venta_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
            venta_button.pack(side="left", pady=2)
            
            articulo_button = tk.Button(
                button_frame, 
                text="Articulos", 
                command=self.open_articulo_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
            articulo_button.pack(side="left", pady=2)
            
            compra_button = tk.Button(
                button_frame, 
                text="Compras", 
                command=self.open_compra_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
            compra_button.pack(side="left", pady=2)
            
            proveedor_button = tk.Button(
                button_frame, 
                text="Proveedores", 
                command=self.open_proveedor_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
            proveedor_button.pack(side="left", pady=2)
            
            salir_button = tk.Button(
                button_frame, 
                text="Salir", 
                command=menu_window.destroy, 
                font=button_font, 
                bg="#33658A", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
            salir_button.pack(side="left", pady=2)

        else:
            #CAMBIARLOS POR BOTONES   
            file_menu = tk.Menu(menu_bar, tearoff=0, font=button_font, bg="#f0f0f0", fg="#333333")
            file_menu.add_command(label="Customers", command=self.open_customer_menu)
            file_menu.add_command(label="Cars", command=self.open_cars_menu)
            file_menu.add_command(label="Pieces", command=self.open_pice_menu)
            file_menu.add_command(label="Repairs", command=self.open_repair_menu)
            file_menu.add_separator()
            file_menu.add_command(label="Salir", command=menu_window.destroy)
            menu_bar.add_cascade(label="Menú", menu=file_menu)

        big_title = tk.Label(menu_window, text="SELECCIONA UNA OPCION DEL MENU", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#03012C", anchor="center", justify="center")
        big_title.pack(pady=20)
        
        login_button = tk.Button(
            menu_window, 
            text="Regresar a Login", 
            command=self.show_login_window, 
            font=button_font, 
            bg="#33658A", 
            fg="white", 
            padx=20, 
            pady=10, 
            bd=0, 
            relief="flat"
        )
        login_button.pack(pady=20)

        menu_window.mainloop()

    def open_cajero_menu(self):
        
        menu_window = tk.Tk()
        menu_window.title("Farmacia Cajero")
        menu_window.geometry("800x550")
        menu_window.configure(bg="#ffffff")
        username = self.username
        print("Username:", username)

        button_font = tkfont.Font(family="Helvetica", size=12)

        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)
        
        button_frame = tk.Frame(menu_window, bg="#ffffff")
        button_frame.pack(pady=20)    
            
        cliente_button = tk.Button(
                button_frame, 
                text="Clientes", 
                command=self.open_customer_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
        cliente_button.pack(side="left", pady=2)
            
        venta_button = tk.Button(
                button_frame, 
                text="Ventas", 
                command=self.open_venta_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
        venta_button.pack(side="left", pady=2)
            
        salir_button = tk.Button(
                button_frame, 
                text="Salir", 
                command=menu_window.destroy, 
                font=button_font, 
                bg="#33658A", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
        salir_button.pack(side="left", pady=2)

        big_title = tk.Label(menu_window, text="SELECCIONA UNA OPCION DEL MENU", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#03012C", anchor="center", justify="center")
        big_title.pack(pady=20)
        
        login_button = tk.Button(
            menu_window, 
            text="Regresar a Login", 
            command=self.show_login_window, 
            font=button_font, 
            bg="#33658A", 
            fg="white", 
            padx=20, 
            pady=10, 
            bd=0, 
            relief="flat"
        )
        login_button.pack(pady=20)

        menu_window.mainloop()

    def open_gerente_menu(self):
        
        menu_window = tk.Tk()
        menu_window.title("Farmacia Gerente")
        menu_window.geometry("800x550")
        menu_window.configure(bg="#ffffff")
        username = self.username
        print("Username:", username)

        button_font = tkfont.Font(family="Helvetica", size=12)

        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)
        
        button_frame = tk.Frame(menu_window, bg="#ffffff")
        button_frame.pack(pady=20)    
            
        cliente_button = tk.Button(
                button_frame, 
                text="Clientes", 
                command=self.open_customer_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
        cliente_button.pack(side="left", pady=2)
            
        venta_button = tk.Button(
                button_frame, 
                text="Ventas", 
                command=self.open_venta_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
        venta_button.pack(side="left", pady=2)
        
        compra_button = tk.Button(
                button_frame, 
                text="Compras", 
                command=self.open_compra_menu, 
                font=button_font, 
                bg="#86BBD8", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
        compra_button.pack(side="left", pady=2)
            
        salir_button = tk.Button(
                button_frame, 
                text="Salir", 
                command=menu_window.destroy, 
                font=button_font, 
                bg="#33658A", 
                fg="white", 
                padx=20, 
                pady=3, 
                bd=3, 
                relief="flat"
            )
        salir_button.pack(side="left", pady=2)

        big_title = tk.Label(menu_window, text="SELECCIONA UNA OPCION DEL MENU", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#03012C", anchor="center", justify="center")
        big_title.pack(pady=20)
        
        login_button = tk.Button(
            menu_window, 
            text="Regresar a Login", 
            command=self.show_login_window, 
            font=button_font, 
            bg="#33658A", 
            fg="white", 
            padx=20, 
            pady=10, 
            bd=0, 
            relief="flat"
        )
        login_button.pack(pady=20)

        menu_window.mainloop()


    def open_user_menu(self):
        #user_window = tk.Tk()
        #user_window.title("Menú de Usuario")
        
        app_root = tk.Tk()  
        app = App(app_root, self.username)  
        app_root.geometry("600x400")
        app_root.mainloop()

        #user_window.mainloop()

    def open_customer_menu(self):
        customer_window = tk.Tk()
        customer_window.title("Menú de Clientes")
        customer_window.geometry("600x400")
        customer_app = CustomerApp(customer_window, self.db, self.user_id, self.username)
        
        customer_window.mainloop()
        
    def open_proveedor_menu(self):
        customer_window = tk.Tk()
        customer_window.title("Menú de Proveedor")
        customer_window.geometry("600x400")
        customer_app = ProveedorApp(customer_window, self.db, self.user_id, self.username)
        
        customer_window.mainloop()
    
    def open_articulo_menu(self):
            articulo_window = tk.Tk()
            articulo_window.title("Menú de Articulos")
            articulo_window.geometry("600x600")
            articulo_app = ArticuloApp(articulo_window, self.db, self.user_id, self.username)
            
            articulo_window.mainloop()
    
    def open_venta_menu(self):
            venta_window = tk.Tk()
            venta_window.title("Menú de Ventas")
            venta_window.geometry("600x900")
            venta_app = VentaApp(venta_window, self.db, self.user_id, self.username)
            
            venta_window.mainloop()
            
    def open_compra_menu(self):
            compra_window = tk.Tk()
            compra_window.title("Menú de Compras")
            compra_window.geometry("600x900")
            compra_app = CompraApp(compra_window, self.db, self.user_id, self.username)
            
            compra_window.mainloop()

    def show_login_window(self):
        login_window = tk.Tk()
        login_app = LoginWindow(login_window, self.db)
        login_window.geometry("600x400")
        login_window.mainloop()

    def open_cars_menu(self):
        cars_window = tk.Tk()
        cars_window.title("Menú de Vehículos")
        cars_window.geometry("900x400")
        customer_names = self.db.get_all_customer_names()
        cars_app = CarApp(cars_window, self.db, self.username, customer_names)   
        cars_window.mainloop()
    
    def open_pice_menu(self):
        pice_window = tk.Tk()
        pice_window.title("Menú de Piezas")
        pice_window.geometry("600x400")
        customer_names = self.db.get_all_customer_names()
        pice_app = PiceApp(pice_window, self.db, customer_names)    
        pice_window.mainloop()
        
    def open_repair_menu(self):
        repair_window = tk.Tk()
        repair_window.title("Menú de Reparaciones")
        repair_window.geometry("900x700")
        customer_names = self.db.get_all_customer_names()
        repair_app = RepairApp(repair_window, self.db, customer_names)    
        repair_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    db = DBManager()
    login_app = LoginWindow(root,db)
    root.geometry("600x400")
    root.mainloop()