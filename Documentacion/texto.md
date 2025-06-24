# Trabajo practico integrado Comunicaciones digitales

Este trabajo práctico tiene como objetivo estudiar el funcionamiento del sistema de comunicación LoRaWAN el cual es una red de tipo LPWAN (Low Power Wide Area Network), la cual utiliza LoRa (Long Range) como su tecnología de modulación.

Una LPWAN es una red de telecomunicaciones diseñada específicamente para la comunicación de dispositivos que requieren cobertura de largo alcance y bajo consumo energético, características fundamentales en aplicaciones de Internet de las Cosas (IoT).

Con el fin de analizar en profundidad este sistema, se propone la lectura y el estudio de dos artículos científicos:
1. "Frequency Shift Chirp Modulation: The LoRa Modulation" – Lorenzo Vangelista
2. "From Demodulation to Decoding: Toward Complete LoRa PHY Understanding and Implementation" – Zhenqiang Xu, Shuai Tong, Pengjin Xie y Jiliang Wang

A partir del análisis de estos trabajos, se derivan los siguientes resultados y conclusiones sobre el sistema de modulación y funcionamiento de la capa física (PHY) en LoRaWAN.

## Codificador y Decodificador

### 1. Codificador
La codificación propuesta se realiza mediante el polinomio de numeración posicional en base 2. Para ello, se requiere la elección de un parámetro conocido como **_Spreading Factor_ ($SF$)**, el cual puede tomar los siguientes valores: $\{7,8,9,10,11,12\}$. Este parámetro representa la cantidad de dígitos binarios que conforman un símbolo.

Para generar un símbolo, se utiliza la siguiente ecuación:

$$\Large s(nT_s) = \sum_{h=0}^{\text{SF}-1} \text{w}(nT_s)_h \cdot 2^h$$

Donde:
- $s(nT_s)$ Representa el simbolo resultante
- $\text{w}(nT_s)_h$ Es el digito binario en la posicion $h$
- $2^h$ Es el peso del digito binario, en funcion de la posicion del mismo
- $T_s$ es el período de un símbolo
- $n$ es el índice del símbolo que indica la posición temporal dentro de la secuencia.

Por ejemplo, si se tiene un $SF=8$ y se desea codificar el dato $[0\ 1\ 1\ 1\ 1\ 0\ 0\ 0]$:

$$
s(nT_s) = \sum_{h=0}^{7} \text{w}(nT_s)_h \cdot 2^h = 0 \times 2^7 + 1 \times 2^6 + 1 \times 2^5 + 1 \times 2^4 + 1 \times 2^3 + 0 \times 2^2 + 0 \times 2^1 + 0 \times 2^0 = 120
$$

### 2. Decodificador

El proceso de decodificación consiste en recuperar la secuencia de bits original a partir del símbolo recibido. Esto se logra descomponiendo el valor decimal del símbolo en su representación binaria de $SF$ bits. Matemáticamente, se realiza la conversión inversa:

Dado un símbolo $s(nT_s)$ y un $SF$ determinado, se obtiene el vector de bits $\text{w}(nT_s)_h$ tal que:

$$
s(nT_s) = \sum_{h=0}^{\text{SF}-1} \text{w}(nT_s)_h \cdot 2^h
$$

Por ejemplo, si se recibe el símbolo $s(nT_s) = 120$ y $SF = 8$, la representación binaria es:

$$
120_{10} = 01111000_2
$$

Por lo tanto, la secuencia de bits recuperada es $[0\ 1\ 1\ 1\ 1\ 0\ 0\ 0]$.

## Conformador de onda y conformador de n-tuplas

### 1. Conformador de onda

El proximo paso en nuestro sistema de comunicacion es el conformador de onda o waveform former, el cual es la etapa posterior al codificador. Nuestro conformador de onda implementa la modulación **_Frequency Shift Chirp Modulation_ (FSCM)**.

En esta modulación, cada símbolo se asocia a una frecuencia inicial determinada por su valor decimal $s(nT_s)$  A partir de esta frecuencia, la señal modulada presenta un barrido lineal en frecuencia (tipo chirp), donde la frecuencia incrementa linealmente con el tiempo, siguiendo el índice $k=0,1,...,2^{SF}-1$, hasta alcanzar un valor máximo de $2^{SF}$. 

Luego, la frecuencia decae hasta 0 y vuelve a incrementarse, completando así una oscilación en frecuencia que regresa al valor inicial. Esta modulación al realizarse con una señal compleja, se compone de una componente real o fase (I) y otra componente imaginaria o cuadratura (Q). Esto se representa por la siguiente ecuacion: 


$$\Large c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} \cdot e^{j2\pi[(s(nT_s)+k)\cdot{\bmod{2^{SF}}}](kT\frac{B}{2^{SF}})}\quad k=0,...,2^{SF}-1$$

En la misma: 
- Toma un símbolo codificado $𝑠∈{0,1,...,2^{𝑆𝐹}−1}$
- Lo inserta como un shift de frecuencia inicial en una señal chirp.
- Genera una onda compleja cuya frecuencia aumenta linealmente en el tiempo (chirp) y comienza en una frecuencia determinada por **𝑠**.

Aplicando la ecuación de **Euler** se llega a la siguiente expresión equivalente:

$$c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} \cdot \left[ \cos\left(2\pi \cdot \left((s(nT_s) + k) \bmod 2^{SF}\right) \cdot k\frac{T B}{2^{SF}}\right) + j \cdot \sin\left(2\pi \cdot \left((s(nT_s) + k) \bmod 2^{SF}\right) \cdot k\frac{T B}{2^{SF}}\right) \right] \quad k = 0, \dots, 2^{SF} - 1$$

De este modo, se muestran claramente las dos partes ortogonales de la señal: la componente en fase, asociada al **coseno** (parte real), y la componente en cuadratura, asociada al **seno** (parte imaginaria)

Analizando las ecuación se pueden observar:


- $k$ Es el indice de tiempo discreto que actua como contador haciendo que la frecuencia aumente linealmente.
- La frecuencia inicial (cuando $k=0$) viene dado por el valor del simbolo $s(nT_s)$
- El modulo de $(s(nT_s) + k)$ en base $2^{SF}$ ($(s(nT_s) + k) \bmod 2^{SF}$) tiene por fin limitar el crecimiento lineal de la frecuencia hasta un valor de frecuencia maximo $2^{SF}-1$ con el proposito de limitar el ancho de banda. Esta operacion genera un discontinuidad en la frecuencia haciendo que la misma caiga desde el valor maximo hasta $0$ para luego continuar creciendo hasta el valor inicial $s(nT_s)$ finalizando el periodo $T_s$ del simbolo.
- El factor $\frac{1}{\sqrt{2^{SF}}}$ tiene por fin normalizar la potencia de la señal
- El periodo de muestreo $\frac{TB}{2^{SF}}$

### 2. Formador de ntuplas

El formador de n-tuplas (o n-tuple former) es una etapa fundamental en la recepción de señales LoRa, ya que permite identificar el símbolo transmitido a partir de la señal recibida. Su función principal es correlacionar la señal recibida con todas las posibles formas de onda base (chirps) generadas por los diferentes símbolos posibles, para determinar cuál de ellas se encuentra presente en la señal.

En la práctica, esto se realiza aplicando una proyección (producto interno) de la señal recibida $r(nT_s + kT)$ sobre cada una de las bases conjugadas $c^*(nT_s + kT)$ asociadas a los posibles valores de símbolo $q$. El símbolo detectado será aquel que maximice el valor absoluto de la correlación.

Matemáticamente, la proyección se expresa como:

$$\langle r(nT_s+kT),c(nT_s+kT)|_{s(nT_s)=q} \rangle$$

$$=\sum_{k=0}^{2^{SF}-1}r(nT_s+kT)\, \cdot \, c^*(nT_s+kT)|_{s(nT_s)=q}$$

Para simplificar el procesamiento, se suele realizar una operación de dechirping, que consiste en multiplicar la señal recibida por el conjugado de un chirp de referencia. Esto transforma la señal chirp en una señal de frecuencia constante, facilitando la detección mediante una transformada de Fourier discreta (DFT):

$$d(nT_s + kT)=r(nT_s + kT) \cdot e^{-j2\pi \frac{k^2}{2^{\text{SF}}}}$$

Luego, se calcula la DFT de $d(nT_s + kT)$:

$$\sum_{k=0}^{2^{SF}-1}d(nT_s + kT)\, \cdot \,\frac{1}{\sqrt{2^{SF}}}e^{-j2\pi p k \frac{1}{2^{SF}}}$$

El índice $p$ para el cual la DFT alcanza su máximo corresponde al símbolo transmitido. Así, el formador de n-tuplas permite recuperar el valor original del símbolo a partir de la señal recibida, aprovechando la ortogonalidad de los chirps generados por los diferentes símbolos.

### 3. Symbol error rate

El _Symbol Error Rate_ (SER), similar al BER, representa la proporción de simbolos recibidos con error respecto al total de simbolos transmitidos. Se calcula de la siguiente forma:

$$SER=\frac{\text{número de simbolos erróneos}}{\text{total de simbolos transmitidos}}$$