from solax_lib import SolaxInverter
import time

inv = SolaxInverter("192.168.10.10", "SREAZABLZU")

while True:
    data = inv.get_data()
    if data:
        soc = data['Battery Capacity (SoC)']['value']
        pwr = data['Export/Import Grid']['value']
        
        print(f"Batéria: {soc}% | Sieť: {pwr} W")
    else:
        print("Invertor not anavalible...")
    
    time.sleep(5)