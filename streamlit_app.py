with tabs[3]:
    st.subheader("DO")

    # 1) LIGNES FIXES (pas soulignées -> dans la note automatiquement)
    do_fixed = [
        "Confirmation du plan de tx avec le patient, questions répondues",
        "Etch",
        "Gluma",
        "Ablation excès, occlusion, polissage, soie",
        "Risque de sensibilité temporaire expliqué au patient",
        "Risque d’endo car carie profonde expliqué au patient",
        "Patient comprend",
        "Patient comfortable",
        "Questions du patient répondues",
    ]

    # 2) SEULEMENT LES CHOIX (soulignés) + champs libres utiles
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

    # 3) NOTE SOUS LA SECTION
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
            ("Adhésif:", "do_adhesif"),
            ("Matériel:", "do_materiel"),
            ("Couleur:", "do_couleur"),
            ("Détails à noter:", "do_details"),
            ("PRV:", "do_prv"),
        ],
    )
    note_box("DO", note)
