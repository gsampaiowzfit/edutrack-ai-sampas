# pyrefly: ignore [missing-import]
import streamlit as st
import utils
import datetime

try:
    st.set_page_config(page_title="Disciplinas", page_icon="📚")
except Exception:
    pass
st.title("Gestão de Disciplinas")

utils.load_session()

# Inicializa estados de navegação e edição se não existirem
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "listar"
if "edit_subject_id" not in st.session_state:
    st.session_state["edit_subject_id"] = None
if "disciplinas_cache" not in st.session_state:
    st.session_state["disciplinas_cache"] = None

@st.dialog("Confirmar Exclusão")
def confirmar_exclusao(disp):
    st.write(f"Tem certeza que deseja excluir a disciplina **'{disp.get('name')}'**?")
    st.write("Esta ação não poderá ser desfeita e removerá os dados do servidor.")
    st.write("")
    
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("Sim, Excluir", use_container_width=True, type="primary"):
            with st.spinner("Excluindo..."):
                res_del = utils.xano_delete("subjects", f"subject/delete?subject_id={disp.get('id')}")
                if res_del:
                    st.toast("🗑️ Disciplina excluída com sucesso!")
                    st.session_state["disciplinas_cache"] = None
                    st.rerun()
                else:
                    st.error("Erro ao excluir a disciplina no servidor.")
    with col_no:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()

if "auth_token" not in st.session_state or not st.session_state["auth_token"]:
    st.warning("⚠️ Você precisa estar logado para acessar as disciplinas. Vá até a página principal (Dashboard) para entrar ou cadastrar-se.")
else:
    # --- BUSCAR DISCIPLINAS DO XANO COM CACHE ---
    disciplinas = st.session_state.get("disciplinas_cache")
    if disciplinas is None:
        if st.session_state["active_tab"] == "listar" or st.session_state["edit_subject_id"]:
            with st.spinner("Carregando disciplinas..."):
                disciplinas = utils.xano_get("subjects", "subject/list")
                if disciplinas is None:
                    disciplinas = []
                st.session_state["disciplinas_cache"] = disciplinas
        else:
            disciplinas = []

    # Se estiver em modo de edição, busca a disciplina sendo editada
    editing_sub = None
    if st.session_state["edit_subject_id"]:
        editing_sub = next((d for d in disciplinas if d.get("id") == st.session_state["edit_subject_id"]), None)
        # Se por algum motivo a disciplina não existir mais na lista, cancela a edição
        if not editing_sub:
            st.session_state["edit_subject_id"] = None

    # --- MENU DE NAVEGAÇÃO PREMIUM (BOTÕES ESTILIZADOS) ---
    col_tab1, col_tab2 = st.columns(2)
    with col_tab1:
        if st.button("📋 Listar Disciplinas", use_container_width=True, type="primary" if st.session_state["active_tab"] == "listar" else "secondary"):
            st.session_state["active_tab"] = "listar"
            st.session_state["edit_subject_id"] = None # Cancela edição ao voltar para a lista voluntariamente
            st.rerun()
    with col_tab2:
        tab_label = "✏️ Editar Disciplina" if editing_sub else "➕ Nova Disciplina"
        if st.button(tab_label, use_container_width=True, type="primary" if st.session_state["active_tab"] == "nova" else "secondary"):
            st.session_state["active_tab"] = "nova"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== ABA DE CADASTRO E EDIÇÃO ====================
    if st.session_state["active_tab"] == "nova":
        if editing_sub:
            st.subheader(f"✏️ Editar Disciplina: {editing_sub.get('name')}")
            form_key = f"form_editar_disciplina_{editing_sub.get('id')}"
            default_nome = editing_sub.get("name", "")
            default_prof = editing_sub.get("teacher", "")
            default_carga = int(editing_sub.get("workload") or 60)
            default_codigo = editing_sub.get("code", "")
            default_semestre = editing_sub.get("semester", "")
            if default_codigo == "N/A":
                default_codigo = ""
            btn_label = "Salvar Alterações"
        else:
            st.subheader("➕ Cadastrar Nova Matéria")
            form_key = "form_cadastrar_disciplina"
            default_nome = ""
            default_prof = ""
            default_carga = 60
            default_codigo = ""
            default_semestre = ""
            btn_label = "Salvar Disciplina"

        with st.form(form_key):
            nome = st.text_input("Nome da Disciplina", value=default_nome, placeholder="Ex: Algoritmos e Estruturas de Dados")
            professor = st.text_input("Nome do Professor", value=default_prof, placeholder="Ex: Dr. Hamilton")
            semestre = st.text_input("Semestre/Período Letivo (Opcional)", value=default_semestre, placeholder="Ex: 2026.1 ou 1º Semestre")
            carga_horaria = st.number_input("Carga Horária (em horas)", min_value=1, max_value=400, value=default_carga, step=1)
            codigo = st.text_input("Código da Matéria (Opcional)", value=default_codigo, placeholder="Ex: CC-3021")
            
            col_btn_save, col_btn_cancel = st.columns([3, 1])
            with col_btn_save:
                submitted = st.form_submit_button(btn_label, use_container_width=True)
            with col_btn_cancel:
                cancelar = st.form_submit_button("Cancelar", use_container_width=True)

            if submitted:
                if nome and professor:
                    if editing_sub:
                        # FLUXO DE EDIÇÃO (UPDATE)
                        edit_data = {
                            "subject_id": editing_sub.get("id"),
                            "name": nome,
                            "teacher": professor,
                            "semester": semestre,
                            "workload": int(carga_horaria),
                            "code": codigo if codigo else "N/A",
                            "status": editing_sub.get("status", "active")
                        }
                        with st.spinner("Salvando alterações..."):
                            res = utils.xano_patch("subjects", "subject/update", edit_data)
                            if res:
                                st.toast(f"✅ Disciplina '{nome}' atualizada com sucesso!", icon="✏️")
                                st.session_state["edit_subject_id"] = None
                                st.session_state["disciplinas_cache"] = None
                                st.session_state["active_tab"] = "listar"
                                st.rerun()
                            else:
                                st.error("Erro ao atualizar a disciplina. Verifique se o nome e o professor estão duplicados em outra disciplina.")
                    else:
                        # FLUXO DE CADASTRO (CREATE)
                        data = {
                            "name": nome,
                            "code": codigo if codigo else "N/A",
                            "teacher": professor,
                            "semester": semestre,
                            "workload": int(carga_horaria),
                            "status": "active"
                        }
                        with st.spinner("Salvando disciplina..."):
                            res = utils.xano_post("subjects", "subject/create", data)
                            if res:
                                st.toast(f"🎉 Disciplina '{nome}' cadastrada com sucesso!", icon="🎓")
                                st.session_state["disciplinas_cache"] = None
                                st.session_state["active_tab"] = "listar"
                                st.rerun()
                            else:
                                st.error("Erro ao cadastrar disciplina. Verifique se o nome e o professor já estão cadastrados.")
                else:
                    st.warning("Por favor, preencha o nome da disciplina e o professor.")

            if cancelar:
                st.session_state["edit_subject_id"] = None
                st.session_state["active_tab"] = "listar"
                st.rerun()

    # ==================== ABA DE LISTAGEM ====================
    elif st.session_state["active_tab"] == "listar":
        # Buscar tarefas para calcular progresso e atrasadas
        tarefas = st.session_state.get("tarefas_cache")
        if tarefas is None:
            with st.spinner("Carregando tarefas para progresso..."):
                tarefas = utils.xano_get("academic_tasks", "academic_task/list") or []
                st.session_state["tarefas_cache"] = tarefas

        hoje = datetime.date.today()
        disciplinas_atrasadas = set()
        for t in tarefas:
            if t.get("status") != "completed":
                try:
                    due_date_str = t.get("due_date")[:10]
                    due_date_obj = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    if due_date_obj < hoje:
                        disciplinas_atrasadas.add(t.get("subject_id"))
                except Exception:
                    pass

        if disciplinas:
            # --- FILTROS DE BUSCA ---
            col_search, col_filter = st.columns([2, 1])
            with col_search:
                search_query = st.text_input("🔍 Buscar disciplinas por nome...", placeholder="Digite para buscar...")
            with col_filter:
                overdue_only = st.checkbox("⚠️ Apenas com tarefas em atraso", value=False)

            # --- APLICAR FILTROS INICIAIS ---
            disciplinas_filtradas = disciplinas
            if search_query:
                disciplinas_filtradas = [
                    d for d in disciplinas_filtradas 
                    if search_query.lower() in d.get("name", "").lower()
                ]
            if overdue_only:
                disciplinas_filtradas = [
                    d for d in disciplinas_filtradas 
                    if d.get("id") in disciplinas_atrasadas
                ]

            # Dividir em Abas: Ativas e Arquivadas
            tab_ativas, tab_arquivadas = st.tabs(["🟢 Ativas", "📁 Arquivadas"])

            with tab_ativas:
                ativas = [d for d in disciplinas_filtradas if d.get("status") != "archived"]
                if ativas:
                    for disp in ativas:
                        # Calcular progresso
                        tarefas_disp = [t for t in tarefas if t.get("subject_id") == disp.get("id")]
                        total_t = len(tarefas_disp)
                        concluidas_t = sum(1 for t in tarefas_disp if t.get("status") == "completed")
                        progresso = (concluidas_t / total_t) if total_t > 0 else 0.0

                        with st.container(border=True):
                            col_info, col_actions = st.columns([3, 1])
                            with col_info:
                                st.subheader(f"📚 {disp.get('name')}")
                                st.write(f"👤 **Professor:** {disp.get('teacher', 'Não informado')}")
                                st.write(f"⏱️ **Carga Horária:** {disp.get('workload', 'Não informada')} horas")
                                if disp.get("semester"):
                                    st.write(f"📅 **Semestre/Período:** {disp.get('semester')}")
                                if disp.get("code") and disp.get("code") != "N/A":
                                    st.caption(f"🔑 Código da Matéria: {disp.get('code')}")
                                
                                st.markdown(f"📈 **Progresso:** {concluidas_t}/{total_t} concluídas ({progresso*100:.1f}%)")
                                st.progress(progresso)
                                
                                if disp.get("id") in disciplinas_atrasadas:
                                    st.warning("⚠️ Esta disciplina possui tarefas pendentes em atraso!")
                            with col_actions:
                                st.write("")
                                if st.button("✏️ Editar", key=f"edit_btn_{disp.get('id')}", use_container_width=True):
                                    st.session_state["edit_subject_id"] = disp.get("id")
                                    st.session_state["active_tab"] = "nova"
                                    st.rerun()
                                if st.button("📁 Arquivar", key=f"archive_btn_{disp.get('id')}", use_container_width=True):
                                    edit_data = {
                                        "subject_id": disp.get("id"),
                                        "name": disp.get("name"),
                                        "teacher": disp.get("teacher"),
                                        "workload": int(disp.get("workload") or 60),
                                        "code": disp.get("code") or "N/A",
                                        "semester": disp.get("semester"),
                                        "status": "archived"
                                    }
                                    with st.spinner("Arquivando..."):
                                        res = utils.xano_patch("subjects", "subject/update", edit_data)
                                        if res:
                                            st.toast(f"✅ Disciplina '{disp.get('name')}' arquivada!")
                                            st.session_state["disciplinas_cache"] = None
                                            st.rerun()
                                if st.button("🗑️ Excluir", key=f"del_btn_{disp.get('id')}", use_container_width=True):
                                    confirmar_exclusao(disp)
                else:
                    st.info("Nenhuma disciplina ativa encontrada.")

            with tab_arquivadas:
                arquivadas = [d for d in disciplinas_filtradas if d.get("status") == "archived"]
                if arquivadas:
                    for disp in arquivadas:
                        # Calcular progresso
                        tarefas_disp = [t for t in tarefas if t.get("subject_id") == disp.get("id")]
                        total_t = len(tarefas_disp)
                        concluidas_t = sum(1 for t in tarefas_disp if t.get("status") == "completed")
                        progresso = (concluidas_t / total_t) if total_t > 0 else 0.0

                        with st.container(border=True):
                            col_info, col_actions = st.columns([3, 1])
                            with col_info:
                                st.subheader(f"📚 {disp.get('name')} (Arquivada)")
                                st.write(f"👤 **Professor:** {disp.get('teacher', 'Não informado')}")
                                st.write(f"⏱️ **Carga Horária:** {disp.get('workload', 'Não informada')} horas")
                                if disp.get("semester"):
                                    st.write(f"📅 **Semestre/Período:** {disp.get('semester')}")
                                if disp.get("code") and disp.get("code") != "N/A":
                                    st.caption(f"🔑 Código da Matéria: {disp.get('code')}")
                                
                                st.markdown(f"📈 **Progresso:** {concluidas_t}/{total_t} concluídas ({progresso*100:.1f}%)")
                                st.progress(progresso)
                            with col_actions:
                                st.write("")
                                if st.button("📂 Desarquivar", key=f"unarchive_btn_{disp.get('id')}", use_container_width=True):
                                    edit_data = {
                                        "subject_id": disp.get("id"),
                                        "name": disp.get("name"),
                                        "teacher": disp.get("teacher"),
                                        "workload": int(disp.get("workload") or 60),
                                        "code": disp.get("code") or "N/A",
                                        "semester": disp.get("semester"),
                                        "status": "active"
                                    }
                                    with st.spinner("Desarquivando..."):
                                        res = utils.xano_patch("subjects", "subject/update", edit_data)
                                        if res:
                                            st.toast(f"✅ Disciplina '{disp.get('name')}' reativada!")
                                            st.session_state["disciplinas_cache"] = None
                                            st.rerun()
                                if st.button("🗑️ Excluir", key=f"del_btn_arq_{disp.get('id')}", use_container_width=True):
                                    confirmar_exclusao(disp)
                else:
                    st.info("Nenhuma disciplina arquivada.")
        else:
            st.info("Nenhuma disciplina cadastrada ainda. Use a aba ao lado para cadastrar a primeira!")