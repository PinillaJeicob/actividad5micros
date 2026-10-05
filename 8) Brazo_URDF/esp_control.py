// Definición de los pines ADC para los potenciómetros
const int pinBase = 32;
const int pinBrazo = 33;
const int pinPinza = 34;

void setup() {
  // Iniciar comunicación serial a alta velocidad
  Serial.begin(115200);
  
  // Configurar resolución del ADC a 12 bits (valores de 0 a 4095)
  analogReadResolution(12);
}

void loop() {
  // Leer los valores analógicos
  int valBase = analogRead(pinBase);
  int valBrazo = analogRead(pinBrazo);
  int valPinza = analogRead(pinPinza);

  // Enviar la trama estructurada separada por comas
  Serial.print(valBase);
  Serial.print(",");
  Serial.print(valBrazo);
  Serial.print(",");
  Serial.println(valPinza); // println añade el salto de línea final (\n)

  // Pausa de 50ms para mantener una actualización estable de 20Hz
  delay(50);
}