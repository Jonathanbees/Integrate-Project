from django.db import models

class Categoria(models.Model):
    idcategoria = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria'
    def __str__(self):
        return self.nombre


class Comprador(models.Model):
    idcomprador = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    usuario = models.CharField(max_length=45, blank=True, null=True)
    clave = models.CharField(max_length=60, blank=True, null=True)
    preferencias = models.CharField(max_length=100, blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comprador'
    


class Compras(models.Model):
    idcompras = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    total = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compras'


class Detallecarrito(models.Model):
    iddetalle = models.IntegerField(primary_key=True)
    producto_idproducto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='producto_idproducto')
    comprador_idcomprador = models.ForeignKey(Comprador, models.DO_NOTHING, db_column='comprador_idcomprador')
    precioproducto = models.IntegerField(blank=True, null=True)
    subtotal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detallecarrito'


class Empresa(models.Model):
    idempresa = models.IntegerField(primary_key=True)
    rut = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    mensaje = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresa'


class Listadeseo(models.Model):
    producto_idproducto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='producto_idproducto')
    comprador_idcompradores = models.ForeignKey(Comprador, models.DO_NOTHING, db_column='comprador_idcompradores')
    idlista = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'listadeseo'


class Orden(models.Model):
    idorden = models.IntegerField(primary_key=True)
    comprador_idcomprador = models.ForeignKey(Comprador, models.DO_NOTHING, db_column='comprador_idcomprador')
    estado = models.CharField(max_length=45, blank=True, null=True)
    subtotal = models.IntegerField(blank=True, null=True)
    cantidadproductos = models.IntegerField(blank=True, null=True)
    metodo = models.CharField(max_length=45, blank=True, null=True)
    compras_idcompras = models.ForeignKey(Compras, models.DO_NOTHING, db_column='compras_idcompras')
    fechatransaccion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orden'


class Paypal(models.Model):
    idpaypal = models.IntegerField(primary_key=True)
    fecha = models.CharField(max_length=45, blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    detalles = models.CharField(max_length=45, blank=True, null=True)
    orden_idorden = models.ForeignKey(Orden, models.DO_NOTHING, db_column='orden_idorden')

    class Meta:
        managed = False
        db_table = 'paypal'


class Producto(models.Model):
    idproducto = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preciocompra = models.IntegerField(blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    etiquetas = models.CharField(max_length=60, blank=True, null=True)
    fechavencimiento = models.CharField(max_length=45, blank=True, null=True)
    categoria_idcategoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='categoria_idcategoria')

    class Meta:
        managed = False
        db_table = 'producto'


class ProductoOrden(models.Model):
    idproducto_orden = models.IntegerField(primary_key=True)
    producto_idproducto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='producto_idproducto')
    orden_idorden = models.ForeignKey(Orden, models.DO_NOTHING, db_column='orden_idorden')
    cantidad = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto_orden'


class Review(models.Model):
    idreview = models.IntegerField(primary_key=True)
    calificacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    producto_idproducto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='producto_idproducto')
    comprador_idcomprador = models.ForeignKey(Comprador, models.DO_NOTHING, db_column='comprador_idcomprador')

    class Meta:
        managed = False
        db_table = 'review'


class Tarjeta(models.Model):
    idtarjetacredito = models.IntegerField(primary_key=True)
    numerotarjeta = models.CharField(max_length=45, blank=True, null=True)
    titular = models.CharField(max_length=45, blank=True, null=True)
    fechavencimiento = models.CharField(max_length=45, blank=True, null=True)
    cvv = models.IntegerField(blank=True, null=True)
    tipotarjeta = models.CharField(max_length=45, blank=True, null=True)
    orden_idorden = models.ForeignKey(Orden, models.DO_NOTHING, db_column='orden_idorden')

    class Meta:
        managed = False
        db_table = 'tarjeta'


class Transferencia(models.Model):
    idtransferencia = models.IntegerField(primary_key=True)
    bancoorigen = models.CharField(max_length=45, blank=True, null=True)
    bancodestino = models.CharField(max_length=45, blank=True, null=True)
    numerocuenta = models.IntegerField(blank=True, null=True)
    cuentadestino = models.CharField(max_length=45, blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    orden_idorden = models.ForeignKey(Orden, models.DO_NOTHING, db_column='orden_idorden')

    class Meta:
        managed = False
        db_table = 'transferencia'