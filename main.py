import stremlit as at
st.title('우권이는 고구마가 좋아!')
a=st.texe_input('이름을 입력하세요')
b=st.selectbox('좋아하는음식을선택하세요'),{'치킨','피자,','고기'}
if st.button('인사말 생성'):
  st.write('반갑습니다')
st.info(a+'님,안녕하세요')
st.warning(b+를 좋아하시는군요')
st.error ('잘부탁드려요') 
      st.balloons()
