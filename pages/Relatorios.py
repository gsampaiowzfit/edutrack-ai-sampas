# pyrefly: ignore [missing-import]
import streamlit as st
import utils
import datetime
import pandas as pd
import altair as alt

try:
    st.set_page_config(page_title="Relatórios", page_icon="📊")
except Exception:
    pass

st.markdown('<div class="brand-title" style="text-align: left;">📊 Relatórios Acadêmicos</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle" style="text-align: left;">Analise sua evolução e exporte suas informações acadêmicas.</div>', unsafe_allow_html=True)

# Injeção de estilo para expandir a largura da página de relatórios especificamente
st.markdown(
    """
    <style>
    [data-testid="stAppViewBlockContainer"] {
        max-width: 90% !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

utils.load_session()

if "auth_token" not in st.session_state or not st.session_state["auth_token"]:
    st.warning("⚠️ Você precisa estar logado para acessar os relatórios. Vá até a página principal (Dashboard) para entrar ou cadastrar-se.")
else:
    with st.spinner("Compilando relatórios e estatísticas..."):
        # Buscar dados frescos das APIs do Xano
        disciplinas = utils.xano_get("subjects", "subject/list") or []
        tarefas = utils.xano_get("academic_tasks", "academic_task/list") or []

    # Filtrar disciplinas ativas e deletadas
    disciplinas_ativas = [d for d in disciplinas if d.get("status") != "archived" and not d.get("deleted")]
    
    if not disciplinas_ativas:
        st.info("Nenhuma disciplina ativa encontrada. Comece cadastrando algumas disciplinas para gerar relatórios!")
    else:
        # Seção 1: Progresso por Disciplina
        st.subheader("📈 Progresso de Conclusão por Disciplina")
        st.write("Acompanhe o percentual de tarefas concluídas em cada uma de suas disciplinas ativas:")
        st.write("")

        for disp in disciplinas_ativas:
            # Filtrar tarefas vinculadas a esta disciplina
            tarefas_disp = [t for t in tarefas if t.get("subject_id") == disp.get("id")]
            total_t = len(tarefas_disp)
            concluidas_t = sum(1 for t in tarefas_disp if t.get("status") == "completed")
            progresso = (concluidas_t / total_t) if total_t > 0 else 0.0
            
            # Formatação de exibição do card de progresso
            col_d1, col_d2 = st.columns([4, 1])
            with col_d1:
                st.markdown(f"**📚 {disp.get('name')}**")
                st.progress(progresso)
            with col_d2:
                st.markdown(f"<div style='margin-top: 15px; font-weight: bold;'>{concluidas_t}/{total_t} ({progresso*100:.1f}%)</div>", unsafe_allow_html=True)
            st.write("")

        st.markdown("---")

        # Seção 2: Análise e Histórico de Tarefas
        st.subheader("📋 Resumo do Histórico de Tarefas")
        
        # Estatísticas Rápidas de Status das Tarefas
        status_counts = {"Pendente": 0, "Em andamento": 0, "Concluída": 0}
        priority_counts = {"Baixa": 0, "Média": 0, "Alta": 0}
        
        prio_map_inverse = {"low": "Baixa", "medium": "Média", "high": "Alta"}
        status_map_inverse = {"pending": "Pendente", "in_progress": "Em andamento", "completed": "Concluída"}
        
        hoje = datetime.date.today()
        atrasadas = 0
        
        for t in tarefas:
            status_label = status_map_inverse.get(t.get("status", "pending"), "Pendente")
            status_counts[status_label] += 1
            
            prio_label = prio_map_inverse.get(t.get("priority", "medium"), "Média")
            priority_counts[prio_label] += 1
            
            if t.get("status") != "completed":
                try:
                    due_date_str = t.get("due_date")[:10]
                    due_date_obj = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    if due_date_obj < hoje:
                        atrasadas += 1
                except Exception:
                    pass

        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.markdown("**Distribuição por Status**")
            df_status = pd.DataFrame(list(status_counts.items()), columns=["Status", "Quantidade"])
            
            # Gráfico do Altair para garantir rótulos horizontais (labelAngle=0) e design polido
            chart_status = alt.Chart(df_status).mark_bar(
                color="#6c5ce7", 
                cornerRadiusEnd=4
            ).encode(
                x=alt.X("Status:N", axis=alt.Axis(labelAngle=0, title=None, labelFontSize=11)),
                y=alt.Y("Quantidade:Q", axis=alt.Axis(tickMinStep=1, title="Quantidade", labelFontSize=11)),
                tooltip=["Status", "Quantidade"]
            ).properties(
                height=300
            )
            st.altair_chart(chart_status, use_container_width=True)
            
        with col_stat2:
            st.markdown("**Distribuição por Prioridade**")
            df_priority = pd.DataFrame(list(priority_counts.items()), columns=["Prioridade", "Quantidade"])
            
            # Ordenando as barras e definindo rótulos horizontais (labelAngle=0)
            priority_order = ["Baixa", "Média", "Alta"]
            chart_priority = alt.Chart(df_priority).mark_bar(
                color="#a29bfe", 
                cornerRadiusEnd=4
            ).encode(
                x=alt.X("Prioridade:N", sort=priority_order, axis=alt.Axis(labelAngle=0, title=None, labelFontSize=11)),
                y=alt.Y("Quantidade:Q", axis=alt.Axis(tickMinStep=1, title="Quantidade", labelFontSize=11)),
                tooltip=["Prioridade", "Quantidade"]
            ).properties(
                height=300
            )
            st.altair_chart(chart_priority, use_container_width=True)

        st.markdown("---")

        # Seção 3: Histórico de Tarefas por Prazo
        st.subheader("📅 Histórico de Tarefas por Prazo")
        st.write("Acompanhe o volume de tarefas distribuído pelos meses de entrega, detalhado por status:")
        
        # Agrupar tarefas por mês/ano de vencimento e status
        mapa_meses = {
            "01": "Jan", "02": "Fev", "03": "Mar", "04": "Abr",
            "05": "Mai", "06": "Jun", "07": "Jul", "08": "Ago",
            "09": "Set", "10": "Out", "11": "Nov", "12": "Dez"
        }
        
        hist_data = {}
        for t in tarefas:
            try:
                due_date_str = t.get("due_date")[:10]
                due_date_obj = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                year_month = due_date_obj.strftime("%Y-%m")
                month_label = f"{mapa_meses[due_date_obj.strftime('%m')]}/{due_date_obj.strftime('%y')}"
                
                is_completed = t.get("status") == "completed"
                status_label = "Concluída" if is_completed else "Pendente"
                
                key = (year_month, month_label, status_label)
                hist_data[key] = hist_data.get(key, 0) + 1
            except Exception:
                pass
                
        if hist_data:
            records = []
            for (ym, label, status_label), qtd in hist_data.items():
                records.append({
                    "AnoMes": ym,
                    "Período": label,
                    "Status": status_label,
                    "Quantidade": qtd
                })
            df_hist = pd.DataFrame(records)
            df_hist = df_hist.sort_values(by="AnoMes")
            
            # Gráfico de barras empilhadas do Altair mostrando tarefas Concluídas e Pendentes por mês
            chart_hist = alt.Chart(df_hist).mark_bar(cornerRadiusEnd=4).encode(
                x=alt.X("Período:N", sort=alt.SortField(field="AnoMes", order="ascending"), axis=alt.Axis(labelAngle=0, title=None, labelFontSize=11)),
                y=alt.Y("Quantidade:Q", axis=alt.Axis(tickMinStep=1, title="Tarefas", labelFontSize=11)),
                color=alt.Color("Status:N", scale=alt.Scale(domain=["Concluída", "Pendente"], range=["#10b981", "#3b82f6"]), legend=alt.Legend(title="Status")),
                tooltip=["Período", "Status", "Quantidade"]
            ).properties(
                height=350
            )
            st.altair_chart(chart_hist, use_container_width=True)
        else:
            st.info("Nenhuma tarefa com data de entrega válida encontrada para gerar histórico.")

        st.markdown("---")

        # Seção 4: Exportação de Dados em CSV
        st.subheader("📥 Exportação de Dados Acadêmicos")
        st.write("Gere e faça download dos seus dados nos formatos portáveis CSV abaixo para salvar localmente:")
        st.write("")

        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.write("📂 **Disciplinas Cadastradas**")
            if disciplinas:
                # Filtrar informações irrelevantes ou de sistema antes de exportar
                clean_disciplinas = []
                for d in disciplinas:
                    clean_disciplinas.append({
                        "ID": d.get("id"),
                        "Nome": d.get("name"),
                        "Código": d.get("code"),
                        "Semestre": d.get("semester"),
                        "Professor": d.get("teacher"),
                        "Carga Horaria (h)": d.get("workload"),
                        "Status": d.get("status")
                    })
                df_disp_csv = pd.DataFrame(clean_disciplinas)
                csv_data_disp = df_disp_csv.to_csv(index=False).encode("utf-8")
                
                st.download_button(
                    label="Download CSV de Disciplinas",
                    data=csv_data_disp,
                    file_name="edutrack_disciplinas.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.caption("Nenhum dado de disciplina disponível.")

        with col_exp2:
            st.write("📝 **Tarefas Cadastradas**")
            if tarefas:
                sub_map = {d.get("id"): d.get("name") for d in disciplinas}
                clean_tarefas = []
                for t in tarefas:
                    clean_tarefas.append({
                        "ID": t.get("id"),
                        "Título": t.get("title"),
                        "Descrição": t.get("description"),
                        "Data Prazo": t.get("due_date")[:10] if t.get("due_date") else "",
                        "Status": t.get("status"),
                        "Prioridade": t.get("priority"),
                        "Disciplina": sub_map.get(t.get("subject_id"), "Geral")
                    })
                df_tarefas_csv = pd.DataFrame(clean_tarefas)
                csv_data_tarefas = df_tarefas_csv.to_csv(index=False).encode("utf-8")
                
                st.download_button(
                    label="Download CSV de Tarefas",
                    data=csv_data_tarefas,
                    file_name="edutrack_tarefas.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.caption("Nenhum dado de tarefa disponível.")
