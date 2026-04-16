# 🏥 DataSoluTech – Medical Data Migration & Scalability

Project carried out as part of the **Data Engineer – OpenClassrooms** training program.

In this project, the main objective is to migrate medical data stored in a CSV file into a **MongoDB** database, and then deploy the entire solution within a **Docker containerized architecture**.

The idea is to build a reproducible, automated, and easily runnable local project, while applying best practices in **security**, **access management**, and **data quality**.

---

## ---Project Objectives---

The objectives of this project are:

* migrate patient data from a CSV file to **MongoDB**
* automate the process using a **Python** script
* run the entire solution inside **Docker containers**
* make the project easily runnable locally by another user
* secure database access using **environment variables**
* implement MongoDB role management (**RBAC**)
* ensure data quality using **automated tests**

---

## ---Dataset---

The data used corresponds to a medical dataset containing:

* patient name
* age
* gender
* blood type
* medical condition
* admission date
* attending doctor
* hospital
* insurance provider
* prescribed treatment
* test results

This data is initially stored in a **CSV file** and then transformed before being inserted into **MongoDB**.

---

## ---Project Architecture---

The project is based on a simple containerized architecture using **Docker Compose**:

*  **MongoDB (`mongo:7`)** to store medical data
*  **Python** to run the ETL pipeline
*  **`init-mongo.js`** to automatically initialize MongoDB roles
*  **Docker volume `mongo_data`** to persist data

This architecture allows the project to run in an isolated, reproducible, and portable environment.

---

## ---🔧 Data Transformation & Cleaning---

Several transformations are applied during processing:

* reading the CSV file using **Pandas**
* removing duplicates
* cleaning and normalizing text fields
* converting dates to ISO format
* transforming data into JSON dictionaries
* inserting data into the **`Patients`** collection

---

## ---⚙️ ETL Pipeline---

The script `code_migration.py` implements the following steps:

* **Extraction**: reading data from the CSV file
* **Transformation**: cleaning, deduplication, and formatting
* **Loading**: inserting into MongoDB
* **Optimization**: creating indexes on `Name` and `Date of Admission`

The script is designed to be rerunnable without breaking the existing database, making the pipeline more robust.

---

## ---Automated Tests---

At the end of the Python script, **three tests** are automatically executed:

* ✅ **Test 1 – Volume**: verification of the total number of inserted documents
* ✅ **Test 2 – Uniqueness**: verification that there are no duplicate `_id`
* ✅ **Test 3 – Quality**: verification that no document contains missing values in critical fields `Name` and `Age`

These tests ensure the correct execution of the migration and a minimum level of data quality.

---

## ---🔒 Security & Access Management---

###  Password Management

MongoDB credentials are not hardcoded in the code.

* the `docker-compose.yml` file uses **environment variables**
* credentials are stored in a **`.env`** file
* the real `.env` file must **never** be pushed to GitHub
* the `.gitignore` file is used to block this sensitive file
* only the **`.env.example`** file is versioned in the repository

👉 This helps protect secrets and prevents exposing passwords in plain text.

---

### ---👥 Role Management (RBAC)---

Three roles are configured in the project:

* **`admin_medical`**: **Root** role, defined via the `.env` file
* **`data_engineer`**: role with **`readWrite`** permissions on **MedicalDB**
* **`data_reader`**: role with **`read`** permissions on **MedicalDB**

The roles **`data_engineer`** and **`data_reader`** are automatically created at startup using the **`init-mongo.js`** script.

---

## ---How to Run and Test the Project Locally---

### 1. Clone the repository

```bash
git clone https://github.com/YAD95/DataSoluTech-Migration-MongoDB.git
cd DataSoluTech-Migration-MongoDB
