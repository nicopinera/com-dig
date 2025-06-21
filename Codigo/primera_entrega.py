import numpy as np
import os
os.system('cls')
## Codificador y decodificador para la primera entrega


def generadorBits(cantidad_Bits):
    """
    Genera un vector de bits aleatorios (0 y 1) de longitud especificada.

    Args:
        cantidad_Bits (int): Cantidad de bits a generar.

    Returns:
        bits_transmitidos: Vector de bits aleatorios (0 y 1).
    """
    bits_transmitidos = np.random.randint(0, 2, size=cantidad_Bits)
    return bits_transmitidos



def codificador(cantidad_Bits,SF,bits_transmitidos):
    """
    Devuelve la codificacion en decimal del vector de bits a transmitir.

    Args:
        cantidad_Bits (int): Cantidad de bits a transmitir
        SF (int): Spreading Factor
        bits_transmitidos (array): Vector de bits a transmitir

    Returns:
        numero_de_simbolos (int): Cantidad de simbolos codificados
        simbolos (array): vector de simbolos codificados
    """
    #Numero de simbolos a transmitir
    numero_de_simbolos = cantidad_Bits // SF

    # Vector de ceros con la longitud de la cantidad de simbolos
    simbolos = np.zeros(numero_de_simbolos, dtype=int)

    # Sumatoria - Ecuacion 1
    ## Simbolo i
    for i in range(numero_de_simbolos):

        # de 0 hasta SF-1
        for h in range(SF):
            "Toma bits dentro de un bloque de bits de largo SF"
            "Luego se suma cada bit con su peso para obtener el valor decimal del simbolo a transmitir"

            bit = bits_transmitidos[i * SF + h]
            simbolos[i] += bit * (2 ** h) # Conversion a decimal

    return numero_de_simbolos,simbolos

def decoder(numero_de_bits,numero_de_simbolos,simbolos,SF):
    """
    Devuelve la decodificacion de los bits transmitidos

    Args:
        numero_de_bits (int): Cantidad de bits transmitidos
        numero_de_simbolos (int): Cantidad de Simbolos
        SF (int): Spreading Factor
        simbolos (Array): Vector de numeros decimales para decodificar

    Returns:
        bits_recibidos (array): bits recibidos luego de la decodificacion
    """
    # Se crea un array de ceros donde se almacenarán los bits recuperados.
    bits_recibidos = np.zeros(numero_de_bits, dtype=int)

    # Se recorre cada símbolo (número codificado).
    for i in range(numero_de_simbolos):

        value = simbolos[i]
        for h in range(SF):
            bits_recibidos[i * SF + h] = (value >> h) & 1  # extrae el bit h del símbolo
    return bits_recibidos

def simulacion(cant_de_bits,SF):
    bits_transmitidos = generadorBits(cant_de_bits)
    print("Primeros 10 bits a transmitir: " + bits_transmitidos[0:10])

    numero_simbolos, simbolos = codificador(cant_de_bits,SF,bits_transmitidos)
    print("Cantidad de simbolos detectados: "+numero_simbolos)
    print(simbolos[0:30])

    bits_recibidos = decoder(cant_de_bits,numero_simbolos,simbolos)




    bit_errors = np.sum(bits_recibidos != bits_transmitidos)
    BER = bit_errors / cant_de_bits

    print("Bits originales (muestra):   ", bits_transmitidos[:2*SF])
    print("Bits decodificados (muestra):", bits_recibidos[:2*SF])
    print(f"BER = {BER:.6f}")


# ----------- Simulacion ----------
SF = 7
N_bits = 7000  # Debe ser múltiplo de SF
simulacion(N_bits,SF)

