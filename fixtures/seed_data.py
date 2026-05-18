"""
Script de datos iniciales para VetClinic.
Ejecutar con: python manage.py shell < fixtures/seed_data.py
"""
from apps.pacientes.models import Especie, Raza
from apps.vacunacion.models import Vacuna
from apps.examenes.models import TipoExamen
from apps.inventario.models import Categoria, Producto
from apps.hospitalizacion.models import Habitacion

# Especies
perro, _ = Especie.objects.get_or_create(nombre='Perro', defaults={'icono': '🐶'})
gato, _ = Especie.objects.get_or_create(nombre='Gato', defaults={'icono': '😺'})

# Razas perro
for r in ['Labrador Retriever','Golden Retriever','Bulldog Francés','Poodle','Beagle','Yorkshire Terrier','Boxer','Dachshund','Chihuahua','Mestizo','Rottweiler','Husky Siberiano','Pastor Alemán','Shih Tzu','Cocker Spaniel']:
    Raza.objects.get_or_create(especie=perro, nombre=r)

# Razas gato
for r in ['Persa','Siamés','Maine Coon','Ragdoll','Bengalí','British Shorthair','Abisinio','Sphynx','Scottish Fold','Mestizo','Angora','Birmano']:
    Raza.objects.get_or_create(especie=gato, nombre=r)

# Vacunas
for n, i in [('Parvovirus',365),('Moquillo',365),('Hepatitis infecciosa',365),('Rabia',365),('Leptospirosis',365),('Combo 5 en 1',365),('Bordetella',365)]:
    Vacuna.objects.get_or_create(nombre=n, especie=perro, defaults={'intervalo_dias':i})
for n, i in [('Panleucopenia',365),('Herpesvirus felino',365),('Calicivirus',365),('Rabia felina',365),('Leucemia felina',365),('Combo triple felino',365)]:
    Vacuna.objects.get_or_create(nombre=n, especie=gato, defaults={'intervalo_dias':i})

# Tipos de examen
for n, p in [('Hemograma completo',85000),('Bioquímica sérica',120000),('Urianálisis',70000),('Coprocultivo',90000),('Radiografía',150000),('Ecografía abdominal',200000),('Cultivo y antibiograma',130000),('Electrocardiograma',180000),('Frotis sanguíneo',60000)]:
    TipoExamen.objects.get_or_create(nombre=n, defaults={'precio_ref':p})

# Habitaciones
for num, tipo, cap in [('H01','general',2),('H02','general',2),('H03','general',1),('UCI','uci',1),('POST','postoperatorio',2),('AISL','aislamiento',1)]:
    Habitacion.objects.get_or_create(numero=num, defaults={'tipo':tipo,'capacidad':cap})

print("✅ Datos iniciales cargados correctamente!")
