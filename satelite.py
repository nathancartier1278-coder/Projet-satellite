import serial
import requests
import time

# --- CONFIGURATION ---
PORT_COM = 'COM3'  # Remplace par le port de ton Arduino Récepteur (ex: COM4, COM5...)
VITESSE = 9600
URL_SITE_WEB = "https://nathancartier1278-coder.github.io/Projet-satellite/" # L'adresse de ton site
# ---------------------

print("Démarrage de la passerelle...")

try:
    # Connexion à l'Arduino
    arduino = serial.Serial(PORT_COM, VITESSE, timeout=1)
    print(f"Connecté à l'Arduino sur le port {PORT_COM}")
except Exception as e:
    print(f"Erreur de connexion : {e}")
    exit()

# Boucle de lecture infinie
while True:
    if arduino.in_waiting > 0:
        # On lit la ligne envoyée par l'Arduino
        ligne = arduino.readline().decode('utf-8').strip()
       
        # On vérifie si c'est bien une donnée de mesure (commence par "DATA:")
        if ligne.startswith("DATA:"):
            # On extrait juste le chiffre
            distance = ligne.split(":")[1]
            print(f"🛰️ Satellite : Mesure reçue -> {distance} mm")
           
            # Préparation du colis pour le site web
            donnees_a_envoyer = {'distance': distance}
           
            try:
                # Envoi au site web via une requête POST
                reponse = requests.post(URL_SITE_WEB, data=donnees_a_envoyer)
                if reponse.status_code == 200:
                    print("🌐 Site Web : Donnée enregistrée avec succès !")
                else:
                    print(f"⚠️ Erreur du site : Code {reponse.status_code}")
            except Exception as e:
                print(f"❌ Erreur de connexion au site : {e}")
               
    time.sleep(0.1)
