import streamlit as st
import requests

st.set_page_config(page_title="AI Smart Exam Planner", layout="wide")

st.title("📘 AI Smart Exam Preparation Planner")
st.write("Plan your exam preparation smartly using AI")

# ---------------------------
# USER INPUT
# ---------------------------
st.sidebar.header("🎯 Enter Your Details")

name = st.sidebar.text_input("Your Name")
exam = st.sidebar.text_input("Exam Name (e.g., AIIMS, GATE, Boards)")

total_days = st.sidebar.number_input("Days left for exam", 1, 365, 30)

weak_subjects = st.sidebar.text_area("Weak Subjects (comma separated)")
strong_subjects = st.sidebar.text_area("Strong Subjects (comma separated)")

study_hours = st.sidebar.slider("Daily Study Hours", 1, 16, 6)

generate = st.sidebar.button("🚀 Generate Study Plan")


# ---------------------------
# OUTPUT (AI CONNECTED)
# ---------------------------
if generate:

    if not name or not exam:
        st.warning("Please enter your Name and Exam")
    else:

        payload = {
            "exam": exam,
            "weak": weak_subjects,
            "strong": strong_subjects,
            "days": total_days,
            "hours": study_hours
        }

        try:
            response = requests.post(
                "https://major-project-nhbb.onrender.com/generate-plan",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()

                st.success(f"Study Plan generated for {name} 🎯")

                st.subheader("📅 AI Study Plan")
                st.write(result["plan"])

                st.download_button(
                    "📥 Download Plan",
                    data=result["plan"],
                    file_name="study_plan.txt",
                    mime="text/plain"
                )

                st.subheader("📊 Summary")

                col1, col2, col3 = st.columns(3)

                col1.metric("Total Days", total_days)
                col2.metric("Daily Hours", study_hours)
                col3.metric("Total Study Hours", total_days * study_hours)

            else:
                st.error("Backend error occurred")

        except Exception as e:
            st.error(f"Connection failed: {e}")