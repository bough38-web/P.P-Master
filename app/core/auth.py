import streamlit as st

def check_password():
    """
    Finalized Authentication with ID: admin / PW: 0303.
    """
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
        st.session_state.username = None

    if st.session_state.password_correct:
        return True

    # Render landing/login card
    st.markdown('<div class="landing-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="landing-card">', unsafe_allow_html=True)
    st.markdown("## 🛡️ Data Intel PRO")
    st.markdown("관리자 전용 시스템입니다.")
    
    st.write("") 
    
    user_id = st.text_input("ID", value="admin", placeholder="admin")
    password = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    
    st.write("")
    
    if st.button("시스템 접속", use_container_width=True):
        # Admin ID: admin / PW: 0303 check
        if user_id == "admin" and password == "0303":
            st.session_state.password_correct = True
            st.session_state.username = user_id
            st.success("✅ 인증 성공! 시스템에 진입합니다.")
            st.rerun()
        else:
            st.error("❌ 아이디 또는 비밀번호가 일치하지 않습니다.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    return False

def logout():
    """
    Logs out the user and clears session data.
    """
    st.session_state.password_correct = False
    st.session_state.username = None
    st.rerun()
