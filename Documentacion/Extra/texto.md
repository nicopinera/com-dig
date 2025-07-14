# La modulación LoRa
## 0. Resumen: 
Las redes de área extensa de baja potencia **(LPWAN)** están surgiendo como un nuevo paradigma, especialmente en el ámbito de la conectividad del Internet de las Cosas **(IoT)**. LoRa es una de las LPWAN y está ganando mucha popularidad comercial. La modulación subyacente a LoRa está patentada y nunca se ha descrito teóricamente. 
El objetivo de esta carta es proporcionar la primera descripción rigurosa del procesamiento matemático de señales de los procesos de modulación y demodulación. 
Asimismo, proporcionamos una derivación teórica del receptor óptimo que implica un proceso de demodulación de baja complejidad, utilizando la **Transformada Rápida de Fourier**. 
A continuación, comparamos el rendimiento de la modulación LoRa y la modulación por desplazamiento de frecuencia, tanto en un canal aditivo de ruido blanco gaussiano (AWGN) como en un canal selectivo en frecuencia, demostrando la superioridad de la modulación LoRa en este último. 
Los resultados de esta carta permitirán una evaluación más exhaustiva de las redes basadas en LoRa, mucho más rigurosa que la realizada hasta la fecha.

## 1. Introduccion

Las redes de área amplia de alta potencia (LPWAN) están surgiendo como un nuevo paradigma, especialmente en el campo de Internet de las Cosas (IoT).

LoRa es una de las LPWAN y está ganando bastante terreno comercial. Estrictamente hablando, LoRa es la capa física del sistema LoRaWAN, cuya especificación es mantenida por la LoRa Alliance.
La modulación LoRa está patentada y nunca se ha descrito teóricamente. La patente, de hecho, no proporciona los detalles, en términos de ecuaciones y procesamiento de señales. El artículo 5 ofrece una descripción general de la modulación LoRa, proporcionando algunas ecuaciones básicas y basándose en la intuición del lector para el proceso de decodificación. 
Los artículos 6 y 7 profundizan en la descripción de la señal, la modulación y la demodulación, pero aún carecen de una definición matemática basada en la teoría de señales de los procesos de modulación y demodulación, en parte porque el análisis se limita al dominio analógico. 
Por ejemplo, en [7] se dice que “Para una propagación factor $S$, $log_2(S)$ bits definen $f_0$ ”, es decir, el cambio de frecuencia inicial, pero no hay ninguna explicación de cómo se hace esto.
De hecho, la modulación LoRa suele denominarse **«modulación de chirp»** . Un análisis detallado de LoRa revela que el elemento portador de información es el desplazamiento de frecuencia al inicio del símbolo, y el chirp es similar a una especie de portadora. Por esta razón, en nuestra opinión, LoRa se describe mejor como **Modulación de Chirp por Desplazamiento de Frecuencia (FSCM)**.
El resto del artículo se organiza de la siguiente manera. En la Sección II, se describe el proceso de modulación e identifica la base de señales ortogonales que la caracterizan; en la Sección III, se describe el demodulador óptimo y su implementación eficiente mediante la Transformada Rápida de Fourier; en la Sección IV, se presentan los resultados de experimentos de simulación por computadora sobre el rendimiento a nivel de enlace, comparando también la modulación FSCM con una modulación por desplazamiento de frecuencia (FSK) con la misma cardinalidad. Finalmente, en la Sección V, se presentan las conclusiones del artículo.

## 2. MODULACIÓN DE CHIRP POR DESPLAZAMIENTO DE FRECUENCIA

Supongamos que el ancho de banda del canal que utilizamos para la transmisión es **B** por lo que transmitimos una muestra cada $T=\frac{1}{B}$

Un símbolo $s(n*T_s)$ se envía a la entrada del modulador cada $T_s = 2^{SF} * T$. El símbolo $s(n*T_s)$ es un número real formado utilizando un vector $w(n*T_s)$ de dígitos binarios $SF$, con $SF$ un parámetro entero llamado, en el contexto de LoRa, **Factor de Expansión** (que normalmente toma valores en ${7, 8, 9, 10,11, 12}$) es decir

$s(nT_s) = \sum_{h=0}^{SF-1} w(nT_s)_h .2^h$

Podemos ver que $s(n*T_s)$ toma valores en {0, 1, 2,..., $2^{SF} − 1$}.
La forma de onda transmitida, de duración Ts , para un cierto $s(n*T_s)$ es entonces:

$c(nT_s+ kT) = \frac{1}{\sqrt{2^{SF}}} e^{j2\pi [(s(nT_s)+k)_{mod2^{SF}}]*\frac{k}{2^{SF}}}$

para k = 0 ... $2^{SF} − 1$.

Podemos ver que la señal modulada es una forma de onda de chirrido, ya que la frecuencia aumenta linealmente con k, que es el índice de tiempo; observamos que cada forma de onda difiere de una forma de onda base que tiene Frecuencia inicial igual a 0 por un desplazamiento de frecuencia $s(n*T_s)$. Por eso se denomina FCSM.


Observamos que todo el análisis de la modulación FCSM en esta carta
permanecerá en el dominio discreto Z(T) = {..., −3T, −2T, −T, 0,T, 2T, 3T,...}, es decir, el intervalo fundamental para el análisis de frecuencia es [0, $B = \frac{1}{T}$].
De hecho, cualquier señal en el dominio discreto Z(T) tiene una representación
de frecuencia periódica con período $B = \frac{1}{T}$. Por lo tanto, si uno prefiere tener la FCSM descrita en el intervalo de frecuencia [−B/2,B/2], por ejemplo,para tratar con la señal analítica, la base de señal (4) solo necesita ser multiplicada por $e^{-j2\pi \frac{B}{2}kT} = -1^k$ sin consecuencias en las derivaciones y hallazgos de
la carta actual.

## 3. DETECCIÓN ÓPTIMA DE SEÑALES DE FSCM EN ADITIVOS 
### CANALES DE RUIDO BLANCO GAUSSIANO (AWGN )
.
Dado que tenemos señales de energía iguales y suponemos que son perfectas sincronización de tiempo y frecuencia, así como una fuente que emite símbolos igualmente probables, el receptor óptimo para FSCM

Las señales en un canal AWGN se pueden derivar fácilmente de una descripcion. La señal recibida es: 

$r(nTs + kT ) \cong c(nTs + kT ) + w(nTs + kT )$


donde $w(nTs + kT)$ es un ruido gaussiano blanco de media cero, con
varianza independiente de (nTs + kT). ). El óptimo demodulador consiste en proyectar $r(nTs + kT)$ sobre las diferentes señales $c(nTs + kt )$ con $s(nTs) =q$ , q = 0 a $2^{SF}-1$ y eligiendo la señal c(nTs + kT) de manera que el módulo de la proyección es máximo ya que la mejor estimación de la señal transmitida.  Este proceso proporciona la mejor estimación sˆ(nTs ) = l de la señal transmitida s(nTs)


#### A. Implementación computacionalmente eficien