
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ---------------------------------
# 1. 기본 화면 설정
# ---------------------------------
st.set_page_config(
    page_title="날씨 예측 프로그램",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ 날씨 예측 분석 프로그램")
st.write("과거 기온 데이터를 분석하고 미래의 기온을 예측해 봐요!")

st.divider()

# ---------------------------------
# 2. 데이터 불러오기
# ---------------------------------
st.subheader("📂 기온 데이터 불러오기")

try:
    df = pd.read_csv("temperature.csv", encoding="utf-8-sig")
    st.success("temperature.csv 파일을 불러왔어요!")
except FileNotFoundError:
    uploaded_file = st.file_uploader(
        "temperature.csv 파일을 업로드하세요.",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info("CSV 파일을 업로드하면 분석을 시작할 수 있어요.")
        st.stop()

    df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

# 열 이름 정리
df.columns = df.columns.str.strip().str.lower()

# 필요한 열 확인
required_columns = ["year", "month", "temperature"]

if not all(col in df.columns for col in required_columns):
    st.error(
        "CSV 파일에는 year, month, temperature 열이 필요합니다."
    )
    st.stop()

# 숫자로 변환
for col in required_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=required_columns)

# 연도, 월 범위 확인
df = df[
    (df["year"] > 0) &
    (df["month"].between(1, 12))
]

if df.empty:
    st.error("분석할 수 있는 데이터가 없습니다.")
    st.stop()

# 같은 연도와 월에 여러 자료가 있으면 평균 계산
df = (
    df.groupby(["year", "month"], as_index=False)
    ["temperature"].mean()
)

# ---------------------------------
# 3. 사용자 입력
# ---------------------------------
st.subheader("⚙️ 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "분석할 월을 선택하세요.",
        list(range(1, 13)),
        format_func=lambda x: f"{x}월"
    )

with col2:
    forecast_year = st.number_input(
        "예측하고 싶은 연도",
        min_value=1900,
        max_value=3000,
        value=int(df["year"].max()) + 1,
        step=1
    )

# 선택한 월의 데이터만 추출
month_data = df[df["month"] == selected_month].copy()
month_data = month_data.sort_values("year")

if len(month_data) < 2:
    st.error("선택한 월의 데이터가 2개 연
