import streamlit as st

st.set_page_config(page_title="DO Note Generator", layout="wide")
st.title("DO")

# -----------------------
# Helpers
# -----------------------
def chip(label: str, options: list[str], key: str, index: int = 0):
    return st.radio(label, options, horizontal=True, key=key, index=index)

def render_do_note():
    lines = [
        "DO",
        "Confirmation du plan de tx avec le patient, questions répondues",
    ]

    # 🔴 Open ended
    lines.append(f"# dent: {st.session_state.get('dent','')}")
    lines.append(f"Confirmation dx: {st.session_state.get('confirm_dx','')}")

    # 🔵 Choices
    lines.append(f"Cause: {st.session_state.get('cause','')}")
    lines.append(f"Ablation: {st.session_state.get('ablation','')}")
    lines.append(f"Isolation: {st.session_state.get('isolation','')}")
    lines.append(f"Système matrice: {st.session_state.get('matrice','')}")
    lines.append(f"Liner: {st.session_state.get('liner','')}")
    lines.append(f"Base: {st.session_state.get('base','')}")
    
    # ⚫ Fixed text (not blue, not red)
    lines.append("Etch")
    lines.append("Gluma")

    # 🔵 Choices
    lines.append(f"Adhésif: {st.session_state.get('adhesif','')}")
    lines.append(f"Matériel: {st.session_state.get('materiel','')}")
    lines.append(f"Couleur: {st.session_state.get('couleur','')}")

    # ⚫ Fixed
    lines.append("Ablation excès, occlusion, polissage, soie")

    # 🔴 Open ended
    lines.append(f"Détails à noter: {st.session_state.get('details','')}")

    # ⚫ Fixed
    lines.extend([
        "Risque de sensibilité temporaire expliqué au patient",
        "Risque d’endo car carie profonde expliqué au patient",
        "Patient comprend",
        "Patient confortable",
        "Questions du patient répondues",
    ])

    # 🔴 Open ended
    lines.append(f"PRV: {st.session_state.get('prv','')}")

    return "\n".join(lines)


# =====================================================
# UI (ONLY DO)
# =====================================================

# 🔴 Open-ended fields
st.number_input("# dent:", min_value=1, max_value=32, step=1, key="dent")
st.text_input("Confirmation dx:", key="confirm_dx")

# 🔵 Blue = chips
chip("Cause:", ["restauration défectueuse", "carie"], key="cause")

chip(
    "Ablation:",
    ["totale", "partielle jusqu’à consistance cuire (proximité pulpaire)"],
    key="ablation",
)

chip(
    "Isolation:",
    ["coton + dry-angle", "digue", "svédoptère"],
    key="isolation",
)

chip(
    "Système matrice:",
    ["sectionnelle + coin de bois", "tofflemire + coin de bois"],
    key="matrice",
)

chip("Liner:", ["ionoseal", "dycal", "calcimol"], key="liner")

chip("Base:", ["vitrebond", "fuji 2 LC"], key="base")

chip("Adhésif:", ["optibond", "all-bond"], key="adhesif")

chip(
    "Matériel:",
    ["amalgame", "composite filtek supreme", "composite spectra", "fuji 2LC"],
    key="materiel",
)

chip("Couleur:", ["A1", "A2", "A3"], key="couleur")

# 🔴 Open-ended
st.text_area("Détails à noter:", key="details", height=120)
st.text_input("PRV:", key="prv")

# =====================================================
# NOTE OUTPUT (UNDER SECTION)
# =====================================================

st.divider()
st.subheader("Note générée")
st.text_area("", render_do_note(), height=500)
