# pyrefly: ignore [missing-import]
import streamlit as st  
import utils
import re

st.set_page_config(page_title="EduTrack AI", page_icon="🎓")

# Inicializa e carrega estados de sessão persistentes
utils.load_session()

def show_login():
    st.title("🎓 EduTrack AI")
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
                    with st.spinner("Autenticando..."):
                        res = utils.xano_post("auth", "auth/login_app", {"email": email, "password": password})
                        if res and "authToken" in res:
                            st.session_state["auth_token"] = res["authToken"]
                            me = utils.xano_get("auth", "auth/me_app")
                            if me and "name" in me:
                                st.session_state["user_name"] = me["name"]
                            else:
                                st.session_state["user_name"] = email
                            utils.save_session(res["authToken"], st.session_state["user_name"])
                            st.success("Login realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("E-mail ou senha incorretos.")
                            st.toast("E-mail ou senha incorretos.", icon="❌")
                else:
                    st.warning("Preencha todos os campos.")
        
        st.markdown("---")
        with st.expander("🔑 Esqueci minha senha"):
            st.subheader("Recuperação de Senha")
            if "reset_token_login" not in st.session_state:
                st.session_state["reset_token_login"] = None
            
            email_rec = st.text_input("Digite seu e-mail cadastrado", key="email_rec_input")
            if st.button("Solicitar Código de Redefinição", key="btn_req_rec"):
                if email_rec:
                    with st.spinner("Enviando código de redefinição..."):
                        res_rec = utils.xano_post("auth", "auth/request_password_reset_app", {"email": email_rec})
                        if res_rec and "token" in res_rec:
                            st.session_state["reset_token_login"] = res_rec["token"]
                            st.success(f"Código gerado! Para fins de teste, utilize o código: **{res_rec['token']}**")
                        else:
                            st.error("E-mail não encontrado ou erro ao gerar código.")
                else:
                    st.warning("Preencha o e-mail.")
            
            if st.session_state["reset_token_login"]:
                st.markdown("---")
                st.write("Preencha as informações abaixo para criar sua nova senha:")
                with st.form("form_reset_senha_login"):
                    codigo_rec = st.text_input("Código de verificação", type="password")
                    nova_senha_rec = st.text_input("Nova Senha", type="password", help="Mínimo de 8 caracteres, com pelo menos uma letra e um número")
                    confirmar_senha_rec = st.text_input("Confirmar Nova Senha", type="password")
                    
                    submitted_rec = st.form_submit_button("Alterar Senha")
                    if submitted_rec:
                        if codigo_rec and nova_senha_rec and confirmar_senha_rec:
                            if nova_senha_rec == confirmar_senha_rec:
                                if len(nova_senha_rec) >= 8 and re.search(r"[a-zA-Z]", nova_senha_rec) and re.search(r"\d", nova_senha_rec):
                                    with st.spinner("Alterando senha..."):
                                        res_apply = utils.xano_post("auth", "auth/reset_password_app", {
                                            "email": email_rec,
                                            "token": codigo_rec,
                                            "password": nova_senha_rec
                                        })
                                        if res_apply:
                                            st.success("Senha redefinida com sucesso!")
                                            st.session_state["reset_token_login"] = None
                                            
                                            import time
                                            st.toast("Senha redefinida! Encerrando sessões ativas...", icon="🔒")
                                            with st.spinner("Atualizando credenciais..."):
                                                time.sleep(1.5)
                                                
                                            utils.clear_session()
                                            st.rerun()
                                        else:
                                            st.error("Código de verificação incorreto ou expirado.")
                                else:
                                    st.warning("A senha deve ter no mínimo 8 caracteres, contendo pelo menos uma letra e um número.")
                                    st.toast("A senha não atende aos requisitos!", icon="⚠️")
                            else:
                                st.warning("As senhas não coincidem.")
                        else:
                            st.warning("Preencha todos os campos.")
                    
    with tab_cadastro:
        st.subheader("Criar Nova Conta")
        with st.form("form_cadastro"):
            nome = st.text_input("Nome Completo")
            email_cad = st.text_input("E-mail")
            senha_cad = st.text_input("Senha", type="password", help="A senha deve conter no mínimo 8 caracteres, com pelo menos uma letra e um número")
            submitted_cad = st.form_submit_button("Criar Conta")
            
            if submitted_cad:
                if nome and email_cad and senha_cad:
                    if len(senha_cad) >= 8 and re.search(r"[a-zA-Z]", senha_cad) and re.search(r"\d", senha_cad):
                        with st.spinner("Criando sua conta..."):
                            res = utils.xano_post("auth", "auth/signup_app", {"name": nome, "email": email_cad, "password": senha_cad})
                            if res and "authToken" in res:
                                st.session_state["auth_token"] = res["authToken"]
                                st.session_state["user_name"] = nome
                                utils.save_session(res["authToken"], nome)
                                st.success("Conta criada e logada com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao criar conta. Verifique os dados e tente novamente.")
                    else:
                        st.warning("A senha deve ter no mínimo 8 caracteres, contendo pelo menos uma letra e um número.")
                        st.toast("A senha não atende aos requisitos!", icon="⚠️")
                else:
                    st.warning("Preencha todos os campos.")

def show_dashboard():
    st.title("🎓 EduTrack AI")
    st.write(f"Olá, **{st.session_state['user_name']}**! Bem-vindo ao seu assistente acadêmico!")
    
    # Buscar dados reais do Xano para as métricas
    disciplinas = utils.xano_get("subjects", "subject/list")
    total_disciplinas = len(disciplinas) if disciplinas else 0
    
    col1, col2 = st.columns(2)
    col1.metric("Disciplinas Ativas", str(total_disciplinas))
    col2.metric("Tarefas Pendentes", "0") # Será integrada a seguir

# Controle de navegação dinâmico usando st.navigation do Streamlit
if not st.session_state.get("auth_token"):
    login_page = st.Page(show_login, title="Entrar", icon="🔒")
    pg = st.navigation([login_page], position="hidden")
else:
    # Sidebar global (Cabeçalho e Sair)
    st.sidebar.header("Menu")
    st.sidebar.success(f"Logado como: {st.session_state['user_name']}")
    if st.sidebar.button("Sair", key="global_logout_btn"):
        utils.clear_session()
        st.rerun()

    # Define as páginas acessíveis com títulos e ícones customizados
    dashboard_page = st.Page(show_dashboard, title="Dashboard", icon="🎓")
    disciplinas_page = st.Page("pages/Disciplinas.py", title="Disciplinas", icon="📚")
    tarefas_page = st.Page("pages/Tarefas.py", title="Tarefas", icon="📝")
    perfil_page = st.Page("pages/Perfil.py", title="Meu Perfil", icon="👤")
    
    pg = st.navigation({
        "Acadêmico": [dashboard_page, disciplinas_page, tarefas_page],
        "Conta": [perfil_page]
    })

pg.run()