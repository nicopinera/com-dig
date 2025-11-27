import numpy as np
from funciones import *

SF = 8  # Spreading Factor (debe ser un valor entre 7 y 12)
cant_simbolos = 10  # Cantidad de símbolos a transmitir
total_bits = SF * cant_simbolos  # Total de bits a transmitir

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

print("Generando trama de prueba...")
trama_test = build_tx_frame(simbolos, SF, preamble_len=8)
visualizar_estructura_trama(trama_test, simbolos, SF, preamble_len=8)


payload_chirps = extraer_payload_chirps(trama_test, SF)
simbolos_rx = formador_de_ntuplas(payload_chirps, SF)

print("---" * 10)
print("Símbolos codificados:", simbolos)
print("Símbolos recibidos:", simbolos_rx)
print("La tasa de error de simbolos (SER) es: ",calculador_ser(simbolos, simbolos_rx) * 100,"%",)
print("---" * 10)

# Decodificación de símbolos
bits_rx = decodificador(simbolos_rx, SF)
print("---" * 10)
print("Primeros 20 bits recibidos: ", bits_rx[0:20])
print("---" * 10)

print("---" * 10)
print("Bits originales (muestra):   ", bits_tx[: 2 * SF])
print("Bits decodificados (muestra):", bits_rx[: 2 * SF])
print("La tasa de error de bit (BER) es: ", calculador_ber(bits_tx, bits_rx) * 100, "%")
print("---" * 10)