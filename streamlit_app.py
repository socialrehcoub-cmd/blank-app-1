import streamlit as st

st.set_page_config(page_title="DO Note Generator", layout="wide")

# --- Compact CSS ---
st.markdown(
    """
    <style>
      /* tighter vertical spacing */
      div.block-container {padding-top: 1.2rem; padding-bottom: 1.2rem;}
      .stRadio, .stTextInput, .stNumberInput, .stTextArea {margin-bottom: 0.35rem;}
      label {font-size: 0.85rem !important;}
      /* shrink radio items */
      div[role="radiogroup"] > label {padding: 0.15rem 0.35rem !important;}
      /* make text inputs shorter */
      input {padding-top: 0.15rem !important; padding-bottom: 0.15rem !important;}
      textarea {padding-top: 0.35rem !important; padding-bottom: 0.35rem !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("DO")

def chip(label: str, options: list[str], key: str, index: int = 0):
    return st.radio(label, options, horizontal=True, key=key, index=index)

def render_do_note():
    lines = [
        "DO",
        "Confirmation du plan de tx avec le patient, questions répondues",
        f"# dent: {st.session_state.get('dent','')}",
        f"Confirmation dx: {st.session_state.get('confirm_dx','')}",
        f"Cause: {st.session_state.get('cause','')}",
        f"Ablation: {st.session_state.get('ablation','')}",
        f"Isolation: {st.session_state.get('isolation','')}",
        f"Système matrice: {st.session_state.get('matrice','')}",
        f"Liner: {st.session_state.get('liner','')}",
        f"Base: {st.session_state.get('base','')}",
        "Etch",
        "Gluma",
        f"Adhésif: {st.session_state.get('adhesif','')}",
        f"Matériel: {st.session_state.get('materiel','')}",
        f"Couleur: {st.session_state.get('couleur','')}",
        "Ablation excès, occlusion, polissage, soie",
        f"Détails à noter: {st.session_state.get('details','')}",
        "Risque de sensibilité temporaire expliqué au patient",
        "Risque d’endo car carie profonde expliqué au patient",
        "Patient comprend",
        "Patient confortable",
        "Questions du patient répondues",
        f"PRV: {st.session_state.get('prv','')}",
    ]
    return "\n".join(lines)

# -------------------------
# TOP ROW: dent + dx
# -------------------------
c1, c2 = st.columns([1, 3])
with c1:
    st.number_input("# dent", min_value=1, max_value=32, step=1, key="dent", label_visibility="collapsed")
    st.caption("# dent")
with c2:
    st.text_input("Confirmation dx", key="confirm_dx", label_visibility="collapsed")
    st.caption("Confirmation dx")

st.divider()

# -------------------------
# 2-column layout for chips
# -------------------------
left, right = st.columns(2, gap="large")

with left:
    chip("Cause:", ["restauration défectueuse", "carie"], key="cause")
    chip("Ablation:", ["totale", "partielle jusqu’à consistance cuire (proximité pulpaire)"], key="ablation")
    chip("Isolation:", ["coton + dry-angle", "digue", "svédoptère"], key="isolation")
    chip("Système matrice:", ["sectionnelle + coin de bois", "tofflemire + coin de bois"], key="matrice")

with right:
    chip("Liner:", ["ionoseal", "dycal", "calcimol"], key="liner")
    chip("Base:", ["vitrebond", "fuji 2 LC"], key="base")
    chip("Adhésif:", ["optibond", "all-bond"], key="adhesif")
    chip("Matériel:", ["amalgame", "composite filtek supreme", "composite spectra", "fuji 2LC"], key="materiel")
    chip("Couleur:", ["A1", "A2", "A3"], key="couleur")

st.text_area("Détails à noter", key="details", height=80)
st.text_input("PRV", key="prv")

st.divider()

# -------------------------
# NOTE (compact)
# -------------------------
with st.expander("Note générée", expanded=True):
    st.text_area("", render_do_note(), height=260)
