# GPS Simulator - HiWay

Simulador de rutas GPS para testing del sistema HiWay.

## 🎯 Propósito

Herramienta de desarrollo para simular vehículos enviando datos GPS en tiempo real al broker MQTT, útil para:

- Testing del dashboard sin vehículos reales
- Desarrollo y debugging
- Demos del sistema
- Load testing

## 🚀 Uso

### Iniciar simulación

```bash
docker-compose up -d
```

### Ver logs

```bash
docker-compose logs -f
```

### Detener simulación

```bash
docker-compose down
```

## ⚙️ Configuración

Copia `.env.example` a `.env` y ajusta:

```env
MQTT_BROKER=mqtt.apphiway.io    # Broker MQTT
MQTT_PORT=1883                   # Puerto MQTT
TOPIC=location_drivers/hiway     # Tópico MQTT
SIMULATION_SPEED=1.0             # Velocidad (1.0 = normal)
```

## 📁 Archivos de Rutas

- `routes_demo.py` - Script principal de simulación
- `gps_simulation_data.json` - Datos de rutas predefinidas
- `Estrella Heading` - Ruta específica de prueba

## 🔧 Desarrollo Local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar directamente
python routes_demo.py
```

## 📝 Notas

- Este es un proyecto de **desarrollo/testing**, no para producción
- Los datos GPS son simulados basados en rutas reales de Medellín
- La velocidad de simulación puede ajustarse con `SIMULATION_SPEED`
