
import streamlit as st
import pandas as pd

st.set_page_config(page_title="음식 데이터 분석", page_icon="🍱")

st.title("🍱 음식 데이터 분석 프로그램")
st.write("CSV 파일을 이용해 음식 데이터를 분석합니다.")

# CSV 파일 불러오기
try:
    df = pd.read_csv("food.csv", encoding="utf-8-sig")
except FileNotFoundError:
    st.error("food.csv 파일이 GitHub에 있는지 확인하세요.")
    st.stop()

# 데이터 확인
required = ["food", "category", "price", "calories", "preference"]

if not all(col in df.columns for col in required):
    st.error("CSV 열 이름을 확인하세요.")
    st.stop()

# 숫자 변환
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["calories"] = pd.to_numeric(df["calories"], errors="coerce")
df["preference"] = pd.to_numeric(df["preference"], errors="coerce")

df = df.dropna(subset=required)

# 음식 종류 선택
st.subheader("🔎 음식 종류 선택")

categories = ["전체"] + sorted(df["category"].unique().tolist())
selected = st.selectbox("음식 종류", categories)

if selected == "전체":
    data = df.copy()
else:
    data = df[df["category"] == selected].copy()

# 분석 결과
st.subheader("📊 데이터 분석")

col1, col2, col3 = st.columns(3)

col1.metric("평균 가격", f"{data['price'].mean():,.0f}원")
col2.metric("평균 칼로리", f"{data['calories'].mean():,.0f} kcal")
col3.metric("평균 선호도", f"{data['preference'].mean():.1f}점")

# 가격 그래프
st.subheader("💰 음식별 가격")

price_data = data.sort_values("price", ascending=False)
st.bar_chart(price_data.set_index("food")["price"])

# 칼로리 그래프
st.subheader("🔥 음식별 칼로리")

calorie_data = data.sort_values("calories", ascending=False)
st.bar_chart(calorie_data.set_index("food")["calories"])

# 선호도 그래프
st.subheader("❤️ 음식별 선호도")

preference_data = data.sort_values("preference", ascending=False)
st.bar_chart(preference_data.set_index("food")["preference"])

# 순위 분석
st.subheader("🏆 분석 결과")

highest = data.loc[data["calories"].idxmax()]
popular = data.loc[data["preference"].idxmax()]
expensive = data.loc[data["price"].idxmax()]

st.write(f"🔥 칼로리가 가장 높은 음식: {highest['food']}")
st.write(f"❤️ 선호도가 가장 높은 음식: {popular['food']}")
st.write(f"💰 가격이 가장 높은 음식: {expensive['food']}")

# 데이터 표
st.subheader("📋 전체 데이터")
st.dataframe(data, use_container_width=True)

# 다운로드
csv_data = data.to_csv(index=False, encoding="utf-8-sig")

st.download_button(
    label="📥 분석 데이터 다운로드",
    data=csv_data,
    file_name="food_analysis.csv",
    mime="text/csv"
)

st.success("분석 완료!")
