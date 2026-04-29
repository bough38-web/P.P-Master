import pandas as pd
import io
import streamlit as st
import datetime

# --- Policy Data ---

UPSELLING_RULES = {
    "under_3yr": {"0": 16, "12": 26, "24": 38, "36": 50},
    "over_3yr":  {"0": 18, "12": 28, "24": 40, "36": 52}
}

INST_CHANGE_RULES = {
    "0": [1, 4, 6, 6],
    "12": [4, 6, 8, 8],
    "24": [8, 12, 16, 16],
    "36": [12, 16, 20, 20]
}

RETENTION_DISCOUNT_RULES = {
    "over_300k": {"40": "마케팅본부장", "under_40": "영업채널본부장"},
    "under_300k": {"30": "지역본부장", "under_30": "지사장"}
}

RETENTION_EXEMPT_RULES = {
    "5": "마케팅본부장",
    "4": "영업채널본부장",
    "3": "지역본부장",
    "2": "지사장"
}

CHURN_REPORT_RULES = [
    {"min": 10000000, "label": "CEO (이메일/대면 병행 필수)"},
    {"min": 5000000,  "label": "마케팅 부문장 (기업 부문장)"},
    {"min": 3000000,  "label": "마케팅 본부장"},
    {"min": 1000000,  "label": "영업채널본부장 (기업사업본부장)"},
    {"min": 300000,   "label": "지역본부장 (수도권법단/기업고객본부장)"}
]

# --- Calculation Handlers ---

def calculate_general_pp(eq_cost, eq_type, est_cost, coll_cost, m_fee):
    rates = {"new": 1.0, "used": 0.5, "replace": 0.0, "mix": 0.75}
    rate = rates.get(eq_type, 1.0)
    applied_cost = eq_cost * rate
    numerator = applied_cost + est_cost - coll_cost
    if m_fee <= 0: return None, applied_cost, numerator
    return numerator / m_fee, applied_cost, numerator

def get_upselling_approver(pp, usage_period, contract_period):
    if pp is None: return "데이터 부족"
    rules_dict = UPSELLING_RULES.get(usage_period, UPSELLING_RULES["under_3yr"])
    threshold = rules_dict.get(str(contract_period), 0)
    
    # Simple threshold logic for display (more complex mapping can be added)
    if pp <= threshold: return "지사장"
    if pp <= threshold + 5: return "지역본부장"
    if pp <= threshold + 10: return "영업/기업본부장"
    return "마케팅본부장"

def get_downselling_approver(reduction_rate):
    if reduction_rate <= 20: return "지사장"
    if reduction_rate <= 40: return "지역본부장"
    if reduction_rate <= 60: return "영업/기업본부장"
    return "마케팅본부장"

def get_retention_approver(sub_type, value, m_fee=0):
    if sub_type == "discount":
        fee_type = "over_300k" if m_fee >= 300000 else "under_300k"
        rules = RETENTION_DISCOUNT_RULES[fee_type]
        if fee_type == "over_300k":
            return rules["40"] if value >= 40 else rules["under_40"]
        else:
            return rules["30"] if value >= 30 else rules["under_30"]
    elif sub_type == "exemption":
        if value >= 5: return RETENTION_EXEMPT_RULES["5"]
        return RETENTION_EXEMPT_RULES.get(str(int(value)), "지사장")
    return "지사장"

def get_inst_change_approver(pp, contract_period):
    if pp is None: return "데이터 부족"
    thresholds = INST_CHANGE_RULES.get(str(contract_period), [0, 0, 0, 0])
    labels = ["지사장", "지역본부장", "영업/기업본부장", "마케팅본부장"]
    for i, threshold in enumerate(thresholds):
        if pp <= threshold: return labels[i]
    return "마케팅본부장"

def get_churn_report_approver(fee):
    if fee < 100000: return "보고 대상 제외"
    if 100000 <= fee < 300000: return "'해지고위험 P/L' 보고 대체"
    for rule in CHURN_REPORT_RULES:
        if fee >= rule["min"]: return rule["label"]
    return "지역본부장"

# --- Logging & Data Handlers ---

def init_logs():
    if 'system_logs' not in st.session_state:
        st.session_state.system_logs = []

def add_log(user_id, inputs):
    init_logs()
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "input": inputs,
        "result": {
            "pp": inputs.get("pp"),
            "approver": inputs.get("approver")
        }
    }
    st.session_state.system_logs.append(log_entry)

def get_logs():
    init_logs()
    return st.session_state.system_logs

def export_logs_to_excel(logs):
    if not logs: return None
    # Simplify logs for excel
    flat_logs = []
    for log in logs:
        flat_logs.append({
            "일시": log["timestamp"],
            "사용자": log["user_id"],
            "유형": log["input"].get("mode", "일반"),
            "전결권자": log["result"].get("approver", "-")
        })
    df = pd.DataFrame(flat_logs)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()
