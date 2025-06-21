import numpy as np
import os
os.system('cls')
## Codificador y decodificador para la primera entrega


def generadorBits(cant_de_bits):
    """
    Genera un vector de bits aleatorios (0 y 1) de longitud especificada.

    Args:
        cant_de_bits (int): Cantidad de bits a generar.

    Returns:
        np.ndarray: Vector de bits aleatorios (0 y 1).
    """

    bits_tx = np.random.randint(0, 2, size=cant_de_bits)
    return bits_tx

def encoder(cant_bits,SF,bits_tx):
    N_symbols = cant_bits // SF
    symbols = np.zeros(N_symbols, dtype=int)
    for i in range(N_symbols):
        for h in range(SF):
            bit = bits_tx[i * SF + h]
            symbols[i] += bit * (2 ** h)
    return N_symbols,symbols

def decoder(N_bits,N_symbols,symbols):
    bits_rx = np.zeros(N_bits, dtype=int)
    for i in range(N_symbols):
        value = symbols[i]
        for h in range(SF):
            bits_rx[i * SF + h] = (value >> h) & 1  # extrae el bit h del símbolo
    return bits_rx

def simulacion(cant_de_bits,SF):
    bits_transmitidos = generadorBits(cant_de_bits)
    print(bits_transmitidos[0:30])

    numero_simbolos, simbolos = encoder(cant_de_bits,SF,bits_transmitidos)
    print(numero_simbolos)
    print(simbolos[0:30])

    bits_recibidos = decoder(cant_de_bits,numero_simbolos,simbolos)




    bit_errors = np.sum(bits_recibidos != bits_transmitidos)
    BER = bit_errors / cant_de_bits

    print("Bits originales (muestra):   ", bits_transmitidos[:2*SF])
    print("Bits decodificados (muestra):", bits_recibidos[:2*SF])
    print(f"BER = {BER:.6f}")


# ----------- Parámetros ----------
SF = 7
N_bits = 7000  # Debe ser múltiplo de SF
assert N_bits % SF == 0, "La cantidad de bits debe ser múltiplo del SF."
N_symbols = N_bits // SF

simulacion(N_bits,SF)

# ----------- Generación de bits aleatorios ----------
#bits_tx = np.random.randint(0, 2, N_bits)

# ----------- Codificador (suma directa como en ecuación 1) ----------
#symbols = np.zeros(N_symbols, dtype=int)

#for i in range(N_symbols):
#    for h in range(SF):
#        bit = bits_tx[i * SF + h]
#        symbols[i] += bit * (2 ** h)

# ----------- Decodificador (extrae bits desde cada símbolo) ----------
#bits_rx = np.zeros(N_bits, dtype=int)

#for i in range(N_symbols):
#    value = symbols[i]
#    for h in range(SF):
#        bits_rx[i * SF + h] = (value >> h) & 1  # extrae el bit h del símbolo

# ----------- Cálculo de BER ----------
#bit_errors = np.sum(bits_rx != bits_tx)
#BER = bit_errors / N_bits

# ----------- Mostrar resultados ----------
#print("Bits originales (muestra):   ", bits_tx[:2*SF])
#print("Bits decodificados (muestra):", bits_rx[:2*SF])
#print(f"BER = {BER:.6f}")