# Proyecto integrador
No hay que hacer el proyecto por tareas, sino hay que realizarlo completo e ir presentando, se evalúa el proceso.


El codificador lleva de bit a números decimales. Se espera ver la implementación de la ecuación tal cual como esta en el paper con sus sumas y exponentes, igual en su decodificador (desplazar el numero a la izquierda y realizar divisiones por 2)


Ecuación (2)  $"c(nT_s + kT)"$ es una función que tiene dos argumentos contantes Ts y T son los tiempos a utilizar, Ts es tiempo de símbolos de modulación lora y T es el tiempo de muestreo o funcionamiento del sistema, el Ts es el mayor, el índice k y m marcan cuantos T entran en un Ts. En esa parte se realiza una aritmética de argumentos que modifica la forma de la señal, con las sumas y restas se producen desplazamientos de la señal para cualquiera de los dos lados, como los índices están asociados al tiempo se realizar desplazamientos temporales. Organizamos la funcion en una base de tiempo. El primer argumento "kT" nos dice donde va a existir la señal, marca donde se va a generar la señal (donde se muestrea la señal). K vuelve a 0 cuando termina de muestrear un simbolo o sea termina un $T_s$ se va a ir desplazando la generación de la señal según los nuevos símbolos.

> Simularlo con dos bucles for uno grande por cada $n$ y dentro el bucle for que varié según $k$

Se conforma una señal compleja (exponencial) la cual podríamos verla como una $e^{2.pi.f.j} = cos(2.pi.f) + j.sen(2.pi.f)$ (relación de Euler - utilizarla para graficarla) su frecuencia se va a modificar según los valores de k y los valores decimales o valores codificados, la información viaja en la frecuencia y la tenemos en el primer instante de muestreo (k=0). El modulo que se presenta en la ecuación cumple la función de limitar el ancho de banda.

Cuando llega la señal se proyecta sobre la base del receptor o sea realizamos el producto interno. Algo similar se realiza en el receptor entre la función recibida y las funciones de la base del receptor, cuya base tiene que ser ortogonal. Se parte de eso para encontrar la ecuación.

$SNR_{dB} = 10 log(S/n)$ (potencia de la señal / potencia del ruido) esto es el valor que toma la varianza del ruido AWGN que se le suma al canal

BER = Cantidad de bit errados / Bit totales transmitidos