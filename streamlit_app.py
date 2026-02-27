import streamlit as st

st.set_page_config(page_title="Dental Form Selector", layout="wide")
st.title("Dental Treatment Selector")

st.subheader("Select options:")

# ---- Dent number input ----
dent_number = st.number_input("# dent", min_value=1, max_value=32, step=1)

def chip_choice(label: str, options: list[str], key: str):
    """Single-select 'chips' via horizontal radio."""
    return st.radio(
        label,
        options,
        horizontal=True,
        key=key,
        label_visibility="visible",
    )

# ---- Categories (single-select) ----
categories = {
    "Cause": ["restauration défectueuse", "carie"],
    "Ablation": [
        "totale",
        "partielle jusqu’à consistance cuire (proximité pulpaire)"
    ],
    "Isolation": ["digue", "coton/dry-angle", "svédoptère"],
    "Etch": ["Oui", "Non"],
    "Adhésif": ["optibond", "all-bond"],
    "Base": ["rien", "ionoseal", "dycal", "calcimol"],
    "Matériel": [
        "amalgame",
        "composite filtek supreme",
        "composite spectra",
        "fuji 2LC"
    ],
    "Couleur": ["A1", "A2", "A3"],
    "Occlusion": ["polissage", "soie"]
}

selected_fields = {}
for category, options in categories.items():
    selected_fields[category] = chip_choice(f"{category}:", options, key=category)

# ---- Summary Output ----
st.subheader("Generated Note:")

summary_lines = [f"# dent: {dent_number}"]
summary_lines += [f"{k}: {v}" for k, v in selected_fields.items()]

st.text_area("", "\n".join(summary_lines), height=300)
