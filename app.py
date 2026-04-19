from solax_lib import SolaxInverter
from solax_sim import SolaxSim  # Importujeme simulátor
import time

# PREPÍNAČ: True = kaviareň/vlak | False = doma pri striedači
OFFLINE_MODE = False 

if OFFLINE_MODE:
    inv = SolaxSim("mapping.json")
    print("--- Running in OFFLINE SIMULATION mode ---")
else:
    inv = SolaxInverter("192.168.10.10", "SREAZABLZU")
    print("--- Running in LIVE mode ---")

while True:
    data = inv.get_data()
    if data:
        soc = data['Battery Capacity (SoC)']['value']
        pwr = data['Export/Import Grid']['value']
        invTemp = data["Inverter Temperature"]["value"]
        # V tvojom cykle while True:
        pv_power = (data['PV1 Voltage']['value'] * data['PV1 Current']['value']) + \
                (data['PV2 Voltage']['value'] * data['PV2 Current']['value'])

        print(f"PV Production: {round(pv_power, 0)} W")
        print(f"Grid: {data['Export/Import Grid']['value']} W")

        
        # Smer toku energie
        status = "EXPORT" if pwr > 0 else "IMPORT"
        
        print(f"Battery: {soc}% | Grid: {abs(pwr)} W ({status}) | InvTemperature: {invTemp}°C")
    else:
        print("Data source error...")
    
    time.sleep(5)