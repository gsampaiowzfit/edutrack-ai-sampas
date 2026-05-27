import streamlit as st  
import utils

st.set_page_config(page_title="EduTrack AI", page_icon="🎓")
st.title("🎓 EduTrack AI")

# Inicializa estados de sessão
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_name" not in st.session_state:
    st.session_state["user_name"] = None

# Sidebar
st.sidebar.header("Menu")

if st.session_state["auth_token"]:
    st.sidebar.success(f"Logado como: {st.session_state['user_name']}")
    if st.sidebar.button("Sair"):
        st.session_state["auth_token"] = None
        st.session_state["user_name"] = None
        st.rerun()

    menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])
    
    if menu_option == "Dashboard":
        st.write(f"Olá, **{st.session_state['user_name']}**! Bem-vindo ao seu assistente acadêmico!")
        
        # Buscar dados reais do Xano para as métricas
        disciplinas = utils.xano_get("subjects", "subject/list_app")
        total_disciplinas = len(disciplinas) if disciplinas else 0
        
        col1, col2 = st.columns(2)
        col1.metric("Disciplinas Ativas", str(total_disciplinas))
        col2.metric("Tarefas Pendentes", "0") # Será integrada a seguir
else:
    st.sidebar.info("Faça login para começar.")
    
    tab_login, tab_cadastro = st.tabs(["🔒 Entrar", "📝 Criar Conta"])
    
    with tab_login:
        st.subheader("Login")
        with st.form("form_login"):
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar")
            
            if submitted:
                if email and password:
                    res = utils.xano_post("auth", "auth/login_app", {"email": email, "password": password})
                    if res and "authToken" in res:
                        st.session_state["auth_token"] = res["authToken"]
                        # Buscar dados do usuário logado
                        me = utils.xano_get("auth", "auth/me_app")
                        if me and "name" in me:
                            st.session_state["user_name"] = me["name"]
                        else:
                            st.session_state["user_name"] = email
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("E-mail ou senha incorretos.")
                else:
                    st.warning("Preencha todos os campos.")
                    
    with tab_cadastro:
        st.subheader("Criar Nova Conta")
        with st.form("form_cadastro"):
            nome = st.text_input("Nome Completo")
            email_cad = st.text_input("E-mail")
            senha_cad = st.text_input("Senha (mínimo 8 caracteres)", type="password")
            submitted_cad = st.form_submit_button("Criar Conta")
            
            if submitted_cad:
                if nome and email_cad and senha_cad:
                    res = utils.xano_post("auth", "auth/signup_app", {"name": nome, "email": email_cad, "password": senha_cad})
                    if res and "authToken" in res:
                        st.session_state["auth_token"] = res["authToken"]
                        st.session_state["user_name"] = nome
                        st.success("Conta criada e logada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar conta. Verifique os dados e tente novamente.")
                else:
                    st.warning("Preencha todos os campos.")