import numpy as np
import matplotlib.pyplot as plt

def conformador_de_onda(simbolos, SF, B=125e3):
    M = 2 ** SF
    k = np.arange(M)
    
    # fase REAL del chirp LoRa
    fase_base = (k**2) / (2*M)

    upchirp = (1 / np.sqrt(M)) * np.exp(1j * 2 * np.pi * fase_base)

    waveform = np.zeros((len(simbolos), M), dtype=complex)

    for i, s in enumerate(simbolos):
        # desplazamiento correcto
        waveform[i] = np.roll(upchirp, -s)

    return waveform

def formador_de_ntuplas(simbolos_modulados, SF, B=125e3):
    M = 2**SF
    k = np.arange(M)
    
    fase_base = (k**2) / (2*M)  # <--- IMPORTANTE
    upchirp = (1/np.sqrt(M)) * np.exp(1j * 2 * np.pi * fase_base)
    dechirp = np.conj(upchirp)

    out = []
    for r in simbolos_modulados:
        r_dc = r * dechirp
        fft_out = np.fft.fft(r_dc)
        out.append(int(np.argmax(np.abs(fft_out))))

    return out

def calculador_ser(simbolos_tx, simbolos_rx):
    """
    Calcula la tasa de error de símbolos (SER) entre los símbolos transmitidos y recibidos.

    Args:
        simbolos_tx (list): Arreglo unidimensional de símbolos transmitidos.
        simbolos_rx (list): Arreglo unidimensional de símbolos recibidos.

    Returns:
        SER (float): Tasa de error de símbolos (SER).
    """
    if len(simbolos_tx) != len(simbolos_rx):
        raise ValueError("Los arreglos de símbolos transmitidos y recibidos deben tener la misma longitud.")

    errores = np.sum(simbolos_tx != simbolos_rx)
    ser = errores / len(simbolos_tx)

    return ser

def graficar_señal_modulada(simbolos_modulados, indice, SF, B):
    """
    Grafica la señal modulada en tiempo (I y Q) de un símbolo dado por su índice dentro de la matriz de símbolos modulados.

    Args:
        simbolos_modulados (Array): Lista de símbolos modulados en forma de chirps.
        indice (int): Posición del símbolo que se desea graficar.
        SF (int): Spreading Factor.
        samples_per_chirp (int): Muestras por símbolo o factor de oversampling.
        B (int): Ancho de banda (Hz).
    """
    Ns = 2**SF  # Muestras base por símbolo
    total_muestras = Ns # Muestras por símbolo
    T = 1 / B  # Duración total del símbolo (s)
    T_muestra =Ns* T # Duración de cada muestra (s)

    tiempo = np.arange(total_muestras) * T_muestra * 1e6  # Tiempo en microsegundos

    muestra_simbolo_mod = simbolos_modulados[indice]
    I = np.real(muestra_simbolo_mod)  # Componente en fase
    Q = np.imag(muestra_simbolo_mod)  # Componente en cuadratura

    # Grafica
    fig, axs = plt.subplots(2, 1, figsize=(15, 4), sharex=True)
    axs[0].plot(tiempo, I, color="blue", linewidth=0.9)
    axs[0].set_title(f"Chirp LoRa - Fase (I) - índice {indice} (SF={SF})")
    axs[0].set_ylabel("Amplitud")
    axs[0].grid()

    axs[1].plot(tiempo, Q, color="red", linewidth=0.9)
    axs[1].set_title(f"Chirp LoRa - Cuadratura (Q) - índice {indice} (SF={SF})")
    axs[1].set_xlabel("Tiempo [μs]")
    axs[1].set_ylabel("Amplitud")
    axs[1].grid()

    plt.tight_layout()
    plt.show()

def graficar_chirp_correcto(chirp, SF, B):
    """
    Grafica I, Q y frecuencia instantánea a partir de tu chirp discreto.
    NO requiere oversampling.
    """
    M = 2**SF
    T = M / B  # duración total del símbolo
    Fs = B  # frecuencia de muestreo efectiva en LoRa discreto

    # tiempo en µs
    t = np.arange(M) * (1/Fs) * 1e6

    # I y Q
    I = np.real(chirp)
    Q = np.imag(chirp)

    # ------------------------------
    #   FRECUENCIA INSTANTÁNEA
    # ------------------------------

    # fase
    phase = np.unwrap(np.angle(chirp))

    # derivada discreta → frecuencia
    dphase = np.diff(phase)

    # freq_inst[n] = (dφ/dt) / (2π)
    freq_inst = (dphase * Fs) / (2*np.pi)

    # tiempo de la frecuencia instantánea
    t_f = t[:-1]

    # ------------------------------
    #   GRÁFICAS
    # ------------------------------
    plt.figure(figsize=(14,7))

    plt.subplot(3,1,1)
    plt.plot(t, I, lw=0.8)
    plt.title("Chirp LoRa – Parte real (I)")
    plt.grid()

    plt.subplot(3,1,2)
    plt.plot(t, Q, lw=0.8)
    plt.title("Chirp LoRa – Parte imaginaria (Q)")
    plt.grid()

    plt.subplot(3,1,3)
    plt.plot(t_f, freq_inst/1e3, lw=0.8)
    plt.title("Frecuencia instantánea (kHz) – ¡esta es la rampa lineal!")
    plt.xlabel("Tiempo [µs]")
    plt.ylabel("Frecuencia [kHz]")
    plt.grid()

    plt.tight_layout()
    plt.show()

def graficar_frec_sin_saltos(chirp, s, SF, B):
    M = 2**SF
    k = np.arange(M)

    # Frecuencia exacta que RECONSTRUYE TU CHIRP
    f = ((k + s) % M) * (B / M)

    t = k * (1/B) * 1e6  # tiempo en microsegundos

    plt.figure(figsize=(12,4))
    plt.plot(t, f/1e3, lw=1)
    plt.title("Frecuencia instantánea sin saltos (reconstruida)")
    plt.xlabel("Tiempo [µs]")
    plt.ylabel("Frecuencia [kHz]")
    plt.grid()
    plt.tight_layout()
    plt.show()

def graficar_todas_las_senales_moduladas(simbolos_modulados, SF, B, max_muestras=None):
    """
    Grafica la señal modulada completa solo de la parte en fase (I) concatenando los símbolos,
    y colorea cada símbolo con un color distinto.

    Args:
        simbolos_modulados (Array): Lista de símbolos modulados en forma de chirps.
        SF: Spreading Factor.
        samples_per_chirp: Muestras por símbolo o factor de oversampling.
        B: Ancho de banda (Hz).
        max_muestras: Cantidad de símbolos a graficar (opcional).
    """
    Ns = 2**SF
    total_muestras = Ns
    T = 1 / B
    T_muestra = T 

    if max_muestras is None:
        max_muestras = len(simbolos_modulados)

    cmap = plt.get_cmap("tab10")

    plt.figure(figsize=(15, 3))

    for i in range(max_muestras):
        simbolo = simbolos_modulados[i]
        I = np.real(simbolo)
        tiempo_local = (np.arange(i * total_muestras, (i + 1) * total_muestras) * T_muestra * 1e6)
        plt.plot(tiempo_local, I, label=f"Símbolo {i}", color=cmap(i % 10), linewidth=0.6)

    plt.title(f"Fase (I) de todos los símbolos concatenados (SF={SF})")
    plt.xlabel("Tiempo [μs]")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_lora_frequency_chirp(simbolos,indice, sf=8, B=125e3):
    """
    Genera y grafica la frecuencia instantánea (chirp) del símbolo LoRa dado.

    Args:
        simbolo (int): lista de simbolos 
        indice (int): indice del simbolo a graficar
        sf (int): Spreading Factor (por defecto 7)
        Bw_kHz (float): Ancho de banda en kHz (por defecto 125)
    """
    # Parámetros
    s = simbolos[indice]
    Ns = 2**sf  # Numero de muestra
    Ts = Ns / B  # Duración del símbolo en segundos
    samples = Ns  # 1 muestra por paso
    t = np.linspace(0, Ts, samples)  # vector de tiempo

    # Cálculo de frecuencia instantánea
    f_inst = (s * B / Ns + (B / Ts) * t) % B
    f_inst_kHz = f_inst / 1e3
    t_ms = t * 1e3  # tiempo en milisegundos

    # Gráfico
    plt.figure(figsize=(12, 4))
    plt.title("LoRa Modulation - Chirp Frecuencia Instantánea", fontsize=16, weight="bold")
    plt.xlabel("Time [ms]", fontsize=14)
    plt.ylabel("Frequency [kHz]", fontsize=14)
    plt.plot(t_ms, f_inst_kHz, lw=2, color="deepskyblue")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_lora_frequency_chirps(simbolos, SF=8, B=125e3):
    """
    Genera y grafica la frecuencia instantánea (chirp) de una secuencia de símbolos LoRa.

    Args:
        simbolos (list or array): Secuencia de valores de símbolos LoRa (enteros entre 0 y 2^SF - 1)
        SF (int): Spreading Factor
        B (float): Ancho de banda en Hz
    """
    Ns = 2**SF # Número de muestras por símbolo
    Ts = Ns / B # Duración del símbolo en segundos
    samples = Ns # 1 muestra por paso
    t_total = []
    f_total = []

    for i, s in enumerate(simbolos):
        t = np.linspace(i * Ts, (i + 1) * Ts, samples, endpoint=False)
        f_inst = (s * B / Ns + (B / Ts) * (t - i * Ts)) % B
        t_total.append(t)
        f_total.append(f_inst)

    # Concatenar todo el tiempo y frecuencia
    t_total = np.concatenate(t_total) * 1e3 # a milisegundos
    f_total = np.concatenate(f_total) / 1e3 # a kHz

    # Graficar
    plt.figure(figsize=(12, 4))
    plt.title("LoRa Modulation - Frecuencia Instantánea", fontsize=16, weight="bold")
    plt.xlabel("Tiempo [ms]", fontsize=14)
    plt.ylabel("Frecuencia [kHz]", fontsize=14)
    plt.plot(t_total, f_total, lw=2, color="deepskyblue")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()




simbolos = [0,10,20]
SF = 8
B = 125e3

simbolos_modulados = conformador_de_onda(simbolos, SF, B)
chirp = simbolos_modulados[0]
graficar_frec_sin_saltos(chirp,0,SF,B)
graficar_chirp_correcto(chirp, SF, B)
print("---" * 10)
print("Salida del conformador de onda:", simbolos_modulados[0])
print("---" * 10)
plot_lora_frequency_chirp(simbolos,2, SF)
plot_lora_frequency_chirps(simbolos, SF, B=125e3)
graficar_señal_modulada(simbolos_modulados, 0, SF,B)
graficar_todas_las_senales_moduladas(simbolos_modulados, SF, B)
simbolos_rx = formador_de_ntuplas(simbolos_modulados, SF)
print("---" * 10)
print("Salida del conformador de onda: ", simbolos_rx)
print("---" * 10)
print("---" * 10)
print("Símbolos codificados:", simbolos)
print("Símbolos recibidos:", simbolos_rx)
print("La tasa de error de simbolos (SER) es: ",calculador_ser(simbolos, simbolos_rx) * 100,"%",)
print("---" * 10)