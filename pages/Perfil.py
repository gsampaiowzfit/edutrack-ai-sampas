# pyrefly: ignore [missing-import]
import streamlit as st
import utils

st.set_page_config(page_title="Meu Perfil", page_icon="👤")
st.title("👤 Meu Perfil")

if "profile_updated_toast" in st.session_state and st.session_state["profile_updated_toast"]:
    st.toast("Perfil atualizado com sucesso!", icon="✅")
    del st.session_state["profile_updated_toast"]

if "auth_token" not in st.session_state or not st.session_state["auth_token"]:
    st.warning("⚠️ Você precisa estar logado para acessar seu perfil. Vá até a página principal (Dashboard) para entrar ou cadastrar-se.")
else:
    me = utils.xano_get("auth", "auth/me_app")
    
    if me:
        tab_dados, tab_seguranca = st.tabs(["📋 Meus Dados", "🔑 Segurança e Senha"])
        
        with tab_dados:
            st.subheader("Editar Informações do Perfil")
            with st.form("form_perfil"):
                nome = st.text_input("Nome Completo", value=me.get("name", ""))
                email = st.text_input("E-mail", value=me.get("email", ""))
                
                submitted = st.form_submit_button("Salvar Alterações")
                if submitted:
                    if nome and email:
                        res = utils.xano_patch("auth", "auth/update_profile_app", {"name": nome, "email": email})
                        if res:
                            st.session_state["user_name"] = nome
                            st.session_state["profile_updated_toast"] = True
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar o perfil. Verifique se o e-mail já está em uso.")
                    else:
                        st.warning("Preencha todos os campos obrigatórios.")
                        
        with tab_seguranca:
            st.subheader("Redefinição de Senha")
            
            if "reset_token_simulado" not in st.session_state:
                st.session_state["reset_token_simulado"] = None
                
            st.write("Para redefinir sua senha, solicite um código de verificação.")
            
            if st.button("Solicitar Código de Redefinição"):
                res = utils.xano_post("auth", "auth/request_password_reset_app", {"email": me.get("email")})
                if res and "token" in res:
                    st.session_state["reset_token_simulado"] = res["token"]
                    st.success(f"Código enviado com sucesso! Para fins de teste, seu código é: **{res['token']}**")
                else:
                    st.error("Erro ao solicitar código de redefinição.")
            
            if st.session_state["reset_token_simulado"]:
                st.markdown("---")
                st.subheader("Preencha os dados recebidos")
                with st.form("form_reset_senha_perfil"):
                    codigo = st.text_input("Código de 6 dígitos recebido", type="password")
                    nova_senha = st.text_input("Nova Senha (mínimo 8 caracteres)", type="password")
                    confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
                    
                    submitted_senha = st.form_submit_button("Alterar Senha")
                    if submitted_senha:
                        if codigo and nova_senha and confirmar_senha:
                            if nova_senha == confirmar_senha:
                                if len(nova_senha) >= 8:
                                    res_reset = utils.xano_post("auth", "auth/reset_password_app", {
                                        "email": me.get("email"),
                                        "token": codigo,
                                        "password": nova_senha
                                    })
                                    if res_reset:
                                        st.success("Senha alterada com sucesso!")
                                        st.session_state["reset_token_simulado"] = None
                                        
                                        import time
                                        st.toast("Senha alterada! Encerrando sessão por segurança...", icon="🔒")
                                        with st.spinner("Encerrando sessão com segurança..."):
                                            time.sleep(1.5)
                                            
                                        st.session_state["auth_token"] = None
                                        st.session_state["user_name"] = None
                                        st.rerun()
                                    else:
                                        st.error("Código de verificação incorreto ou expirado.")
                                else:
                                    st.warning("A senha deve ter no mínimo 8 caracteres.")
                            else:
                                st.warning("As senhas não coincidem.")
                        else:
                            st.warning("Preencha todos os campos.")
    else:
        st.error("Erro ao obter dados do perfil do backend.")
