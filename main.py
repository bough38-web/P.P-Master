import streamlit as st
from app.ui.styles import apply_styles
from app.ui.components import render_calculator_input, render_approval_table
from app.core.auth import check_password, logout
from app.core.handlers import get_logs, export_logs_to_excel

def main():
    st.set_page_config(page_title="Data Intel PRO", layout="wide")
    apply_styles()

    if not check_password():
        st.stop()

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">DATA INTEL PRO</div>', unsafe_allow_html=True)
        page = st.radio("메뉴", ["계산자", "관리자 모니터링"])
        st.divider()
        st.write(f"사용자: {st.session_state.get('username', '관리자')}")
        if st.button("로그아웃"):
            logout()

    if page == "계산자":
        render_calculator_page()
    else:
        render_admin_page()

def render_calculator_page():
    # render_calculator_input internally handles the parallel layout and results
    render_calculator_input()
    st.write("")
    render_approval_table()

def render_admin_page():
    st.title("🛡️ 관리자 모니터링")
    logs = get_logs()
    if logs:
        st.dataframe(logs, use_container_width=True)
        excel_data = export_logs_to_excel(logs)
        st.download_button("📥 엑셀 데이터 내보내기", data=excel_data, file_name="system_logs.xlsx")
    else:
        st.info("기록된 로그가 없습니다.")

if __name__ == "__main__":
    main()
