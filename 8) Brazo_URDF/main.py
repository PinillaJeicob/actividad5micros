import pybullet as p
import pybullet_data
import time
import serial

# ==========================================
# CONFIGURACIÓN (SIMULACIÓN VS HARDWARE)
# ==========================================
USAR_ESP32 = False  # Cambia a True cuando tengas el ESP32 montado
PUERTO_COM = 'COM3' # Ajusta al puerto de tu ESP32
BAUD_RATE = 115200

# ==========================================
# INICIALIZACIÓN DE PYBULLET
# ==========================================
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

# Cargar el robot (useFixedBase=True evita que se caiga)
robot_id = p.loadURDF("brazo.urdf", basePosition=[0, 0, 0], useFixedBase=True)

# Índices de las articulaciones según el URDF
JOINT_1 = 0        # Rotación base
JOINT_2 = 1        # Elevación brazo
JOINT_GRIPPER = 2  # Base de pinza
JOINT_DEDO_IZQ = 3 # Dedo izquierdo
JOINT_DEDO_DER = 4 # Dedo derecho

# ==========================================
# CONTROLES VIRTUALES (PARA PRUEBAS SIN ESP32)
# ==========================================
if not USAR_ESP32:
    # Límites extraídos de tu URDF
    slider_base = p.addUserDebugParameter("Base (Joint 1)", -2.5, 2.5, 0)
    slider_brazo = p.addUserDebugParameter("Brazo (Joint 2)", -2.0, 2.0, 0)
    slider_pinza = p.addUserDebugParameter("Apertura Pinza", 0.0, 0.05, 0.02)
else:
    # Inicializar puerto serial
    try:
        esp32_serial = serial.Serial(PUERTO_COM, BAUD_RATE, timeout=0.1)
        time.sleep(2) # Esperar a que la conexión se estabilice
    except Exception as e:
        print(f"Error abriendo puerto serial: {e}")
        USAR_ESP32 = False

# ==========================================
# BUCLE PRINCIPAL (TIEMPO REAL)
# ==========================================
try:
    while True:
        pos_base = 0.0
        pos_brazo = 0.0
        pos_pinza = 0.0
        
        if USAR_ESP32:
            # Leer datos de UART (Formato esperado: "base,brazo,pinza\n")
            if esp32_serial.in_waiting > 0:
                linea = esp32_serial.readline().decode('utf-8').strip()
                if linea:
                    try:
                        valores = linea.split(',')
                        if len(valores) == 3:
                            pos_base = float(valores[0])
                            pos_brazo = float(valores[1])
                            pos_pinza = float(valores[2])
                    except ValueError:
                        pass # Ignorar tramas corruptas
        else:
            # Leer datos de los sliders de la interfaz de PyBullet
            pos_base = p.readUserDebugParameter(slider_base)
            pos_brazo = p.readUserDebugParameter(slider_brazo)
            pos_pinza = p.readUserDebugParameter(slider_pinza)
        
        # Enviar comandos de posición al URDF
        p.setJointMotorControl2(robot_id, JOINT_1, p.POSITION_CONTROL, targetPosition=pos_base)
        p.setJointMotorControl2(robot_id, JOINT_2, p.POSITION_CONTROL, targetPosition=pos_brazo)
        
        # La pinza tiene dos dedos que se abren simétricamente
        p.setJointMotorControl2(robot_id, JOINT_DEDO_IZQ, p.POSITION_CONTROL, targetPosition=pos_pinza)
        p.setJointMotorControl2(robot_id, JOINT_DEDO_DER, p.POSITION_CONTROL, targetPosition=pos_pinza)
        
        # Avanzar un paso en la simulación
        p.stepSimulation()
        time.sleep(1/240.) # Frecuencia de actualización (240 Hz)

except KeyboardInterrupt:
    print("Simulación terminada.")
finally:
    if USAR_ESP32 and 'esp32_serial' in locals() and esp32_serial.is_open:
        esp32_serial.close()
    p.disconnect()