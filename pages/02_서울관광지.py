
import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 관광명소 TOP 10",
    page_icon="🇰🇷",
    layout="wide"
)

# 제목
st.title("🇰🇷 외국인이 좋아하는 서울 관광명소 TOP 10")
st.write("서울의 인기 관광지를 지도에서 찾아보세요! ✈️")

# 관광지 데이터
places = [
    {
        "rank": 1,
        "name": "경복궁",
        "emoji": "🏯",
        "lat": 37.5796,
        "lon": 126.9770,
        "description": "조선 시대의 대표 궁궐이에요. 한복을 입고 전통 건축과 사진을 즐겨 보세요."
    },
    {
        "rank": 2,
        "name": "N서울타워",
        "emoji": "🗼",
        "lat": 37.5512,
        "lon": 126.9882,
        "description": "남산에 있는 전망 명소예요. 서울의 아름다운 야경을 감상할 수 있어요."
    },
    {
        "rank": 3,
        "name": "북촌한옥마을",
        "emoji": "🏘️",
        "lat": 37.5826,
        "lon": 126.9830,
        "description": "한국 전통 한옥이 모여 있는 마을이에요. 조용한 주거 지역이므로 방문 예절을 지켜 주세요."
    },
    {
        "rank": 4,
        "name": "명동",
        "emoji": "🛍️",
        "lat": 37.5636,
        "lon": 126.9850,
        "description": "화장품과 패션 쇼핑, 맛있는 길거리 음식을 즐길 수 있어요."
    },
    {
        "rank": 5,
        "name": "홍대거리",
        "emoji": "🎸",
        "lat": 37.5563,
        "lon": 126.9236,
        "description": "버스킹 공연과 개성 있는 카페, 상점이 가득한 젊음의 거리예요."
    },
    {
        "rank": 6,
        "name": "인사동",
        "emoji": "🎨",
        "lat": 37.5742,
        "lon": 126.9850,
        "description": "전통 공예품과 기념품, 한국 문화를 경험할 수 있는 거리예요."
    },
    {
        "rank": 7,
        "name": "창덕궁",
        "emoji": "🌳",
        "lat": 37.5794,
        "lon": 126.9910,
        "description": "유네스코 세계유산으로 지정된 아름다운 궁궐이에요."
    },
    {
        "rank": 8,
        "name": "청계천",
        "emoji": "🌊",
        "lat": 37.5692,
        "lon": 126.9785,
        "description": "서울 도심에서 산책과 휴식을 즐길 수 있는 아름다운 하천이에요."
    },
    {
        "rank": 9,
        "name": "동대문디자인플라자",
        "emoji": "🏢",
        "lat": 37.5671,
        "lon": 127.0095,
        "description": "독특한 건축물과 전시, 디자인 행사를 즐길 수 있는 공간이에요."
    },
    {
        "rank": 10,
        "name": "롯데월드타워",
        "emoji": "🌆",
        "lat": 37.5125,
        "lon": 127.1025,
        "description": "서울의 전망과 한강 풍경을 감상할 수 있는 높은 랜드마크예요."
    }
]

# 서울 지도 만들기
st.subheader("📍 서울 관광명소 지도")

m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# 지도에 관광지 표시
for place in places:

    popup_html = f"""
    <h3>{place['rank']}위 {place['emoji']} {place['name']}</h3>
    <p>{place['description']}</p>
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{place['rank']}위 {place['name']}",
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background-color:#e63946;
                color:white;
                border-radius:50%;
                width:32px;
                height:32px;
                text-align:center;
                line-height:32px;
                font-weight:bold;
                border:2px solid white;
                box-shadow:0 2px 5px #777;
            ">
                {place['rank']}
            </div>
            """,
            icon_size=(32, 32),
            icon_anchor=(16, 16)
        )
    ).add_to(m)

# 지도 화면 출력
st_folium(
    m,
    width=None,
    height=570,
    use_container_width=True
)

# 지도 아래 관광지 설명
st.divider()

st.subheader("✨ 서울 관광명소 TOP 10 설명")

for i in range(0, 10, 2):

    col1, col2 = st.columns(2)

    for col, place in zip(
        [col1, col2],
        places[i:i+2]
    ):

        with col:
            with st.container(border=True):

                st.markdown(
                    f"### {place['rank']}위 {place['emoji']} {place['name']}"
                )

                st.write(place["description"])

                st.caption(
                    f"위도: {place['lat']} / 경도: {place['lon']}"
                )

st.divider()

st.success("🎉 서울의 멋진 관광지를 즐겁게 여행해 보세요!")

st.caption(
    "※ 대표적인 인기 관광지를 바탕으로 구성한 추천 목록이며 "
    "공식 방문객 통계 순위는 아닙니다."
)
