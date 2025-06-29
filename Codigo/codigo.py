import numpy as np
import matplotlib.pyplot as plt
import os

# Limpia la consola al iniciar el script
os.system("cls")

## Codificador y decodificador para la primera entrega

# Generador de bits aleatorios
def generate_random_bits(total_bits):
    """
    Genera un vector de bits aleatorios (0 y 1) de longitud especificada.

    Args:
        total_bits (int): Cantidad de bits a generar.

    Returns:
        bits_transmitidos: Vector de bits aleatorios (0 y 1).
    """
    return np.random.randint(0, 2, total_bits)

def codificador(SF, bits_transmitidos):
    """
    Codifica una señal binaria mediante el polinomio de numeración posicional en base 2.

    Args:
        SF (int): Spreading Factor.
        bits_transmitidos (array): Vector de bits a transmitir.

    Returns:
        numero_de_simbolos (int): Cantidad de símbolos codificados.
        simbolos (array): Vector de símbolos codificados.
    """
    cantidad_Bits = len(bits_transmitidos)  # Cantidad de bits transmitidos
    numero_de_simbolos = cantidad_Bits // SF  # Número de símbolos a transmitir
    simbolos = np.zeros(numero_de_simbolos, dtype=int)  # Vector de ceros para los símbolos

    # Conversión de bloques de SF bits a decimal (símbolo)
    for i in range(numero_de_simbolos):
        for h in range(SF):
            bit = bits_transmitidos[i * SF + h]
            simbolos[i] += bit * (2**h)  # Conversión a decimal

    return numero_de_simbolos, simbolos

def decodificador(simbolos_rx, SF=8):
    """
    Decodifica una señal binaria mediante el polinomio de numeración posicional en base 2.

    Args:
        SF (int, optional): Spreading factor, cantidad de bits por símbolo [7,12]. Defaults to 8.
        simbolos_rx (array): Vector de símbolos recibidos.

    Returns:
        bits_rx (np.ndarray): Vector plano de bits decodificados.
    """
    if(SF < 7 or SF > 12):
        raise ValueError("El Spreading Factor debe ser un valor entero entre 7 y 12")
    
    bits_rx = []

    for simbolo in simbolos_rx:  # Se toma cada símbolo
        bits = []
        for _ in range(SF):  # Se repite la división por 2 hasta SF-1
            bits.append(simbolo % 2)
            simbolo = simbolo // 2
        bits_rx.extend(bits)  # Agrega los bits en orden LSB a MSB

    return np.array(bits_rx, dtype=int)  # Devuelve un array plano de enteros

def calculador_ber(bits_tx, bits_rx):
    """
    Calcula la tasa de error de bit (BER) entre los bits transmitidos y recibidos.

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

# Parámetros de la simulación
SF = 8                              # Spreading Factor (debe ser un valor entre 7 y 12)
cant_simbolos = 10                  # Cantidad de símbolos a transmitir             
total_bits = SF * cant_simbolos     # Total de bits a transmitir
B = 125e3                           # Ancho de banda (en Hz)

# Generación de bits aleatorios
bits_tx = generate_random_bits(total_bits)
print("---" * 10)
print("Primeros 20 bits a transmitir: ", bits_tx[0:20])
print("---" * 10)

# Codificación de los bits en símbolos
numero_simbolos, simbolos = codificador(SF, bits_tx)
print("---" * 10)
print("Cantidad de simbolos detectados: ", numero_simbolos)
print("Primeros 10 simbolos: ", simbolos[0:numero_simbolos])
print("---" * 10)

# Decodificación de los símbolos a bits
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
    - simbolos (list): Lista de símbolos a ser modulados en forma de chirps.
    - SF (int): Spreading Factor.
    - samples_per_chirp (int): Muestras por chirp o factor de oversampling.
    - B (int): Ancho de banda (Hz).

    Retorna:
    - Array (len(simbolos), total_muestras): Símbolos modulados en forma de chirps.
    """
    Ns = 2**SF  # Muestras por símbolo (cuando samples_per_chirp=1)
    T = 1 / B   # Duración de símbolo (segundos)
    delta = 1 / samples_per_chirp  # Paso de tiempo para oversampling
    total_muestras = Ns * samples_per_chirp  # Total de muestras por símbolo

    simbolos_modulados = []
    fmax = (Ns - 1) * B / Ns  # Frecuencia máxima para el chirp

    for s in simbolos:
        chirp = np.zeros(total_muestras, dtype=complex)
        k = s  
        for n in range(total_muestras):
            f = k * B / Ns
            t = k * T
            if f >= fmax:  # Modulo de 2**SF
                k -= Ns    # Devuelve k a 0
                f = k * B / Ns
            arg = f * t * 0.5 
            sample = (1 / np.sqrt(Ns * samples_per_chirp)) * np.exp(1j * 2 * np.pi * arg)
            chirp[n] = sample
            k += delta
        simbolos_modulados.append(chirp)

    return np.array(simbolos_modulados)

def formador_de_ntuplas(simbolos_modulados, SF, samples_per_chirp):
    """
    Recupera los símbolos modulados mediante FSCM y estima los símbolos transmitidos a partir de ellos.

    Parámetros:
    - simbolos_modulados (Array): Lista de símbolos modulados en forma de chirps.
    - SF (int): Spreading Factor.
    - samples_per_chirp (int): Muestras por chirp o factor de oversampling.

    Retorna:
    - (list (int)): Lista de símbolos estimados.
    """
    Ns = 2**SF
    total_muestras = Ns * samples_per_chirp

    simbolos_estimados = []

    n = np.arange(total_muestras)
    k = n / samples_per_chirp  # Ajuste para oversampling
    
    exp_frec_decr = np.exp(-1j * np.pi * (k**2) / Ns)

    for r in simbolos_modulados:
        # Dechirp multiplicando por el conjugado del chirp base
        dechirp = r * exp_frec_decr
        
        # Calculamos la FFT
        fft_out = np.fft.fft(dechirp)
        
        # El valor máximo en la FFT nos da el símbolo estimado
        simbolo_estimado = int(np.argmax(np.abs(fft_out)))
        
        # Ajuste para oversampling
        simbolo_estimado = simbolo_estimado % Ns
        
        simbolos_estimados.append(simbolo_estimado)

    return simbolos_estimados

def calculador_ser(simbolos_tx, simbolos_rx):
    """
    Calcula la tasa de error de símbolos (SER) entre los símbolos transmitidos y recibidos.

    Args:
        simbolos_tx (list): Arreglo unidimensional de símbolos transmitidos.
        simbolos_rx (list): Arreglo unidimensional de símbolos recibidos.

    Returns:
        float: Tasa de error de símbolos (SER).
    """
    if len(simbolos_tx) != len(simbolos_rx):
        raise ValueError("Los arreglos de símbolos transmitidos y recibidos deben tener la misma longitud.")
    
    errores = np.sum(simbolos_tx != simbolos_rx)
    ser = errores / len(simbolos_tx)
    
    return ser

def graficar_señal_modulada(simbolos_modulados, indice, SF, samples_per_chirp, B):
    """
    Grafica la señal modulada en tiempo (I y Q) de un símbolo dado por su índice
    dentro de la matriz de símbolos modulados, usando subplots para mostrar ambas componentes.

    Parámetros:
    - simbolos_modulados (Array): Lista de símbolos modulados en forma de chirps.
    - indice (int): Posición del símbolo que se desea graficar.
    - SF (int): Spreading Factor.
    - B (int): Ancho de banda (Hz).
    - samples_per_chirp (int): Muestras por símbolo o factor de oversampling.
    """
    Ns = 2**SF                                          # Muestras base por símbolo (sin oversampling)
    total_muestras = Ns * samples_per_chirp             # Muestras por símbolo con oversampling
    T = 1 / B                                           # Duración total del símbolo (s)
    T_muestra = T / samples_per_chirp                   # Duración de cada muestra (s)

    tiempo = np.arange(total_muestras) * T_muestra * 1e6  # Tiempo en microsegundos

    muestra_simbolo_mod = simbolos_modulados[indice]
    I = np.real(muestra_simbolo_mod)  # Componente en fase
    Q = np.imag(muestra_simbolo_mod)  # Componente en cuadratura

    # Crear subplots para I y Q
    fig, axs = plt.subplots(2, 1, figsize=(15, 4), sharex=True)
    axs[0].plot(tiempo, I, color='blue', linewidth=0.9)
    axs[0].set_title(f"Chirp LoRa - Fase (I) - índice {indice} (SF={SF})")
    axs[0].set_ylabel("Amplitud")
    axs[0].grid()

    axs[1].plot(tiempo, Q, color='red', linewidth=0.9)
    axs[1].set_title(f"Chirp LoRa - Cuadratura (Q) - índice {indice} (SF={SF})")
    axs[1].set_xlabel("Tiempo [μs]")
    axs[1].set_ylabel("Amplitud")
    axs[1].grid()

    plt.tight_layout()
    plt.show()

def graficar_todas_las_senales_moduladas(simbolos_modulados, SF, samples_per_chirp, B, max_muestras=None):
    """
    Grafica la señal modulada completa solo de la parte en fase (I) concatenando los símbolos,
    y colorea cada símbolo con un color distinto.

    Parámetros:
    - simbolos_modulados (Array): Lista de símbolos modulados en forma de chirps.
    - SF: Spreading Factor.
    - B: Ancho de banda (Hz).
    - samples_per_chirp: Muestras por símbolo o factor de oversampling.
    - max_muestras: Cantidad de símbolos a graficar (opcional).
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

# Ejemplo de uso, continuando el ejemplo del capítulo anterior (Codificador y Decodificador)
samples_per_chirp = 4
simbolos_modulados = conformador_de_onda(simbolos, SF, samples_per_chirp, B)
graficar_señal_modulada(simbolos_modulados, 2, SF, samples_per_chirp, B)
graficar_todas_las_senales_moduladas(simbolos_modulados, SF, samples_per_chirp, B, 5)
simbolos_rx = formador_de_ntuplas(simbolos_modulados, SF, samples_per_chirp)
print("Símbolos codificados:", simbolos)
print("Símbolos recibidos:", simbolos_rx)
print("La tasa de error de simbolos (SER) es: ", calculador_ser(simbolos, simbolos_rx)*100, "%")

samples_per_chirp = 4
simbolos_modulados = conformador_de_onda(simbolos,SF,samples_per_chirp,B)
graficar_señal_modulada(simbolos_modulados,2,SF,samples_per_chirp,B)
graficar_todas_las_senales_moduladas(simbolos_modulados,SF,samples_per_chirp,B,5)
simbolos_rx = formador_de_ntuplas(simbolos_modulados, SF,samples_per_chirp)
print("Símbolos codificados:", simbolos)
print("Símbolos recibidos:", simbolos_rx)
print("La tasa de error de simbolos (SER) es: ", calculador_ser(simbolos, simbolos_rx)*100, "%")

# ------------------------------------------------------

def canal_awgn_sin_filtro(signal, pot_ruido):
    """
    Simula canal AWGN sin filtrado. Con media cero y varianza pot_ruido/2.
    """

    desv_est = np.sqrt(pot_ruido / 2)
    ruido = np.random.normal(0, desv_est, size=signal.shape) + 1j * np.random.normal(0, desv_est, size=signal.shape)
    return (signal + ruido)

def potencias_de_ruido(pot_signal, lim_inf=-12, lim_sup=0):
    """Calcula el rango de potencias de ruido en escala lineal para un rango de SNR en dB.

    Args:
        pot_signal (float): Potencia de la señal en escala lineal.
        lim_inf (int, optional): Valor de SNR inferior. Defaults to -12.
        lim_sup (int, optional): Valor de SNR superior. Defaults to -1.

    Returns:
        list: lista de SNR en dB
        list: lista de potencias de ruido.
    """
    snr_db = np.arange(lim_inf, lim_sup+1, 1)
    pot_ruido = pot_signal / (10 ** (snr_db / 10))
    return snr_db, pot_ruido

def simulacion_canal_awgn_sin_filtro(bits_tx, SF, samples_per_chirp, B, min_snr, max_snr):
    """Simula el envio de bits a traves de un canal AWGN sin filtro, grafica la BER vs SNR 

    Args:
        bits_tx (list): Bits a transmitir.
        SF (int): Spreading Factor.
        samples_per_chirp (int): Muestras por chirp o factor de oversampling.
        B (int): Ancho de banda en Hz.
        min_snr (int): SNR mínima en dB.
        max_snr (int): SNR máxima en dB.
    """
    # 1. Codificacion
    numero_simbolos, simbolos_tx = codificador(SF,bits_tx)
    
    # 2. Modulacion
    simbolos_modulados = conformador_de_onda(simbolos_tx, SF, samples_per_chirp, B)
    
    # 3. Calcular potencia de la señal
    pot_signal = np.mean(np.abs(simbolos_modulados)**2)
    
    # 4. Generar SNR y potencias de ruido
    snr_db, pot_ruido = potencias_de_ruido(pot_signal, min_snr, max_snr)
    
    # 5. Simular canal y demodular para cada SNR
    ber_values = []
    for pn in pot_ruido:
        simbolos_con_ruido = canal_awgn_sin_filtro(simbolos_modulados, pn)
        simbolos_rx = formador_de_ntuplas(simbolos_con_ruido, SF, samples_per_chirp)
        bits_rx = decodificador(simbolos_rx, SF)
        ber = calculador_ber(bits_tx, bits_rx)
        ber_values.append(ber)

    # 6. Graficar
    plt.figure(figsize=(6, 4))
    plt.semilogy(snr_db, ber_values, 'rs-', label="flat FCSM", linewidth=0.8)
    plt.xlim(-12, -1)  
    plt.ylim(10**-5, 10**-1)  
    plt.xticks(np.arange(-12, 0, 1)) 
    plt.title('BER vs SNR en canal AWGN')
    plt.xlabel('SNR [dB]')
    plt.ylabel('BER')
    plt.grid(True, which='both')
    plt.legend()
    plt.tight_layout()
    plt.show()

#Ejemplo de uso:
#Configuración/Parametros
SF = 8
cant_simbolos = 20000           
total_bits = SF * cant_simbolos
samples_per_chirp = 4
B=125e3

# Generación de bits aleatorios
bits_tx = generate_random_bits(total_bits)

# Simulación del canal AWGN sin filtro y graficar BER vs SNR
simulacion_canal_awgn_sin_filtro(bits_tx, SF, samples_per_chirp, B, -10, -7)

def canal_awgn_varianza(senal, SNR_dB):
    """
    Agrega ruido AWGN a una señal compleja, usando SNR en dB como entrada.
    """
    potencia_senal = np.mean(np.abs(senal)**2)
    SNR_lineal = 10 ** (SNR_dB / 10)
    varianza_ruido = potencia_senal / SNR_lineal
    sigma = np.sqrt(varianza_ruido / 2)
    ruido = sigma * (np.random.randn(*senal.shape) + 1j * np.random.randn(*senal.shape))
    return senal + ruido

SNR_dB = -10  # SNR en dB, podés probar con 0, 5, 10, 15, etc.
senal_ruidosa = canal_awgn_varianza(simbolos_modulados, SNR_dB)
simbolos_rx = formador_de_ntuplas(senal_ruidosa, SF, samples_per_chirp)
#print(simbolos_modulados[0])
#print(senal_ruidosa[0])

def graficar_curva_ber(SF, snr_dBs, samples_per_chirp, B, cant_simbolos=1000):
    """
    Simula un sistema LoRa y grafica la curva BER vs SNR (log-log).

    Parámetros:
    - SF (int): Spreading Factor.
    - snr_dBs (list or np.ndarray): Lista de valores de SNR en dB.
    - samples_per_chirp (int): Oversampling (muestras por chirp).
    - B (float): Ancho de banda (Hz).
    - cant_simbolos (int): Cantidad de símbolos a transmitir por SNR.

    Resultado:
    - Gráfico BER vs SNR en escala log.
    """
    total_bits = SF * cant_simbolos
    ber_values = []

    for snr in snr_dBs:
        # 1. Generar y codificar bits
        bits_tx = generate_random_bits(total_bits)
        _, simbolos_tx = codificador(SF, bits_tx)

        # 2. Modulación chirp
        simbolos_modulados = conformador_de_onda(simbolos_tx, SF, samples_per_chirp, B)

        # 3. Canal AWGN muestra a muestra
        simbolos_con_ruido = canal_awgn(simbolos_modulados, snr)

        # 4. Demodulación
        simbolos_rx = formador_de_ntuplas(simbolos_con_ruido, SF, samples_per_chirp)

        # 5. Decodificación
        bits_rx = decodificador(simbolos_rx, SF)

        # 6. BER
        ber = calculador_ber(bits_tx, bits_rx)
        ber_values.append(ber if ber > 0 else 1e-6)  # prevenir log(0)

        print(f"SNR = {snr} dB --> BER = {ber:.6f}")

    # Prevenir log(0)
    ber_values = [ber if ber > 0 else 1e-5 for ber in ber_values]

    plt.figure(figsize=(8, 5))
    plt.semilogy(snr_dBs, ber_values, marker='o', color='blue', label=f'SF = {SF}')

    for x, y in zip(snr_dBs, ber_values):
        if y > 1e-5:
            plt.text(x, y*1.5, f'{y:.1e}', ha='center', fontsize=8)

    plt.grid(True, which='both', linestyle='--')
    plt.xlabel('SNR [dB]')
    plt.ylabel('BER (escala log)')
    plt.title(f'Curva BER vs SNR para LoRa (SF={SF})')
    plt.xticks(snr_dBs)
    plt.ylim(1e-5, 1e-1)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)
    plt.show()

SF = 8
samples_per_chirp = 4
B = 125e3
snr_dBs = np.array([-10, -9, -8, -7])
cant_simbolos = 10000

graficar_curva_ber(SF, snr_dBs, samples_per_chirp, B, cant_simbolos)

def graficar_curva_ber2(SF, snr_dBs, samples_per_chirp, B, cant_simbolos=1000):
    """
    Simula un sistema LoRa y grafica la curva BER vs SNR (log-log).
    """
    total_bits = SF * cant_simbolos
    ber_values = []

    for snr in snr_dBs:
        # 1. Generar y codificar bits
        bits_tx = generate_random_bits(total_bits)
        _, simbolos_tx = codificador(SF, bits_tx)

        # 2. Modulación chirp
        simbolos_modulados = conformador_de_onda(simbolos_tx, SF, samples_per_chirp, B)

        # 3. Canal AWGN
        simbolos_con_ruido = canal_awgn_varianza(simbolos_modulados, snr)

        # 4. Demodulación
        simbolos_rx = formador_de_ntuplas(simbolos_con_ruido, SF, samples_per_chirp)

        # 5. Decodificación
        bits_rx = decodificador(simbolos_rx, SF)

        # 6. BER
        ber = calculador_ber(bits_tx, bits_rx)
        ber_values.append(ber if ber > 0 else 1e-6)  # prevenir log(0)

        print(f"SNR = {snr} dB --> BER = {ber:.6f}")

    # Prevenir log(0)
    ber_values = [ber if ber > 0 else 1e-5 for ber in ber_values]

    plt.figure(figsize=(8, 5))
    plt.semilogy(snr_dBs, ber_values, marker='o', color='blue', label=f'Flat FSCM (SF={SF})')

    for x, y in zip(snr_dBs, ber_values):
        if y > 1e-5:
            plt.text(x, y*1.5, f'{y:.1e}', ha='center', fontsize=8)

    plt.grid(True, which='both', linestyle='--')
    plt.xlabel('SNR [dB]')
    plt.ylabel('BER (escala log)')
    plt.title('Uncoded BER comparison')
    plt.xticks(snr_dBs)
    plt.ylim(1e-5, 1e-1)
    plt.legend()
    plt.show()

SF = 8
samples_per_chirp = 4
B = 125e3
snr_dBs = np.array([-10, -9, -8, -7])
cant_simbolos = 10000

graficar_curva_ber2(SF, snr_dBs, samples_per_chirp, B, cant_simbolos)

from scipy.special import erfc
def ber_lora(SNR_db):
    SNR_lin = 10**(SNR_db/10)
    Q_arg = np.sqrt(2 * SNR_lin)
    Pb = 0.5 * erfc(Q_arg / np.sqrt(2))
    return Pb

# Rango de SNR en dB
SNR_db = np.linspace(-10, -7, 100)
BER = ber_lora(SNR_db)

plt.semilogy(SNR_db, BER, 'b-', label='LoRa BER')
plt.xlabel('SNR (dB)')
plt.ylabel('BER')
plt.title('BER vs SNR for LoRa')
plt.grid(True, which='both')
plt.legend()
plt.show()

def codificador(bits_tx, SF=8):
    """Codifica un señal binaria mediante el polinomio de numeración posicional en base 2 

    Args:
        bits_tx (list): Arreglo unidimensional de bits (0s y 1s) que representa la señal binaria a codificar.
        SF (int, optional): Spreading factor valor entero que representa la cantidad de bits que componen un simbolo puede tomar valores [7,12]. Defaults to 8.

    Returns:
        (list) simbolos_tx: Simbolos codificados en base 2.
    """
    if(SF < 7 or SF > 12):
        raise ValueError("El Spreading Factor debe ser un valor entero entre 7 y 12")
    
    bits_estructurados = bits_tx.reshape(-1, SF) #Toma el arreglo de bits y lo reestructura en una matriz de tamaño num_simbolos x SF         
    potencias = 2**np.arange(SF) #Arreglo de potencias de 2 para realizar la codificación de los símbolos
    simbolos_tx = np.dot(bits_estructurados, potencias) # Producto interno entre los bits estructurados y las potencias de 2 para obtener los símbolos codificados         

    return simbolos_tx

def decodificador(simbolos_rx, SF=8):
    """Decodifica una señal binaria mediante el polinomio de numeración posicional en base 2 
    
    Args:
        SF (int, optional): Spreading factor valor entero que representa la cantidad de bits que componen un simbolo codificado puede tomar valores [7,12]. Defaults to 8.
        simbolos_rx (list, optional): Lista de simbolos recibidos. Defaults to None.
        
    Returns:
        (list) bits_rx: Simbolos decodificados en base 2.
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

# Ejemplo de uso

#Configuración/Parametros
SF = 8                              # Spreading Factor (debe ser un valor entre 7 y 12)
cant_simbolos = 10                  # Cantidad de símbolos a transmitir             
total_bits = SF * cant_simbolos     # Total de bits a transmitir
B=125e3                             # Ancho de banda (en Hz)

# Generación de bits aleatorios
bits_tx = generate_random_bits(total_bits)

# Codificacion
simbolos_tx = codificador(bits_tx, SF)

print("Bits transmitidos:\n(LSB) (MSB)")
for i in range(0, len(bits_tx), SF):
    print(*bits_tx[i:i+SF])
    
print("Símbolos codificados:", simbolos_tx)

# Decodificacion
bits_rx = decodificador(simbolos_tx, SF)

print("Bits recibidos:\n(LSB) (MSB)")
for i in range(0, len(bits_tx), SF):
    print(*bits_rx[i:i+SF])
    
simbolos_rx = codificador(bits_rx, SF)
print("Símbolos decodificados:", simbolos_rx)

print("La tasa de error de bit (BER) es: ", calculador_ber(bits_tx, bits_rx)*100, "%")

def conformador_de_onda(simbolos, SF, samples_per_chirp, B):
    """
    Genera la forma de onda aplicando FSCM para una secuencia de símbolos. 

    Parámetros:
    - simbolos (list): lista de símbolos codificados a ser modulados en forma de chirps.
    - SF (int): Spreading Factor
    - samples_per_chirp (int): muestras por chirp o factor de oversampling
    - B (int): Ancho de banda (Hz). 

    Retorna:
    - Array (len(simbolos), total_muestras): Simbolos modulados en forma de chirps
    """
    Ns = 2**SF                                       # Muestras por símbolo (cuando samples_per_chirp=1)
    T = 1 / B                                        # Duración de símbolo (segundos)
    delta = 1 / samples_per_chirp                    # Paso de tiempo para oversampling
    total_muestras = Ns * samples_per_chirp          # Total de muestras por símbolo

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
#Configuración/Parametros
SF = 8                              # Spreading Factor (debe ser un valor entre 7 y 12)
cant_simbolos = 10                  # Cantidad de símbolos a transmitir             
total_bits = SF * cant_simbolos     # Total de bits a transmitir
B=125e3                             # Ancho de banda (en Hz)

samples_per_chirp = 4

simbolos_modulados = conformador_de_onda(simbolos_tx,SF,samples_per_chirp,B)
graficar_señal_modulada(simbolos_modulados,2,SF,samples_per_chirp,B)
graficar_todas_las_senales_moduladas(simbolos_modulados,SF,samples_per_chirp,B,5)
simbolos_rx = formador_de_ntuplas(simbolos_modulados, SF,samples_per_chirp)

print("Símbolos codificados:", simbolos_tx)
print("Símbolos recibidos:", simbolos_rx)

print("La tasa de error de simbolos (SER) es: ", calculador_ser(simbolos_tx, simbolos_rx))


