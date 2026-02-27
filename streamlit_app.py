import streamlit as st

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="Notes dentaires", layout="wide")
st.title("Générateur de notes dentaires")

# -----------------------
# UI HELPERS (chips)
# -----------------------
def chip_single(label: str, options: list[str], key: str, index: int = 0):
    return st.radio(label, options, horizontal=True, key=key, index=index)

def chip_multi(label: str, options: list[str], key_prefix: str, columns: int = 4):
    """
    Multi-select style 'chips' (checkboxes). Returns list of selected options.
    """
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

# -----------------------
# NOTE RENDERING HELPERS
# -----------------------
def render_section(title: str, fixed_lines: list[str], kv_lines: list[tuple[str, str]], include_if_empty: bool = False):
    """
    title: section title
    fixed_lines: always included (non-underlined in your rule)
    kv_lines: list of (label, session_state_key) -> included if value not empty (unless include_if_empty)
    """
    lines = [title]
    for l in fixed_lines:
        if l.strip():
            lines.append(l)

    for label, key in kv_lines:
        val = st.session_state.get(key, "")
        # handle lists (multi selections)
        if isinstance(val, list):
            if val or include_if_empty:
                lines.append(f"{label} {', '.join(val)}")
            continue

        if val is None:
            continue

        if str(val).strip() == "" and not include_if_empty:
            continue

        # show as "Label: value"
        if label.endswith(":"):
            lines.append(f"{label} {val}")
        else:
            lines.append(f"{label}: {val}")

    return "\n".join(lines).strip()

def oneline_bool(text: str, key: str, default: bool = True):
    """Boolean that, if true, includes the text line in the note."""
    st.checkbox(text, key=key, value=default)

# -----------------------
# SECTION TABS
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
    "Note complète",
])

# ======================================================
# 1) TEMPLATE DE BASE
# ======================================================
with tabs[0]:
    st.subheader("Template de base")

    # (Not underlined => always in note)
    field_text("HM:", key="base_hm", height=80, placeholder="pas de changement, fait aujourd’hui, détails")

    # Underlined choices => chips (multi)
    chip_multi("Radiographies prises:", ["PA", "BW", "PAN"], key_prefix="base_radio")

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_base", value=True)

# ======================================================
# 2) URGENCE
# ======================================================
with tabs[1]:
    st.subheader("Urgence")

    # free fields
    field_text("Plainte du patient:", key="urg_plainte", height=80)
    field_text("Détails de la plainte:", key="urg_plainte_details", height=80)
    field_text("Douleur:", key="urg_douleur", height=60)
    field_text("EEO:", key="urg_eeo", height=60)
    field_text("EIO:", key="urg_eio", height=60)
    field_text("Examen radiologique:", key="urg_exam_radio", height=60)

    field_number("# dent:", key="urg_dent")

    # choices (chips)
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

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_urgence", value=True)

# ======================================================
# 3) ANESTHÉSIE
# ======================================================
with tabs[2]:
    st.subheader("Anesthésie")

    # Technique: could be multiple injections -> multi chips
    chip_multi(
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

    field_text("Produit:", key="anes_produit", placeholder="Arti…")

    # numeric
    st.number_input("Nb carpules:", min_value=0.0, step=0.5, key="anes_nb_carp")
    st.caption("Affiché comme: Nb carpules: x 1,8 mL")

    chip_single("Aiguille:", ["30C", "27L"], key="anes_aiguille", index=0)

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_anesth", value=True)

# ======================================================
# 4) DO
# ======================================================
with tabs[3]:
    st.subheader("DO")

    # Fixed (not underlined -> always in note)
    st.markdown("Ces lignes seront ajoutées automatiquement dans la note (selon ta règle).")

    # Choices/inputs
    field_number("# dent:", key="do_dent")
    field_text("Confirmation dx:", key="do_confirm_dx")

    chip_single("Cause:", ["restauration défectueuse", "carie"], key="do_cause", index=0)

    chip_single(
        "Ablation:",
        ["totale", "partielle jusqu’à consistance cuire (proximité pulpaire)"],
        key="do_ablation",
        index=0,
    )

    chip_single("Isolation:", ["coton + dry-angle", "digue", "svédoptère"], key="do_isolation", index=0)

    chip_single(
        "Système matrice:",
        ["sectionnelle + coin de bois", "tofflemire + coin de bois"],
        key="do_matrice",
        index=0,
    )

    chip_single("Liner:", ["ionoseal", "dycal", "calcimol"], key="do_liner", index=0)

    chip_single("Base:", ["vitrebond", "fuji 2 LC"], key="do_base", index=0)

    # Etch + Gluma (treated as choices yes/no)
    chip_single("Etch:", ["Oui", "Non"], key="do_etch", index=0)
    chip_single("Gluma:", ["Oui", "Non"], key="do_gluma", index=1)

    chip_single("Adhésif:", ["optibond", "all-bond"], key="do_adhesif", index=0)

    chip_single(
        "Matériel:",
        ["amalgame", "composite filtek supreme", "composite spectra", "fuji 2LC"],
        key="do_materiel",
        index=0,
    )

    chip_single("Couleur:", ["A1", "A2", "A3"], key="do_couleur", index=0)

    field_text("Détails à noter:", key="do_details", height=120)
    field_text("PRV:", key="do_prv")

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_do", value=True)

# ======================================================
# 5) PPF
# ======================================================
with tabs[4]:
    st.subheader("PPF")

    # inputs
    field_number("# dent:", key="ppf_dent")
    field_text("Sondage (MB DB / ML DL):", key="ppf_sondage", height=80)
    field_text("Exam radio:", key="ppf_exam_radio", height=80)
    field_text("Ratio couronne/racine:", key="ppf_ratio", height=60)

    # choices
    chip_single("Choix restauration:", ["couronne", "onlay"], key="ppf_rest", index=0)
    chip_single("Choix matériel:", ["zircone", "E-max"], key="ppf_mat", index=0)
    chip_single("Couleur:", ["A1", "A2", "A3"], key="ppf_couleur", index=0)

    # fixed line "Pt d’accord..." is auto included
    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_ppf", value=True)

# ======================================================
# 6) Production couronne
# ======================================================
with tabs[5]:
    st.subheader("Production couronne")

    field_text("Paramètres:", key="cour_param", height=80)
    field_text("Bloc:", key="cour_bloc")
    field_text("Glaçage:", key="cour_glacage")

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_prod_couronne", value=True)

# ======================================================
# 7) Retrait temporaire (inclut empreinte/tempo/cimentation + protocole)
# ======================================================
with tabs[6]:
    st.subheader("Retrait temporaire / Empreinte / Temporisation / Cimentation")

    # Empreinte pour temporaire: template (fixed)
    field_text("Taille de la dent:", key="rt_taille_dent")

    chip_single("Cordes à rétracter:", ["0", "00", "000"], key="rt_cordes", index=1)
    st.text_input("Enduites d’hémodent (détails):", key="rt_hemodent")

    chip_single("Isolation:", ["digue", "coton/dry-angle", "svédoptère"], key="rt_isolation", index=0)

    chip_single("Empreinte:", ["numérique", "PVS (triple tray)"], key="rt_empreinte", index=0)
    chip_single("Bite:", ["numérique", "régisil"], key="rt_bite", index=0)

    # Temporisation / Cimentation
    chip_single("Temporisation:", ["alike", "voco", "integrity"], key="rt_tempo", index=0)
    chip_single("Cimentation:", ["temp-bond"], key="rt_ciment_temp", index=0)

    # finitions are fixed line in template; but if you want explicit:
    field_text("Ajustements / détails (optionnel):", key="rt_details", height=100)

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_retrait_temp", value=True)

# ======================================================
# 8) Exo
# ======================================================
with tabs[7]:
    st.subheader("Exo")

    field_number("# dent:", key="exo_dent")

    # choices
    chip_multi(
        "Point suture:",
        ["simple", "X"],
        key_prefix="exo_suture",
        columns=2,
    )

    # free details
    field_text("Détails (si nécessaire):", key="exo_details", height=120)
    field_text("PRV:", key="exo_prv")

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_exo", value=True)

# ======================================================
# 9) PLO / Blanchiment
# ======================================================
with tabs[8]:
    st.subheader("PLO / Blanchiment")

    chip_single("Prise d’empreintes H/B:", ["numérique", "alginate"], key="plo_empreinte", index=0)
    chip_single("Prise du bite:", ["numérique", "régisil"], key="plo_bite", index=0)

    field_text("Envoi au lab (détails):", key="plo_lab", height=80)

    # Confection + remise + explications (fixed lines auto included)
    field_text("Notes additionnelles (optionnel):", key="plo_notes", height=100)

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_plo", value=True)

# ======================================================
# 10) MEB PLO
# ======================================================
with tabs[9]:
    st.subheader("MEB PLO")

    field_text("Ajustement occlusion:", key="meb_ajust_occl", height=80)
    field_text("RC balancée:", key="meb_rc", height=60)
    field_text("Latéralité canines:", key="meb_lat", height=60)
    field_text("Protrusion pas de contacts postérieurs:", key="meb_protr", height=60)

    field_text("PRV:", key="meb_prv")

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_meb", value=True)

# ======================================================
# 11) Prescriptions
# ======================================================
with tabs[10]:
    st.subheader("Prescriptions")

    # Antibiotiques (choice among standard templates)
    st.markdown("### Antibiotiques (choisir un template)")
    abx = chip_single(
        "Antibiotiques:",
        [
            "Aucun",
            "Amoxicilline 500 mg (21 co) 1 co PO TID x 7 jours",
            "Azithromycine 250 mg (6 co) 2 co PO STAT, 1 co PO DIE x 4 jours",
            "Amoxicilline 500 mg (4 co) 4 co 1h avant RDV",
            "Azithromycine 250 mg (2 co) 2 co 1h avant RDV",
        ],
        key="rx_abx",
        index=0,
    )

    st.markdown("### Anti-douleur")
    analges = chip_single(
        "Anti-douleur:",
        [
            "Aucun",
            "Acétaminophène 500 mg (20 co) 2 co PO q6h prn dlr",
            "Tramadol 50 mg (10 co) 1 co PO q6h prn dlr",
        ],
        key="rx_analges",
        index=0,
    )

    st.markdown("### Anti-inflammatoire")
    ains = chip_single(
        "Anti-inflammatoire:",
        [
            "Aucun",
            "Ibuprofène 600 mg (20 co) 1 co PO q6h prn dlr",
        ],
        key="rx_ains",
        index=0,
    )

    st.markdown("### Anti-fongique")
    antif = chip_single(
        "Anti-fongique:",
        [
            "Aucun",
            "Nystatin susp. orale 100 000u/mL (300 mL) 5 mL bain buccal x 3 min q6h x 14 jours (Ne pas avaler et ne pas rincer)",
        ],
        key="rx_antif",
        index=0,
    )

    # optional free text
    field_text("Autres prescriptions / notes:", key="rx_notes", height=120)

    st.divider()
    st.checkbox("Inclure cette section dans la note", key="inc_rx", value=True)

# ======================================================
# 12) NOTE COMPLETE
# ======================================================
with tabs[11]:
    st.subheader("Note complète (copier-coller)")

    # ---- TEMPLATE DE BASE block ----
    base_fixed = ["Template de base"]
    base_fields = [
        ("HM:", "base_hm"),
        ("Radiographies prises:", "base_radio_selected"),
    ]

    # compute radiographies list from checkboxes
    radios = []
    for i, opt in enumerate(["PA", "BW", "PAN"]):
        if st.session_state.get(f"base_radio_{i}", False):
            radios.append(opt)
    st.session_state["base_radio_selected"] = radios

    base_block = render_section(
        "Template de base",
        fixed_lines=[],
        kv_lines=[
            ("HM:", "base_hm"),
            ("Radiographies prises:", "base_radio_selected"),
        ],
    )

    # ---- URGENCE block ----
    urgence_block = render_section(
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

    # ---- ANESTHESIE block ----
    tech = []
    tech_opts = [
        "infiltration B",
        "infiltration L",
        "spix D + long buccal D",
        "spix G + long buccal G",
        "mentonnier D",
        "mentonnier G",
    ]
    for i, opt in enumerate(tech_opts):
        if st.session_state.get(f"anes_tech_{i}", False):
            tech.append(opt)
    st.session_state["anes_tech_selected"] = tech

    anesth_block = render_section(
        "Anesthésie",
        fixed_lines=[],
        kv_lines=[
            ("Technique:", "anes_tech_selected"),
            ("Produit:", "anes_produit"),
            ("Nb carpules:", "anes_nb_carp"),
            ("Aiguille:", "anes_aiguille"),
        ],
    )
    # tweak carpule line formatting
    anesth_block = anesth_block.replace("Nb carpules: ", "Nb carpules: ") + "\n" if anesth_block else anesth_block
    if "Nb carpules:" in anesth_block:
        # ensure "x 1,8 mL"
        lines = anesth_block.splitlines()
        out = []
        for ln in lines:
            if ln.startswith("Nb carpules:"):
                out.append(f"{ln} x 1,8 mL")
            else:
                out.append(ln)
        anesth_block = "\n".join(out)

    # ---- DO block ----
    do_fixed_lines = [
        "Confirmation du plan de tx avec le patient, questions répondues",
        "Ablation excès, occlusion, polissage, soie",
        "Risque de sensibilité temporaire expliqué au patient",
        "Risque d’endo car carie profonde expliqué au patient",
        "Patient comprend",
        "Patient comfortable",
        "Questions du patient répondues",
    ]
    do_block = render_section(
        "DO",
        fixed_lines=do_fixed_lines,
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

    # ---- PPF block ----
    ppf_fixed = [
        "Confirmation du plan de tx avec le patient, questions répondues",
        "Pt d’accord avec couleur",
    ]
    ppf_block = render_section(
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

    # ---- Production couronne block ----
    prod_block = render_section(
        "Production couronne",
        fixed_lines=[],
        kv_lines=[
            ("Paramètres:", "cour_param"),
            ("Bloc:", "cour_bloc"),
            ("Glaçage:", "cour_glacage"),
        ],
    )

    # ---- Retrait temporaire block ----
    rt_fixed = [
        "Empreinte pour temporaire: template",
    ]
    rt_block = render_section(
        "Retrait temporaire",
        fixed_lines=rt_fixed,
        kv_lines=[
            ("Taille de la dent:", "rt_taille_dent"),
            ("Cordes à rétracter:", "rt_cordes"),
            ("enduites d’hémodent:", "rt_hemodent"),
            ("Isolation:", "rt_isolation"),
            ("Empreinte:", "rt_empreinte"),
            ("Bite:", "rt_bite"),
            ("Temporisation:", "rt_tempo"),
            ("Cimentation:", "rt_ciment_temp"),
            ("Détails:", "rt_details"),
        ],
    )

    # ---- EXO block ----
    suture = []
    for i, opt in enumerate(["simple", "X"]):
        if st.session_state.get(f"exo_suture_{i}", False):
            suture.append(opt)
    st.session_state["exo_suture_selected"] = suture

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
    exo_block = render_section(
        "Exo",
        fixed_lines=exo_fixed,
        kv_lines=[
            ("# dent:", "exo_dent"),
            ("Point suture:", "exo_suture_selected"),
            ("Détails:", "exo_details"),
            ("PRV:", "exo_prv"),
        ],
    )

    # ---- PLO/Blanchiment block ----
    plo_fixed = [
        "Envoi au lab",
        "Confection gouttières",
        "Remise gouttières",
        "Fit ok, patient confortable",
        "Explication fonctionnement blanchiement",
    ]
    plo_block = render_section(
        "PLO/Blanchiement",
        fixed_lines=plo_fixed,
        kv_lines=[
            ("Prise d’empreintes H/B:", "plo_empreinte"),
            ("Prise du bite:", "plo_bite"),
            ("Détails lab:", "plo_lab"),
            ("Notes:", "plo_notes"),
        ],
    )

    # ---- MEB PLO block ----
    meb_fixed = [
        "Fit ok",
        "Patient confortable",
    ]
    meb_block = render_section(
        "MEB PLO",
        fixed_lines=meb_fixed,
        kv_lines=[
            ("Ajustement occlusion:", "meb_ajust_occl"),
            ("RC balancée:", "meb_rc"),
            ("Latéralité canines:", "meb_lat"),
            ("Protrusion pas de contacts postérieurs:", "meb_protr"),
            ("PRV:", "meb_prv"),
        ],
    )

    # ---- Prescriptions block ----
    rx_fixed = ["Prescriptions"]
    rx_block = render_section(
        "Prescriptions",
        fixed_lines=[],
        kv_lines=[
            ("Antibiotiques:", "rx_abx"),
            ("Anti-douleur:", "rx_analges"),
            ("Anti-inflammatoire:", "rx_ains"),
            ("Anti-fongique:", "rx_antif"),
            ("Autres:", "rx_notes"),
        ],
    )

    # Assemble only included sections
    sections = []
    if st.session_state.get("inc_base", True): sections.append(base_block)
    if st.session_state.get("inc_urgence", True): sections.append(urgence_block)
    if st.session_state.get("inc_anesth", True): sections.append(anesth_block)
    if st.session_state.get("inc_do", True): sections.append(do_block)
    if st.session_state.get("inc_ppf", True): sections.append(ppf_block)
    if st.session_state.get("inc_prod_couronne", True): sections.append(prod_block)
    if st.session_state.get("inc_retrait_temp", True): sections.append(rt_block)
    if st.session_state.get("inc_exo", True): sections.append(exo_block)
    if st.session_state.get("inc_plo", True): sections.append(plo_block)
    if st.session_state.get("inc_meb", True): sections.append(meb_block)
    if st.session_state.get("inc_rx", True): sections.append(rx_block)

    note = "\n\n".join([s for s in sections if s.strip()])

    st.text_area("NOTE", note, height=700)
    st.caption("Ctrl/Cmd+A puis Ctrl/Cmd+C pour copier.")
