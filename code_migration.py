import pandas as pd
import pymongo
import os 
#charge le fichier
file_path = os.path.join(os.path.dirname(__file__), "healthcare_dataset.csv")
df = pd.read_csv(file_path)

#Le scanner complet : Types de colonnes et Valeurs manquantes
print(" ----- INFOS SUR LES COLONNES -----")
print(df.info())
print("\n")

#Le détecteur de doublons
nombre_doublons = df.duplicated().sum()
print(f" ----- NOMBRE DE DOUBLONS EXACTS : {nombre_doublons} -----")

# suppression doublon
df.drop_duplicates(inplace=True)
print(f"Les doublons supprimés. Nouveau total : {len(df)} lignes.")

# mise en format propre 1er lettre en majuscule
colonnes_texte = ['Name', 'Gender', 'Medical Condition', 'Doctor', 'Hospital', 'Insurance Provider', 'Admission Type', 'Medication', 'Test Results']
for col in colonnes_texte:
    df[col] = df[col].str.title().str.strip()

# conversion des dates
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])

print("Dates converties et text nettoyé")

# dernière vérification  
print("\n ----- NOUVEAU BILAN APRÈS NETTOYAGE -----")
df.info()


# connexion à MongoDB 
try:
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_user = os.getenv("MONGO_USER", "")
    mongo_mdp = os.getenv("MONGO_MDP", "")
    
    # 1. On prépare l'URL de connexion selon si on a un mot de passe ou non
    if mongo_user and mongo_mdp:
        print("🔒 Tenative de la connexion SÉCURISÉE avec identifiants...")
        mongo_url = f"mongodb://{mongo_user}:{mongo_mdp}@{mongo_host}:27017/"
        print("  connexion SÉCURISÉE avec identifiants résussis✅ ")

    else:
        print("🔓 connexion SÉCURISÉE avec identifiants échoué ❌ \n  Connexion LOCALE sans mot de passe...")
        mongo_url = f"mongodb://{mongo_host}:27017/"

    
    client = pymongo.MongoClient(mongo_url)
    db = client["MedicalDB"]
    collection = db["Patients"]
    
    
    print("✅✅✅ Connexion à MongoDB réussie")

except Exception as e:
    print(f"❌❌❌ Erreur de connexion : {e}")

# DataFrame ---> Liste de dictionnaires car mongo comprends pas CVS il veut dictionnaire json
donnees_a_importer = df.to_dict(orient='records')


# si on relance le script encore et encore ça supprime tout avant de remettre des données
collection.delete_many({}) 

# On envoie tout 
resultat = collection.insert_many(donnees_a_importer)
print(f"✅✅✅ Migration terminée ! {len(resultat.inserted_ids)} documents insérés dans MongoDB.")

#création index pour performance (requête de Boris) pour que la recherhce soit plus rapide
# On en crée un sur le 'Name' et 'Date of Admission' 
collection.create_index([("Name", pymongo.ASCENDING)])
collection.create_index([("Date of Admission", pymongo.DESCENDING)])
print(" Index créés sur 'Name' et 'Date of Admission'.")


# On récupère les données depuis MongoDB (Demande de la mission )
cursor = collection.find({})
df_export = pd.DataFrame(list(cursor))

# correction  de l'erreur : On transforme l'_id MongoDB en texte  pour le JSON
if '_id' in df_export.columns:
    df_export['_id'] = df_export['_id'].astype(str)

# Exportation en JSON (on précise le format des dates pour éviter les bugs)
df_export.to_json("export_data_medical.json", orient="records", date_format='iso', indent=4)
print("📥 Données exportées avec succès dans 'export_data_medical.json'.")

# test 'd'intégrité automatisé (Recommandation Boris ) 
count_mongo = collection.count_documents({})
count_df = len(df)

print("\n ----- RAPPORT DE TEST AUTOMATISÉ -----")
if count_mongo == count_df:
    print(f"✅ SUCCÈS : 54966 documents trouvés en base sur 54966 attendus.")
else:
    print(f"❌ ÉCHEC : Incohérence entre le fichier ({count_df}) et la base ({count_mongo}).")