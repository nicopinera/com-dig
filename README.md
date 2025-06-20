# Comunicaciones Digitales - Trabajo Integrador
Trabajo Integrador de Comunicaciones Digitales - UNC - Facultad de Ciencias Exactas Fisica y Naturales
Alumnos:
1. Krede, Julian
2. Piñera, Nicolas

---

## Primera Parte: Diseño del Codificador-Decodificador
Utilizando una Jupyter Notebook, implementar el codificador de la ecuación (1) propuesto en el paper de Vangelista y su correspondiente decodificador. 
- El diseño debe permitir enviar una cantidad de bits múltiplo del **Spreading Factor (SF)**. Estos bits tienen que ser aleatorios con una función de distribución de probabilidad uniforme. 
- El script debe permitir imprimir una parte de los bits transmitidos y los bits decodificados. 
- A la salida del decodificador se debe calcular e imprimir la probabilidad de error de bit (BER), entendiendose como la relación entre la cantidad de bits errados sobre la cantidad de bits enviados. 
- Utilizar una celda de la Jupyter Notebook para desarrollar la matematica y/o lógica utilizada en el algoritmo propuesto por ud. 

**Test:** Si el codificador y decodificador se encuentran bien diseñados, bajo esta condición de funcionamiento debe dar un BER=0, cualquiera sea la cantidad de bits generados. 
**Nota:** Para optimizar el rendimiento de las etapas a diseñar utilizar los recursos brindados por la biblioteca numpy, evitando utilizar listas.

![Imagen1](img/image1.png)

## Segunda Parte: Diseño del Waveform Former - n-Tuple former

Agregar a la Jupyter Notebook utilizada anteriormente, la implementación del waveform Former propuesto en la ecuación 2 del paper de Vangelista y su correspondiente n-Tuple Former descripto en la sección III. Con el agregado de esta etapa el diseño debe permitir enviar una cantidad de bits múltiplo del Spreading Factor (SF). El script debe permitir imprimir una parte de los símbolos transmitidos y los símbolos decodificados. A la salida del n-Tuple former se debe calcular e imprimir la probabilidad de error de símbolo (SER), entendiéndose como la relación entre la cantidad de símbolos errados sobre la cantidad de símbolos enviados. Utilizar una celda de la Jupyter Notebook para desarrollar la matematica y/o lógica utilizada en el algoritmo propuesto por ud.

**Test:** Si el Waveform Former y el n-Tuple Former se encuentran bien diseñados, bajo esta condición de funcionamiento debe dar un SER=0, cualquiera sea la cantidad de bits generados. **Nota:** Para optimizar el rendimiento de las etapas a diseñar utilizar los recursos brindados por la biblioteca numpy, evitando utilizar listas.
