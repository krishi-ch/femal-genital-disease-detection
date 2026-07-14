import random
import csv
import pandas as pd

# After creating CSV, load to check
df = pd.read_csv("womens_health_symptoms.csv")

# Check for missing values
assert df.isnull().sum().sum() == 0, "Warning: Dataset contains missing values!"

# Check for duplicates
num_dupes = df.duplicated().sum()
print(f"Number of duplicate rows: {num_dupes}")

# Check class balance
print(df['diagnosis'].value_counts())

diagnoses = [
    "Bacterial Vaginosis", "Bartholin's Cyst", "Genital Herpes", "Genital Warts",
    "Lichen Sclerosus", "Trichomoniasis", "Vaginal Cancer", "Vaginal Fistula",
    "Vulvar Cancer", "Vulvar Dermatitis", "Vulvodynia", "Yeast Infection",
    "Cervical Cancer", "Cervical Dysplasia", "Cervical Incompetence", "Cervical Polyps",
    "Cervicitis", "Adenomyosis", "Asherman's Syndrome", "Endometrial Hyperplasia",
    "Endometrial Polyps", "Heavy Menstrual Bleeding", "Uterine Cancer", "Uterine Fibroids",
    "Uterine Prolapse", "Ectopic Pregnancy", "Fallopian Tube Cancer", "Hydrosalpinx",
    "Salpingitis", "Ovarian Cancer", "Ovarian Cysts", "Ovarian Endometrioma",
    "Ovarian Torsion", "Primary Ovarian Insufficiency", "Amenorrhea", "Dysmenorrhea",
    "Polycystic Ovary Syndrome (PCOS)", "Premenstrual Syndrome", "Premenstrual Dysphoric Disorder",
    "Endometriosis", "Infertility", "Pelvic Inflammatory Disease", "Pelvic Organ Prolapse",
    "Urinary Incontinence", "Chlamydia", "Gonorrhea", "Syphilis"
]
fields = ["age","itching","discharge","abdominal_pain","rash","bleeding","ulcer","swelling","lump","odor","painful_urination","diagnosis"]

symptoms = fields[1:-1]
signature_map = {}
used_signatures = set()
random.seed(42)
for d in diagnoses:
    while True:
        sig = tuple(sorted(random.sample(symptoms, 3)))
        if sig not in used_signatures:
            signature_map[d] = set(sig)
            used_signatures.add(sig)
            break

rows = []
n_per_class = 200
for diagnosis in diagnoses:
    for i in range(n_per_class):
        age = random.randint(18, 70)
        row = [age]
        for symptom in symptoms:
            if symptom in signature_map[diagnosis]:
                prob = 0.98
            else:
                prob = 0.02
            row.append(1 if random.random() < prob else 0)
        row.append(diagnosis)
        rows.append(row)

with open("womens_health_symptoms.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(rows)

print("Highly distinct dataset written—{:,} rows, {} classes!".format(len(rows), len(diagnoses)))
