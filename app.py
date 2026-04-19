from solax_lib import SolaxInverter
import time

inv = SolaxInverter("192.168.10.10", "SREAZABLZU")

while True:
    data = inv.get_data()
    if data:
        soc = data['Kapacita Batérie (SoC)']['value']
        pwr = data['Export/Import Siete']['value']
        
        print(f"Batéria: {soc}% | Sieť: {pwr} W")
    else:
        print("Menič nedostupný...")
    
    time.sleep(5)