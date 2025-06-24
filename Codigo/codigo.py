import numpy as np
import matplotlib.pyplot as plt
import os

os.system("cls")
## Codificador y decodificador para la primera entrega


# Generador de bits aleatorios
def generate_random_bits(total_bits):
    """
    Genera un vector de bits aleatorios (0 y 1) de longitud especificada.

    Args:
        cantidad_Bits (int): Cantidad de bits a generar.

    Returns:
        bits_transmitidos: Vector de bits aleatorios (0 y 1).
    """
    return np.random.randint(0, 2, total_bits)

def codificador(SF, bits_transmitidos):
    """
    Codifica un señal binaria mediante el polinomio de numeración posicional en base 2 

    Args:
        SF (int): Spreading Factor
        bits_transmitidos (array): Vector de bits a transmitir

    Returns:
        numero_de_simbolos (int): Cantidad de simbolos codificados
        simbolos (array): vector de simbolos codificados
    """
    cantidad_Bits = len(bits_transmitidos) # Cantidad de bits transmitidos
    
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
        bits_rx (np.ndarray): Vector plano de bits decodificados.
    """
    if(SF < 7 or SF > 12):
        raise ValueError("El Spreading Factor debe ser un valor entero entre 7 y 12")
    
    bits_rx = []

    for simbolo in simbolos_rx: # Se toma cada simbolo
        bits = []
        for _ in range(SF): # Se repite la division por 2 hasta SF-1
            bits.append(simbolo % 2)
            simbolo = simbolo//2
        bits_rx.extend(bits)  # Agrega los bits en orden LSB a MSB

    return np.array(bits_rx, dtype=int)  # Asegura que sea un array plano de enteros

def calculador_ber(bits_tx, bits_rx):
    """Calcula la tasa de error de bit (BER) entre los bits transmitidos y recibidos.

    Args:
        bits_tx (list): Arreglo unidimensional de bits transmitidos.
        bits_rx (list): Arreglo unidimensional de bits recibidos.

    Returns:
        float: Tasa de error de bit (BER).
    """
    if len(bits_tx) != len(bits_rx):
        raise ValueError("Los arreglos de bits transmitidos y recibidos deben tener la misma longitud.")
    
    errores = np.sum(bits_tx != bits_rx)
    ber = errores / len(bits_tx)
    
    return ber

# Parametros
SF = 8
cant_simbolos = 11
total_bits = SF * cant_simbolos

# Generación de bits aleatorios
bits_tx = generate_random_bits(total_bits)
print("---" * 10)
print("Primeros 20 bits a transmitir: ", bits_tx[0:20])
print("---" * 10)

numero_simbolos, simbolos = codificador(SF, bits_tx)
print("---" * 10)
print("Cantidad de simbolos detectados: ", numero_simbolos)
print("Primeros 10 simbolos: ", simbolos[0:numero_simbolos])
print("---" * 10)

# Decodificaion de simbolos
bits_rx = decodificador(simbolos, SF)
print("---" * 10)
print("Primeros 20 bits recibidos: ", bits_rx[0:20])
print("---" * 10)

print("---" * 10)
print("Bits originales (muestra):   ", bits_tx[: 2 * SF])
print("Bits decodificados (muestra):", bits_rx[: 2 * SF])
print("La tasa de error de bit (BER) es: ", calculador_ber(bits_tx, bits_rx)*100, "%")
print("---" * 10)

# -------------------------------------------------------------
def conformador_de_onda(simbolos, SF, B=125e3):
    """
    Genera la forma de onda LoRa para una secuencia de símbolos.

    Parámetros:
    - simbolos: matriz unidimensional de enteros entre 0 y 2**SF - 1
    - SF: Spreading Factor
    - B: Ancho de banda (Hz), por defecto 125 kHz

    Retorna:
    - matriz de forma (len(simbolos), 2**SF) con los chirps generados 
    """
    Ns = 2**SF # Muestras por simbolo
    amplitud = (1 / np.sqrt(Ns))
    T = 1/B  # Periodo de muestreo
    k = np.arange(Ns) # Arreglo de indices de muestras
    simbolos_modulados = []

    for s in simbolos:
        arg = ((s + k) % Ns) * (k * T * B / Ns) # Obtiene el argumento de la exponencial compleja
        chirp = amplitud * np.exp(1j * 2 * np.pi * arg) # Modula el simbolo
        simbolos_modulados.append(chirp) # Agrega el simbolo modulado a la matriz

    return np.array(simbolos_modulados)  # Matriz de salida (símbolos x muestras)

def formador_de_ntuplas(simbolos_modulados, SF):
    """
    Demodula la señal previamente modulada con la funcion conformador_de_onda recuperando los símbolos.

    Parámetros:
    - simbolos_modulados: matriz de (cantidad de simbolos x 2**SF) de chirps modulados
    - SF: Spreading Factor

    Retorna:
    - Lista de símbolos estimados (enteros entre 0 y 2**SF - 1)
    """
    Ns = 2**SF
    k = np.arange(Ns)
    
    
    simbolos_estimados = []
    func_aux = np.exp(-1j * 2 * np.pi * k**2 / Ns)

    for r in simbolos_modulados:
        # Multiplicación para obtener d(nTs+kT)
        d = r * func_aux
        # Calcula la transformada de Fourier discreta de d(nTs+kT)
        fft_out = np.fft.fft(d)
        # Estima el simbolo a partir del pico en frecu  encia
        simbolo_estimado = int(np.argmax(np.abs(fft_out)))

        simbolos_estimados.append(simbolo_estimado)

    return simbolos_estimados

def calculador_ser(simbolos_tx, simbolos_rx):
    """Calcula la tasa de error de simbolos (SER) entre los simbolos transmitidos y recibidos.

    Args:
        simbolos_tx (list): Arreglo unidimensional de simbolos transmitidos.
        simbolos_rx (list): Arreglo unidimensional de simbolos recibidos.

    Returns:
        float: Tasa de error de simbolos (SER).
    """
    if len(simbolos_tx) != len(simbolos_rx):
        raise ValueError("Los arreglos de simbolos transmitidos y recibidos deben tener la misma longitud.")
    
    errores = np.sum(simbolos_tx != simbolos_rx)
    ser = errores / len(simbolos_tx)
    
    return ser

def graficar_señal_modulada(simbolos_modulados, indice, SF, B=125e3):
    """
    Grafica la señal modulada en tiempo (I y Q) de un símbolo dado por su índice
    dentro de la matriz de simbolos modulados.

    Parámetros:
    - simbolos_modulados: matriz de salida de conformador_de_onda
    - indice: posición del símbolo que se desea graficar
    - SF: Spreading Factor
    - B: ancho de banda (Hz)
    """
    Ns = 2**SF # Muestras por simbolo
    T = 1/B  # Periodo de muestreo
    k = np.arange(Ns) # Arreglo de indices de muestras
    tiempo = k * T * 1e6  # microsegundos

    muestra_simbolo_mod = simbolos_modulados[indice]
    I = np.real(muestra_simbolo_mod)
    Q = np.imag(muestra_simbolo_mod)

    plt.figure(figsize=(10, 4))
    plt.plot(tiempo, I, color='blue')
    plt.title(f"Chirp LoRa - Fase (I) - índice {indice} (SF={SF})")
    plt.xlabel("Tiempo [μs]")
    plt.ylabel("Amplitud")
    plt.grid()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 4))
    plt.plot(tiempo, Q, color='red')
    plt.title(f"Chirp LoRa - Cuadratura (Q) - índice {indice} (SF={SF})")
    plt.xlabel("Tiempo [μs]")
    plt.ylabel("Amplitud")
    plt.grid()
    plt.tight_layout()
    plt.show()

def graficar_señal_modulada2(simbolos_modulados, indice, SF, B=125e3):
    """
    Grafica la señal modulada en tiempo (I y Q) de un símbolo dado por su índice
    dentro de la matriz de simbolos modulados.
    """
    Ns = 2**SF
    T = 1/B
    k = np.arange(Ns)
    tiempo = k * T * 1e6  # microsegundos

    muestra_simbolo_mod = simbolos_modulados[indice]
    I = np.real(muestra_simbolo_mod)
    Q = np.imag(muestra_simbolo_mod)

    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    axs[0].plot(tiempo, I, color='blue')
    axs[0].set_title(f"Chirp LoRa - Fase (I) - índice {indice} (SF={SF})")
    axs[0].set_ylabel("Amplitud")
    axs[0].grid()

    axs[1].plot(tiempo, Q, color='red')
    axs[1].set_title(f"Chirp LoRa - Cuadratura (Q) - índice {indice} (SF={SF})")
    axs[1].set_xlabel("Tiempo [μs]")
    axs[1].set_ylabel("Amplitud")
    axs[1].grid()

    plt.tight_layout()
    plt.show()

#Ejemplo de uso, continuando el ejemplo del capitulo anterior (Codificador y Decodificador)

simbolos_modulados = conformador_de_onda(simbolos,SF)
graficar_señal_modulada(simbolos_modulados,1,SF)
graficar_señal_modulada2(simbolos_modulados,1,SF)
simbolos_rx = formador_de_ntuplas(simbolos_modulados, SF)

print("Símbolos codificados:", simbolos)
print("Símbolos recibidos:", simbolos_rx)

print("La tasa de error de simbolos (SER) es: ", calculador_ser(simbolos, simbolos_rx)*100, "%")



"""

def simulacion(cantidad_de_bits, SF):
    
    Realiza la simulacion de generar bits, codificarlos, decodificarlos
    y calculo del BER (cantidad de bit errados / Bit totales transmitidos)
    Como es el caso ideal, el BER = 0.

    Args:
        cantidad_de_bits (int) : cantidad de bits a transmitir
        SF (int): Spreading Factor
    

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

"""