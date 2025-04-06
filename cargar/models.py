from django.db import models
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TipoFlete(models.Model):
    flete = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.flete

    @staticmethod
    def insertar_fletes_desde_excel(ruta):
        """
        Inserta tipos de flete desde un archivo Excel.
        La columna esperada debe llamarse 'Flete'.
        """
        try:
            df = pd.read_excel(ruta)
            if "Flete" not in df.columns:
                logger.warning("La columna 'Flete' no existe en el archivo.")
                return
            df = df.fillna('')
            for flete_nombre in df["Flete"].drop_duplicates():
                flete_nombre = str(flete_nombre).strip().capitalize()
                if flete_nombre:
                    obj, created = TipoFlete.objects.get_or_create(flete=flete_nombre)
                    if created:
                        logger.info(f"TipoFlete '{flete_nombre}' creado.")
                    else:
                        logger.info(f"TipoFlete '{flete_nombre}' ya existía.")
        except Exception as e:
            logger.error(f"Error al insertar tipos de flete desde Excel: {e}")

class Transporte(models.Model):
    transportista = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.transportista

    @staticmethod
    def insertar_transportes_desde_excel(ruta):
        """
        Inserta transportistas desde un archivo Excel.
        La columna esperada debe llamarse 'Transporte'.
        """
        try:
            df = pd.read_excel(ruta)
            if "Transporte" not in df.columns:
                logger.warning("La columna 'Transporte' no existe en el archivo.")
                return
            df = df.fillna('')
            for nombre in df["Transporte"].drop_duplicates():
                nombre = str(nombre).strip().title()
                if nombre:
                    obj, created = Transporte.objects.get_or_create(transportista=nombre)
                    if created:
                        logger.info(f"Transporte '{nombre}' creado.")
                    else:
                        logger.info(f"Transporte '{nombre}' ya existía.")
        except Exception as e:
            logger.error(f"Error al insertar transportistas desde Excel: {e}")


class Proveedor(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_proveedor = models.CharField(max_length=100)
    vencimiento = models.IntegerField()
    nombre_corto = models.CharField(max_length=50)
    rut = models.CharField(max_length=20, unique=True)
    nombre_vendedor = models.CharField(max_length=100)
    telefono_vendedor = models.CharField(max_length=20)
    correo_vendedor = models.CharField(max_length=100)
    correo_vendedor2 = models.CharField(max_length=100)
    correo_pago = models.CharField(max_length=100)
    tipo_flete = models.ForeignKey(TipoFlete, on_delete=models.CASCADE)
    transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_proveedor}"

    @staticmethod
    def leer_datos_excel(ruta):
        """
        Lee los datos desde un archivo Excel.
        """
        try:
            df = pd.read_excel(ruta, sheet_name=0)
            logger.info("Datos leídos correctamente desde el archivo Excel.")
            logger.debug(df.head())
            return df
        except Exception as e:
            logger.error(f"Error al leer el archivo Excel: {e}")
            return None

    @staticmethod
    def insertar_proveedores(df):
        """
        Inserta los datos desde un DataFrame al modelo Proveedor en la base de datos.
        """
        required_columns = [
            "Name", "Vencimiento días", "Nombre Corto", "RUT", "Nombre vendedor",
            "Teléfono - celular", "Mail Vendedor", "Mail 2do Vendedor", "Mail Pago",
            "Flete", "Transporte"
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.warning(f"Columnas faltantes en el archivo Excel: {missing_columns}")
            return

        if df.empty:
            logger.warning("El archivo Excel no contiene datos.")
            return

        df["Vencimiento días"] = df["Vencimiento días"].fillna(0).astype(int)
        df = df.fillna('')  # Reemplaza NaN por string vacío

        for _, row in df.iterrows():
            try:
                # Normalizar strings
                flete_val = str(row["Flete"]).strip().capitalize()
                transporte_val = str(row["Transporte"]).strip().title()

                # Obtener o crear relaciones
                tipo_flete_obj, _ = TipoFlete.objects.get_or_create(flete=flete_val)
                transporte_obj, _ = Transporte.objects.get_or_create(transportista=transporte_val)

                # Verificar existencia por RUT
                proveedor, created = Proveedor.objects.get_or_create(
                    rut=row["RUT"],
                    defaults={
                        "nombre_proveedor": row["Name"],
                        "vencimiento": row["Vencimiento días"],
                        "nombre_corto": row["Nombre Corto"],
                        "nombre_vendedor": row["Nombre vendedor"],
                        "telefono_vendedor": row["Teléfono - celular"],
                        "correo_vendedor": row["Mail Vendedor"],
                        "correo_vendedor2": row["Mail 2do Vendedor"],
                        "correo_pago": row["Mail Pago"],
                        "tipo_flete": tipo_flete_obj,
                        "transporte": transporte_obj,
                    }
                )

                if created:
                    logger.info(f"Proveedor {row['Name']} creado exitosamente.")
                else:
                    logger.info(f"Proveedor {row['Name']} ya existía, no se duplicó.")

            except Exception as e:
                logger.error(f"Error al insertar el proveedor {row['Name']}: {e}")
