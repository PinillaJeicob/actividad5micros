# actividad5micros

**Autores:** Jeicob David Pinilla Ruiz  y Fabian Abril Casallas
**Institución:** Universidad Militar Nueva Granada

## Descripción
Este proyecto implementa una simulación *hardware-in-the-loop* de un brazo robótico. Se utiliza un microcontrolador ESP32 para adquirir señales analógicas mediante tres potenciómetros (pines 32, 33 y 34) y enviarlas estructuradas vía comunicación serial (UART). Un script en Python recibe esta trama, mapea los valores a los límites mecánicos (radianes y metros) y controla las articulaciones del modelo 3D (archivo URDF) en tiempo real mediante la librería PyBullet.

## Estructura del Proyecto
*   `brazo.urdf`: Modelo tridimensional y cinemático del robot.
*   `simulacion.py`: Middleware en Python para recepción UART y control en PyBullet.
*   `codigo_esp32/`: Firmware del ESP32 para lectura ADC y transmisión de datos.
*   `evidencias/`: Carpeta con capturas de pantalla del funcionamiento.

## Evidencias
*(Reemplaza el enlace con el nombre de tu foto)*
![Simulación en PyBullet](evidencias/pantallazo.png)
