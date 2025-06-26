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
SF = 8                              # Spreading Factor (debe ser un valor entre 7 y 12)
cant_simbolos = 10                  # Cantidad de símbolos a transmitir             
total_bits = SF * cant_simbolos     # Total de bits a transmitir
B=125e3                             # Ancho de banda (en Hz)

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
def conformador_de_onda(simbolos, SF, samples_per_chirp, B):
    """
    Genera la forma de onda aplicando FSCM para una secuencia de símbolos. 

    Parámetros:
    - simbolos (list): lista de símbolos a ser modulados en forma de chirps.
    - SF (int): Spreading Factor
    - samples_per_chirp (int): muestras por chirp o factor de oversampling
    - B (int): Ancho de banda (Hz). 

    Retorna:
    - Array (len(simbolos), total_muestras): Simbolos modulados en forma de chirps
    """
    Ns = 2**SF # Muestras por símbolo (cuando samples_per_chirp=1)
    T = 1 / B # Duración de símbolo (segundos)
    delta = 1 / samples_per_chirp # Paso de tiempo para oversampling
    total_muestras = Ns * samples_per_chirp # Total de muestras por símbolo

    simbolos_modulados = []
    fmax = (Ns - 1) * B / Ns                         # Frecuencia máxima para el chirp, utilizado para aplicar el modulo de manera condicional
    for s in simbolos:
        chirp = np.zeros(total_muestras, dtype=complex)
        k = s  

        for n in range(total_muestras):
            f = k * B / Ns
            t = k * T
            if f >= fmax:               # Modulo de 2**SF
                k -= Ns                 # Devuelve k a 0
                f = k * B / Ns          # Calcula f para k=0
            arg = f * t * 0.5 
            sample = (1 / np.sqrt(Ns * samples_per_chirp)) * np.exp(1j * 2 * np.pi * arg)
            chirp[n] = sample
            k += delta

        simbolos_modulados.append(chirp)

    return np.array(simbolos_modulados)

def formador_de_ntuplas(simbolos_modulados, SF, samples_per_chirp):
    """
    Recupera los símbolos modulados en mediante FSCM y estima los símbolos transmitidos a partir de ellos.

    Parámetros:
    - simbolos_modulados(Array (len(simbolos), total_muestras)): Lista de símbolos modulados en forma de chirps.
    - SF (int): Spreading Factor
    - samples_per_chirp (int): muestras por chirp o factor de oversampling

    Retorna:
    -(list (int)) Lista de símbolos estimados
    """
    Ns = 2**SF
    total_muestras = Ns * samples_per_chirp

    simbolos_estimados = []

    n = np.arange(total_muestras)
    k = n / samples_per_chirp # Ajustamos para la cantidad de samples por chirp
    
    exp_frec_decr= np.exp(-1j * np.pi * (k**2) / Ns)

    for r in simbolos_modulados:
        # Dechirp multiplicando por el conjugado del chirp base
        dechirp = r * exp_frec_decr
        
        # Calculamos la FFT
        fft_out = np.fft.fft(dechirp)
        
        # El valor máximo en la FFT nos da el símbolo estimado
        simbolo_estimado = int(np.argmax(np.abs(fft_out)))
        
        # Cuando se usa samples_per_chirp > 1 (oversampling), la FFT se calcula sobre Ns * samples_per_chirp puntos (en lugar de Ns).
        simbolo_estimado = simbolo_estimado % Ns
        
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

def graficar_señal_modulada(simbolos_modulados, indice, SF, samples_per_chirp, B):
    """
    Grafica la señal modulada en tiempo (I y Q) de un símbolo dado por su índice
    dentro de la matriz de simbolos modulados.

    Parámetros:
    - simbolos_modulados(Array (len(simbolos), total_muestras)): Lista de símbolos modulados en forma de chirps.
    - indice (int): posición del símbolo que se desea graficar
    - SF (int): Spreading Factor
    - B (int): ancho de banda (Hz)
    - samples_per_chirp (int): muestras por simbolo o factor de oversampling
    """
    Ns = 2**SF                                          # Muestras base por símbolo (sin oversampling)
    total_muestras = Ns * samples_per_chirp             # Muestras por símbolo con oversampling
    T = 1 / B                                           # Duración total del símbolo (s)
    T_muestra = T / samples_per_chirp                   # Duración de cada muestra (s)

    tiempo = np.arange(total_muestras) * T_muestra * 1e6  # en microsegundos

    muestra_simbolo_mod = simbolos_modulados[indice]
    I = np.real(muestra_simbolo_mod)
    Q = np.imag(muestra_simbolo_mod)

    plt.figure(figsize=(15, 2))
    plt.plot(tiempo, I, color='blue', linewidth=0.9)
    plt.title(f"Chirp LoRa - Fase (I) - índice {indice} (SF={SF})")
    plt.xlabel("Tiempo [μs]")
    plt.ylabel("Amplitud")
    plt.grid()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(15, 2))
    plt.plot(tiempo, Q, color='red', linewidth=0.9)
    plt.title(f"Chirp LoRa - Cuadratura (Q) - índice {indice} (SF={SF})")
    plt.xlabel("Tiempo [μs]")
    plt.ylabel("Amplitud")
    plt.grid()
    plt.tight_layout()
    plt.show()

def graficar_todas_las_senales_moduladas(simbolos_modulados, SF, samples_per_chirp, B, max_muestras=None):
    """
    Grafica la señal modulada completa solo de la parte en fase (I) concatenando los símbolos,
    y colorea cada símbolo con un color distinto.

    Parámetros:
    - simbolos_modulados(Array (len(simbolos), total_muestras)): Lista de símbolos modulados en forma de chirps.
    - SF: Spreading Factor
    - B: Ancho de banda (Hz)
    - samples_per_chirp: muestras por símbolo o factor de oversampling
    - max_muestras: cantidad de símbolos a graficar (opcional)
    """
    Ns = 2**SF
    total_muestras = Ns * samples_per_chirp
    T = 1 / B
    T_muestra = T / samples_per_chirp

    if max_muestras is None:
        max_muestras = len(simbolos_modulados)

    cmap = plt.get_cmap('tab10')

    plt.figure(figsize=(15, 3))
    for i in range(max_muestras):
        simbolo = simbolos_modulados[i]
        I = np.real(simbolo)
        tiempo_local = np.arange(i * total_muestras, (i + 1) * total_muestras) * T_muestra * 1e6
        plt.plot(tiempo_local, I, label=f'Símbolo {i}', color=cmap(i % 10), linewidth=0.6)

    plt.title(f'Fase (I) de todos los símbolos concatenados (SF={SF})')
    plt.xlabel('Tiempo [μs]')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#Ejemplo de uso, continuando el ejemplo del capitulo anterior (Codificador y Decodificador)

samples_per_chirp = 4
simbolos_modulados = conformador_de_onda(simbolos,SF,samples_per_chirp,B)
graficar_señal_modulada(simbolos_modulados,2,SF,samples_per_chirp,B)
graficar_todas_las_senales_moduladas(simbolos_modulados,SF,samples_per_chirp,B,5)
simbolos_rx = formador_de_ntuplas(simbolos_modulados, SF,samples_per_chirp)
print("Símbolos codificados:", simbolos)
print("Símbolos recibidos:", simbolos_rx)
print("La tasa de error de simbolos (SER) es: ", calculador_ser(simbolos, simbolos_rx)*100, "%")

