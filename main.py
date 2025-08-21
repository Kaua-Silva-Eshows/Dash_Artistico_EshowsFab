import base64
import requests
import streamlit as st
from utils.jwt_utils import *
from utils.user import *
from utils.components import component_hide_sidebar

def initialize_session_state():
    if 'jwt_token' not in st.session_state:
        st.session_state['jwt_token'] = None
        st.session_state['loggedIn'] = False
        st.session_state['user_data'] = None
        st.session_state['page'] = 'login'

def authenticate(userName: str, userPassword: str):
    login_data = {
        "username": userName,
        "password": userPassword,
        "loginSource": 1,
    }
    
    try :
        response = requests.post('https://api.eshows.com.br/v1/Security/Login', json=login_data).json()
        if "error" in response:
            try:
                response = requests.post('https://apps.blueprojects.com.br/fb/Security/Login', json=login_data).json()
            except Exception as e:
                return None
        elif response["data"]["success"]:
            return response
        else:
            return None
    except Exception as e:
            st.error("Não foi possível acessar seu login")

def main():
    initialize_session_state()
    if st.session_state['jwt_token']:
        user_data = decode_jwt(st.session_state['jwt_token'])
        if user_data:
            st.session_state['user_data'] = user_data
            st.session_state['loggedIn'] = True
        else:
            st.session_state['jwt_token'] = None
            st.session_state['loggedIn'] = False

    if not st.session_state['loggedIn']:
        show_login_page()
        st.stop()
    else:
        st.switch_page("pages/home.py")

def show_login_page():
    col1, col2, col3 = st.columns([6,1,1])
    col1.write("## DashBoard Acompanhamento Eshows X Fabrica")

    with col2:
        st.markdown(
            """
            <div style="margin-top: 40px;">
                <img src="data:image/png;base64,{}" width="100"/>
            </div>
            """.format(base64.b64encode(open("./assets/imgs/eshows-logo.png", "rb").read()).decode()),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style="margin-top: 40px;">
                <img src="data:image/png;base64,{}" width="70"/>
            </div>
            """.format(base64.b64encode(open("./assets/imgs/logo_FB.png", "rb").read()).decode()),
            unsafe_allow_html=True
        )

    userName = st.text_input(label="", value="", placeholder="login")
    userPassword = st.text_input(label="", value="", placeholder="Senha",type="password")
    if st.button("login"):
        user_data = authenticate(userName, userPassword)
        if user_data:
            st.session_state['jwt_token'] = encode_jwt(user_data)
            st.session_state['user_data'] = user_data
            st.session_state['loggedIn'] = True
            st.switch_page("pages/home.py")
            st.experimental_rerun() #Força o carreganeto da pagina
        else:
            st.error("Email ou senha inválidos!")

if __name__ == "__main__":
    initialize_session_state()
    st.set_page_config(
    page_title="login | Acompanhamento Eshows X Fabrica",
    page_icon="./assets/imgs/eshows_fab-logo.png",
    layout="centered",
    )

    component_hide_sidebar()
    main()