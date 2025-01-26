from django.db import models
import pandas as pd

# Create your models here.
class Proveedor(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_proveedor = models.CharField(max_length=100)
    vencimiento = models.IntegerField()
    nombre_corto = models.CharField(max_length=50)
    rut = models.CharField(max_length=20)
    nombre_vendedor = models.CharField(max_length=100)
    telefono_vendedor = models.CharField(max_length=20)
    correo_vendedor = models.CharField(max_length=100)
    correo_vendedor2 = models.CharField(max_length=100)
    correo_pago = models.CharField(max_length=100)
    tipo_flete = models.CharField(max_length=100)
    transporte = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre_proveedor}"

    @staticmethod
    def leer_datos_excel(ruta):
        """
        Lee los datos desde un archivo Excel.
        """
        try:
            df = pd.read_excel(ruta, sheet_name=0)
            print("Datos leídos correctamente desde el archivo Excel.")
            print(df.head())  # Muestra las primeras filas para confirmar
            return df
        except Exception as e:
            print(f"Error al leer el archivo Excel: {e}")
            return None

    @staticmethod
    def insertar_proveedores(df):
        """
        Inserta los datos desde un DataFrame al modelo Proveedor en la base de datos.
        """
        # Validar columnas requeridas
        required_columns = ["Name", "Vencimiento días", "Nombre Corto", "RUT", "Nombre vendedor",
                            "Teléfono - celular", "Mail Vendedor", "Mail 2do Vendedor", "Mail Pago",
                            "Flete si/no", "Transporte"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Las siguientes columnas faltan en el archivo Excel: {missing_columns}")
            return

        # Validar si el DataFrame está vacío
        if df.empty:
            print("El archivo Excel no contiene datos.")
            return

        # Limpieza de datos
        df["Vencimiento días"] = df["Vencimiento días"].fillna(0).astype(int)
        # Replace NaN values with empty strings
        df = df.fillna('')
        # Insertar los datos
        for _, row in df.iterrows():
            try:
                proveedor = Proveedor(
                    nombre_proveedor=row["Name"],
                    vencimiento=row["Vencimiento días"],
                    nombre_corto=row["Nombre Corto"],
                    rut=row["RUT"],
                    nombre_vendedor=row["Nombre vendedor"],
                    telefono_vendedor=row["Teléfono - celular"],
                    correo_vendedor=row["Mail Vendedor"],
                    correo_vendedor2=row["Mail 2do Vendedor"],
                    correo_pago=row["Mail Pago"],
                    tipo_flete=row["Flete si/no"],
                    transporte=row["Transporte"],
                )
                proveedor.save()  # Guarda el registro en la base de datos
                print(f"Proveedor {row['Name']} insertado correctamente.")
            except Exception as e:
                print(f"Error al insertar el proveedor {row['Name']}: {e}")
