import numpy as np
class LoraTx:
    def __init__(self,total_bits,SF,B,samples_per_chirp):
        """
        Funcion Constructor
        
        Args:
            - total_bits (int): Total de bits a transmitir
            - SF (int) : Spreading Factor
            - B (int) : Ancho de Banda
            - samples_per_chirp (int) : Muestras por chirp
        """
        self.total_bits = total_bits # Cantidad de bits a transmitir
        self.bits_tx = None # Bits transmitidos
        self.SF = SF # Spreading Factor
        self.numero_de_simbolos = None # Cantidad de simbolos detectados
        self.simbolos = None
        self.B = B
        self.samples_per_chirp = samples_per_chirp
        self.simbolos_modulados = None
        self.simulacion()
        
    def generate_random_bits(self):
        """
        Genera un vector de bits aleatorios (0 y 1) de longitud especificada.

        Args:
            cantidad_Bits (int): Cantidad de bits a generar.

        Returns:
            bits_transmitidos: Vector de bits aleatorios (0 y 1).
        """
        self.bits_tx = np.random.randint(0,2,self.total_bits)
    
    def codificador(self):
        numero_de_simbolos = self.total_bits // self.SF
        # Vector de ceros con la longitud de la cantidad de simbolos
        simbolos = np.zeros(numero_de_simbolos, dtype=int)

        # Sumatoria - Ecuacion 1
        ## Simbolo i
        for i in range(numero_de_simbolos):

            # de 0 hasta SF-1
            for h in range(self.SF):
                "Toma bits dentro de un bloque de bits de largo SF"
                "Luego se suma cada bit con su peso para obtener el valor decimal del simbolo a transmitir"

                bit = self.bits_tx[i*self.SF + h]
                simbolos[i] += bit * (2**h)  # Conversion a decimal

        self.simbolos = simbolos
        self.numero_de_simbolos = numero_de_simbolos

    def conformador_de_onda(self,):
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
        Ns = 2**self.SF  # Muestras por símbolo (cuando samples_per_chirp=1)
        T = 1 / self.B   # Duración de símbolo (segundos)
        delta = 1 / self.samples_per_chirp  # Paso de tiempo para oversampling
        total_muestras = Ns * self.samples_per_chirp  # Total de muestras por símbolo

        simbolos_modulados = []
        fmax = (Ns - 1) * self.B / Ns  # Frecuencia máxima para el chirp

        for s in self.simbolos:
            chirp = np.zeros(total_muestras, dtype=complex)
            k = s  
            for n in range(total_muestras):
                f = k * self.B / Ns
                t = k * T
                if f >= fmax:  # Modulo de 2**SF
                    k -= Ns    # Devuelve k a 0
                    f = k * self.B / Ns
                arg = f * t * 0.5 
                sample = (1 / np.sqrt(Ns * self.samples_per_chirp)) * np.exp(1j * 2 * np.pi * arg)
                chirp[n] = sample
                k += delta
            simbolos_modulados.append(chirp)
        self.simbolos_modulados = np.array(simbolos_modulados)


    def simulacion(self):
        self.generate_random_bits()
        self.codificador()
        self.conformador_de_onda()

    def toString(self):
        print("---" * 10)
        print("Primeros 20 bits a transmitir: ", self.bits_tx[0:20])
        print("---" * 10)
        print("Cantidad de simbolos detectados: ", self.numero_de_simbolos)
        print(f"Primeros {self.numero_de_simbolos} simbolos: ", self.simbolos[0:self.numero_de_simbolos])
        print("Primer Chirp: ", self.simbolos_modulados[0])
