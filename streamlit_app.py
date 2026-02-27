import streamlit as st

st.set_page_config(page_title="Générateur notes dentaires", layout="wide")
st.title("Générateur de notes dentaires")

def chip(label: str, options: list[str], key: str, index: int = 0):
    return st.radio(label, options, horizontal=True, key=key, index=index)

def chips_multi(label: str, options: list[str], key_prefix: str):
    """Multi-select style 'chips' avec des checkboxes en colonnes."""
    st.markdown(f"**{label}**")
    cols = st.columns(min(4, len(options)))
    selected = []
    for i, opt in enumerate(options):
        with cols[i % len(cols)]:
            if st.checkbox(opt, key=f"{key_prefix}_{i}"):
                selected.append(opt)
    return selected

# -------------------------
# TABS (sections)
# -------------------------
tab_base, tab_urgence, tab_anesth, tab_do, tab_resume = st.tabs(
    ["Template de base", "Urgence", "Anesthésie", "DO", "Résumé"]
)

# -------------------------
# TEMPLATE DE BASE
# -------------------------
with tab_base:
    st.subheader("Template de base")

    hm = st.text_area("HM:", value="pas de changement, fait aujourd’hui, détails", key="hm")
    radios = chips_multi("Radiographies prises:", ["PA", "BW", "PAN"], key_prefix="radio")

# -------------------------
# URGENCE
# -------------------------
with tab_urgence:
    st.subheader("Urgence")

    plainte = st.text_area("Plainte du patient:", key="plainte")
    details_plainte = st.text_area("Détails de la plainte:", key="details_plainte")
    douleur = st.text_area("Douleur:", key="douleur")

    eeo = st.text_area("EEO:", key="eeo")
    eio = st.text_area("EIO:", key="eio")
    exam_radio = st.text_area("Examen radiologique:", key="exam_radio")

    dent_urgence = st.number_input("# dent:", min_value=1, max_value=32, step=1, key="dent_urgence")

    froid = chip("Froid:", ["N/A", "Positif", "Négatif", "Exagéré"], key="froid_urgence", index=0)
    percussion = chip("Percussion:", ["N/A", "Positif", "Négatif"], key="perc_urgence", index=0)

    dent_temoin = st.number_input("# dent témoin:", min_value=1, max_value=32, step=1, key="dent_temoin")
    froid_temoin = chip("Froid (témoin):", ["N/A", "Positif", "Négatif", "Exagéré"], key="froid_temoin", index=0)
    percussion_temoin = chip("Percussion (témoin):", ["N/A", "Positif", "Négatif"], key="perc_temoin", index=0)

    dx = st.text_area("Dx:", key="dx")
    plan_ideal = st.text_area("Plan de tx idéal:", key="plan_ideal")
    pronostic_ideal = st.text_area("Pronostic:", key="pronostic_ideal")
    plan_alt = st.text_area("Plan de tx alternatif:", key="plan_alt")
    pronostic_alt = st.text_area("Pronostic (alternatif):", key="pronostic_alt")
    pt_choisit = st.text_area("Pt choisit:", key="pt_choisit")
    discussion = st.text_area("Discussion:", key="discussion")

# -------------------------
# ANESTHÉSIE
# -------------------------
with tab_anesth:
    st.subheader("Anesthésie")

    technique = chip(
        "Technique:",
        [
            "infiltration B",
            "infiltration L",
            "spix D + long buccal D",
            "spix G + long buccal G",
            "mentonnier D",
            "mentonnier G",
        ],
        key="anesth_tech",
        index=0,
    )
    produit = st.text_input("Produit:", value="Arti…", key="anesth_produit")
    nb_carp = st.number_input("Nb carpules (x 1,8 mL):", min_value=0.0, step=0.5, key="anesth_nb")
    aiguille = chip("Aiguille:", ["30C", "27L"], key="anesth_aig", index=0)

# -------------------------
# DO
# -------------------------
with tab_do:
    st.subheader("DO")

    st.checkbox("Confirmation du plan de tx avec le patient, questions répondues", key="do_confirm", value=True)

    dent_do = st.number_input("# dent (DO):", min_value=1, max_value=32, step=1, key="dent_do")
    confirmation_dx = st.text_input("Confirmation dx:", key="do_dx")

    cause = chip("Cause:", ["restauration défectueuse", "carie"], key="do_cause", index=0)

    ablation = chip(
        "Ablation:",
        ["totale", "partielle jusqu’à consistance cuire (proximité pulpaire)"],
        key="do_ablation",
        index=0,
    )

    isolation = chip(
        "Isolation:",
        ["coton + dry-angle", "digue", "svédoptère"],
        key="do_isolation",
        index=0,
    )

    systeme_matrice = chip(
        "Système matrice:",
        ["sectionnelle + coin de bois", "tofflemire + coin de bois"],
        key="do_matrice",
        index=0,
    )

    liner = chip("Liner:", ["ionoseal", "dycal", "calcimol"], key="do_liner", index=0)

    base = chip("Base:", ["vitrebond", "fuji 2 LC"], key="do_base", index=0)

    etch = chip("Etch:", ["Oui", "Non"], key="do_etch", index=0)
    gluma = chip("Gluma:", ["Oui", "Non"], key="do_gluma", index=1)

    adhesif = chip("Adhésif:", ["optibond", "all-bond"], key="do_adh", index=0)

    materiel = chip(
        "Matériel:",
        ["amalgame", "composite filtek supreme", "composite spectra", "fuji 2LC"],
        key="do_mat",
        index=0,
    )

    couleur = chip("Couleur:", ["A1", "A2", "A3"], key="do_coul", index=0)

    finitions = chips_multi("Finitions:", ["Ablation excès", "Occlusion", "Polissage", "Soie"], key_prefix="do_fin")
    details_a_noter = st.text_area("Détails à noter:", key="do_details")

    st.checkbox("Risque de sensibilité temporaire expliqué au patient", key="do_risque_sens", value=True)
    st.checkbox("Risque d’endo car carie profonde expliqué au patient", key="do_risque_endo", value=True)
    st.checkbox("Patient comprend", key="do_comprend", value=True)
    st.checkbox("Patient comfortable", key="do_comfort", value=True)
    st.checkbox("Questions du patient répondues", key="do_questions", value=True)

    prv_do = st.text_input("PRV:", key="do_prv")

# -------------------------
# RÉSUMÉ (NOTE GÉNÉRÉE)
# -------------------------
with tab_resume:
    st.subheader("Note générée (copier-coller)")

    ss = st.session_state

    # Template de base
    radios_txt = ", ".join(ss.get("radio", [])) if isinstance(ss.get("radio"), list) else ""
    base_block = "\n".join([
        "Template de base",
        f"HM: {ss.get('hm','')}",
        f"Radiographies prises: {', '.join([x for x in ['PA','BW','PAN'] if ss.get(f'radio_{['PA','BW','PAN'].index(x)}', False)])}"
    ])

    # Urgence
    urgence_block = "\n".join([
        "",
        "Urgence",
        f"Plainte du patient: {ss.get('plainte','')}",
        f"Détails de la plainte: {ss.get('details_plainte','')}",
        f"Douleur: {ss.get('douleur','')}",
        f"EEO: {ss.get('eeo','')}",
        f"EIO: {ss.get('eio','')}",
        f"Examen radiologique: {ss.get('exam_radio','')}",
        f"# dent: {ss.get('dent_urgence','')}",
        f"Froid: {ss.get('froid_urgence','')}",
        f"Percussion: {ss.get('perc_urgence','')}",
        f"# dent témoin: {ss.get('dent_temoin','')}",
        f"Froid: {ss.get('froid_temoin','')}",
        f"Percussion: {ss.get('perc_temoin','')}",
        f"Dx: {ss.get('dx','')}",
        f"Plan de tx idéal: {ss.get('plan_ideal','')}",
        f"Pronostic: {ss.get('pronostic_ideal','')}",
        f"Plan de tx alternatif: {ss.get('plan_alt','')}",
        f"Pronostic: {ss.get('pronostic_alt','')}",
        f"Pt choisit: {ss.get('pt_choisit','')}",
        f"Discussion: {ss.get('discussion','')}",
    ])

    # Anesthésie
    anesth_block = "\n".join([
        "",
        "Anesthésie",
        f"Technique: {ss.get('anesth_tech','')}",
        f"Produit: {ss.get('anesth_produit','')}",
        f"Nb carpules: {ss.get('anesth_nb','')} x 1,8 mL",
        f"Aiguille: {ss.get('anesth_aig','')}",
    ])

    # DO
    fin_list = []
    for i, opt in enumerate(["Ablation excès", "Occlusion", "Polissage", "Soie"]):
        if ss.get(f"do_fin_{i}", False):
            fin_list.append(opt)

    do_block = "\n".join([
        "",
        "DO",
        "Confirmation du plan de tx avec le patient, questions répondues" if ss.get("do_confirm") else "",
        f"# dent: {ss.get('dent_do','')}",
        f"Confirmation dx: {ss.get('do_dx','')}",
        f"Cause: {ss.get('do_cause','')}",
        f"Ablation: {ss.get('do_ablation','')}",
        f"Isolation: {ss.get('do_isolation','')}",
        f"Système matrice: {ss.get('do_matrice','')}",
        f"Liner: {ss.get('do_liner','')}",
        f"Base: {ss.get('do_base','')}",
        f"Etch: {ss.get('do_etch','')}",
        f"Gluma: {ss.get('do_gluma','')}",
        f"Adhésif: {ss.get('do_adh','')}",
        f"Matériel: {ss.get('do_mat','')}",
        f"Couleur: {ss.get('do_coul','')}",
        f"{', '.join(fin_list)}" if fin_list else "",
        f"Détails à noter: {ss.get('do_details','')}",
        "Risque de sensibilité temporaire expliqué au patient" if ss.get("do_risque_sens") else "",
        "Risque d’endo car carie profonde expliqué au patient" if ss.get("do_risque_endo") else "",
        "Patient comprend" if ss.get("do_comprend") else "",
        "Patient comfortable" if ss.get("do_comfort") else "",
        "Questions du patient répondues" if ss.get("do_questions") else "",
        f"PRV: {ss.get('do_prv','')}",
    ]).strip()

    note = "\n".join([base_block, urgence_block, anesth_block, do_block]).strip()

    st.text_area("Note", note, height=600)
    st.caption("Tip: clique dans la zone, Ctrl/Cmd+A puis Ctrl/Cmd+C.")
