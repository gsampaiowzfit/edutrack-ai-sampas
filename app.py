# pyrefly: ignore [missing-import]
import streamlit as st  
import utils
import re
import datetime

st.set_page_config(page_title="EduTrack AI", page_icon="🎓")

# Inicializa e carrega estados de sessão persistentes
utils.load_session()

# Injeção de CSS global para design premium e consistente
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Título estilizado com gradiente */
    .brand-title {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .brand-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 25px;
    }
    
    /* Customizar botões */
    div.stButton > button {
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(108, 92, 231, 0.25) !important;
    }
    
    /* Cartões Métricos Personalizados */
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 15px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #6c5ce7;
    }
    .metric-value {
        font-size: 2.4rem;
        font-weight: 700;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    /* Badges de Prioridade */
    .priority-high {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
    }
    .priority-medium {
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
    }
    .priority-low {
        background-color: rgba(59, 130, 246, 0.15);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
    }
    
    /* Login Box */
    .login-container {
        max-width: 450px;
        margin: 40px auto;
        padding: 30px;
        border-radius: 16px;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

def show_login():
    st.markdown('<div class="brand-title">🎓 EduTrack AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Gestão acadêmica inteligente com IA</div>', unsafe_allow_html=True)
    
    st.sidebar.info("Faça login para começar.")
    
    tab_login, tab_cadastro = st.tabs(["🔒 Entrar", "📝 Criar Conta"])
    
    with tab_login:
        st.subheader("Login")
        with st.form("form_login"):
            email = st.text_input("E-mail", placeholder="seuemail@exemplo.com")
            password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
            
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
            
            email_rec = st.text_input("Digite seu e-mail cadastrado", key="email_rec_input", placeholder="email@provedor.com")
            if st.button("Solicitar Código de Redefinição", key="btn_req_rec", use_container_width=True):
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
                    
                    submitted_rec = st.form_submit_button("Alterar Senha", use_container_width=True)
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
            nome = st.text_input("Nome Completo", placeholder="Seu Nome")
            email_cad = st.text_input("E-mail", placeholder="seuemail@exemplo.com")
            senha_cad = st.text_input("Senha", type="password", placeholder="Mínimo 8 caracteres", help="A senha deve conter no mínimo 8 caracteres, com pelo menos uma letra e um número")
            submitted_cad = st.form_submit_button("Criar Conta", use_container_width=True)
            
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
    st.markdown('<div class="brand-title" style="text-align: left;">🎓 EduTrack AI</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="brand-subtitle" style="text-align: left;">Olá, <b>{st.session_state["user_name"]}</b>! Veja a visão geral do seu semestre.</div>', unsafe_allow_html=True)
    
    # Buscar dados reais no Xano
    with st.spinner("Carregando dados acadêmicos..."):
        disciplinas = utils.xano_get("subjects", "subject/list") or []
        tarefas = utils.xano_get("academic_tasks", "academic_task/list") or []
    
    # Filtrar disciplinas ativas
    disciplinas_ativas = [d for d in disciplinas if d.get("status") != "archived" and not d.get("deleted")]
    total_disciplinas_ativas = len(disciplinas_ativas)
    
    # Exibir tela de boas-vindas caso não possua disciplinas
    if total_disciplinas_ativas == 0:
        st.markdown(
            """
            <div style="padding: 40px; border-radius: 16px; background: rgba(108, 92, 231, 0.05); border: 1px solid rgba(108, 92, 231, 0.2); margin: 20px 0; text-align: center;">
                <span style="font-size: 3rem;">👋</span>
                <h2 style="color: #6C5CE7; margin-top: 15px; margin-bottom: 10px;">Seja muito bem-vindo!</h2>
                <p style="font-size: 1.1rem; line-height: 1.6; color: #b2bec3; max-width: 600px; margin: 0 auto 25px auto;">
                    Estamos muito felizes em ter você aqui no EduTrack AI! Para começar a gerenciar sua jornada acadêmica, você precisa criar a sua primeira disciplina.
                </p>
                <div style="font-size: 0.95rem; color: #94a3b8; margin-bottom: 30px;">
                    💡 <b>Dica:</b> Vá para a página de "Disciplinas" no menu e insira os dados das suas matérias atuais.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("📚 Cadastrar Minha Primeira Disciplina", type="primary", use_container_width=True):
            st.switch_page("pages/Disciplinas.py")
        return
        
    # Calcular métricas
    hoje = datetime.date.today()
    total_tarefas = len(tarefas)
    concluidas = 0
    pendentes = 0
    atrasadas = 0
    
    proximas_tarefas = []
    
    for t in tarefas:
        is_completed = t.get("status") == "completed"
        if is_completed:
            concluidas += 1
        else:
            pendentes += 1
            try:
                due_date_str = t.get("due_date")[:10]
                due_date_obj = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if due_date_obj < hoje:
                    atrasadas += 1
                proximas_tarefas.append((due_date_obj, t))
            except Exception:
                pass
                
    progresso_geral = (concluidas / total_tarefas * 100) if total_tarefas > 0 else 0.0
    
    # Ordenar as próximas tarefas pelo prazo (menor prazo primeiro)
    proximas_tarefas.sort(key=lambda x: x[0])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">📚 Disciplinas</div>
                <div class="metric-value" style="color: #6c5ce7;">{total_disciplinas_ativas}</div>
                <div style="font-size: 0.8rem; color: #64748b;">Ativas no Semestre</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">⏳ Pendentes</div>
                <div class="metric-value" style="color: #3b82f6;">{pendentes}</div>
                <div style="font-size: 0.8rem; color: #64748b;">Aguardando execução</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">🚨 Em Atraso</div>
                <div class="metric-value" style="color: #ef4444;">{atrasadas}</div>
                <div style="font-size: 0.8rem; color: #64748b;">Prazo vencido</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">📈 Progresso</div>
                <div class="metric-value" style="color: #10b981;">{progresso_geral:.1f}%</div>
                <div style="font-size: 0.8rem; color: #64748b;">Geral concluído</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.write("")
    
    # Indicador de progresso geral
    st.subheader("Progresso de Conclusão Geral")
    st.progress(progresso_geral / 100.0)
    
    st.write("")
    st.markdown("---")
    
    # Próximas tarefas com prazo mais próximo
    st.subheader("🔮 Próximas Tarefas do Calendário")
    if not proximas_tarefas:
        st.info("Excelente! Você não tem tarefas pendentes. Tudo em dia! 🎉")
    else:
        sub_id_to_name = {d.get("id"): d.get("name") for d in disciplinas}
        
        for due_obj, t in proximas_tarefas[:5]:
            due_str = due_obj.strftime("%d/%m/%Y")
            sub_name = sub_id_to_name.get(t.get("subject_id"), "Geral")
            prio = t.get("priority", "medium")
            
            prio_label = "Média"
            prio_class = "priority-medium"
            if prio == "low":
                prio_label = "Baixa"
                prio_class = "priority-low"
            elif prio == "high":
                prio_label = "Alta"
                prio_class = "priority-high"
                
            is_overdue = due_obj < hoje
            overdue_tag = " <span style='color:#ef4444; font-weight:bold; margin-left:10px;'>[ATRASADA]</span>" if is_overdue else ""
            
            col_t1, col_t2 = st.columns([5, 1])
            with col_t1:
                st.markdown(
                    f"""
                    <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid #6C5CE7; padding: 12px; border-radius: 4px 8px 8px 4px; margin-bottom: 10px; border-top: 1px solid rgba(255,255,255,0.05); border-right: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <div style="font-weight: 600; font-size: 1.05rem; color: #f8fafc;">{t.get('title')}</div>
                        <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">
                            📚 Disciplina: <b>{sub_name}</b> | 📅 Prazo: {due_str}{overdue_tag}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_t2:
                st.markdown(f'<div style="margin-top: 14px; text-align: center;"><span class="{prio_class}">{prio_label}</span></div>', unsafe_allow_html=True)

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
    relatorios_page = st.Page("pages/Relatorios.py", title="Relatórios", icon="📊")
    perfil_page = st.Page("pages/Perfil.py", title="Meu Perfil", icon="👤")
    
    pg = st.navigation({
        "Acadêmico": [dashboard_page, disciplinas_page, tarefas_page, relatorios_page],
        "Conta": [perfil_page]
    })

pg.run()