import json

with open("lab4", "JSON", "sample-data (1).json", "r") as file:
    data = json.load(file)

# Заголовок таблицы
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU':<10}")
print("-" * 90)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    descr = attributes["descr"] or "N/A"
    speed = attributes["speed"]
    mtu = attributes["mtu"]

    print(f"{dn:<50} {descr:<20} {speed:<10} {mtu:<10}")
