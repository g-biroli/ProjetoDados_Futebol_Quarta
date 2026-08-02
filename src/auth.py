"""Login simples para proteger a pagina de insercao de dados.

As credenciais ficam em st.secrets (nunca no codigo-fonte), para nao vazar a
senha em um repositorio publico no GitHub. Veja o README para configurar
st.secrets localmente e no Streamlit Community Cloud.
"""

import streamlit as st

SESSION_KEY = "futquarta_authenticated"


def _get_credentials() -> tuple[str, str] | None:
    try:
        auth = st.secrets["admin"]
        return auth["username"], auth["password"]
    except (KeyError, FileNotFoundError):
        return None


def require_admin_login() -> bool:
    """Mostra um formulario de login e retorna True somente se autenticado."""
    if st.session_state.get(SESSION_KEY):
        return True

    credentials = _get_credentials()
    if credentials is None:
        st.error(
            "Credenciais de administrador nao configuradas. Defina "
            "`[admin]` (username e password) em st.secrets - veja o README."
        )
        return False

    valid_user, valid_pass = credentials

    st.subheader("Login administrativo")
    st.caption("Acesso restrito para inserir novos dados de partidas.")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Usuario")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

    if submitted:
        if username == valid_user and password == valid_pass:
            st.session_state[SESSION_KEY] = True
            st.rerun()
        else:
            st.error("Usuario ou senha invalidos.")

    return False


def logout_button() -> None:
    if st.session_state.get(SESSION_KEY) and st.sidebar.button("Sair"):
        st.session_state[SESSION_KEY] = False
        st.rerun()
