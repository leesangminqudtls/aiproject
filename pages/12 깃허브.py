
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 화면 설정
st.set_page_config(
    page_title="음식 데이터 분석",
    page_icon="🍱",
    layout="wide"
)

st.title("🍱 음식 데이터 분석 프로그램")
st.write("CSV 파일을 이용해 다양한 음식 정보를 분석해 봐요!")

st.divider()

# CSV 파일 불러오기
st.subheader("📂 CSV 데이터 불러오기")

uploaded_file = st.file_uploader(
    "food.csv 파일을 업로드하세요",
    type=["csv"]
)

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("food.csv")

    st.success("음식 데이터를 불러왔습니다!")

except FileNotFoundError:
    st.error("food.csv 파일을 찾을 수 없습니다.")
    st.stop()

# 데이터 확인
required = [
    "food", "category", "price",
    "calories", "preference"
]

if not all(col in df.columns for col in required):
    st.error("CSV 파일의 열 이름을 확인해 주세요.")
    st.stop()

# 숫자 데이터 변환
for col in ["price", "calories", "preference"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=required)

if df.empty:
    st.error("분석할 데이터가 없습니다.")
    st.stop()

# 음식 종류 선택
st.subheader("🔎 음식 종류 선택")

categories = ["전체"] + sorted(
    df["category"].unique().tolist()
)

selected = st.selectbox(
    "분석할 음식 종류를 선택하세요",
    categories
)

if selected == "전체":
    data = df.copy()
else:
    data = df[df["category"] == selected].copy()

if data.empty:
    st.warning("선택한 음식 데이터가 없습니다.")
    st.stop()

# 핵심 통계
st.subheader("📊 데이터 분석 결과")

col1, col2, col3 = st.columns(3)

col1.metric(
    "평균 가격",
    f"{data['price'].mean():,.0f}원"
)

col2.metric(
    "평균 칼로리",
    f"{data['calories'].mean():,.0f} kcal"
)

col3.metric(
    "평균 선호도",
    f"{data['preference'].mean():.1f}점"
)

st.divider()

# 음식별 가격 그래프
st.subheader("💰 음식별 가격 비교")

price_data = data.sort_values(
    "price", ascending=False
)

st.bar_chart(
    price_data.set_index("food")["price"],
    color="#3498db"
)

# 음식별 칼로리 그래프
st.subheader("🔥 음식별 칼로리 비교")

calorie_data = data.sort_values(
    "calories", ascending=False
)

st.bar_chart(
    calorie_data.set_index("food")["calories"],
    color="#e67e22"
)

# 선호도 그래프
st.subheader("❤️ 음식별 선호도")

preference_data = data.sort_values(
    "preference", ascending=False
)

st.bar_chart(
    preference_data.set_index("food")["preference"],
    color="#e74c3c"
)

# 순위 분석
st.divider()
st.subheader("🏆 음식 순위 분석")

col1, col2 = st.columns(2)

with col1:
    st.write("🔥 칼로리가 가장 높은 음식")
    highest = data.loc[data["calories"].idxmax()]
    st.success(
        f"{highest['food']} : "
        f"{highest['calories']:,.0f} kcal"
    )

with col2:
    st.write("❤️ 가장 인기 있는 음식")
    popular = data.loc[data["preference"].idxmax()]
    st.success(
        f"{popular['food']} : "
        f"{popular['preference']:.0f}점"
    )

# 전체 데이터 표
st.divider()
st.subheader("📋 음식 데이터 전체 보기")

st.dataframe(data, use_container_width=True)

# CSV 다운로드
csv_data = data.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    "📥 분석 결과 CSV 다운로드",
    data=csv_data,
    file_name="food_analysis.csv",
    mime="text/csv"
)

st.success("🎉 음식 데이터 분석이 완료되었습니다!")
