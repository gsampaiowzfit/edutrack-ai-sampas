# pyrefly: ignore [missing-import]
import streamlit as st
import utils

st.set_page_config(page_title="Tarefas", page_icon="📝")
st.title("Gerenciamento de Tarefas")

utils.load_session()

# Verifica autenticação
if "auth_token" not in st.session_state or not st.session_state["auth_token"]:
    st.warning("⚠️ Você precisa estar logado para acessar as tarefas. Vá até a página principal (Dashboard) para entrar ou cadastrar-se.")
else:
    # Buscar disciplinas reais do Xano para vincular às tarefas
    disciplinas = utils.xano_get("subjects", "subject/list")
    
    # Inicializa tarefas locais na sessão se não existirem
    if "tarefas_locais" not in st.session_state:
        st.session_state["tarefas_locais"] = [
            {"id": 1, "titulo": "Estudar Streamlit e No-Code", "disciplina": "Geral", "prazo": "2026-05-30", "concluida": False},
            {"id": 2, "titulo": "Revisar metadados do XanoScript", "disciplina": "Geral", "prazo": "2026-05-28", "concluida": True}
        ]

    tab_lista, tab_nova = st.tabs(["📋 Minhas Tarefas", "➕ Nova Tarefa"])

    with tab_nova:
        st.subheader("Criar Nova Tarefa")
        
        if not disciplinas:
            st.info("💡 Dica: Cadastre uma Disciplina primeiro na página 'Disciplinas' para poder vinculá-la a uma tarefa!")
            lista_materias = ["Geral"]
        else:
            lista_materias = [d.get("name") for d in disciplinas]
            lista_materias.append("Geral")
            
        with st.form("form_tarefa"):
            titulo = st.text_input("Título da Tarefa", placeholder="Ex: Resolver lista de exercícios")
            materia = st.selectbox("Vincular à Disciplina", lista_materias)
            prazo = st.date_input("Data de Entrega")
            
            submitted = st.form_submit_button("Criar")
            if submitted:
                if titulo:
                    with st.spinner("Criando tarefa..."):
                        nova_t = {
                            "id": len(st.session_state["tarefas_locais"]) + 1,
                            "titulo": titulo,
                            "disciplina": materia,
                            "prazo": str(prazo),
                            "concluida": False
                        }
                        st.session_state["tarefas_locais"].append(nova_t)
                        st.success(f"Tarefa '{titulo}' criada com sucesso!")
                        st.rerun()
                else:
                    st.warning("Por favor, dê um título para a sua tarefa.")

    with tab_lista:
        st.subheader("Lista de Atividades")
        
        # Filtros na UI
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("Buscar tarefa...", placeholder="Digite para filtrar...")
        with col2:
            filtro = st.selectbox("Status", ["Todas", "Pendente", "Concluída"])
            
        st.markdown("---")
        
        # Filtragem das tarefas
        tarefas_filtradas = st.session_state["tarefas_locais"]
        if search:
            tarefas_filtradas = [t for t in tarefas_filtradas if search.lower() in t["titulo"].lower()]
        if filtro == "Pendente":
            tarefas_filtradas = [t for t in tarefas_filtradas if not t["concluida"]]
        elif filtro == "Concluída":
            tarefas_filtradas = [t for t in tarefas_filtradas if t["concluida"]]

        # Renderização dinâmica das tarefas em cards
        if tarefas_filtradas:
            for idx, tarefa in enumerate(tarefas_filtradas):
                card_title = f"{'✅' if tarefa['concluida'] else '⏳'} {tarefa['titulo']}"
                with st.expander(card_title, expanded=not tarefa['concluida']):
                    st.write(f"**📚 Disciplina Vinculada:** {tarefa['disciplina']}")
                    st.write(f"**📅 Prazo de Entrega:** {tarefa['prazo']}")
                    
                    # Identificar o índice real no session_state para atualizar status
                    real_idx = next(i for i, t in enumerate(st.session_state["tarefas_locais"]) if t["id"] == tarefa["id"])
                    
                    col_status, col_del = st.columns([2, 1])
                    with col_status:
                        # Checkbox para marcar status de conclusão
                        marcado = st.checkbox("Marcar como Concluída", value=tarefa["concluida"], key=f"check_{tarefa['id']}")
                        if marcado != tarefa["concluida"]:
                            st.session_state["tarefas_locais"][real_idx]["concluida"] = marcado
                            st.rerun()
                    with col_del:
                        if st.button("🗑️ Excluir Tarefa", key=f"del_{tarefa['id']}"):
                            with st.spinner("Excluindo tarefa..."):
                                st.session_state["tarefas_locais"].pop(real_idx)
                                st.success("Tarefa excluída!")
                                st.rerun()
        else:
            st.info("Nenhuma tarefa encontrada com os filtros selecionados.")