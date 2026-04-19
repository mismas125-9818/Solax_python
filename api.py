from fastapi import FastAPI, HTTPException
from solax_lib import SolaxInverter
from datetime import datetime

app = FastAPI(title="SolaX Dynamic API")
inv = SolaxInverter("192.168.10.10", "SREAZABLZU")

@app.get("/api/v1/status")
async def get_status():
    data = inv.get_data() # Toto volá tvoju knižnicu
    
    if not data:
        raise HTTPException(status_code=503, detail="Inverter is offline or unreachable")

    # Dynamické výpočty (používame presné názvy z tvojho JSON)
    try:
        pv_pwr = (data["PV1 Voltage"]["value"] * data["PV1 Current"]["value"]) + \
                 (data["PV2 Voltage"]["value"] * data["PV2 Current"]["value"])
        
        bat_pwr = data["Battery Power"]["value"]
        grid_pwr = data["Export/Import Grid"]["value"]
        
        # House Load = PV výroba + Výkon batérie (vybíjanie) - Grid (export)
        house_load = pv_pwr + bat_pwr - grid_pwr
    except KeyError as e:
        # Ak by si v JSON zmenil názov a zabudol ho tu opraviť
        pv_pwr, house_load = 0, 0

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "metrics": {
            "pv_total_watts": round(pv_pwr, 2),
            "house_load_watts": round(abs(house_load), 2),
            "is_exporting": grid_pwr > 0
        },
        "full_data": data  # Tu FastAPI automaticky vypíše všetky linknuté údaje z JSON
    }

if __name__ == "__main__":
    import uvicorn
    # Spustí server na porte 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)