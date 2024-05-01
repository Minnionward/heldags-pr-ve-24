from pymongo import MongoClient
from bson.objectid import ObjectId

# Koble til MongoDB
client = MongoClient("mongodb+srv://Minionward:czQmUj28yr9kR9S@cluster0.szjwecp.mongodb.net/") 
db = client.dronedrop  # Navn på databasen
missions = db.missions  # Collection for oppdrag

# funskjon for å vise info om oppdrag
def vis_oppdrag(oppdrag):
    print(f"ID: {oppdrag['_id']}")
    print(f"Beskrivelse: {oppdrag['description']}")
    print(f"Status: {oppdrag['status']}")
    print(f"Tildelt drone: {oppdrag['assigned_drone']}")
    print(f"Tidspunkt: {oppdrag['timestamp']}")
    print("-" * 20)

# kommande linje grensesnitt
while True:
    print("Velg en handling:")
    print("1. Opprett et nytt oppdrag")
    print("2. Vis alle oppdrag")
    print("3. Oppdater et oppdrag")
    print("4. Slett et oppdrag")
    print("5. Avslutt")

    valg = input("Skriv inn nummeret til ønsket handling: ")

    if valg == "1":
        # Opprett et nytt oppdrag
        beskrivelse = input("Beskrivelse: ")
        status = input("Status (standard 'pending'): ") or "pending"
        tildelt_drone = input("Tildelt drone: ")
        tidspunkt = input("Tidspunkt: ")
        
        nytt_oppdrag = {
            "description": beskrivelse,
            "status": status,
            "assigned_drone": tildelt_drone,
            "timestamp": tidspunkt,
        }
        
        result = missions.insert_one(nytt_oppdrag)
        print(f"Oppdrag opprettet med ID: {result.inserted_id}")

    elif valg == "2":
        # Vis alle oppdrag
        alle_oppdrag = list(missions.find({}))
        for oppdrag in alle_oppdrag:
            vis_oppdrag(oppdrag)

    elif valg == "3":
        # Oppdater et oppdrag
        mission_id = input("Skriv inn ID til oppdraget som skal oppdateres: ")
        oppdateringer = {}

        beskrivelse = input("Ny beskrivelse (trykk Enter for å hoppe over): ")
        if beskrivelse:
            oppdateringer["description"] = beskrivelse

        status = input("Ny status (trykk Enter for å hoppe over): ")
        if status:
            oppdateringer["status"] = status

        tildelt_drone = input("Ny tildelt drone (trykk Enter for å hoppe over): ")
        if tildelt_drone:
            oppdateringer["assigned_drone"] = tildelt_drone

        tidspunkt = input("Nytt tidspunkt (trykk Enter for å hoppe over): ")
        if tidspunkt:
            oppdateringer["timestamp"] = tidspunkt
        
        result = missions.update_one({"_id": ObjectId(mission_id)}, {"$set": oppdateringer})
        
        if result.matched_count == 0:
            print("Oppdrag ikke funnet")
        else:
            print("Oppdrag oppdatert")

    elif valg == "4":
        # Slett et oppdrag
        mission_id = input("Skriv inn ID til oppdraget som skal slettes: ")
        result = missions.delete_one({"_id": ObjectId(mission_id)})

        if result.deleted_count == 0:
            print("Oppdrag ikke funnet")
        else:
            print("Oppdrag slettet")

    elif valg == "5":
        # Avslutt
        break
    
    else:
        print("Ugyldig valg, prøv igjen.")

    print("\n")  # Tom linje mellom handlinger
