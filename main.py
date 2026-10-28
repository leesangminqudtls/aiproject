import stremlit as at
st.title('우권이는 고구마가 좋아!')
a=st.texe_input('이름을 입력하세요')
b=st.selectbox('좋아하는음식을선택하세요'),{'치킨','피자,','고기'}
if st.button('인사말 생성'):
  st.write('반갑습니다')
