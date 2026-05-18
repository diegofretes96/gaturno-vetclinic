# 🐾 VetClinic – Sistema de Gestión Veterinaria

Sistema completo de gestión veterinaria desarrollado en Django/Python.  
Diseñado para clínicas de animales pequeños (gatos y perros) en Paraguay.

## 📋 Módulos incluidos

| Módulo            | Descripción                              |
|-------------------|------------------------------------------|
| Historia clínica  | Pacientes con 9 tabs de historial        |
| Agenda            | Citas, calendario FullCalendar, sala espera |
| Consultas         | SOAP completo, prescripciones, notas     |
| Vacunación        | Registro, catálogo, alertas de vencimiento |
| Desparasitación   | Interna, externa, combinada              |
| Exámenes Lab.     | Solicitud y resultados                   |
| Cirugía           | Programación, anestesia, evolución       |
| Hospitalización   | Internados, habitaciones, evoluciones    |
| Farmacia          | Recetas, despacho, descuento automático de stock |
| Inventario        | Productos, movimientos, proveedores      |
| Facturación       | Facturas, cobros, IVA 10%                |
| Estética          | Baño, corte, guardería, fotos            |
| Certificados      | 6 tipos con numeración automática        |
| Vademécum         | Medicamentos por especie                 |
| Reportes          | Dashboard, estadísticas del mes          |
| Propietarios      | CRUD con historial de facturas y mascotas |
| Usuarios          | Roles: admin, vet, asistente, recepcionista, esteticista |

## 🚀 Instalación rápida (SQLite – desarrollo)

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
Acceder en: **http://127.0.0.1:8000/**

## 🔑 Usuarios iniciales (si corriste seed)

| Usuario      | Contraseña | Rol             |
|--------------|------------|-----------------|
| admin        | admin123   | Administrador   |
| dra.garcia   | vet123     | Veterinaria     |
| recepcion    | rec123     | Recepcionista   |

## 🗄️ Base de datos (producción – PostgreSQL)

Edita `.env`:
```
DB_NAME=vetclinic_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

Luego en `settings.py` cambia el backend de SQLite a PostgreSQL.

## ⚙️ Variables de entorno

```env
CLINICA_NOMBRE=Mi Veterinaria
CLINICA_DIRECCION=Av. Principal 123
CLINICA_TELEFONO=+595 21 000000
CLINICA_RUC=12345678-9
MONEDA_SIMBOLO=Gs.
IVA_PORCENTAJE=10
```

## 🛠️ Stack técnico

- **Backend**: Django 4.2 + Python 3.x
- **Base de datos**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Calendario**: FullCalendar 6
- **Fuente**: Nunito
- **Colores**: Teal #1D9E75 · Ámbar #EF9F27

## 📁 Estructura del proyecto

```
vetclinic/
├── apps/              # 17 módulos Django
├── templates/         # 67+ templates HTML
├── static/css/        # vetclinic.css
├── static/js/         # vetclinic.js
├── fixtures/          # Datos iniciales
├── manage.py
├── requirements.txt
└── .env.example
```
