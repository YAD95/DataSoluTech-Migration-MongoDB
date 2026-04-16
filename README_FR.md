🇫🇷 Français | [🇬🇧 English](README_ENG.md)
# 🏥 DataSoluTech – Migration & Scalabilité de Données Médicales

Projet réalisé dans le cadre de la formation **Data Engineer – OpenClassrooms**.

Dans ce projet, l’objectif principal est de migrer des données médicales stockées dans un fichier CSV vers une base **MongoDB**, puis de déployer l’ensemble de la solution dans une architecture **conteneurisée avec Docker**.

L’idée est donc de construire un projet reproductible, automatisé et facilement exécutable en local, tout en appliquant de bonnes pratiques de **sécurité**, de **gestion des accès** et de **qualité des données**.

---

## ---Objectif du projet---

Les objectifs de ce projet sont :

* migrer des données patients depuis un fichier CSV vers **MongoDB**
* automatiser le traitement avec un script **Python**
* exécuter toute la solution dans des **conteneurs Docker**
* rendre le projet facilement lançable en local par un autre utilisateur
* sécuriser les accès à la base avec des **variables d’environnement**
* mettre en place une gestion des rôles MongoDB (**RBAC**)
* vérifier la qualité des données grâce à des **tests automatisés**

---

##  ---Données utilisées---

Les données utilisées correspondent à un dataset médical contenant notamment :

* le nom du patient
* l’âge
* le genre
* le groupe sanguin
* la pathologie
* la date d’admission
* le médecin en charge
* l’hôpital
* l’assurance
* le traitement prescrit
* les résultats d’examens

Ces données sont initialement stockées dans un **fichier CSV** puis transformées avant leur insertion dans **MongoDB**.

---

## ---Architecture du projet---

Le projet repose sur une architecture simple et conteneurisée avec **Docker Compose** :

*  **MongoDB (`mongo:7`)** pour stocker les données médicales
*  **Python** pour exécuter le pipeline ETL
*  **`init-mongo.js`** pour initialiser automatiquement les rôles MongoDB
*  **Volume Docker `mongo_data`** pour conserver les données

Cette architecture permet d’exécuter le projet dans un environnement isolé, reproductible et portable.

---

## ---🔧 Transformation et nettoyage des données---

Plusieurs transformations sont appliquées lors du traitement :

* lecture du fichier CSV avec **Pandas**
* suppression des doublons
* nettoyage et normalisation des champs texte
* conversion des dates au format ISO
* transformation des données en dictionnaires JSON
* insertion dans la collection **`Patients`**

---

## ---⚙️ Pipeline ETL---

Le script `code_migration.py` met en œuvre les étapes suivantes :

* **Extraction** : lecture des données du fichier CSV
* **Transformation** : nettoyage, déduplication et formatage
* **Chargement** : insertion dans MongoDB
* **Optimisation** : création d’index sur `Name` et `Date of Admission`

Le script est conçu de manière à pouvoir être relancé sans casser la base existante, ce qui rend le pipeline plus robuste.

---

## ---Tests automatisés---

À la fin du script Python, **trois tests** sont exécutés automatiquement :

* ✅ **Test 1 – Volumétrie** : vérification du nombre total de documents insérés
* ✅ **Test 2 – Unicité** : vérification qu’il n’existe aucun doublon sur `_id`
* ✅ **Test 3 – Qualité** : vérification qu’aucun document n’a de valeur manquante sur les champs critiques `Name` et `Age`

Ces tests permettent de valider la bonne exécution de la migration et la qualité minimale des données chargées.

---

## ---🔒 Sécurité & gestion des accès---

###  Gestion des mots de passe

Les identifiants MongoDB ne sont pas écrits en dur dans le code.

* le fichier `docker-compose.yml` utilise des **variables d’environnement**
* les identifiants sont renseignés dans un fichier **`.env`**
* le vrai fichier `.env` ne doit **jamais** être envoyé sur GitHub
* le fichier `.gitignore` est utilisé pour bloquer ce fichier sensible
* seul le fichier **`.env.example`** est versionné dans le repository

👉 Cela permet de protéger les secrets et d’éviter d’exposer un mot de passe en clair.

---

### ---👥 Gestion des rôles (RBAC)---

Trois rôles sont configurés dans le projet :

* **`admin_medical`** : rôle **Root**, défini via le fichier `.env`
* **`data_engineer`** : rôle avec droits **`readWrite`** sur la base **MedicalDB**
* **`data_reader`** : rôle avec droits **`read`** sur la base **MedicalDB**

Les rôles **`data_engineer`** et **`data_reader`** sont créés automatiquement au démarrage grâce au script **`init-mongo.js`**.

---

## ---Comment lancer et tester le projet en local---

### 1. Cloner le repository

```bash
git clone https://github.com/YAD95/DataSoluTech-Migration-MongoDB.git
cd DataSoluTech-Migration-MongoDB
```

### 2. Préparer le fichier d’environnement

Copier le fichier d’exemple fourni dans le projet :

```bash
cp .env.example .env
```

Puis compléter le fichier `.env` avec ses propres identifiants :

```env
MONGO_ROOT_USER=admin_medical
MONGO_ROOT_PASSWORD=your_secure_password
```

### 3. Construire et lancer les conteneurs

```bash
docker compose up --build
```

Cette commande permet de :

* construire les services
* démarrer MongoDB
* injecter les variables d’environnement
* créer automatiquement les rôles MongoDB
* exécuter le script de migration Python

### 4. Vérifier que la migration a bien fonctionné

L’utilisateur peut contrôler le résultat de plusieurs façons :

* en lisant les logs du conteneur Python
* en vérifiant l’exécution des **3 tests automatisés**
* en se connectant à MongoDB Compass avec une URI du type :

```bash
mongodb://<MONGO_ROOT_USER>:<MONGO_ROOT_PASSWORD>@localhost:27018/
```

Il peut ensuite consulter la base **MedicalDB** et la collection **`Patients`**.

### 5. Arrêter et nettoyer l’environnement

```bash
docker compose down -v
```

Cette commande supprime les conteneurs ainsi que les volumes pour repartir d’un environnement propre.

---

## ---📊 Structure des données---

La collection principale du projet est :

* **`Patients`**

Elle contient des informations médicales, administratives et personnelles sur les patients.

Exemples de champs présents :

* `Name`
* `Age`
* `Gender`
* `Blood Type`
* `Medical Condition`
* `Date of Admission`
* `Doctor`
* `Hospital`
* `Insurance Provider`
* `Billing Amount`
* `Medication`
* `Test Results`

---

## --- Technologies utilisées---

* **Python**
* **Pandas**
* **MongoDB**
* **Docker**
* **Docker Compose**
* **JavaScript (`init-mongo.js`)**
* **NoSQL**
* **ETL**

---

## ---Contenu du repository---

* `code_migration.py` → script Python de migration ETL
* `docker-compose.yml` → orchestration des conteneurs
* `init-mongo.js` → création automatique des rôles MongoDB
* `.env.example` → modèle de fichier d’environnement
* `README.md` → documentation du projet
* fichier CSV → source de données patients

---

## ---Compétences mobilisées---

Ce projet met en pratique plusieurs compétences de Data Engineering :

* migration de données
* traitement ETL
* manipulation de données avec Python
* utilisation de MongoDB
* conteneurisation avec Docker
* sécurisation des credentials
* gestion des rôles et permissions
* automatisation des contrôles qualité

---

## ---👨‍💻 Auteur---

**YAD95**
Projet OpenClassrooms – Data Engineer
