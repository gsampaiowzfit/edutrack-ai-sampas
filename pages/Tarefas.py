# pyrefly: ignore [missing-import]
import streamlit as st
import utils
import datetime

try:
    st.set_page_config(page_title="Tarefas", page_icon="📝")
except Exception:
    pass
st.title("Gestão de Tarefas Acadêmicas")

utils.load_session()

if "active_tab_tarefas" not in st.session_state:
    st.session_state["active_tab_tarefas"] = "listar"
if "edit_task_id" not in st.session_state:
    st.session_state["edit_task_id"] = None
if "tarefas_cache" not in st.session_state:
    st.session_state["tarefas_cache"] = None
if "disciplinas_cache" not in st.session_state:
    st.session_state["disciplinas_cache"] = None

@st.dialog("Confirmar Exclusão de Tarefa")
def confirmar_exclusao_tarefa(task):
    st.write(f"Tem certeza que deseja excluir a tarefa **'{task.get('title')}'**?")
    st.write("Esta ação removerá permanentemente a tarefa do servidor.")
    st.write("")
    
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("Sim, Excluir", use_container_width=True, type="primary"):
            with st.spinner("Excluindo..."):
                res_del = utils.xano_delete("academic_tasks", f"academic_task/delete?task_id={task.get('id')}")
                if res_del:
                    st.toast("🗑️ Tarefa excluída com sucesso!")
                    st.session_state["tarefas_cache"] = None
                    st.rerun()
                else:
                    st.error("Erro ao excluir a tarefa no servidor.")
    with col_no:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()

if "auth_token" not in st.session_state or not st.session_state["auth_token"]:
    st.warning("⚠️ Você precisa estar logado para acessar as tarefas. Vá até a página principal (Dashboard) para entrar ou cadastrar-se.")
else:
    with st.spinner("Carregando dados..."):
        if st.session_state["tarefas_cache"] is None:
            st.session_state["tarefas_cache"] = utils.xano_get("academic_tasks", "academic_task/list") or []
        if st.session_state["disciplinas_cache"] is None:
            st.session_state["disciplinas_cache"] = utils.xano_get("subjects", "subject/list") or []

    tarefas = st.session_state["tarefas_cache"]
    disciplinas = st.session_state["disciplinas_cache"]

    editing_task = None
    if st.session_state["edit_task_id"]:
        editing_task = next((t for t in tarefas if t.get("id") == st.session_state["edit_task_id"]), None)
        if not editing_task:
            st.session_state["edit_task_id"] = None

    col_tab1, col_tab2 = st.columns(2)
    with col_tab1:
        if st.button("📋 Listar Tarefas", use_container_width=True, type="primary" if st.session_state["active_tab_tarefas"] == "listar" else "secondary"):
            st.session_state["active_tab_tarefas"] = "listar"
            st.session_state["edit_task_id"] = None
            st.rerun()
    with col_tab2:
        tab_label = "✏️ Editar Tarefa" if editing_task else "➕ Nova Tarefa"
        if st.button(tab_label, use_container_width=True, type="primary" if st.session_state["active_tab_tarefas"] == "nova" else "secondary"):
            st.session_state["active_tab_tarefas"] = "nova"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state["active_tab_tarefas"] == "nova":
        if not disciplinas:
            st.warning("⚠️ Você precisa cadastrar ao menos uma disciplina na aba 'Disciplinas' antes de gerenciar tarefas!")
        else:
            if editing_task:
                st.subheader(f"✏️ Editar Tarefa: {editing_task.get('title')}")
                form_key = f"form_editar_tarefa_{editing_task.get('id')}"
                default_title = editing_task.get("title", "")
                default_desc = editing_task.get("description", "")
                
                try:
                    default_due = datetime.datetime.strptime(editing_task.get("due_date")[:10], "%Y-%m-%d").date()
                except Exception:
                    default_due = datetime.date.today()
                    
                default_sub_id = editing_task.get("subject_id")
                default_status = editing_task.get("status", "pending")
                btn_label = "Salvar Alterações"
            else:
                st.subheader("➕ Cadastrar Nova Tarefa")
                form_key = "form_cadastrar_tarefa"
                default_title = ""
                default_desc = ""
                default_due = datetime.date.today()
                default_sub_id = disciplinas[0].get("id")
                default_status = "pending"
                btn_label = "Criar Tarefa"

            sub_map = {d.get("name"): d.get("id") for d in disciplinas}
            sub_list = list(sub_map.keys())
            
            sub_id_to_name = {d.get("id"): d.get("name") for d in disciplinas}
            initial_sub_name = sub_id_to_name.get(default_sub_id, sub_list[0])

            with st.form(form_key):
                title = st.text_input("Título da Tarefa", value=default_title, placeholder="Ex: Exercícios de Álgebra Linear")
                description = st.text_area("Descrição (Opcional)", value=default_desc, placeholder="Ex: Resolver os exercícios de 1 a 10 da lista 3")
                due_date = st.date_input("Data de Entrega", value=default_due)
                selected_sub_name = st.selectbox("Disciplina Vinculada", options=sub_list, index=sub_list.index(initial_sub_name))
                
                # Seleção de Prioridade
                prio_options = {"Baixa": "low", "Média": "medium", "Alta": "high"}
                default_prio = editing_task.get("priority", "medium") if editing_task else "medium"
                selected_prio_label = st.selectbox("Prioridade da Tarefa", options=list(prio_options.keys()), index=list(prio_options.values()).index(default_prio))
                priority = prio_options[selected_prio_label]

                status = "pending"
                if editing_task:
                    status_options = {"Pendente": "pending", "Em andamento": "in_progress", "Concluída": "completed"}
                    inverse_status = {v: k for k, v in status_options.items()}
                    selected_status_label = st.selectbox("Status da Tarefa", options=list(status_options.keys()), index=list(status_options.values()).index(default_status))
                    status = status_options[selected_status_label]

                col_btn_save, col_btn_cancel = st.columns([3, 1])
                with col_btn_save:
                    submitted = st.form_submit_button(btn_label, use_container_width=True)
                with col_btn_cancel:
                    cancelar = st.form_submit_button("Cancelar", use_container_width=True)

                if submitted:
                    if title:
                        sub_id = sub_map[selected_sub_name]
                        if editing_task:
                            edit_data = {
                                "task_id": editing_task.get("id"),
                                "title": title,
                                "description": description,
                                "due_date": str(due_date),
                                "status": status,
                                "priority": priority
                            }
                            with st.spinner("Salvando alterações..."):
                                res = utils.xano_patch("academic_tasks", "academic_task/update", edit_data)
                                if res:
                                    st.toast(f"✅ Tarefa '{title}' atualizada com sucesso!", icon="✏️")
                                    st.session_state["edit_task_id"] = None
                                    st.session_state["tarefas_cache"] = None
                                    st.session_state["active_tab_tarefas"] = "listar"
                                    st.rerun()
                                else:
                                    st.error("Erro ao atualizar a tarefa no servidor.")
                        else:
                            create_data = {
                                "title": title,
                                "description": description,
                                "due_date": str(due_date),
                                "subject_id": sub_id,
                                "priority": priority
                            }
                            with st.spinner("Criando tarefa..."):
                                res = utils.xano_post("academic_tasks", "academic_task/create", create_data)
                                if res:
                                    st.toast(f"🎉 Tarefa '{title}' criada com sucesso!", icon="📝")
                                    st.session_state["tarefas_cache"] = None
                                    st.session_state["active_tab_tarefas"] = "listar"
                                    st.rerun()
                                else:
                                    st.error("Erro ao cadastrar tarefa no servidor.")
                    else:
                        st.warning("Por favor, preencha o título da tarefa.")

                if cancelar:
                    st.session_state["edit_task_id"] = None
                    st.session_state["active_tab_tarefas"] = "listar"
                    st.rerun()

    elif st.session_state["active_tab_tarefas"] == "listar":
        if not tarefas:
            st.info("Nenhuma tarefa cadastrada ainda. Use a aba ao lado para criar a primeira!")
        else:
            col_search, col_filter, col_group = st.columns([2, 1, 1])
            with col_search:
                search_query = st.text_input("🔍 Buscar tarefas por título...", placeholder="Digite para filtrar...")
            with col_filter:
                status_filter = st.selectbox("Status", ["Todas", "Pendente", "Em andamento", "Concluída"])
            with col_group:
                group_by = st.selectbox("Agrupar por", ["Nenhum", "Disciplina", "Prazo"])

            st.markdown("---")

            status_map_inverse = {"Pendente": "pending", "Em andamento": "in_progress", "Concluída": "completed"}
            
            tarefas_filtradas = tarefas
            if search_query:
                tarefas_filtradas = [t for t in tarefas_filtradas if search_query.lower() in t.get("title", "").lower()]
            if status_filter != "Todas":
                tarefas_filtradas = [t for t in tarefas_filtradas if t.get("status") == status_map_inverse[status_filter]]

            sub_id_to_name = {d.get("id"): d.get("name") for d in disciplinas}
            hoje = datetime.date.today()

            def process_due_date(t):
                try:
                    return datetime.datetime.strptime(t.get("due_date")[:10], "%Y-%m-%d").date()
                except Exception:
                    return hoje

            def render_task_card(t):
                due_date_obj = process_due_date(t)
                is_overdue = due_date_obj < hoje and t.get("status") != "completed"
                
                border_color = "red" if is_overdue else "rgba(49, 51, 63, 0.2)"
                
                with st.container(border=True):
                    col_c1, col_c2 = st.columns([3, 1])
                    with col_c1:
                        status_labels = {"pending": "⏳ Pendente", "in_progress": "🔄 Em andamento", "completed": "✅ Concluída"}
                        status_disp = status_labels.get(t.get("status", "pending"), "⏳ Pendente")
                        
                        prio = t.get("priority", "medium")
                        prio_labels = {"low": "🟢 Prioridade Baixa", "medium": "🟡 Prioridade Média", "high": "🔴 Prioridade Alta"}
                        prio_disp = prio_labels.get(prio, "🟡 Prioridade Média")
                        
                        st.subheader(f"{t.get('title')}")
                        st.caption(f"📚 **Disciplina:** {sub_id_to_name.get(t.get('subject_id'), 'Geral')} | {status_disp} | {prio_disp}")
                        
                        if t.get("description"):
                            st.write(t.get("description"))
                            
                        date_str = due_date_obj.strftime("%d/%m/%Y")
                        if is_overdue:
                            st.markdown(f"<span style='color:red; font-weight:bold;'>🚨 PRAZO VENCIDO: {date_str}</span>", unsafe_allow_html=True)
                        else:
                            st.write(f"📅 **Prazo:** {date_str}")
                    
                    with col_c2:
                        st.write("")
                        
                        is_completed = t.get("status") == "completed"
                        check_label = "Concluída"
                        marcado = st.checkbox(check_label, value=is_completed, key=f"status_check_{t.get('id')}")
                        
                        if marcado != is_completed:
                            new_status = "completed" if marcado else "pending"
                            update_data = {
                                "task_id": t.get("id"),
                                "title": t.get("title"),
                                "description": t.get("description", ""),
                                "due_date": t.get("due_date")[:10] if t.get("due_date") else None,
                                "status": new_status,
                                "priority": t.get("priority", "medium")
                            }
                            with st.spinner("Atualizando status..."):
                                res = utils.xano_patch("academic_tasks", "academic_task/update", update_data)
                                if res:
                                    st.session_state["tarefas_cache"] = None
                                    st.toast(f"Tarefa marcada como {check_label.lower()}!" if marcado else "Tarefa marcada como pendente!")
                                    st.rerun()
                        
                        if st.button("✏️ Editar", key=f"edit_t_{t.get('id')}", use_container_width=True):
                            st.session_state["edit_task_id"] = t.get("id")
                            st.session_state["active_tab_tarefas"] = "nova"
                            st.rerun()
                            
                        if st.button("🗑️ Excluir", key=f"del_t_{t.get('id')}", use_container_width=True):
                            confirmar_exclusao_tarefa(t)

            if not tarefas_filtradas:
                st.info("Nenhuma tarefa corresponde aos filtros aplicados.")
            else:
                if group_by == "Nenhum":
                    for t in tarefas_filtradas:
                        render_task_card(t)
                        st.write("")
                elif group_by == "Disciplina":
                    grouped = {}
                    for t in tarefas_filtradas:
                        sub_name = sub_id_to_name.get(t.get("subject_id"), "Outras")
                        if sub_name not in grouped:
                            grouped[sub_name] = []
                        grouped[sub_name].append(t)
                        
                    for sub_name, task_list in grouped.items():
                        st.markdown(f"### 📚 {sub_name}")
                        for t in task_list:
                            render_task_card(t)
                            st.write("")
                elif group_by == "Prazo":
                    grouped_dates = {"🚨 Vencidas": [], "📅 Hoje": [], "🔮 Futuras": [], "✅ Concluídas": []}
                    for t in tarefas_filtradas:
                        if t.get("status") == "completed":
                            grouped_dates["✅ Concluídas"].append(t)
                        else:
                            due_date_obj = process_due_date(t)
                            if due_date_obj < hoje:
                                grouped_dates["🚨 Vencidas"].append(t)
                            elif due_date_obj == hoje:
                                grouped_dates["📅 Hoje"].append(t)
                            else:
                                grouped_dates["🔮 Futuras"].append(t)
                                
                    for category, task_list in grouped_dates.items():
                        if task_list:
                            st.markdown(f"### {category}")
                            for t in task_list:
                                render_task_card(t)
                                st.write("")