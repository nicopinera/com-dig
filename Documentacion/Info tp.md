# Proyecto integrador
No hay que hacer el proyecto por tareas, sino hay que realizarlo completo e ir presentando, se evalúa el proceso.

El codificador lleva de bit a números decimales. Se espera ver la implementación de la ecuación tal cual como esta en el paper con sus sumas y exponentes, igual en su decodificador (desplazar el numero a la izquierda y realizar divisiones por 2)

Ecuación (2)  $"c(nT_s + kT)"$ es una función que tiene dos argumentos contantes Ts y T son los tiempos a utilizar, Ts es tiempo de símbolos de modulación lora y T es el tiempo de muestreo o funcionamiento del sistema, el Ts es el mayor, el índice k y m marcan cuantos T entran en un Ts. En esa parte se realiza una aritmética de argumentos que modifica la forma de la señal, con las sumas y restas se producen desplazamientos de la señal para cualquiera de los dos lados, como los índices están asociados al tiempo se realizar desplazamientos temporales. Organizamos la funcion en una base de tiempo. El primer argumento "kT" nos dice donde va a existir la señal, marca donde se va a generar la señal (donde se muestrea la señal). K vuelve a 0 cuando termina de muestrear un simbolo o sea termina un $T_s$ se va a ir desplazando la generación de la señal según los nuevos símbolos.

> Simularlo con dos bucles for uno grande por cada $n$ y dentro el bucle for que varié según $k$

Se conforma una señal compleja (exponencial) la cual podríamos verla como una $e^{2.pi.f.j} = cos(2.pi.f) + j.sen(2.pi.f)$ (relación de Euler - utilizarla para graficarla) su frecuencia se va a modificar según los valores de k y los valores decimales o valores codificados, la información viaja en la frecuencia y la tenemos en el primer instante de muestreo (k=0). El modulo que se presenta en la ecuación cumple la función de limitar el ancho de banda.

Cuando llega la señal se proyecta sobre la base del receptor o sea realizamos el producto interno. Algo similar se realiza en el receptor entre la función recibida y las funciones de la base del receptor, cuya base tiene que ser ortogonal. Se parte de eso para encontrar la ecuación.

$SNR_{dB} = 10 log(S/n)$ (potencia de la señal / potencia del ruido) esto es el valor que toma la varianza del ruido AWGN que se le suma al canal

BER = Cantidad de bit errados / Bit totales transmitidos

---

El archivo titulado **"Frequency Shift Chirp Modulation: The LoRa Modulation"** es un artículo técnico que describe en detalle la modulación utilizada en LoRa, una tecnología clave para redes de área amplia de baja potencia (LPWAN) en el contexto del Internet de las Cosas (IoT). A continuación, se presenta una explicación detallada del contenido:

---

### **1. Resumen (Abstract)**
- **Contexto**: Las redes LPWAN son fundamentales para IoT, y LoRa es una de las tecnologías más destacadas en este ámbito.
- **Objetivo**: El artículo proporciona la primera descripción matemática rigurosa de la modulación y demodulación en LoRa, denominada **Frequency Shift Chirp Modulation (FSCM)**. También deriva el receptor óptimo y compara su rendimiento con la modulación FSK (Frequency-Shift Keying).
- **Contribución**: La descripción teórica permite evaluar de manera más precisa las redes basadas en LoRa.

---

### **2. Introducción (Section I)**
- **LoRa**: Es la capa física del sistema LoRaWAN, mantenido por la LoRa Alliance. Su modulación está patentada pero carecía de una descripción teórica detallada.
- **FSCM**: A diferencia de las descripciones previas que se limitaban al dominio analógico, este artículo define la modulación como FSCM, donde la información se codifica en un desplazamiento de frecuencia al inicio de cada símbolo, y el "chirp" actúa como portadora.
- **Organización**: El artículo se divide en:
  - Sección II: Descripción del proceso de modulación.
  - Sección III: Demodulador óptimo y su implementación eficiente.
  - Sección IV: Análisis de rendimiento comparativo con FSK.
  - Sección V: Conclusiones.

---

### **3. Modulación FSCM (Section II)**
- **Parámetros clave**:
  - **Banda ancha del canal (B)**: Se transmite una muestra cada \( T = 1/B \).
  - **Duración del símbolo (\( T_s \))**: \( T_s = 2^{SF} \cdot T \), donde **SF (Spreading Factor)** es un entero (típicamente entre 7 y 12).
  - **Símbolo (\( s(nT_s) \))**: Se forma a partir de un vector binario de longitud SF, tomando valores en \( \{0, 1, \ldots, 2^{SF} - 1\} \).

- **Señal transmitida**:
  \[
  c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} e^{j2\pi \left[(s(nT_s) + k) \mod 2^{SF}\right] \frac{k}{2^{SF}}}
  \]
  - Es una señal **chirp** (frecuencia aumenta linealmente con el tiempo).
  - La frecuencia inicial está desplazada por \( s(nT_s) \), lo que define la modulación FSCM.

- **Ortogonalidad**: Se demuestra que las señales FSCM son ortogonales entre sí, lo que es esencial para la detección óptima.

---

### **4. Demodulación Óptima (Section III)**
- **Canal AWGN**: El receptor óptimo para señales FSCM en este canal se basa en:
  1. **Proyección**: La señal recibida \( r(nT_s + kT) \) se proyecta sobre cada posible señal FSCM.
  2. **Decisión**: Se elige la señal con la proyección de mayor módulo.

- **Implementación eficiente**:
  - **Paso 1**: Multiplicar la señal recibida por un **down-chirp** (\( e^{-j2\pi k^2 / 2^{SF}} \)).
  - **Paso 2**: Aplicar la **Transformada Rápida de Fourier (FFT)** al resultado.
  - El índice del máximo en la FFT corresponde al símbolo detectado.

---

### **5. Análisis de Rendimiento (Section IV)**
- **Comparación FSCM vs. FSK**:
  - **Canal AWGN**: Ambas modulaciones tienen el mismo rendimiento.
  - **Canal selectivo en frecuencia**: FSCM supera a FSK porque barre todo el rango de frecuencias, promediando el efecto del ruido. En cambio, FSK sufre más en frecuencias con atenuación.

- **Resultados**: La Figura 1 muestra que FSCM es más robusta en entornos con desvanecimiento selectivo en frecuencia.

---

### **6. Conclusiones (Section V)**
- El artículo proporciona la primera descripción matemática completa de la modulación LoRa (FSCM).
- El demodulador óptimo basado en FFT es eficiente y práctico.
- FSCM ofrece ventajas en canales selectivos en frecuencia, lo que la hace ideal para aplicaciones IoT en entornos complejos.

---

### **7. Referencias**
El artículo cita trabajos previos sobre LPWAN, chirp modulation y técnicas de demodulación, así como libros de teoría de señales y comunicaciones.

---

### **Conceptos Clave**
- **Chirp Modulation**: Señal cuya frecuencia varía linealmente con el tiempo.
- **Spreading Factor (SF)**: Determina la duración del símbolo y la robustez de la señal.
- **Ortogonalidad**: Permite distinguir claramente entre símbolos diferentes.
- **FFT en demodulación**: Reduce la complejidad computacional del receptor.

Este artículo es fundamental para entender la base teórica de LoRa y su superioridad en escenarios IoT con desafíos de propagación.


---


¡Ah, claro! Vamos a profundizar en los detalles del **codificador (modulador)** y los primeros pasos del **decodificador (demodulador)** en LoRa (FSCM), que son clave para entender cómo se transmite y decodifica la información.  

---

### **1. Codificador (Modulador)**
El proceso de modulación en LoRa convierte bits de información en una señal chirp con un desplazamiento de frecuencia inicial. Aquí está el desglose:

#### **a. Generación del Símbolo (\( s(nT_s) \))**
- **Entrada**: Un vector binario \( \mathbf{w}(nT_s) \) de longitud \( SF \) (Spreading Factor).  
  - Ejemplo: Si \( SF = 8 \), se procesan 8 bits por símbolo (\( 2^8 = 256 \) valores posibles).  
- **Cálculo del símbolo**:  
  \[
  s(nT_s) = \sum_{h=0}^{SF-1} \mathbf{w}(nT_s)_h \cdot 2^h
  \]  
  - Esto convierte los bits en un número entero entre \( 0 \) y \( 2^{SF} - 1 \).  
  - Ejemplo: Para \( \mathbf{w} = [1, 0, 1, 1] \) (SF=4), \( s(nT_s) = 1 \cdot 2^0 + 0 \cdot 2^1 + 1 \cdot 2^2 + 1 \cdot 2^3 = 1 + 0 + 4 + 8 = 13 \).

#### **b. Generación de la Señal Chirp Modulada**
- **Duración del símbolo**: \( T_s = 2^{SF} \cdot T \), donde \( T = 1/B \) (tiempo de muestra).  
- **Señal transmitida**:  
  \[
  c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} e^{j2\pi \left[(s(nT_s) + k) \mod 2^{SF}\right] \frac{k}{2^{SF}}}
  \]
  - **Explicación**:  
    1. **Desplazamiento inicial**: La frecuencia inicial de la chirp está determinada por \( s(nT_s) \).  
    2. **Evolución en el tiempo**: La frecuencia aumenta linealmente con \( k \) (índice de tiempo), creando el barrido chirp.  
    3. **Operación módulo \( 2^{SF} \)**: Garantiza que la señal "repita" su barrido dentro del ancho de banda \( B \).  

- **Ejemplo visual**:  
  - Si \( s(nT_s) = 3 \) y \( SF = 4 \), la chirp comienza en una frecuencia proporcional a 3 y barre hasta \( 2^4 = 16 \) pasos, luego "vuelve a empezar".  

---

### **2. Primeros Bloques del Decodificador (Demodulador)**
El demodulador debe recuperar el símbolo \( s(nT_s) \) a partir de la señal recibida \( r(nT_s + kT) \), que incluye ruido. Aquí los pasos clave:

#### **a. Señal Recibida**
\[
r(nT_s + kT) = c(nT_s + kT) + w(nT_s + kT)
\]  
- \( w(nT_s + kT) \): Ruido blanco gaussiano (AWGN).

#### **b. Proyección sobre la Base de Señales**
El receptor óptimo calcula la correlación entre la señal recibida y todas las posibles señales chirp (una para cada \( s(nT_s) \)).  

1. **Multiplicación por el "down-chirp"**:  
   - Se multiplica \( r(nT_s + kT) \) por una chirp inversa:  
     \[
     d(nT_s + kT) = r(nT_s + kT) \cdot e^{-j2\pi \frac{k^2}{2^{SF}}}
     \]  
   - **Propósito**: Eliminar el barrido de frecuencia de la chirp, dejando solo el desplazamiento inicial \( s(nT_s) \).  

2. **Transformada de Fourier (FFT)**:  
   - Se aplica una FFT de \( 2^{SF} \) puntos a \( d(nT_s + kT) \):  
     \[
     D(q) = \sum_{k=0}^{2^{SF}-1} d(nT_s + kT) \cdot e^{-j2\pi \frac{qk}{2^{SF}}}
     \]  
   - **Resultado**:  
     - Si no hay ruido, \( D(q) \) tendrá un pico en \( q = s(nT_s) \).  
     - Con ruido, se elige el \( q \) que maximiza \( |D(q)| \).  

3. **Decisión**:  
   - El índice \( l \) del máximo de \( |D(q)| \) es el símbolo estimado:  
     \[
     \hat{s}(nT_s) = \arg\max_q |D(q)|
     \]  

---

### **3. Ejemplo Numérico (Simplificado)**
Supongamos:  
- \( SF = 3 \) (\( 8 \) símbolos posibles).  
- Símbolo transmitido: \( s(nT_s) = 5 \).  

#### **En el Transmisor**:  
1. Se genera la chirp con desplazamiento inicial 5.  
2. La señal barre frecuencias según:  
   \[
   \text{Frecuencia en } k = \left[(5 + k) \mod 8\right] \cdot \frac{B}{8}
   \]  

#### **En el Receptor**:  
1. Se multiplica la señal recibida por el down-chirp \( e^{-j2\pi k^2 / 8} \).  
2. Se aplica FFT de 8 puntos.  
3. El pico estará en la posición 5, recuperando el símbolo.  

---

### **4. ¿Por qué Funciona?**
- **Ortogonalidad**: Las chirps con diferentes \( s(nT_s) \) son ortogonales (Sección II.A del artículo).  
- **Robustez**: El barrido en frecuencia hace que FSCM sea resistente a canales selectivos (mejor que FSK).  

### **Diagrama de Bloques Conceptual**
```
Transmisor:
Bits → Codificación (s(nT_s)) → Chirp Modulado → Canal

Receptor:
Señal Recibida × Down-Chirp → FFT → Detección de Pico → Símbolo Decodificado
```

Este proceso es la esencia de LoRa: bajo consumo, larga distancia y robustez gracias a la modulación chirp y la demodulación basada en FFT.

---

## Detalle sobre Oversampling y el parámetro delta en la modulación LoRa (FSCM)

### ¿Qué es el oversampling (`samples_per_chirp`)?

- **Oversampling** significa tomar más muestras por cada símbolo de las estrictamente necesarias.
- En LoRa, cada símbolo tiene \( N_s = 2^{SF} \) posiciones posibles, pero si se desea una señal más suave o simular una mayor tasa de muestreo (como haría un DAC real), se pueden tomar varias muestras por cada "paso" de símbolo.
- El parámetro `samples_per_chirp` indica **cuántas muestras se toman por cada paso de símbolo**.  
  Ejemplo:  
  Si \( SF=8 \), entonces \( N_s=256 \). Si `samples_per_chirp=4`, se generan \( 256 \times 4 = 1024 \) muestras por símbolo.

### ¿Qué es `delta` y para qué sirve?

- En el código, se define:
  ```python
  delta = 1 / samples_per_chirp
  ```
- `delta` es el **incremento fraccional** que se le suma al índice \( k \) en cada muestra.
- Si no hubiera oversampling, \( k \) avanzaría de a 1 en cada muestra (es decir, \( k = s, s+1, s+2, ... \)).
- Con oversampling, queremos que \( k \) avance más despacio:  
  - Si `samples_per_chirp=4`, entonces para avanzar de un valor entero de \( k \) al siguiente, necesitamos 4 muestras, así que sumamos \( 1/4 \) en cada paso.
- Así, \( k \) avanza de a `delta` en cada muestra, logrando el efecto de oversampling.

**Resumen:**  
- **`samples_per_chirp`**: lo define el usuario, según cuántas muestras quiera por símbolo (mayor valor = señal más suave y precisa).
- **`delta`**: es el paso fraccional para que, al recorrer todas las muestras de un símbolo, \( k \) avance exactamente 1 unidad por cada `samples_per_chirp` muestras.

---

## Explicación detallada del codificador (modulador) y decodificador (demodulador) LoRa (FSCM)

### 1. Codificador (Modulador)

El proceso de modulación en LoRa convierte bits de información en una señal chirp con un desplazamiento de frecuencia inicial.

#### a. Generación del Símbolo (\( s(nT_s) \))

- **Entrada**: Un vector binario \( \mathbf{w}(nT_s) \) de longitud \( SF \) (Spreading Factor).  
  - Ejemplo: Si \( SF = 8 \), se procesan 8 bits por símbolo (\( 2^8 = 256 \) valores posibles).  
- **Cálculo del símbolo**:  
  \[
  s(nT_s) = \sum_{h=0}^{SF-1} \mathbf{w}(nT_s)_h \cdot 2^h
  \]  
  - Esto convierte los bits en un número entero entre \( 0 \) y \( 2^{SF} - 1 \).  
  - Ejemplo: Para \( \mathbf{w} = [1, 0, 1, 1] \) (SF=4), \( s(nT_s) = 1 \cdot 2^0 + 0 \cdot 2^1 + 1 \cdot 2^2 + 1 \cdot 2^3 = 1 + 0 + 4 + 8 = 13 \).

#### b. Generación de la Señal Chirp Modulada

- **Duración del símbolo**: \( T_s = 2^{SF} \cdot T \), donde \( T = 1/B \) (tiempo de muestra).  
- **Señal transmitida**:  
  \[
  c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} e^{j2\pi \left[(s(nT_s) + k) \mod 2^{SF}\right] \frac{k}{2^{SF}}}
  \]
  - **Explicación**:  
    1. **Desplazamiento inicial**: La frecuencia inicial de la chirp está determinada por \( s(nT_s) \).  
    2. **Evolución en el tiempo**: La frecuencia aumenta linealmente con \( k \) (índice de tiempo), creando el barrido chirp.  
    3. **Operación módulo \( 2^{SF} \)**: Garantiza que la señal "repita" su barrido dentro del ancho de banda \( B \).  

- **Ejemplo visual**:  
  - Si \( s(nT_s) = 3 \) y \( SF = 4 \), la chirp comienza en una frecuencia proporcional a 3 y barre hasta \( 2^4 = 16 \) pasos, luego "vuelve a empezar".  

---

### 2. Primeros Bloques del Decodificador (Demodulador)

El demodulador debe recuperar el símbolo \( s(nT_s) \) a partir de la señal recibida \( r(nT_s + kT) \), que incluye ruido. Aquí los pasos clave:

#### a. Señal Recibida

\[
r(nT_s + kT) = c(nT_s + kT) + w(nT_s + kT)
\]  
- \( w(nT_s + kT) \): Ruido blanco gaussiano (AWGN).

#### b. Proyección sobre la Base de Señales

El receptor óptimo calcula la correlación entre la señal recibida y todas las posibles señales chirp (una para cada \( s(nT_s) \)).  

1. **Multiplicación por el "down-chirp"**:  
   - Se multiplica \( r(nT_s + kT) \) por una chirp inversa:  
     \[
     d(nT_s + kT) = r(nT_s + kT) \cdot e^{-j2\pi \frac{k^2}{2^{SF}}}
     \]  
   - **Propósito**: Eliminar el barrido de frecuencia de la chirp, dejando solo el desplazamiento inicial \( s(nT_s) \).  

2. **Transformada de Fourier (FFT)**:  
   - Se aplica una FFT de \( 2^{SF} \) puntos a \( d(nT_s + kT) \):  
     \[
     D(q) = \sum_{k=0}^{2^{SF}-1} d(nT_s + kT) \cdot e^{-j2\pi \frac{qk}{2^{SF}}}
     \]  
   - **Resultado**:  
     - Si no hay ruido, \( D(q) \) tendrá un pico en \( q = s(nT_s) \).  
     - Con ruido, se elige el \( q \) que maximiza \( |D(q)| \).  

3. **Decisión**:  
   - El índice \( l \) del máximo de \( |D(q)| \) es el símbolo estimado:  
     \[
     \hat{s}(nT_s) = \arg\max_q |D(q)|
     \]  

---

### 3. Ejemplo Numérico (Simplificado)

Supongamos:  
- \( SF = 3 \) (\( 8 \) símbolos posibles).  
- Símbolo transmitido: \( s(nT_s) = 5 \).  

#### En el Transmisor

1. Se genera la chirp con desplazamiento inicial 5.  
2. La señal barre frecuencias según:  
   \[
   \text{Frecuencia en } k = \left[(5 + k) \mod 8\right] \cdot \frac{B}{8}
   \]  

#### En el Receptor

1. Se multiplica la señal recibida por el down-chirp \( e^{-j2\pi k^2 / 8} \).  
2. Se aplica FFT de 8 puntos.  
3. El pico estará en la posición 5, recuperando el símbolo.  

---

### 4. ¿Por qué Funciona?

- **Ortogonalidad**: Las chirps con diferentes \( s(nT_s) \) son ortogonales.
- **Robustez**: El barrido en frecuencia hace que FSCM sea resistente a canales selectivos (mejor que FSK).  

---

### Diagrama de Bloques Conceptual

```
Transmisor:
Bits → Codificación (s(nT_s)) → Chirp Modulado → Canal

Receptor:
Señal Recibida × Down-Chirp → FFT → Detección de Pico → Símbolo Decodificado
```

Este proceso es la esencia de LoRa: bajo consumo, larga distancia y robustez gracias a la modulación chirp y la demodulación basada en FFT.

---

## Detalle sobre Oversampling y el parámetro delta en la modulación LoRa (FSCM)

### ¿Qué es el oversampling (`samples_per_chirp`)?

- **Oversampling** significa tomar más muestras por cada símbolo de las estrictamente necesarias.
- En LoRa, cada símbolo tiene \( N_s = 2^{SF} \) posiciones posibles, pero si se desea una señal más suave o simular una mayor tasa de muestreo (como haría un DAC real), se pueden tomar varias muestras por cada "paso" de símbolo.
- El parámetro `samples_per_chirp` indica **cuántas muestras se toman por cada paso de símbolo**.  
  Ejemplo:  
  Si \( SF=8 \), entonces \( N_s=256 \). Si `samples_per_chirp=4`, se generan \( 256 \times 4 = 1024 \) muestras por símbolo.

### ¿Qué es `delta` y para qué sirve?

- En el código, se define:
  ```python
  delta = 1 / samples_per_chirp
  ```
- `delta` es el **incremento fraccional** que se le suma al índice \( k \) en cada muestra.
- Si no hubiera oversampling, \( k \) avanzaría de a 1 en cada muestra (es decir, \( k = s, s+1, s+2, ... \)).
- Con oversampling, queremos que \( k \) avance más despacio:  
  - Si `samples_per_chirp=4`, entonces para avanzar de un valor entero de \( k \) al siguiente, necesitamos 4 muestras, así que sumamos \( 1/4 \) en cada paso.
- Así, \( k \) avanza de a `delta` en cada muestra, logrando el efecto de oversampling.

**Resumen:**  
- **`samples_per_chirp`**: lo define el usuario, según cuántas muestras quiera por símbolo (mayor valor = señal más suave y precisa).
- **`delta`**: es el paso fraccional para que, al recorrer todas las muestras de un símbolo, \( k \) avance exactamente 1 unidad por cada `samples_per_chirp` muestras.

---

## Explicación detallada del codificador (modulador) y decodificador (demodulador) LoRa (FSCM)

### 1. Codificador (Modulador)

El proceso de modulación en LoRa convierte bits de información en una señal chirp con un desplazamiento de frecuencia inicial.

#### a. Generación del Símbolo (\( s(nT_s) \))

- **Entrada**: Un vector binario \( \mathbf{w}(nT_s) \) de longitud \( SF \) (Spreading Factor).  
  - Ejemplo: Si \( SF = 8 \), se procesan 8 bits por símbolo (\( 2^8 = 256 \) valores posibles).  
- **Cálculo del símbolo**:  
  \[
  s(nT_s) = \sum_{h=0}^{SF-1} \mathbf{w}(nT_s)_h \cdot 2^h
  \]  
  - Esto convierte los bits en un número entero entre \( 0 \) y \( 2^{SF} - 1 \).  
  - Ejemplo: Para \( \mathbf{w} = [1, 0, 1, 1] \) (SF=4), \( s(nT_s) = 1 \cdot 2^0 + 0 \cdot 2^1 + 1 \cdot 2^2 + 1 \cdot 2^3 = 1 + 0 + 4 + 8 = 13 \).

#### b. Generación de la Señal Chirp Modulada

- **Duración del símbolo**: \( T_s = 2^{SF} \cdot T \), donde \( T = 1/B \) (tiempo de muestra).  
- **Señal transmitida**:  
  \[
  c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} e^{j2\pi \left[(s(nT_s) + k) \mod 2^{SF}\right] \frac{k}{2^{SF}}}
  \]
  - **Explicación**:  
    1. **Desplazamiento inicial**: La frecuencia inicial de la chirp está determinada por \( s(nT_s) \).  
    2. **Evolución en el tiempo**: La frecuencia aumenta linealmente con \( k \) (índice de tiempo), creando el barrido chirp.  
    3. **Operación módulo \( 2^{SF} \)**: Garantiza que la señal "repita" su barrido dentro del ancho de banda \( B \).  

- **Ejemplo visual**:  
  - Si \( s(nT_s) = 3 \) y \( SF = 4 \), la chirp comienza en una frecuencia proporcional a 3 y barre hasta \( 2^4 = 16 \) pasos, luego "vuelve a empezar".  

---

### 2. Primeros Bloques del Decodificador (Demodulador)

El demodulador debe recuperar el símbolo \( s(nT_s) \) a partir de la señal recibida \( r(nT_s + kT) \), que incluye ruido. Aquí los pasos clave:

#### a. Señal Recibida

\[
r(nT_s + kT) = c(nT_s + kT) + w(nT_s + kT)
\]  
- \( w(nT_s + kT) \): Ruido blanco gaussiano (AWGN).

#### b. Proyección sobre la Base de Señales

El receptor óptimo calcula la correlación entre la señal recibida y todas las posibles señales chirp (una para cada \( s(nT_s) \)).  

1. **Multiplicación por el "down-chirp"**:  
   - Se multiplica \( r(nT_s + kT) \) por una chirp inversa:  
     \[
     d(nT_s + kT) = r(nT_s + kT) \cdot e^{-j2\pi \frac{k^2}{2^{SF}}}
     \]  
   - **Propósito**: Eliminar el barrido de frecuencia de la chirp, dejando solo el desplazamiento inicial \( s(nT_s) \).  

2. **Transformada de Fourier (FFT)**:  
   - Se aplica una FFT de \( 2^{SF} \) puntos a \( d(nT_s + kT) \):  
     \[
     D(q) = \sum_{k=0}^{2^{SF}-1} d(nT_s + kT) \cdot e^{-j2\pi \frac{qk}{2^{SF}}}
     \]  
   - **Resultado**:  
     - Si no hay ruido, \( D(q) \) tendrá un pico en \( q = s(nT_s) \).  
     - Con ruido, se elige el \( q \) que maximiza \( |D(q)| \).  

3. **Decisión**:  
   - El índice \( l \) del máximo de \( |D(q)| \) es el símbolo estimado:  
     \[
     \hat{s}(nT_s) = \arg\max_q |D(q)|
     \]  

---

### 3. Ejemplo Numérico (Simplificado)

Supongamos:  
- \( SF = 3 \) (\( 8 \) símbolos posibles).  
- Símbolo transmitido: \( s(nT_s) = 5 \).  

#### En el Transmisor

1. Se genera la chirp con desplazamiento inicial 5.  
2. La señal barre frecuencias según:  
   \[
   \text{Frecuencia en } k = \left[(5 + k) \mod 8\right] \cdot \frac{B}{8}
   \]  

#### En el Receptor

1. Se multiplica la señal recibida por el down-chirp \( e^{-j2\pi k^2 / 8} \).  
2. Se aplica FFT de 8 puntos.  
3. El pico estará en la posición 5, recuperando el símbolo.  

---

### 4. ¿Por qué Funciona?

- **Ortogonalidad**: Las chirps con diferentes \( s(nT_s) \) son ortogonales.
- **Robustez**: El barrido en frecuencia hace que FSCM sea resistente a canales selectivos (mejor que FSK).  

---

### Diagrama de Bloques Conceptual

```
Transmisor:
Bits → Codificación (s(nT_s)) → Chirp Modulado → Canal

Receptor:
Señal Recibida × Down-Chirp → FFT → Detección de Pico → Símbolo Decodificado
```

Este proceso es la esencia de LoRa: bajo consumo, larga distancia y robustez gracias a la modulación chirp y la demodulación basada en FFT.

---