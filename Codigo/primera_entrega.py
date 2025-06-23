import numpy as np
import os

os.system("cls")
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


def codificador(SF, bits_transmitidos):
    """
    Codifica un señal binaria mediante el polinomio de numeración posicional en base 2 

    Args:
        cantidad_Bits (int): Cantidad de bits a transmitir
        SF (int): Spreading Factor
        bits_transmitidos (array): Vector de bits a transmitir

    Returns:
        numero_de_simbolos (int): Cantidad de simbolos codificados
        simbolos (array): vector de simbolos codificados
    """
    cantidad_Bits = len(bits_transmitidos)
    # Numero de simbolos a transmitir
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
            simbolos[i] += bit * (2**h)  # Conversion a decimal

    return numero_de_simbolos, simbolos


def decodificador(simbolos_rx, SF=8):
    """Decodifica una señal binaria mediante el polinomio de numeración posicional en base 2 
    
    Args:
        SF (int, optional): Spreading factor valor entero que representa la cantidad de bits que componen un simbolo codificado puede tomar valores [7,12]. Defaults to 8.
        simbolos_rx (_type_, optional): _description_. Defaults to None.
        
    Returns:
        simbolos_tx (list): Simbolos decodificados en base 2.
    """
    if(SF < 7 or SF > 12):
        raise ValueError("El Spreading Factor debe ser un valor entero entre 7 y 12")
    
    bits_rx = []

    for simbolo in simbolos_rx:
        bits = []
        for _ in range(SF):
            # Algoritmo de division sucesiva por 2 para obtener los bits del simbolo
            bits.append(simbolo % 2)
            simbolo = simbolo//2
        bits_rx.extend(bits)

    return np.array(bits_rx)


def simulacion(cantidad_de_bits, SF):
    """
    Realiza la simulacion de generar bits, codificarlos, decodificarlos
    y calculo del BER (cantidad de bit errados / Bit totales transmitidos)
    Como es el caso ideal, el BER = 0.

    Args:
        cantidad_de_bits (int) : cantidad de bits a transmitir
        SF (int): Spreading Factor
    """

    print("SIMULACION")
    print("---" * 5)
    # Generacion de bits
    bits_transmitidos = generadorBits(cantidad_de_bits)
    print("Primeros 10 bits a transmitir: ", bits_transmitidos[0:10])
    print("---" * 5)

    # Codificacion de los bits
    numero_simbolos, simbolos = codificador(SF, bits_transmitidos)
    print("Cantidad de simbolos detectados: ", numero_simbolos)
    print("Primeros 10 simbolos: ", simbolos[0:10])
    print("---" * 5)

    # Decodificaion de simbolos
    bits_recibidos = decodificador(simbolos,SF)
    print("Primeros 10 bits recibidos: ", bits_recibidos[0:10])

    # Calculo
    bit_errors = np.sum(bits_recibidos != bits_transmitidos)
    BER = bit_errors / cantidad_de_bits
    print("---" * 5)
    print("Bits originales (muestra):   ", bits_transmitidos[: 2 * SF])
    print("Bits decodificados (muestra):", bits_recibidos[: 2 * SF])
    print(f"BER = {BER:.6f}")


# ----------- Simulacion ----------
SF = 7
N_bits = 7000  # Debe ser múltiplo de SF
simulacion(N_bits, SF)
