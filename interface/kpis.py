import streamlit as st

def afficher_kpi_montant(title, montant, devise):
    couleur = "#a09980" if devise in ["€", "$"] else "black"
    montant_formate = f"{montant:,.0f}".replace(",", " ") + f" {devise}"

    st.markdown(
        f"""
        <div style="
            font-family: 'Book Antiqua';
            border: 0.2px solid #dbd1b0;
            border-radius: 8px;
            padding: 12px 50px;
            background-color: #eae7e1;
            box-shadow: 0 0 4px rgba(212, 175, 55, 0.3);
        ">
            <p style='
                font-weight: 600;
                font-size: 16px;
                margin-bottom: 6px;
                color: #3d3d43;
            '>{title}</p>
            <p style='
                font-size: 28px;
                font-weight: bold;
                color: {couleur};
                margin: 0;
            '>{montant_formate}</p>
        </div>
        """,
        unsafe_allow_html=True
    )