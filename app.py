import streamlit as st
import pandas as pd
from datetime import datetime
from src.database import init_db, add_request, get_requests, update_status, delete_request
from src.classifier import classify_request, detect_priority, department_for, suggest_response
from src.reporting import build_summary

st.set_page_config(page_title="Intelligent Communication Manager", page_icon="📨", layout="wide")
init_db()

st.title("📨 Intelligent Communication Management System")
st.caption("Classify incoming requests • identify priority • route departments • track resolution")

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Add / Import Requests", "Manage Requests", "Reports"])

df = get_requests()
with tab1:
    summary = build_summary(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total requests", summary["total"])
    c2.metric("Pending", summary["pending"])
    c3.metric("High priority", summary["high"])
    c4.metric("Resolved", summary["resolved"])
    left, right = st.columns(2)
    with left:
        st.subheader("Requests by category")
        if not df.empty:
            st.bar_chart(df["category"].value_counts())
        else:
            st.info("Add requests to see category analytics.")
    with right:
        st.subheader("Requests by priority")
        if not df.empty:
            st.bar_chart(df["priority"].value_counts())
        else:
            st.info("No data available yet.")
    st.subheader("Recent requests")
    if not df.empty:
        st.dataframe(df.sort_values("created_at", ascending=False).head(10), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Register a communication request")
    with st.form("new_request", clear_on_submit=True):
        col1, col2 = st.columns(2)
        sender = col1.text_input("Sender name")
        email = col2.text_input("Email address")
        subject = st.text_input("Subject *")
        message = st.text_area("Request / email content *", height=140)
        submitted = st.form_submit_button("Analyse and save request", type="primary")
        if submitted:
            if not subject.strip() or not message.strip():
                st.error("Subject and message are required.")
            else:
                category = classify_request(subject, message)
                priority = detect_priority(subject, message)
                dept = department_for(category)
                response = suggest_response(category, sender or "there", subject)
                rid = add_request(sender, email, subject, message, category, priority, dept, response)
                st.success(f"Request #{rid} saved. Category: {category} | Priority: {priority} | Department: {dept}")
                st.info("Suggested response")
                st.write(response)

    st.divider()
    st.subheader("Import requests from CSV")
    st.write("Required columns: **subject**, **message**. Optional: sender, email.")
    uploaded = st.file_uploader("Choose CSV file", type=["csv"])
    if uploaded is not None:
        try:
            incoming = pd.read_csv(uploaded).fillna("")
            required = {"subject", "message"}
            if not required.issubset(set(incoming.columns.str.lower())):
                st.error("CSV must contain subject and message columns.")
            else:
                incoming.columns = incoming.columns.str.lower()
                if st.button("Import and classify CSV"):
                    count = 0
                    for _, row in incoming.iterrows():
                        subject, message = str(row["subject"]), str(row["message"])
                        if not subject.strip() or not message.strip():
                            continue
                        category = classify_request(subject, message)
                        priority = detect_priority(subject, message)
                        dept = department_for(category)
                        response = suggest_response(category, str(row.get("sender", "there")), subject)
                        add_request(str(row.get("sender", "")), str(row.get("email", "")),
                                    subject, message, category, priority, dept, response)
                        count += 1
                    st.success(f"Imported {count} requests successfully.")
        except Exception as e:
            st.error(f"Could not read CSV: {e}")

with tab3:
    st.subheader("Request tracker")
    df = get_requests()
    if df.empty:
        st.info("No requests have been registered yet.")
    else:
        f1, f2, f3 = st.columns(3)
        categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
        priorities = ["All", "High", "Medium", "Low"]
        statuses = ["All", "Pending", "In Progress", "Resolved"]
        cat_filter = f1.selectbox("Category", categories)
        pri_filter = f2.selectbox("Priority", priorities)
        status_filter = f3.selectbox("Status", statuses)
        view = df.copy()
        if cat_filter != "All": view = view[view.category == cat_filter]
        if pri_filter != "All": view = view[view.priority == pri_filter]
        if status_filter != "All": view = view[view.status == status_filter]
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.divider()
        ids = view["id"].tolist()
        if ids:
            selected = st.selectbox("Select request ID", ids)
            record = view[view.id == selected].iloc[0]
            st.markdown(f"**{record['subject']}**")
            st.write(record["message"])
            st.caption(f"{record['category']} • {record['priority']} priority • {record['department']}")
            st.text_area("Suggested response (editable)", value=record["suggested_response"], key=f"response_{selected}", height=110)
            new_status = st.selectbox("Update status", ["Pending", "In Progress", "Resolved"],
                                      index=["Pending", "In Progress", "Resolved"].index(record["status"]))
            a, b = st.columns(2)
            if a.button("Save status", type="primary"):
                update_status(int(selected), new_status)
                st.success("Status updated.")
                st.rerun()
            if b.button("Delete request"):
                delete_request(int(selected))
                st.warning("Request deleted.")
                st.rerun()

with tab4:
    st.subheader("Operational reports")
    df = get_requests()
    if df.empty:
        st.info("Reports will appear after requests are added.")
    else:
        summary = build_summary(df)
        st.write("**Summary**")
        st.json(summary)
        st.download_button("Download full report (CSV)", df.to_csv(index=False).encode("utf-8"),
                           "communication_requests_report.csv", "text/csv")
        category_report = df.groupby("category").size().reset_index(name="request_count")
        st.download_button("Download category report (CSV)", category_report.to_csv(index=False).encode("utf-8"),
                           "category_report.csv", "text/csv")
        priority_report = df.groupby("priority").size().reset_index(name="request_count")
        st.download_button("Download priority report (CSV)", priority_report.to_csv(index=False).encode("utf-8"),
                           "priority_report.csv", "text/csv")

st.sidebar.header("About")
st.sidebar.write("A lightweight workflow tool for institutional email and request management.")
st.sidebar.caption("Classification is rule-based and can be customised in src/classifier.py.")
