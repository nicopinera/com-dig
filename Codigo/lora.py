import numpy as np
class Lora:
    def __init__(self,total_bits,SF):
        self.total_bits = total_bits # Cantidad de bits a transmitir
        self.bits_tx = None # Bits transmitidos
        self.SF = SF # Spreading Factor
        self.numero_de_simbolos = None # Cantidad de simbolos detectados
        self.simbolos = None
        self.bits_rx = None
        self.ber = 0
        
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

    def decodificador(self):
        bits_rx = []

        for simbolo in self.simbolos: # Se toma cada simbolo
            bits = []
            for _ in range(self.SF): # Se repite la division por 2 hasta SF-1
                bits.append(simbolo % 2)
                simbolo = simbolo//2
            bits_rx.extend(bits)  # Agrega los bits en orden LSB a MSB

        self.bits_rx = np.array(bits_rx,dtype=int) # Asegura que sea un array plano de enteros

    def calculador_ber(self):
        errores = np.sum(self.bits_tx != self.bits_rx)
        ber = errores / len(self.bits_tx)
        self.ber = ber

    def toString(self):
        print("---" * 10)
        print("Primeros 20 bits a transmitir: ", self.bits_tx[0:20])
        print("---" * 10)
        print("Cantidad de simbolos detectados: ", self.numero_de_simbolos)
        print(f"Primeros {self.numero_de_simbolos} simbolos: ", self.simbolos[0:self.numero_de_simbolos])
        print("---" * 10)
        print("Primeros 20 bits recibidos: ", self.bits_rx[0:20])
        print("---" * 10)
        print("Bits originales (muestra):   ", self.bits_tx[: 2 * SF])
        print("Bits decodificados (muestra):", self.bits_rx[: 2 * SF])
        print("La tasa de error de bit (BER) es: ", self.ber*100, "%")
        print("---" * 10)

simbolos = 10
SF = 8
bits = SF * simbolos
mi_lora = Lora(bits,SF)
mi_lora.generate_random_bits()
mi_lora.codificador()
mi_lora.decodificador()
mi_lora.calculador_ber()
mi_lora.toString()