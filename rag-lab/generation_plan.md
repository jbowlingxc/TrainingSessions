# Ironfoot Banking & Vault Services - Data Generation Plan

## 📂 Workspace Setup
All generated data will be contained within a dedicated subfolder: `rag-lab/ironfoot-bank-demo/`. This ensures isolation from other RAG experiments.

## 1. Data Archetypes & Complexity Strategy
To test a RAG system, we won't just generate text; we will generate specific *failure modes* and *retrieval challenges*.

| Document Type | Format | Technical Challenge | Middle-earth Theme |
| :--- | :--- | :--- | :--- |
| **Account Ledgers** | `Markdown` (Tables) | Extracting values from structured tables. | Deposits of Mithril, Gold, and Dragon-scale in Erebor. |
| **Loan Agreements** | `HTML` (Nested Tags) | Parsing hierarchical text and "fine print" in nested lists. | Terms for borrowing dwarven ale or iron ore; collateral requirements involving ancestral axes. |
| **Vault Security Protocols** | `Plain Text / PDF` | Following multi-step, sequential instructions. | Runes required to open the Khazad-dûm vault; dragon-fire's impact on security. |
| **Market Intelligence Reports** | `Markdown` (Narrative) | Disambiguating conflicting/noisy information. | News from the Iron Hills regarding trade route disruptions or Orc activity affecting gold value. |

## 2. Implementation Plan

### Phase 1: Entity & Lore Definition
I will first define a "Source of Truth" dictionary to ensure consistency across all generated files:
*   **Currencies**: Mithril (High), Gold (Medium), Iron (Low), Silmaril (Legendary/Non-existent).
*   **Locations**: Erebor, Iron Hills, Khazad-dûm, Blue Mountains.
*   **Key Figures**: Thrain II, Dain Ironfoot, etc.
*   **The "Conflict" Layer**: I will explicitly define one piece of "outpostdated" information (e.g., an old policy from the Second Age) to see if the RAG system retrieves the most recent regulation or the old one.

### Phase 2: Automated Generation Scripting
Instead of writing each file manually, I will create a Python generation script that:
1.  Uses a template engine (like Jinja2) to inject the "Lore" into structured Markdown and HTML templates.
2.  Generates random but consistent numbers (e.g., ensuring a withdrawal doesn't exceed a balance).
3.  Outputs the files into the destination folder: `rag-lab/ironfoot-bank-demo/`.

### Phase 3: Verification & Test Suite
Once generated, I will create a `test_queries.json` file containing:
*   **Simple Retrieval**: "What is the current interest rate for Mithril deposits?"
*   **Reasoning/Math**: "If a Dwarf deposits 50 Gold and the interest is 2%, what is the total after one year?"
*   **Disambiguation**: "Which vault protocol applies to the Erebar branch vs. the Iron Hills branch?"
*   **Conflict Detection**: "Does the 2941 Decree or the 3018 Amendment govern silver withdrawals?"

## 3. Key Constraints
*   **Pacing**: Total presentation time should be ~1 hour.
*   **Demos**: Allocate approximately **30 minutes** of the total time for demonstrations.
*   **Tone**: Professional, engaging, and authoritative.
*   **Clarity**: Expand all acronyms; use analogies where appropriate.
