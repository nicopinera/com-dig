import numpy as np
import matplotlib.pyplot as plt
from funciones import calculador_ber, calculador_ser, codificador, conformador_de_onda, decodificador, formador_de_ntuplas, generate_random_bits, graficar_chirp_con_y_sin_ruido, graficar_histograma, graficar_señal_modulada, graficar_todas_las_senales_moduladas, plot_lora_frequency_chirp, plot_lora_frequency_chirps, potencias_de_ruido, simulaciones_de_canal

SF = 8  # Spreading Factor (debe ser un valor entre 7 y 12)
cant_simbolos = 10  # Cantidad de símbolos a transmitir
total_bits = SF * cant_simbolos  # Total de bits a transmitir

# Se aplica en Seccion 2
B = 125e3  # Ancho de banda (en Hz)
indice = 0

# Generación de bits aleatorios
bits_tx = generate_random_bits(total_bits)
print("---" * 10)
print("Primeros 20 bits a transmitir: ", bits_tx[0:20])
print("---" * 10)

simbolos = codificador(SF, bits_tx)
print("---" * 10)
print("Cantidad de simbolos detectados: ", len(simbolos))
print("Primeros 10 simbolos: ", simbolos[0 : 10])
print("---" * 10)

graficar_histograma(simbolos)

# Decodificaion de simbolos
bits_rx = decodificador(simbolos, SF)
print("---" * 10)
print("Primeros 20 bits recibidos: ", bits_rx[0:20])
print("---" * 10)

print("---" * 10)
print("Bits originales (muestra):   ", bits_tx[: 2 * SF])
print("Bits decodificados (muestra):", bits_rx[: 2 * SF])
print("La tasa de error de bit (BER) es: ", calculador_ber(bits_tx, bits_rx) * 100, "%")
print("---" * 10)

simbolos_modulados = conformador_de_onda(simbolos, SF, B)
print("---" * 10)
print("Salida del conformador de onda:", simbolos_modulados[0])
print("---" * 10)

plot_lora_frequency_chirp(simbolos,2, SF)
plot_lora_frequency_chirps(simbolos, SF, B=125e3)

graficar_señal_modulada(simbolos_modulados, 2, SF,B)

graficar_todas_las_senales_moduladas(simbolos_modulados, SF, B, 8)

simbolos_rx = formador_de_ntuplas(simbolos_modulados, SF)
print("---" * 10)
print("Salida del conformador de onda: ", simbolos_rx)
print("---" * 10)

print("---" * 10)
print("Símbolos codificados:", simbolos)
print("Símbolos recibidos:", simbolos_rx)
print("La tasa de error de simbolos (SER) es: ",calculador_ser(simbolos, simbolos_rx) * 100,"%",)
print("---" * 10)

# Calcular potencia de señal y obtener potencia de ruido
pot_signal = np.mean(np.abs(simbolos_modulados[indice])**2)
_, pot_ruidos = potencias_de_ruido(pot_signal, lim_inf=0, lim_sup=0)
pot_ruido = pot_ruidos[0] 
graficar_chirp_con_y_sin_ruido(simbolos_modulados, indice, SF, B, pot_ruido)

# Configuración/Parametros
cant_simbolos = 50000
total_bits = SF * cant_simbolos

# Generación de bits aleatorios
bits_tx = generate_random_bits(total_bits)

# Simulación del canal AWGN y multipath y graficar BER vs SNR
simulaciones_de_canal(bits_tx, SF, B, -10, -7, -9, -3)