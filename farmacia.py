import tkinter as tk
from tkinter import font as tkfont
from tkinter import END, messagebox, ttk
import psycopg2
import datetime
import re
from psycopg2 import Error
#COLORES:
#86BBD8 (AZUL BOTON)
#03012C (AZULTITULOS GRANDES)
#daf1fa (AZUL MUY BAJITO BACKGROUND)
#33658A (BOTONES O RESALTAR ALGO)
#A88FAC (CONTRASTES)

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
        values = (user['nombre'], user['password'], user['perfil'])
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
        query = "INSERT INTO clientes (cliente_id, user_id, nombre, telefono, rfc ) VALUES (%s, %s, %s, %s, %s)"
        values = (customer['cliente_id'], customer['user_id'], customer['nombre'], customer['telefono'],  customer['rfc'])
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
    
    def update_articulo(self, articulo):
        query = "UPDATE articulos SET descripcion=%s, precio_unitario=%s, precio_venta=%s, descuento=%s, puntos=%s WHERE articulo_id=%s"
        values = (articulo['descripcion'], articulo['precio_unitario'], articulo['precio_venta'], articulo['descuento'], articulo['puntos'], articulo['articulo_id'])
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_articulo(self, articulo_id):
        query = "DELETE FROM articulos WHERE articulo_id = %s"
        self.cursor.execute(query, (articulo_id,))
        self.conn.commit()
    
    def save_articulo(self, articulo):
        query = "INSERT INTO articulos (articulo_id, descripcion, precio_unitario, precio_venta, descuento, puntos ) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (articulo['articulo_id'], articulo['descripcion'], articulo['precio_unitario'], articulo['precio_venta'], articulo['descuento'], articulo['puntos'])
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

            self.ent_user_id.insert(0, user[0])
            self.ent_name.insert(0, user[1])
            self.ent_password.insert(0, user[2])
            self.ent_profile.set(user[3])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            
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
            or not self.ent_username.get()
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
    def __init__(self, root, db, user_id, username):
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
        if self.username in ["Secre", "Mecanico"]:
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")

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
        self.disable_buttons([self.btn_insert, self.btn_cancel])
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

            self.ent_customer_id.insert(0, customer[0])
            self.ent_name.insert(0, customer[2])
            self.ent_phone.insert(0, customer[3])
            self.ent_user_id.insert(0, customer[1])
            self.ent_rfc.insert(0, customer[4])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])  
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            
            self.btn_edit["state"] = "normal"
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

            self.ent_proveedor_id.insert(0, proveedor[0])
            self.ent_name.insert(0, proveedor[1])
            self.ent_empresa.insert(0, proveedor[2])
            self.ent_direccion.insert(0, proveedor[3])
            self.ent_phone.insert(0, proveedor[4])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])  
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            
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

    def insert(self):
        if not self.validate_fields():
            return

        articulo = {
            'articulo_id': self.ent_articulo_id.get(),
            'descripcion': self.ent_descripcion.get(),
            'precio_unitario': self.ent_preciouni.get(),
            'precio_venta': self.ent_precioven.get(),            
            'descuento': self.ent_descuento.get(),
            'puntos': self.ent_puntos.get()
        }
        
        if not re.match(r'^\d+$', articulo['precio_unitario']):
            messagebox.showerror("Error", "El precio unitario debe ser un número positivo.")
            return
        
        if not re.match(r'^\d+$', articulo['precio_venta']):
            messagebox.showerror("Error", "El precio de venta debe ser un número positivo.")
            return
        
        if not re.match(r'^\d+$', articulo['descuento']):
            messagebox.showerror("Error", "El descuento debe ser un número positivo.")
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

            self.ent_articulo_id.insert(0, articulo[0])
            self.ent_descripcion.insert(0, articulo[1])
            self.ent_preciouni.insert(0, articulo[2])
            self.ent_precioven.insert(0, articulo[3])
            self.ent_descuento.insert(0, articulo[4])
            self.ent_puntos.insert(0, articulo[5])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])  
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            
            self.btn_edit["state"] = "normal"
        else:
            messagebox.showinfo("Error", "Articulo no encontrado.")

    def edit(self):
        if not self.validate_fields():
            return
        
        articulo = {
            'articulo_id': self.ent_customer_id.get(),
            'descripcion': self.ent_descripcion.get(),
            'precio_unitario': self.ent_preciouni.get(),
            'precio_venta': self.ent_precioven.get(),
            'descuento': self.ent_descuento.get(),
            'puntos':self.ent_puntos.get()
            
        }
        
        self.db.update_articulo(articulo)
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
            or not self.ent_descuento.get().isdigit()
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
        self.ent_descuento.delete(0, END)
        self.ent_puntos.delete(0, END)
        self.ent_stock.delete(0, END)
        #self.ent_user_id.delete(0, END)

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
                messagebox.showinfo("Login Exitoso", "Bienvenido, {}!".format(username))
                self.root.destroy()
                self.open_cajero_menu()
            elif user[3] == "gerente":
                messagebox.showinfo("Login Exitoso", "Bienvenido, {}!".format(username))
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
                command=self.open_user_menu, 
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
                command=self.open_user_menu, 
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
        menu_window.title("Farmacia cajero")
        menu_window.geometry("300x200")
        menu_window.configure(bg="#f0f0f0")

        button_font = tkfont.Font(family="Helvetica", size=12)

        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0, font=button_font, bg="#f0f0f0", fg="#333333")
        file_menu.add_command(label="Customers", command=self.open_customer_menu)
        file_menu.add_command(label="Cars", command=self.open_cars_menu)
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

    def open_gerente_menu(self):
        menu_window = tk.Tk()
        menu_window.title("Farmacia Gerente")
        menu_window.geometry("300x200")
        menu_window.configure(bg="#f0f0f0")

        button_font = tkfont.Font(family="Helvetica", size=12)

        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0, font=button_font, bg="#f0f0f0", fg="#333333")
        
        file_menu.add_command(label="Repair", command=self.open_repair_menu)
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