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
    
    /* Estilos para a Tela de Boas-Vindas */
    .welcome-container {
        max-width: 900px;
        margin: 20px auto;
        text-align: center;
    }
    .welcome-hero {
        background: linear-gradient(135deg, rgba(108, 92, 231, 0.08) 0%, rgba(162, 155, 254, 0.03) 100%);
        border: 1px solid rgba(108, 92, 231, 0.15);
        border-radius: 20px;
        padding: 40px 25px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.25);
    }
    .welcome-features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        margin-bottom: 35px;
    }
    .welcome-feature-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 22px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: left;
        backdrop-filter: blur(5px);
    }
    .welcome-feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(108, 92, 231, 0.4);
        background: rgba(30, 41, 59, 0.7);
        box-shadow: 0 8px 20px -10px rgba(108, 92, 231, 0.3);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 12px;
        display: inline-block;
    }
    .feature-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 6px;
    }
    .feature-desc {
        font-size: 0.9rem;
        color: #94a3b8;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def show_login():
    if "login_view" not in st.session_state:
        st.session_state["login_view"] = "welcome"
        
    view = st.session_state["login_view"]
    
    if view == "welcome":
        # Botões sempre visíveis na barra lateral
        st.sidebar.markdown("### Acesso Rápido")
        if st.sidebar.button("🔒 Entrar na Conta", key="side_login_btn", use_container_width=True, type="primary"):
            st.session_state["login_view"] = "login"
            st.rerun()
        if st.sidebar.button("📝 Criar Conta", key="side_signup_btn", use_container_width=True):
            st.session_state["login_view"] = "signup"
            st.rerun()
        st.sidebar.markdown("---")
        st.sidebar.info("Utilize os botões acima ou no painel principal para acessar.")
        
        st.markdown(
            """
            <div class="welcome-container">
                <div class="welcome-hero">
                    <div class="brand-title">🎓 EduTrack AI</div>
                    <div class="brand-subtitle" style="margin-bottom: 15px;">Gestão acadêmica inteligente com IA</div>
                    <p style="font-size: 1.05rem; color: #cbd5e1; max-width: 650px; margin: 0 auto; line-height: 1.6;">
                        A plataforma moderna que simplifica sua rotina acadêmica. Organize suas disciplinas, 
                        controle seus prazos de tarefas e impulsione seu aprendizado com insights gerados por inteligência artificial.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Grid de Funcionalidades
        st.markdown(
            """
            <div class="welcome-features">
                <div class="welcome-feature-card">
                    <span class="feature-icon">📚</span>
                    <div class="feature-title">Gestão de Disciplinas</div>
                    <div class="feature-desc">Gerencie suas matérias do semestre, acompanhe o status de cada uma e centralize suas informações in um único lugar.</div>
                </div>
                <div class="welcome-feature-card">
                    <span class="feature-icon">📅</span>
                    <div class="feature-title">Controle de Tarefas</div>
                    <div class="feature-desc">Cadastre e monitore prazos de entrega de trabalhos, projetos e provas com marcadores de prioridade e controle de atrasos.</div>
                </div>
                <div class="welcome-feature-card">
                    <span class="feature-icon">📊</span>
                    <div class="feature-title">Relatórios e IA</div>
                    <div class="feature-desc">Visualize seu progresso de tarefas concluídas e obtenha relatórios analíticos de desempenho em tempo real.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<h4 style='text-align: center; margin-bottom: 25px; color: #f8fafc; font-weight: 600;'>Como você deseja prosseguir?</h4>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("🔒 Entrar na Minha Conta", use_container_width=True, type="primary", key="welcome_login_btn"):
                st.session_state["login_view"] = "login"
                st.rerun()
        with col_btn2:
            if st.button("📝 Criar Conta Gratuita", use_container_width=True, key="welcome_signup_btn"):
                st.session_state["login_view"] = "signup"
                st.rerun()
                
    elif view == "login":
        # Botão discreto para voltar à tela inicial
        if st.button("← Voltar para Apresentação", key="back_to_welcome_login"):
            st.session_state["login_view"] = "welcome"
            st.rerun()
            
        st.markdown('<div class="brand-title">🎓 EduTrack AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-subtitle">Acesse sua conta para continuar</div>', unsafe_allow_html=True)
        
        st.sidebar.info("Insira suas credenciais de acesso.")
        
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
        
        # Link rápido para cadastrar nova conta
        st.write("")
        col_l1, col_l2 = st.columns([3, 2])
        with col_l1:
            st.markdown("<p style='margin-top: 6px; font-size: 0.95rem; color: #94a3b8;'>Não possui uma conta?</p>", unsafe_allow_html=True)
        with col_l2:
            if st.button("Cadastre-se aqui", key="go_to_signup_btn", use_container_width=True):
                st.session_state["login_view"] = "signup"
                st.rerun()

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
                            
    elif view == "signup":
        # Botão discreto para voltar à tela inicial
        if st.button("← Voltar para Apresentação", key="back_to_welcome_signup"):
            st.session_state["login_view"] = "welcome"
            st.rerun()
            
        st.markdown('<div class="brand-title">🎓 EduTrack AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-subtitle">Crie sua conta gratuita em segundos</div>', unsafe_allow_html=True)
        
        st.sidebar.info("Preencha o formulário para criar sua conta acadêmica.")
        
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

        # Link rápido para voltar à tela de Login
        st.write("")
        col_s1, col_s2 = st.columns([3, 2])
        with col_s1:
            st.markdown("<p style='margin-top: 6px; font-size: 0.95rem; color: #94a3b8;'>Já possui uma conta?</p>", unsafe_allow_html=True)
        with col_s2:
            if st.button("Faça login aqui", key="go_to_login_btn", use_container_width=True):
                st.session_state["login_view"] = "login"
                st.rerun()

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