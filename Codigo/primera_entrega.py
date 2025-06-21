import numpy as np
## Encoder segun la ecuacion 1 del paper

def generadorBits(cant_de_bits,SF):
    if(cant_de_bits % SF == 0):
        bits_tx = np.random.randint(0, 2, size=N_bits)
        return bits_tx
    else:
        return "La cantidad de bits debe ser múltiplo del SF."

def encoder():
    pass

def decoder():
    pass

def simulacion(cant_de_bits,SF):
    bits_transmitidos = generadorBits(cant_de_bits,SF)
    print(bits_transmitidos[0:30])
    pass



simulacion()
# Parámetro: Spreading Factor
SF = 7  # podés cambiarlo entre 7 y 12

# Cantidad de bits a transmitir (debe ser múltiplo de SF)
N_bits = 7000  # por ejemplo


# ---------- Codificador ----------
# Generación de bits aleatorios (0 o 1)
bits_tx = np.random.randint(0, 2, size=N_bits)

# Reshape en bloques de SF bits
bits_reshaped = bits_tx.reshape((-1, SF))

# Cálculo de los símbolos (Eq. 1)
powers_of_two = 2 ** np.arange(SF)  # [2^0, 2^1, ..., 2^{SF-1}]
symbols = bits_reshaped @ powers_of_two  # producto matricial

# ---------- Decodificador ----------
# Decodificación de cada símbolo a bits (binario)
bits_rx = ((symbols[:, None] & (1 << np.arange(SF))) > 0).astype(int)

# Decodificación de cada símbolo a bits (binario)
bits_rx = ((symbols[:, None] & (1 << np.arange(SF))) > 0).astype(int)

# Reconstrucción de la secuencia de bits
bits_rx_flat = bits_rx.reshape(-1)

# ---------- Comparación y BER ----------
# Cálculo del Bit Error Rate (BER)
bit_errors = np.sum(bits_rx_flat != bits_tx)
BER = bit_errors / N_bits

# ---------- Resultados ----------
print("Bits originales (muestra):", bits_tx[:SF*2])
print("Bits decodificados (muestra):", bits_rx_flat[:SF*2])
print(f"BER = {BER:.6f}")
