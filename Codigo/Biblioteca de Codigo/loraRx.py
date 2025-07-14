import numpy as np
class LoraRx:
    def __init__(self,lora_tx_instance):
        """
        Funcion Constructor
        
        Args:
            - total_bits (int): Total de bits a transmitir
            - SF (int) : Spreading Factor
            - B (int) : Ancho de Banda
            - samples_per_chirp (int) : Muestras por chirp
        """
        self.lora_tx = lora_tx_instance # Instancia de la clase
        self.total_bits = lora_tx_instance.total_bits # Total de bits
        self.bits_tx = lora_tx_instance.bits_tx # Bits transmitidos
        self.SF = lora_tx_instance.SF # Spreading Factor
        self.numero_de_simbolos = lora_tx_instance.numero_de_simbolos # Cantidad de simbolos
        self.simbolos_tx = lora_tx_instance.simbolos # Simbolos transmitidos
        self.B = lora_tx_instance.B #Ancho de banda
        self.samples_per_chirp = lora_tx_instance.samples_per_chirp #Muestras por simbolo
        self.simbolos_modulados = lora_tx_instance.simbolos_modulados # Chirps
        self.simbolos_rx = None # Salida del conformador de n-tuplas
        self.bits_rx = None # Bits recibidos
        self.ber = 0 # BER
        self.ser = 0 # SER
        self.simulacion()

    def decodificador(self):
        bits_rx = []

        for simbolo in self.simbolos_tx: # Se toma cada simbolo
            bits = []
            for _ in range(self.SF): # Se repite la division por 2 hasta SF-1
                bits.append(simbolo % 2)
                simbolo = simbolo//2
            bits_rx.extend(bits)  # Agrega los bits en orden LSB a MSB

        self.bits_rx = np.array(bits_rx,dtype=int) # Asegura que sea un array plano de enteros

    def formador_de_ntuplas(self):
        """
        Recupera los símbolos modulados mediante FSCM y estima los símbolos transmitidos a partir de ellos.

        Parámetros:
        - simbolos_modulados (Array): Lista de símbolos modulados en forma de chirps.
        - SF (int): Spreading Factor.
        - samples_per_chirp (int): Muestras por chirp o factor de oversampling.

        Retorna:
        - (list (int)): Lista de símbolos estimados.
        """
        Ns = 2**self.SF
        total_muestras = Ns * self.samples_per_chirp

        simbolos_estimados = []

        n = np.arange(total_muestras)
        k = n / self.samples_per_chirp  # Ajuste para oversampling
    
        exp_frec_decr = np.exp(-1j * np.pi * (k**2) / Ns)

        for r in self.simbolos_modulados:
        # Dechirp multiplicando por el conjugado del chirp base
            dechirp = r * exp_frec_decr
        
        # Calculamos la FFT
            fft_out = np.fft.fft(dechirp)
        
        # El valor máximo en la FFT nos da el símbolo estimado
            simbolo_estimado = int(np.argmax(np.abs(fft_out)))
        
        # Ajuste para oversampling
            simbolo_estimado = simbolo_estimado % Ns
        
            simbolos_estimados.append(simbolo_estimado)

        self.simbolos_rx = simbolos_estimados

    def calculador_ser(self):
        """
        Calcula la tasa de error de símbolos (SER) entre los símbolos transmitidos y recibidos.

        Args:
        simbolos_tx (list): Arreglo unidimensional de símbolos transmitidos.
        simbolos_rx (list): Arreglo unidimensional de símbolos recibidos.

        Returns:
        float: Tasa de error de símbolos (SER).
        """
        if len(self.simbolos_tx) != len(self.simbolos_rx):
            raise ValueError("Los arreglos de símbolos transmitidos y recibidos deben tener la misma longitud.")
    
        errores = np.sum(self.simbolos_tx != self.simbolos_rx)
        self.ser = errores / len(self.simbolos_tx)
    
    def calculador_ber(self):
        errores = np.sum(self.bits_tx != self.bits_rx)
        ber = errores / len(self.bits_tx)
        self.ber = ber
    def simulacion(self):
        self.formador_de_ntuplas()
        self.decodificador()
        self.calculador_ser()
        self.calculador_ber()
        
    def toString(self):
        print("---" * 10)
        print("Primeros 20 bits recibidos: ", self.bits_rx[0:20])
        print("---" * 10)
        print("Bits originales (muestra):   ", self.bits_tx[: 2 * self.SF])
        print("Bits decodificados (muestra):", self.bits_rx[: 2 * self.SF])
        print("La tasa de error de bit (BER) es: ", self.ber*100, "%")
        print("La tasa de error de simbolo (SER) es: ", self.ser*100, "%")
        print("---" * 10)