# Lumen Supply

Demo ecommerce en Django para bebidas energéticas y tés exóticos. Incluye index, catálogo, carrito de compras y checkout simulado sin cobros reales.

## Ejecutar

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en el navegador.

## Validar

```powershell
python manage.py check
python manage.py test store
```

El carrito se guarda en la sesión del navegador y empieza vacío para cada sesión nueva. Agregar desde el catálogo lleva al carrito; desde allí se puede ajustar cantidad, eliminar productos y completar una orden simulada.