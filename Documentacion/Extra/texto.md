# Trabajo práctico integrado Comunicaciones digitales

Alumnos:

- Krede Julian
- Piñera, Nicolas

---

## Introducción

Este trabajo práctico tiene como objetivo estudiar el funcionamiento del sistema de comunicación LoRaWAN el cual es una red de tipo LPWAN (Low Power Wide Area Network), la cual utiliza LoRa (Long Range) como su tecnología de modulación.

Una LPWAN es una red de telecomunicaciones diseñada específicamente para la comunicación de dispositivos que requieren cobertura de largo alcance y bajo consumo energético, características fundamentales en aplicaciones de Internet de las Cosas (IoT).

Con el fin de analizar en profundidad este sistema, se propone la lectura y el estudio de dos artículos científicos:

1. **"Frequency Shift Chirp Modulation: The LoRa Modulation"** – Lorenzo Vangelista
2. **"From Demodulation to Decoding: Toward Complete LoRa PHY Understanding and Implementation"** – Zhenqiang Xu, Shuai Tong, Pengjin Xie y Jiliang Wang

A partir del análisis de estos trabajos, se derivan los siguientes resultados y conclusiones sobre el sistema de modulación y funcionamiento de la capa física (PHY) en LoRaWAN.

### 1.2 Codificador

La codificación propuesta se realiza mediante el polinomio de numeración posicional en base 2. Para ello, se requiere la elección de un parámetro conocido como **_Spreading Factor_ ($SF$)**, el cual puede tomar los siguientes valores: $\{7,8,9,10,11,12\}$. Este parámetro representa la cantidad de dígitos binarios que conforman un símbolo.

Para generar un símbolo, se utiliza la siguiente ecuación:

$$\Large s(nT_s) = \sum_{h=0}^{\text{SF}-1} \text{w}(nT_s)_h \cdot 2^h$$

Donde:

- $s(nT_s)$: Representa el símbolo resultante
- $w(nT_s)_h$: Es el digito binario en la posición $h$
- $2^h$: Es el peso del digito binario, en función de la posición del mismo
- $T_s$: Tiempo total que dura un símbolo $(T_s=2^{SF}*T = \frac{2^{SF}}{B})$
- $n$ es el índice del símbolo que indica la posición temporal dentro de la secuencia.

Por ejemplo, si se tiene un $SF=8$ y se desea codificar el dato $[0\ 1\ 1\ 1\ 1\ 0\ 0\ 0]$:

$$s(nT_s) = \sum_{h=0}^{7} \text{w}(nT_s)_h \cdot 2^h = 0 \times 2^7 + 1 \times 2^6 + 1 \times 2^5 + 1 \times 2^4 + 1 \times 2^3 + 0 \times 2^2 + 0 \times 2^1 + 0 \times 2^0 = 120$$

Se realiza la función que se va a encargar de codificar los bits generados en símbolos a transmitir, por medio de la ecuación presentada en el documento. Este codificador recibe por parámetro los bits generados y el SF (Spreading Factor)

### 1.3 Decodificador

El decodificador implementa el algoritmo de divisiones sucesivas por 2 (Base Binaria) para recuperar el dato a partir del símbolo recibido. El procedimiento consiste en dividir el número original entre 2 de forma repetida. En cada división, se registra el residuo o módulo (que siempre será 0 o 1), y se reemplaza el número por el cociente entero obtenido. Este proceso se repite hasta que el cociente sea igual a cero. Finalmente, el número binario se construye leyendo los residuos en orden inverso al que fueron generados; es decir, desde el último hasta el primero.

$$\large \mathbf{w}(nT_s)_h = \left( \left\lfloor \frac{s(nT_s)}{2^h} \right\rfloor \bmod 2 \right), \quad h = 0, 1, \dots, SF - 1$$

$$
\mathbf{w}(nT_s) = \left[
\left\lfloor \frac{s(nT_s)}{2^0} \right\rfloor \bmod 2,\
\left\lfloor \frac{s(nT_s)}{2^1} \right\rfloor \bmod 2,\
\ldots,\
\left\lfloor \frac{s(nT_s)}{2^{SF - 1}} \right\rfloor \bmod 2
\right]
$$

El _Bit Error Rate_ (BER) representa la proporción de bits recibidos con error respecto al total de bits transmitidos. Se calcula de la siguiente forma:

$$BER=\frac{\text{número de bits erróneos}}{\text{total de bits transmitidos}}$$

## 2. Conformador de onda y conformador de n-tuplas

### 2.1 Conformador de onda

El próximo paso en nuestro sistema de comunicación es el conformador de onda o waveform former, el cual es la etapa posterior al codificador y ambos componen el bloque del transmisor. El conformador de onda implementa la modulación **_Frequency Shift Chirp Modulation_ (FSCM)**.

En esta modulación, cada símbolo se asocia a una frecuencia inicial $s(nT_s)$. A partir de esta frecuencia, la señal modulada presenta un barrido lineal en frecuencia (tipo chirp), donde la frecuencia incrementa linealmente con el tiempo, siguiendo el índice $k=0, 1, … ,2^{SF}-1$, hasta alcanzar un valor máximo de $2^{SF}$.

Luego, la frecuencia decae hasta 0 y vuelve a incrementarse hasta volver al valor de $s(nT_s)$, completando así el periodo del símbolo $T_s$. Esta modulación al realizarse con una señal compleja, se compone de una componente real o fase (I) y otra componente imaginaria o cuadratura (Q). Esto se representa por la siguiente ecuación:

$$\Large c(nT_s + kT) = \frac{1}{\sqrt{2^{SF}}} \cdot e^{j2\pi[(s(nT_s)+k){\bmod{2^{SF}}}](kT\frac{B}{2^{SF}})}\quad k=0,...,2^{SF}-1$$

En la misma:

- Toma un símbolo codificado $𝑠∈{0, 1,...,2^{𝑆𝐹}−1}$
- Lo inserta como un shift de frecuencia inicial en una señal chirp.
- Genera una onda compleja cuya frecuencia aumenta linealmente en el tiempo (chirp) y comienza en una frecuencia determinada por **𝑠**.

$c(nT_s + kT)$ es una función que tiene dos argumentos constantes $T_s$ que representa el tiempo que dura un símbolo y $T$ que representa el periodo de muestreo dentro de cada símbolo. El primer argumento $kT$ nos dice dónde va a existir la señal (donde se muestrea).

Se conforma una señal compleja (exponencial) la cual podríamos verla como una $e^{j2\pi f t} = cos(2\pi f t) + j.sen(2\pi f t)$ (relación de Euler). Donde:

- $f(kT)=(s(nT_s)+k) \bmod 2^{SF}\cdot \frac{B}{2^{SF}}$
- $t=kT$

Dado que se tiene una señal de frecuencia variable, la fase de la señal modulada se obtiene integrando la frecuencia instantánea a lo largo del tiempo. Esto permite expresar la señal modulada como una exponencial compleja cuya fase varía cuadráticamente con el tiempo, característica fundamental de los chirps utilizados en LoRa.
Para obtener la fase $\phi(t)$ de la exponencial compleja en $c(nT_s + kT)$:

$$\phi(t)=2\pi\int^t_0{f(\tau)d\tau} $$

En el dominio discreto $k=\frac{\tau}{T}$ Entonces:

$$\phi(t) =2\pi \int^t_0 \left[(s+\frac{\tau}{T}) \frac{B}{2^{SF}}\right]d\tau =2\pi \frac{B}{2^{SF}} \int^t_0 \left[(s+\frac{\tau}{T})\right]d\tau =2\pi \frac{B}{2^{SF}}\left[s t +\frac{t^2}{2T}\right]$$

Entonces. Remplazando $t$ por $kT$:

$$\phi(kT) = 2\pi \frac{B}{2^{SF}}\left[s (kT)+\frac{(kT)^2}{2T}\right]$$

Se llega a:

$$\phi(kT) = 2\pi \frac{B\cdot T}{2^{SF}}\left[s\cdot k+\frac{k^2}{2}\right]= 2\pi \frac{B\cdot T}{2^{SF}}(s+\frac{k}{2})k$$
$$\phi(kT)= 2\pi (s+\frac{k}{2})\frac{B}{2^{SF}}\cdot t$$

Esto muestra por qué en la implementación del código se calcula el argumento de la exponencial como:
$$\text{arg}= f\cdot t \cdot 0.5 \quad f\neq s$$

Analizando las ecuaciones se pueden observar:

- $k$ Es el índice de tiempo discreto que varía la frecuencia linealmente.
- La frecuencia inicial (cuando $k=0$) viene dado por el valor del símbolo $s(nT_s)$
- El módulo de $(s(nT_s) + k)$ en base $2^{SF}$ tiene por fin limitar el crecimiento lineal de la frecuencia hasta un valor de frecuencia máximo $2^{SF}-1$ con el propósito de limitar el ancho de banda. Esta operación genera un discontinuidad en la frecuencia haciendo que la misma caiga desde el valor máximo hasta $0$ para luego continuar creciendo hasta el valor inicial $s(nT_s)$ finalizando el periodo $T_s$ del símbolo.

A continuación, se presenta el **conformador de onda**. Por cada símbolo codificado, genera su función chirps compleja, devuelve una matriz en la cual cada fila tiene los valores de la función chirp correspondiente a su símbolo, y en las columnas tiene los valores de esa función chirp en cada tiempo de muestreo

### 2.2 Formador de ntuplas

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

## 3. Canal

En este apartado se utilizarán dos tipos de canales simulados

- Canal **AWGN**
- Canal **Selectivo en Frecuencia**

Con el fin de verificar y validar el funcionamiento del software realizado para posteriormente llevarlo a una implementación en un canal real

### 3.1 Canal AWGN

El primer canal a simular es el **canal AWGN** el cual suma un ruido blanco gaussiano a la señal transmitida, ruido que tiene una distribución normal con media cero y varianza $\sigma^2$. El modelo matemático propuesto por Vangelista es el siguiente:

$$r(nT_s+kT)=c(nT_s +kT)+w(nT_s +kT)$$

Donde:

- $𝑐(𝑛𝑇_𝑠+𝑘𝑇)$ : es la señal chirp transmitida para el símbolo $𝑠$
- $𝑤(𝑛𝑇_𝑠+𝑘𝑇)$ : es ruido blanco gaussiano complejo
- $r(nT_s+kT)$ : es la señal recibida

La señal transmitida es una secuencia de muestras complejas (un chirp), y a cada muestra le suma un valor complejo aleatorio. Ahora simularemos el canal AWGN sin el componente de filtrado del canal, es decir, únicamente agregando ruido al a señal.

#### 3.1.1 Obtención de la potencia del ruido a partir de la SNR

La potencia de una señal aleatoria $x$ se define como:

$$P_x = \mathbb{E}[|x|^2]$$

Donde $|x|^2 = x.x^*$, producto de $x$ por su conjugado.

Desarrollando la expresión:

$$P_x=\mathbb{E}[(x - \mu +\mu)^2] =\mathbb{E}[(x - \mu)^2] + |\mu|^2 + 2\cdot \mathbb{E}[x - \mu]$$

Donde:

$2\cdot \mathbb{E}[x - \mu]=2 (\mathbb{E}[x]−\mathbb{E}[\mu])=2\cdot (\mu-\mu)=0$

$\mathbb{E}[(x - \mu)^2]=Var(x)$

Entonces:

$$P_x = \mathbb{E}[|x|^2]=\text{Var}(x) + |\mu|^2$$

Ecuación que utilizaremos para calcular la potencia de la señal transmitida

Si la media es cero ($\mu=0$):

$$P_x = \text{Var}(x) = \sigma^2$$

Ecuación utilizada para calcular la potencia de ruido al ser un canal AWGN

En AWGN, las partes real e imaginaria son independientes e idénticamente distribuidas cada una con varianza $\frac{\sigma^2}{2}$, si $x = a + jb$ entonces $P_x = Var(a) + Var(b)= \frac{\sigma^2}{2} + \frac{\sigma^2}{2}  = \sigma^2$

Para modelar el canal se utiliza un ruido complejo con distribución normal, cuya desviación estándar para la parte real e imaginaria que cumpla la descripción matemática anterior es:

$$\sigma = \sqrt{\frac{Potencia_{Ruido}}{2}}$$

La Relación Señal Ruido se define como $SNR = \frac{P_s}{P_n}$ siendo $P_s$ la potencia de la señal y $P_n$ la potencia del ruido. Para calcular la SNR en decibelios se utiliza la siguiente formula

$$\large \text{SNR}_{dB}=10\cdot log(\frac{P_s}{P_n})$$

Despejando, la potencia de Ruido se puede calcular realizando

$$\large P_n=\frac{P_s}{10^{\frac{\text{SNR}_{dB}}{10}}}$$

#### 3.1.2 Canal Flat

La modulación FSCM está realizada sobre un **canal plano (Flat)** con la suma de ruido gaussiano blanco (AWGN). Un canal plano en frecuencia es un canal cuya respuesta en frecuencia es constante dentro del ancho de banda de la señal, no hay distorsión selectiva: todos los componentes de frecuencia de la señal se ven afectados igual.

### 3.2 Canal selectivo en frecuencia

El modelo de canal selectivo en frecuencia que propone Vangelista es un canal _multipath_ (de múltiples trayectorias) lo que este canal modela es que la señal rebota en objetos del entorno (paredes, árboles, etc.) y llega al receptor con varios retardos y distintas potencias, de esta manera distorsiona la señal, porque introduce interferencia Inter símbolo (ISI). La respuesta al impulso del canal matemáticamente:

$$h[nT]=\sqrt{0.8}\cdot\delta[nT]+\sqrt{0.2}\cdot\delta[nT-T]$$

Esto significa que el canal tiene dos trayectorias:

- Una señal principal (sin retardo) con ganancia $\sqrt{0.8}$
- Una segunda señal (retrasada 𝑇) con ganancia $\sqrt{0.2}$

Cuya transformada de Fourier es:

$$H(f)=\sqrt{0.8}+\sqrt{0.2}\cdot e^{-j2\pi f T}$$

Donde $f=\frac{f_{real}}{f_s}$ con

- $f_{s}$ : frecuencia de muestreo

Suponiendo $T=1$ tiempo normalizado

$$H(f)=\sqrt{0.8}+\sqrt{0.2}\cdot e^{-j2\pi f }$$

Se puede observar su efecto sobre señales para distintos valores de frecuencia:

|  f   | magnitud de H(f) |        Efecto        |
| :--: | :--------------: | :------------------: |
| 0.25 |        1         |  Sin interferencia   |
| 0.5  |       0.45       |  Maxima atenuación   |
| 0.75 |        1         |  Sin interferencia   |
|  1   |       1.34       | Maxima amplificación |

Como se puede observar el filtro del canal es un filtro rechaza-banda
