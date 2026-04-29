import streamlit as st
from app.core.handlers import (
    calculate_general_pp, get_upselling_approver, 
    get_downselling_approver, get_retention_approver, 
    get_inst_change_approver, get_churn_report_approver
)

def apply_example_data():
    st.session_state.calc_mode = "업셀링"
    st.session_state.eq_cost = 350000
    st.session_state.m_fee_prev = 44000
    st.session_state.m_fee_after = 55000
    st.session_state.est_cost = 50000
    st.session_state.coll_cost = 0
    st.session_state.churn_fee = 0
    st.toast("💡 시나리오 데이터가 적용되었습니다.")

def render_calculator_input():
    # Initialization
    for key in ['eq_cost', 'm_fee_prev', 'm_fee_after', 'est_cost', 'coll_cost', 'churn_fee']:
        if key not in st.session_state: st.session_state[key] = 0
    if 'calc_mode' not in st.session_state: st.session_state.calc_mode = "업셀링"

    # Top Navigation
    st.write("")
    nav_col1, nav_col2 = st.columns([4, 1])
    with nav_col1:
        modes = ["업셀링", "다운셀링", "설치변경", "리텐션", "해지보고", "일반P.P"]
        mode_cols = st.columns(6)
        for i, m in enumerate(modes):
            if mode_cols[i].button(m, key=f"btn_{m}", use_container_width=True):
                st.session_state.calc_mode = m; st.rerun()
    with nav_col2:
        if st.button("💡 시나리오 로드", use_container_width=True):
            apply_example_data(); st.rerun()

    st.write("")
    
    # Parallel Layout
    main_col_left, main_col_right = st.columns([1.1, 0.9], gap="large")
    curr_mode = st.session_state.calc_mode
    
    with main_col_left:
        st.markdown(f"#### 🛠️ {curr_mode} 상세 입력")
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if curr_mode == "해지보고":
                st.session_state.churn_fee = st.number_input("해지 월정료 합계 (원)", value=st.session_state.churn_fee, step=100000)
            elif curr_mode == "리텐션":
                ret_type = st.radio("리텐션 구분", ["할인/인하", "면제"], horizontal=True)
                val = st.slider("수치 적용", 0, 100, 30) if ret_type=="할인/인하" else st.select_slider("개월수 선택", [1,2,3,4,5], 3)
            elif curr_mode == "다운셀링":
                st.session_state.eq_cost = st.number_input("기존 장비비 (원)", value=st.session_state.eq_cost, step=100000)
                val = st.number_input("철거 장비비 (원)", value=0, step=100000)
            else:
                st.session_state.eq_cost = st.number_input("투자 장비비 (원)", value=st.session_state.eq_cost, step=10000)
                equipment_type = st.selectbox("장비 구성", ["new", "used", "mix"], format_func=lambda x: {"new":"신품 (100%)", "used":"중품 (50%)", "mix":"혼합"}[x])
                usage_period = st.radio("고객 사용기간", ["under_3yr", "over_3yr"], format_func=lambda x: "3년 미만" if x=="under_3yr" else "3년 이상", horizontal=True)
                val = 0
        with c2:
            if curr_mode != "해지보고":
                st.session_state.m_fee_prev = st.number_input("변경 전 월정료 (원)", value=st.session_state.m_fee_prev, step=1000)
                st.session_state.m_fee_after = st.number_input("변경 후 월정료 (원)", value=st.session_state.m_fee_after, step=1000)
                delta = st.session_state.m_fee_after - st.session_state.m_fee_prev
                delta_pct = (abs(delta) / st.session_state.m_fee_prev * 100) if st.session_state.m_fee_prev > 0 else 0
                st.markdown(f"<small>증감액: {delta:+,}원 ({delta_pct:.1f}%)</small>", unsafe_allow_html=True)
                contract_period = st.selectbox("약정 기간", ["0", "12", "24", "36"], format_func=lambda x: {"0":"무약정", "12":"12개월", "24":"24개월", "36":"36개월"}[x])
            else:
                st.info("💡 30만원 이상 건은 결재 필수")
                delta_pct = 0; contract_period = "0"
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("📂 추가 비용 및 실무 가이드"):
            st.session_state.est_cost = st.number_input("실투입 공사비 (원)", value=st.session_state.est_cost, step=1000)
            st.session_state.coll_cost = st.number_input("공사비 수익 (원)", value=st.session_state.coll_cost, step=1000)

    with main_col_right:
        res_inputs = {
            "mode": curr_mode, "equipment_cost": st.session_state.eq_cost,
            "equipment_type": equipment_type if curr_mode in ["업셀링", "일반P.P"] else "replace",
            "usage_period": usage_period if curr_mode == "업셀링" else "under_3yr",
            "estimate_cost": st.session_state.est_cost, "collected_cost": st.session_state.coll_cost,
            "monthly_fee": st.session_state.m_fee_after, "m_fee_prev": st.session_state.m_fee_prev,
            "contract_period": contract_period, "ret_type": ret_type if curr_mode == "리텐션" else None,
            "ret_val": val if curr_mode == "리텐션" else delta_pct, "churn_fee": st.session_state.churn_fee
        }
        render_results(res_inputs)

def render_results(inputs):
    mode = inputs["mode"]
    approver, pp_display = "-", "-"
    
    if mode == "해지보고":
        approver = get_churn_report_approver(inputs["churn_fee"])
        pp_display = f"{inputs['churn_fee']:,}원"
    elif mode == "리텐션":
        sub_type = "discount" if inputs["ret_type"] == "할인/인하" else "exemption"
        approver = get_retention_approver(sub_type, inputs["ret_val"], inputs["m_fee_prev"])
        pp_display = f"{inputs['ret_val']}%" if sub_type == "discount" else f"{inputs['ret_val']}개월"
    elif mode == "설치변경":
        pp = (inputs["estimate_cost"] - inputs["collected_cost"]) / inputs["monthly_fee"] if inputs["monthly_fee"] > 0 else 0
        approver = get_inst_change_approver(pp, inputs["contract_period"])
        pp_display = f"{pp:.2f}"
    elif mode == "다운셀링":
        approver = get_downselling_approver(inputs["ret_val"])
        pp_display = f"{inputs['ret_val']:.1f}%"
    else: # 업셀링 / 일반
        pp, _, _ = calculate_general_pp(inputs["equipment_cost"], inputs["equipment_type"], inputs["estimate_cost"], inputs["collected_cost"], inputs["monthly_fee"])
        if mode == "업셀링": approver = get_upselling_approver(pp, inputs["usage_period"], inputs["contract_period"])
        pp_display = f"{pp:.2f}" if pp else "-"

    st.markdown(f"""
    <div class="insight-header">
        <div class="approver-label">최종 보고/승인 전결권자</div>
        <div class="pp-value">{pp_display}</div>
        <div class="status-badge">✅ {approver}</div>
    </div>
    """, unsafe_allow_html=True)

def render_approval_table():
    with st.expander("📘 정책 기준표 상세 조회 (클릭 시 확장)"):
        tabs = st.tabs(["업셀링", "리텐션", "설치변경", "해지보고", "다운셀링"])
        with tabs[0]: st.markdown("**[업셀링 P.P 승인 기준]**\n| 약정 | 지사장 | 지역본부 | 본부장 | 마케팅 |\n| :--- | :---: | :---: | :---: | :---: |\n| **0** | 16 | 20 | 22 | 22↑ |\n| **12** | 26 | 31 | 34 | 34↑ |\n| **24** | 38 | 43 | 46 | 46↑ |\n| **36** | 50 | 55 | 58 | 58↑ |")
        with tabs[1]: st.markdown("**[리텐션 승인 기준]**\n- 할인 30만↑: 40%↑(마케팅), 40%↓(영업채널)\n- 할인 30만↓: 30%↑(지역본부), 30%↓(지사장)\n- 면제: 5개월(마케팅), 4개월(영업채널), 3개월(지역본부), 1~2개월(지사장)")
        with tabs[2]: st.markdown("**[설치변경 P.P 전결]**\n| 약정 | 지사장 | 지역본부 | 본부장 | 마케팅 |\n| :--- | :---: | :---: | :---: | :---: |\n| **0** | 1.0 | 1~4 | 4~6 | 6↑ |\n| **12** | 4.0 | 4~6 | 6~8 | 8↑ |\n| **24** | 8.0 | 8~12 | 12~16 | 16↑ |\n| **36** | 12.0 | 12~16 | 16~20 | 20↑ |")
        with tabs[3]: st.markdown("**[해지사유 보고]**\n| 금액 | 전결권자 |\n| :--- | :--- |\n| 1,000만↑ | CEO |\n| 500~1,000만 | 마케팅부문장 |\n| 300~500만 | 마케팅본부장 |\n| 100~300만 | 영업채널본부장 |\n| 30~100만 | 지역본부장 |")
        with tabs[4]: st.markdown("**[다운셀링]**\n- 20%↓: 지사장\n- 21~40%: 지역본부장\n- 41~60%: 영업본부장\n- 61%↑: 마케팅본부장")
