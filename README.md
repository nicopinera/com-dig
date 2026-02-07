# Trabajo práctico integrado - Comunicaciones digitales

Alumnos:

- Krede, Julian
- Piñera, Nicolas

---

## Introducción

Este trabajo práctico tiene como objetivo estudiar el funcionamiento de la tecnología de modulación LoRa, utilizada en la capa física del protocolo de red LoRaWAN, el cual pertenece a la categoría de redes LPWAN (Low Power Wide Area Network).

LPWAN es una categoría de redes diseñada específicamente para la comunicación de dispositivos que requieren cobertura de largo alcance y bajo consumo energético, características fundamentales en aplicaciones de Internet de las Cosas (IoT).

Con el fin de analizar en profundidad esta modulación, se propone la lectura y el estudio de dos artículos científicos: [1] y [2]

A partir del análisis de estos trabajos, se presentan los siguientes resultados y conclusiones sobre el sistema de modulación y el funcionamiento de la capa física (PHY) en LoRaWAN

## 1. Codificador y Decodificador

### 1.1 Generador de Bits

Utilizando una Jupyter Notebook, generamos un array binario con distribucion uniforme el cual seran nuestros bits a transmitir, tiene una longitud multiplo del **SF (Spreading Factor)**

### 1.2 Codificador

La codificación propuesta en [1] se realiza mediante el polinomio de numeración posicional en base 2. Para ello, se requiere la elección de un parámetro conocido como **_Spreading Factor_ ($SF$)**, el cual puede tomar los siguientes valores: $\{7,8,9,10,11,12\}$. Este parámetro representa la cantidad de dígitos binarios que conforman un símbolo.

Para generar un símbolo, se utiliza la siguiente ecuación:

$$\Large s(nT_s) = \sum_{h=0}^{\text{SF}-1} \text{w}(nT_s)_h \cdot 2^h$$

Donde:

- $s(nT_s)$: Representa el símbolo resultante
- $w(nT_s)_h$: Es el dígito binario en la posición $h$
- $2^h$: Es el peso del dígito binario, en función de la posición del mismo
- $T_s$: Tiempo total que dura un símbolo $(T_s=2^{SF}*T = \frac{2^{SF}}{B})$
- $n$ es el índice del símbolo que indica la posición temporal dentro de la secuencia.

Por ejemplo, si se tiene un $SF=8$ y se desea codificar el dato $[0\ 1\ 1\ 1\ 1\ 0\ 0\ 0]$:

$$s(nT_s) = \sum_{h=0}^{7} \text{w}(nT_s)_h \cdot 2^h = 0 \times 2^7 + 1 \times 2^6 + 1 \times 2^5 + 1 \times 2^4 + 1 \times 2^3 + 0 \times 2^2 + 0 \times 2^1 + 0 \times 2^0 = 120$$

### 1.3 Decodificador

El decodificador propuesto en [1] implementa el algoritmo de divisiones sucesivas por 2 (Base Binaria) para recuperar el dato a partir del símbolo recibido. El procedimiento consiste en dividir el número original entre 2 de forma repetida. En cada división, se registra el residuo o módulo (que siempre será 0 o 1), y se reemplaza el número por el cociente entero obtenido. Este proceso se repite hasta que el cociente sea igual a cero. Finalmente, el número binario se construye leyendo los residuos en orden inverso al que fueron generados; es decir, desde el último hasta el primero.

$$\large \mathbf{w}(nT_s)_h = \left( \left\lfloor \frac{s(nT_s)}{2^h} \right\rfloor \bmod 2 \right), \quad h = 0, 1, \dots, SF - 1$$

$$
\mathbf{w}(nT_s) = \left[
\left\lfloor \frac{s(nT_s)}{2^0} \right\rfloor \bmod 2,\
\left\lfloor \frac{s(nT_s)}{2^1} \right\rfloor \bmod 2,\
\ldots,\
\left\lfloor \frac{s(nT_s)}{2^{SF - 1}} \right\rfloor \bmod 2
\right]
$$

### 1.4 Bit error rate

El _Bit Error Rate_ (BER) representa la proporción de bits recibidos con error respecto al total de bits transmitidos. Se calcula de la siguiente forma:

$$BER=\frac{\text{número de bits erróneos}}{\text{total de bits transmitidos}}$$

![Imagen1](https://github.com/user-attachments/assets/31ecf1a7-321c-4eae-b0fc-4bae4595d368)

---

## 2. Conformador de onda y conformador de n-tuplas

### 2.1 Conformador de onda

El próximo paso en nuestro sistema de comunicación es el conformador de onda o waveform former, el cual es la etapa posterior al codificador y ambos componen el bloque del transmisor. El conformador de onda propuesto en [1] implementa la modulación **_Frequency Shift Chirp Modulation_ (FSCM)**.

En esta modulación, cada símbolo se asocia a una frecuencia inicial $s(nT_s)$. A partir de esta frecuencia, la señal modulada presenta un barrido lineal en frecuencia (tipo chirp), donde la frecuencia incrementa linealmente con el tiempo, siguiendo el índice $k=0, 1, … ,2^{SF}-1$, hasta alcanzar un valor máximo de $2^{SF}$.

Luego, la frecuencia decae hasta 0 y vuelve a incrementarse hasta volver al valor de $s(nT_s)$, completando así el periodo del símbolo $T_s$. Esta modulación al realizarse con una señal compleja, se compone de una componente real o fase (I) y otra componente imaginaria o cuadratura (Q). Esto se representa por la siguiente ecuación:

$$\Large c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} \cdot e^{j2\pi[(s(nT_s)+k){\bmod{2^{SF}}}](kT\frac{B}{2^{SF}})}\quad k=0,...,2^{SF}-1$$

En la misma:

- Toma un símbolo codificado $𝑠∈{0, 1,...,2^{𝑆𝐹}−1}$
- Lo inserta como un shift de frecuencia inicial en una señal chirp.
- Genera una onda compleja cuya frecuencia aumenta linealmente en el tiempo (chirp) y comienza en una frecuencia determinada por **𝑠**.

$c(nT_s + kT)$ es una función que tiene dos argumentos constantes $T_s$ que representa el tiempo que dura un símbolo y $T$ que representa el periodo de muestreo dentro de cada símbolo. El primer argumento $kT$ nos dice dónde va a existir la señal (donde se muestrea).

Analizando las ecuaciones se pueden observar:

- $k$ Es el índice de tiempo discreto que varía la frecuencia linealmente.
- La frecuencia inicial (cuando $k=0$) viene dado por el valor del símbolo $s(nT_s)$
- El módulo de $(s(nT_s) + k)$ en base $2^{SF}$ tiene por fin limitar el crecimiento lineal de la frecuencia hasta un valor de frecuencia máximo $2^{SF}-1$ con el propósito de limitar el ancho de banda. Esta operación genera un discontinuidad en la frecuencia haciendo que la misma caiga desde el valor máximo hasta $0$ para luego continuar creciendo hasta el valor inicial $s(nT_s)$ finalizando el periodo $T_s$ del símbolo.

### 2.2 Formador de n-tuplas

Para recuperar el símbolo modulado se proyecta la señal recibida $r(nT_s + kT)$ en el conjunto de bases conjugadas con las que se moduló la señal, en nuestro caso la base con la que se modulo la señal está formada por una única señal $c(nT_s + kT)$. Por lo tanto, la proyección:

$$\langle r(nT_s+kT),c(nT_s+kT)|_{s(nT_s)=q} \rangle$$

$$=\sum_{k=0}^{2^{SF}-1}r(nT_s+kT)\, \cdot \, c^*(nT_s+kT)|_{s(nT_s)=q}$$

Se llega a la siguiente expresión:

$$=\sum_{k=0}^{2^{SF}-1}\underbrace{r(nT_s + kT) \cdot e^{-j2\pi \frac{k^2}{2^{\text{SF}}}}}_{d(nT_s + kT)}\, \cdot \,\frac{1}{\sqrt{2^{SF}}}e^{-j2\pi p k \frac{1}{2^{SF}}}$$

Reescribiendo el producto:
$$d(nT_s + kT)=r(nT_s + kT) \cdot e^{-j2\pi \frac{k^2}{2^{\text{SF}}}}$$

Se tiene:

$$\sum_{k=0}^{2^{SF}-1}d(nT_s + kT)\, \cdot \,\frac{1}{\sqrt{2^{SF}}}e^{-j2\pi p k \frac{1}{2^{SF}}}$$

La cual es la transformada de Fourier discreta de la señal $d(nT_s + kT)$

### 2.3 Symbol error rate (SER)

El _Symbol Error Rate_ (SER), similar al BER, representa la proporción de símbolos recibidos con error respecto al total de símbolos transmitidos. Se calcula de la siguiente forma:

$$SER=\frac{\text{número de símbolos erróneos}}{\text{total de símbolos transmitidos}}$$

Los símbolos que salen del **n-tuple former** y se comparan con los símbolos que entran al **waveform former**

![Imagen1](https://github.com/user-attachments/assets/cfa1d79f-c1a5-4ba6-9e48-7fedce5bdb68)

---

## 3. Canal

En este apartado se utilizarán dos tipos de canales simulados

- Canal **AWGN**
- Canal **Selectivo en Frecuencia**

Con el fin de verificar y validar el funcionamiento del software desarrollado para posteriormente llevarlo a una implementación en un canal real

### 3.1 Canal AWGN

El primer canal a simular es el **canal AWGN** el cual suma un ruido blanco gaussiano a la señal transmitida, ruido que tiene una distribución normal con media cero y varianza $\sigma^2$. El modelo matemático típico de un canal AWGN es el siguiente:

$$r(nT_s+kT)=c(nT_s +kT)+w(nT_s +kT)$$

Donde:

- $𝑐(𝑛𝑇_𝑠+𝑘𝑇)$ : es la señal chirp transmitida para el símbolo $𝑠$
- $𝑤(𝑛𝑇_𝑠+𝑘𝑇)$ : es ruido blanco gaussiano complejo
- $r(nT_s+kT)$ : es la señal recibida

La señal transmitida es una secuencia de muestras complejas (un chirp), y a cada muestra le suma un valor complejo aleatorio.

### 3.2 Canal selectivo en frecuencia

El modelo de canal selectivo en frecuencia que se propone en [1] es un canal _multipath_ (de múltiples trayectorias) lo que este canal modela es que la señal rebota en objetos del entorno (paredes, árboles, etc.) y llega al receptor con varios retardos y distintas potencias, de esta manera distorsiona la señal, porque introduce interferencia Inter símbolo (ISI). La respuesta al impulso del canal matemáticamente:

$$h[nT]=\sqrt{0.8}\cdot\delta[nT]+\sqrt{0.2}\cdot\delta[nT-T]$$

Esto significa que el canal tiene dos trayectorias:

- Una señal principal (sin retardo) con ganancia $\sqrt{0.8}$
- Una segunda señal (retrasada 𝑇) con ganancia $\sqrt{0.2}$

Cuya transformada de Fourier continua es:

$$H(f)=\sqrt{0.8}+\sqrt{0.2}\cdot e^{-j2\pi f T}$$

Suponiendo $T=1$ tiempo normalizado

$$H(f)=\sqrt{0.8}+\sqrt{0.2}\cdot e^{-j2\pi f }$$

Se puede observar su efecto sobre señales para distintos valores de frecuencia:

|  f   | magnitud de H(f) |        Efecto        |
| :--: | :--------------: | :------------------: |
| 0.25 |        1         |  Sin interferencia   |
| 0.5  |       0.45       |  Maxima atenuación   |
| 0.75 |        1         |  Sin interferencia   |
|  1   |       1.34       | Maxima amplificación |

![Imagen1](https://github.com/user-attachments/assets/3d7abb8f-426f-4287-882c-0cb3f746db30)

---

## Quinta Parte: Implementación del sistema LoRa en el SDR

A partir del Paper de referencia **"From Demodulation to Decoding: Toward Complete LoRa PHY Understanding and Implementation"** implementar la transmisión de tramas LoRa en el transmisor

![Imagen1](https://github.com/user-attachments/assets/c41dd4a1-3875-476c-93e6-6d9e0f03841c)

y las etapas de Dechirping, Window Alignment, Peak Merging y clock Recovery en el receptor

![Imagen1](https://github.com/user-attachments/assets/3f183028-e22e-4c90-804e-7eb645634e3b)

Probar el sistema futilizando en los SDRs para el envío de mensajes cortos.

Utilizar ademas una celda de la Jupyter Notebook para desarrollar la matematica, conceptualizar la teoría y/o lógica utilizada en el algoritmo propuesto por ud.

**Nota:** Para optimizar el rendimiento de las etapas a diseñar utilizar los recursos brindados por la biblioteca numpy, evitando utilizar listas.

---

## Información relevante y referencias

- **Codificador/Decodificador:** Implementados según la ecuación (1) del paper, usando operaciones vectorizadas para conversión bits ↔ símbolos.
- **Waveform Former/n-Tuple Former:** Basados en la ecuación (2) y la sección III del paper de Vangelista, con generación y demodulación chirp usando Numpy y FFT.
- **Canal AWGN:** Ruido generado con distribución normal compleja, varianza ajustada por SNR.
- **Canal selectivo:** Implementado por convolución discreta con la respuesta al impulso propuesta.
- **Curvas BER/SER:** Calculadas y graficadas para ambos escenarios de canal, validando la robustez del sistema LoRa.

### Ecuaciones clave

- **Codificación símbolo:** $s(nT_s) = \sum_{h=0}^{SF-1} w(nT_s)_h \cdot 2^h$
- **Waveform Former:** $c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} e^{j2\pi \left[(s(nT_s) + k) \mod 2^{SF}\right] \frac{k}{2^{SF}}}$
- **Demodulación (n-Tuple Former):** Downchirp $\cdot$ FFT, símbolo estimado por el máximo de la FFT.
- **Canal selectivo:** $h(nT) = \sqrt{0.8}\,\delta(nT) + \sqrt{0.2}\,\delta(nT-T)$

### Referencias

- Vangelista, L. "Frequency Shift Chirp Modulation: The LoRa Modulation"
- Xu, Z., Tong, S., Xie, P., Wang, J. "From Demodulation to Decoding: Toward Complete LoRa PHY Understanding and Implementation"
- Apuntes y ejemplos de clase

---
