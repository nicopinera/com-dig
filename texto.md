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