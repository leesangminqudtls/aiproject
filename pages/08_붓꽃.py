
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# ---------------------------------
# 1. 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 붓꽃 품종 예측 프로그램")
st.write("꽃잎의 길이와 너비를 입력하면 AI가 붓꽃의 품종을 예측합니다.")

st.divider()

# ---------------------------------
# 2. 데이터 불러오기
# ---------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "Iris(1).csv"

    df = pd.read_csv(file_path, encoding="cp949")

    # 컬럼 이름의 불필요한 공백 제거
    df.columns = df.columns.str.strip()

    return df

try:
    df = load_data()

except FileNotFoundError:
    st.error("Iris(1).csv 파일을 찾을 수 없습니다.")
    st.info("app.py와 같은 폴더에 CSV 파일을 올려주세요.")
    st.stop()

# ---------------------------------
# 3. 사용할 변수 설정
# ---------------------------------
X = df[["꽃잎길이", "꽃잎 너비"]]
y = df["품종"]

# 입력 범위 자동 계산
petal_length_min = float(df["꽃잎길이"].min())
petal_length_max = float(df["꽃잎길이"].max())

petal_width_min = float(df["꽃잎 너비"].min())
petal_width_max = float(df["꽃잎 너비"].max())

# ---------------------------------
# 4. KNN 알고리즘 학습
# ---------------------------------
model = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=5))
])

model.fit(X, y)

# ---------------------------------
# 5. 사용자 입력 화면
# ---------------------------------
st.subheader("✏️ 꽃잎 크기 입력하기")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"꽃잎길이 입력 범위: "
        f"{petal_length_min} ~ {petal_length_max} cm"
    )

    petal_length = st.number_input(
        "꽃잎길이 (cm)",
        min_value=petal_length_min,
        max_value=petal_length_max,
        value=1.5,
        step=0.1
    )

with col2:
    st.info(
        f"꽃잎 너비 입력 범위: "
        f"{petal_width_min} ~ {petal_width_max} cm"
    )

    petal_width = st.number_input(
        "꽃잎 너비 (cm)",
        min_value=petal_width_min,
        max_value=petal_width_max,
        value=0.3,
        step=0.1
    )

# ---------------------------------
# 6. 품종 예측
# ---------------------------------
if st.button("🔍 붓꽃 품종 예측하기", type="primary"):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎길이", "꽃잎 너비"]
    )

    prediction = model.predict(input_data)[0]

    st.divider()

    st.subheader("🎉 예측 결과")

    if prediction == "Iris-setosa":
        st.success("예측 품종: Iris-setosa (세토사) 🌼")

    elif prediction == "Iris-versicolor":
        st.success("예측 품종: Iris-versicolor (버시컬러) 🌷")

    elif prediction == "Iris-virginica":
        st.success("예측 품종: Iris-virginica (버지니카) 🌺")

    else:
        st.success(f"예측 품종: {prediction}")

    # ---------------------------------
    # 7. 산점도 그리기
    # ---------------------------------
    st.subheader("📊 꽃잎 크기 분포 그래프")

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {
        "Iris-setosa": "blue",
        "Iris-versicolor": "green",
        "Iris-virginica": "red"
    }

    # 품종별 산점도
    for species in df["품종"].unique():

        species_data = df[df["품종"] == species]

        ax.scatter(
            species_data["꽃잎길이"],
            species_data["꽃잎 너비"],
            color=colors.get(species, "gray"),
            label=species,
            alpha=0.65,
            s=55
        )

    # 사용자가 입력한 위치: 노란색 별
    ax.scatter(
        petal_length,
        petal_width,
        color="yellow",
        edgecolors="black",
        marker="*",
        s=450,
        label="Your Input",
        zorder=10
    )

    ax.set_xlabel("Petal Length (cm)", fontsize=12)
    ax.set_ylabel("Petal Width (cm)", fontsize=12)

    ax.set_title(
        "Iris Flower Classification",
        fontsize=16
    )

    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    st.markdown(
        "⭐ **노란색 별**이 사용자가 입력한 꽃잎의 위치입니다."
    )

    st.write(
        f"입력한 꽃잎길이: {petal_length} cm"
    )

    st.write(
        f"입력한 꽃잎 너비: {petal_width} cm"
    )

# ---------------------------------
# 8. 알고리즘 설명
# ---------------------------------
st.divider()

st.subheader("🤖 KNN 알고리즘 알아보기")

st.write("""
**KNN(K-Nearest Neighbors)은 최근접 이웃 알고리즘입니다.**

1. 새로운 붓꽃 데이터가 입력됩니다.
2. 기존 붓꽃 데이터 중 입력값과 가까운 데이터를 찾습니다.
3. 가장 가까운 5개의 데이터를 확인합니다.
4. 가장 많이 등장한 품종을 새로운 데이터의 품종으로 예측합니다.

이번 프로그램에서는 꽃잎길이와 꽃잎 너비를 이용합니다.
또한 두 변수의 단위와 크기 차이를 고려하기 위해
StandardScaler로 표준화한 후 KNN을 적용합니다.
""")

st.caption("분석 데이터: Iris(1).csv | 분류 알고리즘: KNN")
