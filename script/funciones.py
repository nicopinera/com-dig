import numpy as np
import matplotlib.pyplot as plt

def generate_random_bits(total_bits):
    """
    Genera un vector de bits aleatorios (0 y 1) de longitud especificada.

    Args:
        cantidad_Bits(int) : Cantidad de bits a generar.

    Returns:
        bits_transmitidos(Array) : Vector de bits aleatorios (0 y 1).
    """
    return np.random.randint(0, 2, total_bits)

def codificador(SF, bits_transmitidos):
    """
    Codifica un señal binaria mediante el polinomio de numeración posicional en base 2

    Args:
        SF (int): Spreading Factor
        bits_transmitidos (array): Vector de bits a transmitir

    Returns:
        simbolos (array): vector de simbolos codificados
    """
    cantidad_Bits = len(bits_transmitidos)  # Cantidad de bits transmitidos

    # Numero de simbolos a transmitir
    numero_de_simbolos = cantidad_Bits // SF

    # Vector de ceros con la longitud de la cantidad de simbolos
    simbolos = np.zeros(numero_de_simbolos, dtype=int)

    # Sumatoria - Ecuacion 1
    ## Simbolo i - Toma de a paquetes de SF
    for i in range(numero_de_simbolos):

        # de 0 hasta SF-1
        for h in range(SF):
            "Toma bits dentro de un bloque de bits de largo SF"
            "Luego se suma cada bit con su peso para obtener el valor decimal del simbolo a transmitir"

            bit = bits_transmitidos[i * SF + h]  # Va desde el LSB al MSB
            simbolos[i] += bit * (2**h)  # Conversion a decimal

    return simbolos

def decodificador(simbolos_rx, SF):
    """
    Decodifica una señal binaria mediante el polinomio de numeración posicional en base 2

    Args:
        SF (int, optional): Spreading factor
        simbolos_rx (array, optional): Vector de simbolos recibidos

    Returns:
        bits_rx (array): Vector bits decodificados.
    """
    if SF < 7 or SF > 12:
        raise ValueError("El Spreading Factor debe ser un valor entero entre 7 y 12")

    bits_rx = []

    for simbolo in simbolos_rx:  # Se toma cada simbolo
        bits = []
        for _ in range(SF):  # Se repite la division por 2 hasta SF-1
            bits.append(simbolo % 2)
            simbolo = simbolo // 2
        bits_rx.extend(bits)  # Agrega los bits en orden LSB a MSB

    return np.array(bits_rx, dtype=int)  # Asegura que sea un array plano de enteros

def calculador_ber(bits_tx, bits_rx):
    """
    Calcula la tasa de error de bit (BER) entre los bits transmitidos y recibidos.

    Args:
        bits_tx (list): Arreglo unidimensional de bits transmitidos.
        bits_rx (list): Arreglo unidimensional de bits recibidos.

    Returns:
        BER (float): Tasa de error de bit (BER).
    """
    if len(bits_tx) != len(bits_rx):
        raise ValueError("Los arreglos de bits transmitidos y recibidos deben tener la misma longitud.")

    errores = np.sum(bits_tx != bits_rx)
    ber = errores / len(bits_tx)

    return ber

def graficar_histograma(simbolos_codificados):
    """
    Grafica el histograma de los símbolos codificados.

    Args:
        simbolos_codificados (list or array): Lista o array de símbolos codificados.
    """
    plt.figure(figsize=(14, 6))  # Aumenta el tamaño de la figura
    bins = range(min(simbolos_codificados), max(simbolos_codificados)+2)
    plt.hist(simbolos_codificados, bins=bins, align='left', rwidth=0.85, color='skyblue', edgecolor='black')
    plt.xlabel('Símbolo', fontsize=16)
    plt.ylabel('Frecuencia', fontsize=16)
    plt.title('Histograma de símbolos codificados', fontsize=18)
    step = 8
    plt.xticks(bins[::step], fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def conformador_de_onda(simbolos, SF, B=125e3):
    """
    Genera la forma de onda LoRa para una secuencia de símbolos usando la ecuación 2 o 3 del paper.

    Args:
    - simbolos: matriz unidimensional de enteros entre 0 y 2**SF - 1
    - SF: Spreading Factor
    - B: Ancho de banda (Hz), por defecto 125 kHz

    Return:
    - matriz de forma (len(simbolos), 2**SF) con los chirps generados
    """
    M = 2 ** SF
    k = np.arange(M)
    waveform = np.zeros((len(simbolos), len(k)), dtype=complex)

    for i, simbolo in enumerate(simbolos):
        fase = ((simbolo + k)) * (k) / M
        chirp = (1 / np.sqrt(M)) * np.exp(1j * 2 * np.pi * fase)
        waveform[i] = chirp
    return waveform

def formador_de_ntuplas(simbolos_modulados, SF, B=125e3):
    """
    Recupera los símbolos modulados mediante FSCM y estima los símbolos transmitidos a partir de ellos.

    Args:
        simbolos_modulados (Array): Lista de símbolos modulados en forma de chirps.
        SF (int): Spreading Factor.

    Return:
        simbolos_estimados (list): Lista de símbolos estimados.
    """
    
    M = 2**SF  
    k = np.arange(M)
    fase = (k**2) / M
    upchirp = (1 / np.sqrt(M)) * np.exp(1j * 2 * np.pi * fase)
    # Upchirp base para dechirp
    dechirp = np.conj(upchirp)

    simbolos_estimados = []

    for r in simbolos_modulados:
        # Dechirp multiplicando por el conjugado del upchirp base
        r_dechirped = r * dechirp
        fft_out = np.fft.fft(r_dechirped)
        simbolo_estimado = int(np.argmax(np.abs(fft_out)))
        simbolos_estimados.append(simbolo_estimado)

    return simbolos_estimados

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
    Ns = 2**SF  # Muestras base por símbolo (sin oversampling)
    total_muestras = Ns # Muestras por símbolo
    T = 1 / B  # Duración total del símbolo (s)
    T_muestra = T # Duración de cada muestra (s)

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

def canal_AWGN(signal, pot_ruido):
    """
    Simula un canal AWGN. Con media cero y varianza pot_ruido/2.

    Args
        signal (array)
        pot_ruido (int)
    
    Return
        Señal + Ruido (array)
    """
    # el parametro que requiere la funcion random.normal es el desvio estandar, el cual es la raiz cuadrada de la potencia
    # la potencia es divida en 2 porque el ruido es complejo (I y Q)
    desv_est = np.sqrt(pot_ruido / 2)
    ruido = np.random.normal(0, desv_est, size=signal.shape) + 1j * np.random.normal(0, desv_est, size=signal.shape)
    return signal + ruido

def potencias_de_ruido(pot_signal, lim_inf=-12, lim_sup=0):
    """
    Calcula el rango de potencias de ruido en escala lineal para un rango de SNR en dB.

    Args:
        pot_signal (float): Potencia de la señal en escala lineal.
        lim_inf (int, optional): Valor de SNR inferior. Defaults to -12.
        lim_sup (int, optional): Valor de SNR superior. Defaults to -1.

    Returns:
        list: lista de SNR en dB
        list: lista de potencias de ruido.
    """
    snr_db = np.arange(lim_inf, lim_sup + 1, 1)
    pot_ruido = pot_signal / (10 ** (snr_db / 10))
    return snr_db, pot_ruido

def graficar_chirp_con_y_sin_ruido(simbolos_modulados, indice, SF, B, pot_ruido):
    """
    Grafica la parte real o imaginaria del chirp LoRa con y sin ruido.

    Args:
        simbolos_modulados (Array): Lista de símbolos modulados en forma de chirps.
        indice (int): Índice del símbolo a graficar.
        SF (int): Spreading Factor.
        B (float): Ancho de banda en Hz.
        pot_ruido (float): Potencia de ruido (en escala lineal).
    """
    simbolo = simbolos_modulados[indice]
    simbolo_con_ruido = canal_AWGN(simbolo, pot_ruido)

    num_muestras = len(simbolo)
    Ts = (2**SF) / B # Duración total de un chirp
    T_muestra = Ts / num_muestras # Duración de una muestra
    tiempo = np.arange(num_muestras) * T_muestra * 1e6  # Tiempo en μs

    sin_ruido = np.real(simbolo)
    con_ruido = np.real(simbolo_con_ruido)
    titulo_parte = "Parte Real"

    plt.figure(figsize=(12, 4))
    plt.plot(tiempo, sin_ruido, label='Sin Ruido', linewidth=1.2, color='blue')
    plt.plot(tiempo, con_ruido, label='Con Ruido', linewidth=1.2, color='orange', alpha=0.7)
    plt.title(f"Chirp LoRa - {titulo_parte} - Índice {indice} (SF={SF})", fontsize=14, weight='bold')
    plt.xlabel("Tiempo [μs]")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def canal_multipath(signal_in, pot_ruido):
    """
    Aplica el filtro h[n] = sqrt(0.8)δ[n] + sqrt(0.2)δ[n−1] a cada chirp (fila) y
    agrega ruido. Se recorta para mantener la longitud original sin relleno artificial.

    Args:
        signal_in (np.ndarray): Array (n_chirps, total_muestras)
        pot_ruido (float): Potencia del ruido (lineal)

    Returns:
        np.array: Señal con forma (n_chirps, total_muestras)
    """
    h = np.array([np.sqrt(0.8), np.sqrt(0.2)])
    chirps_filtrados = []

    for chirp in signal_in:
        chirp_filtrado = np.convolve(chirp, h, mode="full")[: len(chirp)]
        chirps_filtrados.append(chirp_filtrado)

    signal_filtrada = np.array(chirps_filtrados)

    # Agregar ruido complejo
    desv_est = np.sqrt(pot_ruido / 2)
    ruido = np.random.normal(0, desv_est, size=signal_filtrada.shape) + 1j * np.random.normal(0, desv_est, size=signal_filtrada.shape)

    return signal_filtrada + ruido

def simulaciones_de_canal(bits_tx,SF,B,min_snr_AWGN,max_snr_AWGN,min_snr_multipath,max_snr_multipath,):
    """
    Simula el envio de bits a traves de un canal multipath, grafica la BER vs SNR
    
    Args:
        bits_tx (list): Bits a transmitir.
        SF (int): Spreading Factor.
        samples_per_chirp (int): Muestras por chirp o factor de oversampling.
        B (int): Ancho de banda en Hz.
        min_snr (int): SNR mínima en dB.
        max_snr (int): SNR máxima en dB.
    """
    # 1. Codificacion
    simbolos_tx = codificador(SF, bits_tx)

    # 2. Modulacion
    simbolos_modulados = conformador_de_onda(simbolos_tx, SF, B)

    # 3. Calcular potencia de la señal
    pot_signal = np.var(simbolos_modulados) + (np.mean(np.abs(simbolos_modulados))) ** 2

    # 4. Generar SNR y potencias de ruido
    snr_db_AWGN, pot_ruido_AWGN = potencias_de_ruido(pot_signal, min_snr_AWGN, max_snr_AWGN)
    snr_db_multipath, pot_ruido_multipath = potencias_de_ruido(pot_signal, min_snr_multipath, max_snr_multipath)

    # 5. Simular canal y demodular para cada SNR
    ber_values_AWGN = []
    ber_values_multipath = []
    i = 1
    print("---"*10)
    print("BER VS CANAL AWGN")
    for pn in pot_ruido_AWGN:
        simbolos_con_ruido_AWGN = canal_AWGN(simbolos_modulados, pn)
        simbolos_rx_AWGN = formador_de_ntuplas(simbolos_con_ruido_AWGN, SF)
        bits_rx_AWGN = decodificador(simbolos_rx_AWGN, SF)
        ber_AWGN = calculador_ber(bits_tx, bits_rx_AWGN)
        print(f" Punto {i} - BER: {ber_AWGN}")
        ber_values_AWGN.append(ber_AWGN)
        i += 1
    print("---"*10)
    print("BER VS CANAL SELECTIVO EN FRECUENCIA")
    j = 1
    for pn in pot_ruido_multipath:
        simbolos_con_ruido_multipath = canal_multipath(simbolos_modulados, pn)
        simbolos_rx_multipath = formador_de_ntuplas(simbolos_con_ruido_multipath, SF)
        bits_rx_multipath = decodificador(simbolos_rx_multipath, SF)
        ber_multipath = calculador_ber(bits_tx, bits_rx_multipath)
        print(f"Punto {j} - BER: {ber_multipath}")
        ber_values_multipath.append(ber_multipath)
        j += 1
    print("---"*10)
    # 6. Graficar
    plt.figure(figsize=(6, 4))
    plt.semilogy(snr_db_AWGN, ber_values_AWGN, "s-r", label="Flat FSCM", linewidth=0.8)
    plt.semilogy(snr_db_multipath, ber_values_multipath, "D-b", label="Freq. sel. FSCM", linewidth=0.8)
    plt.xlim(-12, -1)
    plt.ylim(10**-5, 10**-1)
    plt.xticks(np.arange(-12, 0, 1))
    plt.title("BER vs SNR")
    plt.xlabel("SNR [dB]")
    plt.ylabel("BER")
    plt.grid(True, linestyle="--", which="both")
    plt.legend()
    plt.tight_layout()
    plt.show()

def build_tx_frame(simbolos_data, SF, preamble_len=8):
    M  = 2**SF  
    k = np.arange(M)
    fase = (k**2) / M
    upchirp = (1 / np.sqrt(M)) * np.exp(1j * 2 * np.pi * fase)
    # Upchirp base para dechirp
    dechirp = np.conj(upchirp)

    # preámbulo: Np up-chirps
    pre = np.tile(upchirp, preamble_len) #Repite el up-chirp 'preamble_len' veces

    # SFD: 2 + 1/4 down-chirps (2.25)
    sfd = np.concatenate([np.tile(dechirp, 2), dechirp[:M//4]]) #repite 2 veces el down-chirp y luego agrega un cuarto de down-chirp

    # payload (matriz símbolos → vector)
    payload = conformador_de_onda(simbolos_data,SF).flatten()          

    trama = np.concatenate([pre, sfd, payload])

    return trama

def visualizar_estructura_trama(frame, simbolos_data, SF, preamble_len=8):
    """
    Visualiza la estructura de una trama LoRa, mostrando las secciones de preámbulo, SFD y payload,
    tanto en el dominio temporal como en la frecuencia instantánea.

    Args:
        frame (array): Trama LoRa completa.
        simbolos_data (array): Símbolos de datos (payload).
        SF (int): Spreading Factor.
        preamble_len (int): Longitud del preámbulo en chirps (por defecto 8).
    """
    M = 2**SF  # Número de muestras por chirp (dependiente de SF)

    # Calcular longitudes de cada sección
    len_preamble = preamble_len * M
    len_sfd = int(2.25 * M)  # SFD: 2.25 chirps
    len_payload = len(simbolos_data) * M
    len_total = len_preamble + len_sfd + len_payload

    # Índices de delimitación
    idx_sfd_start = len_preamble
    idx_payload_start = len_preamble + len_sfd

    # Verificar longitud de la trama
    print("---" * 10)
    print("ESTRUCTURA TEORICA DE LA TRAMA LoRa")
    print(f"SF = {SF}, M = {M}")
    print("---" * 10)
    print(f"\nLongitudes esperadas:")
    print(f"Preámbulo ({preamble_len} up-chirps): {len_preamble} muestras")
    print(f"SFD (2.25 down-chirps):  {len_sfd} muestras")
    print(f"Payload ({len(simbolos_data)} símbolos): {len_payload} muestras")
    print(f"TOTAL: {len_total} muestras")
    print("---" * 10)
    print("ESTRUCTURA REAL DE LA TRAMA LoRa")
    print(f"\nLongitud real de la trama: {len(frame)} muestras")
    print(f"Diferencia: {len(frame) - len_total} muestras")
    print(f"\nSímbolos del payload: {simbolos_data}")
    print("---" * 10)

    # GRÁFICO 1: Estructura temporal completa (parte real)
    fig, ax = plt.subplots(figsize=(15, 4))
    fig.patch.set_facecolor('black')  # Fondo negro para toda la figura
    ax.set_facecolor('black')  # Fondo negro para el área del gráfico

    t = np.arange(len(frame))  # Vector de tiempo
    ax.plot(t, np.real(frame), linewidth=1.5, color='blue')  # Parte real de la trama

    # Marcadores verticales para las secciones
    ax.axvline(idx_sfd_start, color='red', linestyle=':', linewidth=2, label='Inicio SFD')
    ax.axvline(idx_payload_start, color='green', linestyle=':', linewidth=2, label='Inicio Payload')

    # Sombreado de regiones
    ax.axvspan(0, idx_sfd_start, alpha=0.4, color='cyan', label='Preámbulo')
    ax.axvspan(idx_sfd_start, idx_payload_start, alpha=0.4, color='yellow', label='SFD')
    ax.axvspan(idx_payload_start, len(frame), alpha=0.4, color='lightgreen', label='Payload')

    # Etiquetas y título
    ax.set_xlabel('Muestras', color='white')
    ax.set_ylabel('Amplitud (Parte Real)', color='white')
    ax.set_title('Estructura Completa de la Trama LoRa', color='white')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
    ax.tick_params(colors='white')  # Cambiar color de los ejes
    plt.tight_layout()
    plt.show()

    # GRÁFICO 2: Frecuencia instantánea de toda la trama
    fase = np.unwrap(np.angle(frame))  # Desenvuelve la fase
    frec_inst = np.diff(fase) / (2 * np.pi)  # Calcula la frecuencia instantánea

    fig, ax = plt.subplots(figsize=(15, 5))
    fig.patch.set_facecolor('black')  # Fondo negro para toda la figura
    ax.set_facecolor('black')  # Fondo negro para el área del gráfico

    t_frec = np.arange(len(frec_inst))  # Vector de tiempo para frecuencia instantánea
    ax.plot(t_frec, frec_inst, linewidth=1, color='blue')  # Frecuencia instantánea

    # Marcadores verticales para las secciones
    ax.axvline(idx_sfd_start, color='red', linestyle='--', linewidth=2, label='Inicio SFD')
    ax.axvline(idx_payload_start, color='green', linestyle='--', linewidth=2, label='Inicio Payload')

    # Sombreado de regiones
    ax.axvspan(0, idx_sfd_start, alpha=0.15, color='cyan')
    ax.axvspan(idx_sfd_start, idx_payload_start, alpha=0.15, color='yellow')
    ax.axvspan(idx_payload_start, len(frame), alpha=0.15, color='lightgreen')

    # Anotaciones para cada sección
    ax.text(len_preamble / 2, ax.get_ylim()[1] * 0.9, 'PREÁMBULO\n(up-chirps)', ha='center', va='top', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='cyan', alpha=0.5))
    ax.text(idx_sfd_start + len_sfd / 2, ax.get_ylim()[1] * 0.9, 'SFD\n(down-chirps)', ha='center', va='top', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    ax.text(idx_payload_start + len_payload / 2, ax.get_ylim()[1] * 0.9, 'PAYLOAD\n(datos)', ha='center', va='top',
            fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

    # Etiquetas y título
    ax.set_xlabel('Muestras', color='white')
    ax.set_ylabel('Frecuencia Normalizada [ciclos/muestra]', color='white')
    ax.set_title('Frecuencia Instantánea - Verificación de Estructura LoRa', color='white')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
    ax.tick_params(colors='white')  # Cambiar color de los ejes
    plt.tight_layout()
    plt.show()

def cortar_en_chirps(trama, SF):
    M = 2**SF
    num_chirps = len(trama) // M
    chirps = trama[:num_chirps*M]    # recorta exceso
    return chirps.reshape(num_chirps, M)

def extraer_payload_chirps(trama, SF, preamble_len=8):
    M = 2**SF
    
    # Cortar la trama en chirps completos
    chirps = cortar_en_chirps(trama, SF)
    
    # Índices
    idx_pre_end = preamble_len
    idx_sfd_end = idx_pre_end + 2  # solo chirps completos (ignorar el 0.25)

    payload = chirps[idx_sfd_end:]
    return payload