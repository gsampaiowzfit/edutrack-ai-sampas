import streamlit as st
import utils

st.set_page_config(page_title="Disciplinas", page_icon="📚")
st.title("Gestão de Disciplinas")

# Verifica autenticação
if "auth_token" not in st.session_state or not st.session_state["auth_token"]:
    st.warning("⚠️ Você precisa estar logado para acessar as disciplinas. Vá até a página principal (Dashboard) para entrar ou cadastrar-se.")
else:
    tab_lista, tab_novo = st.tabs(["📋 Listar", "➕ Nova Disciplina"])

    with tab_novo:
        st.subheader("Cadastrar Nova Matéria")
        with st.form("form_disciplina"):
            nome = st.text_input("Nome da Disciplina")
            professor = st.text_input("Nome do Professor")
            dia_semana = st.selectbox("Dia da Aula", ["Seg", "Ter", "Qua", "Qui", "Sex"])
            codigo = st.text_input("Código da Matéria (Opcional)")
            
            submitted = st.form_submit_button("Salvar")
            if submitted:
                if nome and professor:
                    desc_completa = f"Professor: {professor} | Aula: {dia_semana}"
                    data = {
                        "name": nome,
                        "code": codigo if codigo else "N/A",
                        "description": desc_completa,
                        "status": "active"
                    }
                    res = utils.xano_post("subjects", "subject/create_app", data)
                    if res:
                        st.success(f"Disciplina '{nome}' cadastrada com sucesso no Xano!")
                    else:
                        st.error("Erro ao cadastrar a disciplina no Xano.")
                else:
                    st.warning("Por favor, preencha o nome da disciplina e o professor.")

    with tab_lista:
        st.subheader("Minhas Disciplinas Ativas")
        
        # Buscar lista de disciplinas reais do Xano
        disciplinas = utils.xano_get("subjects", "subject/list_app")
        
        if disciplinas:
            # Formatando os dados para exibição amigável
            dados_formatados = []
            for item in disciplinas:
                dados_formatados.append({
                    "ID": item.get("id"),
                    "Nome": item.get("name"),
                    "Código": item.get("code"),
                    "Detalhes": item.get("description"),
                    "Status": item.get("status")
                })
            
            st.dataframe(dados_formatados, use_container_width=True)
        else:
            st.info("Nenhuma disciplina cadastrada ainda no Xano. Use a aba ao lado para cadastrar a primeira!")