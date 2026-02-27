import streamlit as st

st.set_page_config(page_title="Notes dentaires", layout="wide")
st.title("Générateur de notes dentaires")

# -----------------------
# UI HELPERS
# -----------------------
def chip_single(label: str, options: list[str], key: str, index: int = 0):
    return st.radio(label, options, horizontal=True, key=key, index=index)

def chip_multi(label: str, options: list[str], key_prefix: str, columns: int = 4):
    st.markdown(f"**{label}**")
    cols = st.columns(min(columns, max(1, len(options))))
    picked = []
    for i, opt in enumerate(options):
        with cols[i % len(cols)]:
            if st.checkbox(opt, key=f"{key_prefix}_{i}"):
                picked.append(opt)
    return picked

def field_text(label: str, key: str, height: int | None = None, placeholder: str = ""):
    if height is None:
        return st.text_input(label, key=key, placeholder=placeholder)
    return st.text_area(label, key=key, height=height, placeholder=placeholder)

def field_number(label: str, key: str, min_value: int = 1, max_value: int = 32, step: int = 1):
    return st.number_input(label, min_value=min_value, max_value=max_value, step=step, key=key)

def render_section(title: str, fixed_lines: list[str], kv_lines: list[tuple[str, str]]):
    lines = [title]
    for l in fixed_lines:
        if l.strip():
            lines.append(l)

    for label, key in kv_lines:
        val = st.session_state.get(key, "")
        if isinstance(val, list):
            if val:
                lines.append(f"{label} {', '.join(val)}")
            continue
        if val is None:
            continue
        if str(val).strip() == "":
            continue
        if label.endswith(":"):
            lines.append(f"{label} {val}")
        else:
            lines.append(f"{label}: {val}")
    return "\n".join(lines).strip()

def note_box(title: str, text: str):
    st.subheader("Note générée")
    st.text_area(title, text, height=420)

# -----------------------
# TABS
# -----------------------
tabs = st.tabs([
    "Template de base",
    "Urgence",
    "Anesthésie",
    "DO",
    "PPF",
    "Production couronne",
    "Retrait temporaire",
    "Exo",
    "PLO/Blanchiment",
    "MEB PLO",
    "Prescriptions",
])

# ======================================================
# 1) TEMPLATE DE BASE
# ======================================================
with tabs[0]:
    st.subheader("Template de base")

    field_text("HM:", key="base_hm", height=90, placeholder="pas de changement, fait aujourd’hui, détails")
    radios = chip_multi("Radiographies prises:", ["PA", "BW", "PAN"], key_prefix="base_radio", columns=3)
    st.session_state["base_radios"] = radios

    note = render_section(
        "Template de base",
        fixed_lines=[],
        kv_lines=[
            ("HM:", "base_hm"),
            ("Radiographies prises:", "base_radios"),
        ],
    )
    note_box("Template de base", note)

# ======================================================
# 2) URGENCE
# ======================================================
with tabs[1]:
    st.subheader("Urgence")

    field_text("Plainte du patient:", key="urg_plainte", height=80)
    field_text("Détails de la plainte:", key="urg_plainte_details", height=80)
    field_text("Douleur:", key="urg_douleur", height=60)
    field_text("EEO:", key="urg_eeo", height=60)
    field_text("EIO:", key="urg_eio", height=60)
    field_text("Examen radiologique:", key="urg_exam_radio", height=60)

    field_number("# dent:", key="urg_dent")
    chip_single("Froid:", ["N/A", "Positif", "Négatif", "Exagéré"], key="urg_froid", index=0)
    chip_single("Percussion:", ["N/A", "Positif", "Négatif"], key="urg_perc", index=0)

    field_number("# dent témoin:", key="urg_dent_temoin")
    chip_single("Froid (témoin):", ["N/A", "Positif", "Négatif", "Exagéré"], key="urg_froid_temoin", index=0)
    chip_single("Percussion (témoin):", ["N/A", "Positif", "Négatif"], key="urg_perc_temoin", index=0)

    field_text("Dx:", key="urg_dx", height=60)
    field_text("Plan de tx idéal:", key="urg_plan_ideal", height=70)
    field_text("Pronostic:", key="urg_prono_ideal", height=60)
    field_text("Plan de tx alternatif:", key="urg_plan_alt", height=70)
    field_text("Pronostic:", key="urg_prono_alt", height=60)
    field_text("Pt choisit:", key="urg_pt_choisit", height=60)
    field_text("Discussion:", key="urg_discussion", height=100)

    note = render_section(
        "Urgence",
        fixed_lines=[],
        kv_lines=[
            ("Plainte du patient:", "urg_plainte"),
            ("Détails de la plainte:", "urg_plainte_details"),
            ("Douleur:", "urg_douleur"),
            ("EEO:", "urg_eeo"),
            ("EIO:", "urg_eio"),
            ("Examen radiologique:", "urg_exam_radio"),
            ("# dent:", "urg_dent"),
            ("Froid:", "urg_froid"),
            ("Percussion:", "urg_perc"),
            ("# dent témoin:", "urg_dent_temoin"),
            ("Froid:", "urg_froid_temoin"),
            ("Percussion:", "urg_perc_temoin"),
            ("Dx:", "urg_dx"),
            ("Plan de tx idéal:", "urg_plan_ideal"),
            ("Pronostic:", "urg_prono_ideal"),
            ("Plan de tx alternatif:", "urg_plan_alt"),
            ("Pronostic:", "urg_prono_alt"),
            ("Pt choisit:", "urg_pt_choisit"),
            ("Discussion:", "urg_discussion"),
        ],
    )
    note_box("Urgence", note)

# ======================================================
# 3) ANESTHÉSIE
# ======================================================
with tabs[2]:
    st.subheader("Anesthésie")

    tech = chip_multi(
        "Technique:",
        [
            "infiltration B",
            "infiltration L",
            "spix D + long buccal D",
            "spix G + long buccal G",
            "mentonnier D",
            "mentonnier G",
        ],
        key_prefix="anes_tech",
        columns=3,
    )
    st.session_state["anes_tech_selected"] = tech

    field_text("Produit:", key="anes_produit", placeholder="Arti…")
    st.number_input("Nb carpules:", min_value=0.0, step=0.5, key="anes_nb_carp")
    chip_single("Aiguille:", ["30C", "27L"], key="anes_aiguille", index=0)

    note_lines = [
        "Anesthésie",
        f"Technique: {', '.join(st.session_state.get('anes_tech_selected', []))}" if st.session_state.get("anes_tech_selected") else "Technique:",
        f"Produit: {st.session_state.get('anes_produit','')}",
        f"Nb carpules: {st.session_state.get('anes_nb_carp','')} x 1,8 mL",
        f"Aiguille: {st.session_state.get('anes_aiguille','')}",
    ]
    note_box("Anesthésie", "\n".join(note_lines).strip())

# ======================================================
# 4) DO
# ======================================================
with tabs[3]:
    st.subheader("DO")

    # fixed lines (always appear)
    do_fixed = [
        "Confirmation du plan de tx avec le patient, questions répondues",
        "Ablation excès, occlusion, polissage, soie",
        "Risque de sensibilité temporaire expliqué au patient",
        "Risque d’endo car carie profonde expliqué au patient",
        "Patient comprend",
        "Patient comfortable",
        "Questions du patient répondues",
    ]

    field_number("# dent:", key="do_dent")
    field_text("Confirmation dx:", key="do_confirm_dx")
    chip_single("Cause:", ["restauration défectueuse", "carie"], key="do_cause", index=0)
    chip_single("Ablation:", ["totale", "partielle jusqu’à consistance cuire (proximité pulpaire)"], key="do_ablation", index=0)
    chip_single("Isolation:", ["coton + dry-angle", "digue", "svédoptère"], key="do_isolation", index=0)
    chip_single("Système matrice:", ["sectionnelle + coin de bois", "tofflemire + coin de bois"], key="do_matrice", index=0)
    chip_single("Liner:", ["ionoseal", "dycal", "calcimol"], key="do_liner", index=0)
    chip_single("Base:", ["vitrebond", "fuji 2 LC"], key="do_base", index=0)
    chip_single("Etch:", ["Oui", "Non"], key="do_etch", index=0)
    chip_single("Gluma:", ["Oui", "Non"], key="do_gluma", index=1)
    chip_single("Adhésif:", ["optibond", "all-bond"], key="do_adhesif", index=0)
    chip_single("Matériel:", ["amalgame", "composite filtek supreme", "composite spectra", "fuji 2LC"], key="do_materiel", index=0)
    chip_single("Couleur:", ["A1", "A2", "A3"], key="do_couleur", index=0)
    field_text("Détails à noter:", key="do_details", height=120)
    field_text("PRV:", key="do_prv")

    note = render_section(
        "DO",
        fixed_lines=do_fixed,
        kv_lines=[
            ("# dent:", "do_dent"),
            ("Confirmation dx:", "do_confirm_dx"),
            ("Cause:", "do_cause"),
            ("Ablation:", "do_ablation"),
            ("Isolation:", "do_isolation"),
            ("Système matrice:", "do_matrice"),
            ("Liner:", "do_liner"),
            ("Base:", "do_base"),
            ("Etch:", "do_etch"),
            ("Gluma:", "do_gluma"),
            ("Adhésif:", "do_adhesif"),
            ("Matériel:", "do_materiel"),
            ("Couleur:", "do_couleur"),
            ("Détails à noter:", "do_details"),
            ("PRV:", "do_prv"),
        ],
    )
    note_box("DO", note)

# ======================================================
# 5) PPF
# ======================================================
with tabs[4]:
    st.subheader("PPF")

    ppf_fixed = [
        "Confirmation du plan de tx avec le patient, questions répondues",
        "Pt d’accord avec couleur",
    ]

    field_number("# dent:", key="ppf_dent")
    field_text("Sondage:", key="ppf_sondage", height=80)  # MB/DB/ML/DL in one block
    field_text("Exam radio:", key="ppf_exam_radio", height=80)
    field_text("Ratio couronne/racine:", key="ppf_ratio", height=60)
    chip_single("Choix restauration:", ["couronne", "onlay"], key="ppf_rest", index=0)
    chip_single("Choix matériel:", ["zircone", "E-max"], key="ppf_mat", index=0)
    chip_single("Couleur:", ["A1", "A2", "A3"], key="ppf_couleur", index=0)

    note = render_section(
        "PPF",
        fixed_lines=ppf_fixed,
        kv_lines=[
            ("# dent:", "ppf_dent"),
            ("Sondage:", "ppf_sondage"),
            ("Exam radio:", "ppf_exam_radio"),
            ("Ratio couronne/racine:", "ppf_ratio"),
            ("Choix restauration:", "ppf_rest"),
            ("Choix matériel:", "ppf_mat"),
            ("Couleur:", "ppf_couleur"),
        ],
    )
    note_box("PPF", note)

# ======================================================
# 6) Production couronne
# ======================================================
with tabs[5]:
    st.subheader("Production couronne")

    field_text("Paramètres:", key="cour_param", height=90)
    field_text("Bloc:", key="cour_bloc")
    field_text("Glaçage:", key="cour_glacage")

    note = render_section(
        "Production couronne",
        fixed_lines=[],
        kv_lines=[
            ("Paramètres:", "cour_param"),
            ("Bloc:", "cour_bloc"),
            ("Glaçage:", "cour_glacage"),
        ],
    )
    note_box("Production couronne", note)

# ======================================================
# 7) Retrait temporaire
# ======================================================
with tabs[6]:
    st.subheader("Retrait temporaire")

    rt_fixed = [
        "Nettoyage dent avec pierre ponce",
        "Essayage couronne",
        "Ajustement contacts",
        "Nettoyage couronne: ivoclean, alcool",
        "Ablation excès",
        "Occlusion",
        "Prise BW",
        "Ablation excès",
        "Risque de sensibilité temporaire expliqué au patient",
        "Risque d’endo car carie profonde expliqué au patient",
        "Patient comprend",
        "Patient comfortable",
        "Questions du patient répondues",
    ]

    chip_single("Isolation:", ["digue", "coton/dry-angle", "svédoptère"], key="rt_iso", index=0)
    field_text("Etch couronne:", key="rt_etch_couronne")
    field_text("Etch dent:", key="rt_etch_dent")
    field_text("Adhésif couronne:", key="rt_adh_couronne")
    field_text("Adhésif dent:", key="rt_adh_dent")
    chip_single("Ciment:", ["relyx universal", "theracem"], key="rt_ciment", index=0)
    field_text("PRV:", key="rt_prv")

    note = render_section(
        "Retrait temporaire",
        fixed_lines=rt_fixed,
        kv_lines=[
            ("Isolation:", "rt_iso"),
            ("Etch couronne:", "rt_etch_couronne"),
            ("Etch dent:", "rt_etch_dent"),
            ("Adhésif couronne:", "rt_adh_couronne"),
            ("Adhésif dent:", "rt_adh_dent"),
            ("Ciment:", "rt_ciment"),
            ("PRV:", "rt_prv"),
        ],
    )
    note_box("Retrait temporaire", note)

# ======================================================
# 8) Exo
# ======================================================
with tabs[7]:
    st.subheader("Exo")

    exo_fixed = [
        "Confirmation du plan de tx avec le patient, questions répondues",
        "Consentement et risques expliqués, signature de celui-ci par le patient",
        "Décorticage, élévation",
        "Lambeau enveloppe pleine épaisseur",
        "Relâche au buccal",
        "Ostectomie, odontectomie",
        "Extraction avec davier (toutes les racines sont sorties)",
        "Curettage",
        "Rinçage avec eau stérile",
        "Gelfoam",
        "Hémostase avec 2x2 coton",
        "Consignes post-op expliquées",
        "Remise 2x2 coton",
        "Patient comprend",
        "Patient confortable",
        "Questions du patient répondues",
        "Prescription anti-douleur (voir Rx)",
    ]

    field_number("# dent:", key="exo_dent")
    chip_single("Point suture:", ["simple", "X"], key="exo_suture", index=0)
    field_text("PRV:", key="exo_prv")

    note = render_section(
        "Exo",
        fixed_lines=exo_fixed,
        kv_lines=[
            ("# dent:", "exo_dent"),
            ("Point suture:", "exo_suture"),
            ("PRV:", "exo_prv"),
        ],
    )
    note_box("Exo", note)

# ======================================================
# 9) PLO / Blanchiment
# ======================================================
with tabs[8]:
    st.subheader("PLO/Blanchiement")

    plo_fixed = [
        "Envoi au lab",
        "Confection gouttières",
        "Remise gouttières",
        "Fit ok, patient confortable",
        "Explication fonctionnement blanchiement",
    ]

    chip_single("Prise d’empreintes H/B:", ["numérique", "alginate"], key="plo_emp", index=0)
    chip_single("Prise du bite:", ["numérique", "régisil"], key="plo_bite", index=0)

    note = render_section(
        "PLO/Blanchiement",
        fixed_lines=plo_fixed,
        kv_lines=[
            ("Prise d’empreintes H/B:", "plo_emp"),
            ("Prise du bite:", "plo_bite"),
        ],
    )
    note_box("PLO/Blanchiement", note)

# ======================================================
# 10) MEB PLO
# ======================================================
with tabs[9]:
    st.subheader("MEB PLO")

    meb_fixed = [
        "Fit ok",
        "Patient confortable",
    ]

    field_text("Ajustement occlusion:", key="meb_occl", height=60)
    field_text("RC balancée:", key="meb_rc", height=60)
    field_text("Latéralité canines:", key="meb_lat", height=60)
    field_text("Protrusion pas de contacts postérieurs:", key="meb_protr", height=60)
    field_text("PRV:", key="meb_prv")

    note = render_section(
        "MEB PLO",
        fixed_lines=meb_fixed,
        kv_lines=[
            ("Ajustement occlusion:", "meb_occl"),
            ("RC balancée:", "meb_rc"),
            ("Latéralité canines:", "meb_lat"),
            ("Protrusion pas de contacts postérieurs:", "meb_protr"),
            ("PRV:", "meb_prv"),
        ],
    )
    note_box("MEB PLO", note)

# ======================================================
# 11) Prescriptions
# ======================================================
with tabs[10]:
    st.subheader("Prescriptions")

    rx_fixed = []

    chip_single(
        "Antibiotiques:",
        [
            "Aucun",
            "Amoxicilline 500 mg — Disp: 21 co — Sig: 1 co PO TID x 7 jours",
            "Azithromycine 250 mg — Disp: 6 co — Sig: 2 co PO STAT, 1 co PO DIE x 4 jours",
            "Amoxicilline 500 mg — Disp: 4 co — Sig: 4 co 1h avant le RDV",
            "Azithromycine 250 mg — Disp: 2 co — Sig: 2 co 1h avant le RDV",
        ],
        key="rx_abx",
        index=0,
    )

    chip_single(
        "Anti-douleur:",
        [
            "Aucun",
            "Acétaminophène 500 mg — Disp: 20 co — Sig: 2 co PO q6h prn dlr",
            "Tramadol 50 mg — Disp: 10 co — Sig: 1 co PO q6h prn dlr",
        ],
        key="rx_analges",
        index=0,
    )

    chip_single(
        "Anti-inflammatoire:",
        [
            "Aucun",
            "Ibuprofène 600 mg — Disp: 20 co — Sig: 1 co PO q6h prn dlr",
        ],
        key="rx_ains",
        index=0,
    )

    chip_single(
        "Anti-fongique:",
        [
            "Aucun",
            "Nystatin susp. orale 100 000u/mL — Disp: 300 mL — Sig: 5 mL bain buccal x 3 min q6h x 14 jours — Ne pas avaler et ne pas rincer",
        ],
        key="rx_antif",
        index=0,
    )

    field_text("Autres prescriptions / notes:", key="rx_notes", height=120)

    note = render_section(
        "Prescriptions",
        fixed_lines=rx_fixed,
        kv_lines=[
            ("Antibiotiques:", "rx_abx"),
            ("Anti-douleur:", "rx_analges"),
            ("Anti-inflammatoire:", "rx_ains"),
            ("Anti-fongique:", "rx_antif"),
            ("Autres:", "rx_notes"),
        ],
    )
    note_box("Prescriptions", note)
