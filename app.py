import streamlit as st
import pandas as pd
layout1 = [str(i) for i in range(1, 11)]
layout2 = [f"{q}.{sub}" for q in range(11, 17) for sub in ['a', 'b']]
df1 = pd.DataFrame({
    "Q.No.": layout1,
    "Level (L1/L2/L3)": ["" for _ in layout1],
    "Total": [2 for _ in layout1],
    "Mark": [0 for _ in layout1],
})
df2 = pd.DataFrame({
    "Q.No.": layout2,
    "Level (L1/L2/L3)": ["" for _ in layout2],
    "Total": [13 for _ in layout2],
    "Mark": [0 for _ in layout2],
})
st.title("EduBloom Analyzer – Keyboard Input & Recommendations")
st.subheader("Questions 1–10")
df1 = st.data_editor(df1, key="q1", num_rows="fixed")
st.subheader("Questions 11.a–16.b")
df2 = st.data_editor(df2, key="q2", num_rows="fixed")
full = pd.concat([df1, df2], ignore_index=True)
valid = full[full["Level (L1/L2/L3)"].isin(["L1", "L2", "L3"])]

if not valid.empty:
    agg = valid.groupby("Level (L1/L2/L3)")["Mark"].sum()
    st.subheader("📊 Total Marks by Level")
    st.bar_chart(agg)
    attendance = valid.groupby("Level (L1/L2/L3)")["Mark"].apply(lambda x: (x > 0).sum())
    st.write("Number of Questions Attempted (by Level):")
    st.dataframe(attendance)
    st.subheader("💡 Recommendations")
    issues = []
    if 'L1' not in agg or agg.get('L1', 0) == 0:
        issues.append("No L1 (Remember) marks entered. Encourage basic recall question attempts.")
    if 'L2' not in agg or agg.get('L2', 0) == 0:
        issues.append("No L2 (Understand) marks entered. Add more concept-based questions.")
    if 'L3' not in agg or agg.get('L3', 0) == 0:
        issues.append("No L3 (Apply) marks entered. Focus on application-oriented learning.")
    if not issues and agg.sum() > 0:
        st.success("Great! Marks are distributed across all cognitive levels (L1, L2, L3). Keep a good balance.")
    else:
        for msg in issues:
            st.warning(msg)
    if (attendance < 2).any():
        st.info("Some levels have very few attempts. Motivate students to try every level.")

else:
    st.info("Fill in the cognitive levels (L1/L2/L3) and marks above to see analysis and recommendations.")
