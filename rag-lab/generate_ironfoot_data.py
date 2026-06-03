import os
import random
import json

BASE_DIR = "rag-lab/ironfoot-bank-demo"
os.makedirs(BASE_DIR, exist_ok=True)

LORE = {
    "currencies": ["Mithril", "Gold", "Iron", "Dragon-scale"],
    "locations": ["Erebor", "Iron Hills", "Khazad-dûm", "Blue Mountains"],
    "figures": ["Thrain II", "Dain Ironfoot", "Thorint", "Balin"]
}

def generate_data():
    print(f"Starting generation in {BASE_DIR}")
    
    # 1. Ledgers
    for loc in LORE["locations"]:
        path = os.path.join(BASE_DIR, f"ledger_{loc.lower().replace(' ', '_')}.md")
        with open(path, "w") as f:
            f.write(f"# Ledger for {loc}\n")
            f.write(f"Vault Master: {random.choice(LORE['figures'])}\n\n")
            f.write("| ID | Currency | Amount |\n|---|---|---|\n")
            for _ in range(3):
                f.write(f"| ACC-{random.randint(10,99)} | {random.choice(LORE['currencies'])} | {random.randint(1,100)} |\n")
        print(f"Created: {path}")

    # 2. Loans (HTML)
    for i in range(3):
        loan_id = f"LOAN-{i}"
        path = os.path.join(BASE_DIR, f"loan_{loan_id}.html")
        with open(path, "w") as f:
            f.write(f"<html><body><h1>Loan {loan_id}</h1><p>Collateral: {random.choice(LORE['currencies'])}</p></body></html>")
        print(f"Created: {path}")

    # 3. Security
    for loc in LORE["locations"]:
        path = os.path.join(BASE_DIR, f"security_{loc.lower().replace(' ', '_')}.md")
        with open(path, "w") as f:
            f.write(f"# Security Protocol {loc}\nStep 1: Use rune {random.randint(1,9)}")
        print(f"                Created: {path}")

    # 4. Queries
    queries = [{"query": "test", "type": "test"}]
    with open(os.path.join(BASE_DIR, "test_queries.json"), "w") as f:
        json.dump(queries, f)
    print("Created test_queries.json")

if __name__ == "__main__":
    generate_data()
