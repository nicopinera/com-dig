from loraRx import LoraRx
from loraTx import LoraTx

# Parametros
B=125e3 # Ancho de banda
simbolos = 10 #Simbolos a transmitir
SF = 8 #Tamaño de los simbolos
bits = SF * simbolos #Bits necesarios
samples_per_chirp = 4 #Muestrar por chirp

loratx = LoraTx(bits,SF,B,samples_per_chirp)   # LoRa para transmitir
loratx.toString()
lorarx = LoraRx(loratx) # LoRa para recibir
lorarx.toString()