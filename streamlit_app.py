import streamlit as st

st.set_page_config(page_title="DO", layout="wide")
st.title("DO")

def chip(label: str, options: list[str], key: str, index: int = 0):
    return st.radio(label, options, horizontal=True, key=key, index=index)

def render_do_note():
    ss = st.session_state
    lines = [
        "DO",
        "Confirmation du plan de tx avec le patient, questions répondues",
        f"# dent: {ss.get('dent', '')}",
        f"Confirmation dx: {ss.get('confirm_dx', '')}",
        f"Cause: {ss.get('cause', '')}",
        f"Ablation: {ss.get('ablation', '')}",
        f"Isolation: {ss.get('isolation', '')}",
        f"Système matrice: {ss.get('matrice', '')}",
        f"Liner: {ss.get('liner', '')}",
        f"Base: {ss.get('base', '')}",
        "Etch",
        "Gluma",
        f"Adhésif: {ss.get('adhesif', '')}",
        f"Matériel: {ss.get('materiel', '')}",
        f"Couleur: {ss.get('couleur', '')}",
        "Ablation excès, occlusion, polissage, soie",
        f"Détails à noter: {ss.get('details', '')}".rstrip(),
        "Risque de sensibilité temporaire expliqué au patient",
        "Risque d’endo car carie profonde expliqué au patient",
        "Patient comprend",
        "Patient confortable",
        "Questions du patient répondues",
        f"PRV: {ss.get('prv', '')}",
    ]
    # Remove lines that end up like "Confirmation dx: " with nothing
    cleaned = []
    for ln in lines:
        if ln.endswith(": ") or ln.endswith(":"):
            # keep if you prefer always showing labels; otherwise skip empties
            if ln.strip().endswith(":"):
                continue
            continue
        cleaned.append(ln)
    return "\n".join(cleaned)

# Two-pane layout
form_col, note_col = st.columns([1.15, 1], gap="large")

with form_col:
    st.subheader("Formulaire")

    # Open-ended (red)
    top1, top2 = st.columns([1, 2])
    with top1:
        st.number_input("# dent", min_value=1, max_value=32, step=1, key="dent")
    with top2:
        st.text_input("Confirmation dx", key="confirm_dx")

    st.divider()

    # Choices (blue) grouped into sensible chunks
    with st.expander("Diagnostic et accès", expanded=True):
        chip("Cause", ["restauration défectueuse", "carie"], key="cause")
        chip("Ablation", ["totale", "partielle jusqu’à consistance cuire (proximité pulpaire)"], key="ablation")

    with st.expander("Isolation et matrice", expanded=True):
        chip("Isolation", ["coton + dry-angle", "digue", "svédoptère"], key="isolation")
        chip("Système matrice", ["sectionnelle + coin de bois", "tofflemire + coin de bois"], key="matrice")

    with st.expander("Matériaux", expanded=True):
        m1, m2 = st.columns(2)
        with m1:
            chip("Liner", ["ionoseal", "dycal", "calcimol"], key="liner")
            chip("Adhésif", ["optibond", "all-bond"], key="adhesif")
            chip("Couleur", ["A1", "A2", "A3"], key="couleur")
        with m2:
            chip("Base", ["vitrebond", "fuji 2 LC"], key="base")
            chip("Matériel", ["amalgame", "composite filtek supreme", "composite spectra", "fuji 2LC"], key="materiel")

    st.divider()

    # Open-ended (red)
    st.text_area("Détails à noter", key="details", height=120)
    st.text_input("PRV", key="prv")

with note_col:
    st.subheader("Note générée (copier-coller)")
    st.text_area("", render_do_note(), height=520)
    st.caption("Tip: clique dans la note, Ctrl/Cmd+A puis Ctrl/Cmd+C.")
