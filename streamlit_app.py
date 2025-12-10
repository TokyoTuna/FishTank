import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 기본 설정
st.set_page_config(
    page_title="시프트업(Shift Up) 기업 분석",
    page_icon="🎮",
    layout="wide"
)

# --------------------
# 1. 헤더 섹션
# --------------------
st.title("🎮 시프트업(Shift Up) 기업 분석 대시보드")
st.markdown("""
> 이 대시보드는 **시프트업**의 상장 후 성과, 주요 IP 포트폴리오, 그리고 향후 전망을 분석한 내용을 바탕으로 구성되었습니다.
> *(데이터 출처: Perplexity Search 기반 재구성)*
""")

st.divider()

# --------------------
# 2. 핵심 지표 (Key Metrics) - 예시 데이터
# --------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="주요 대표작", value="승리의 여신: 니케", delta="Global Hit")
with col2:
    st.metric(label="신작 모멘텀", value="스텔라 블레이드", delta="Console AAA")
with col3:
    st.metric(label="기업 가치(IPO 기준)", value="약 3.5조원", delta="Market Cap")

st.divider()

# --------------------
# 3. 주요 게임 포트폴리오 분석
# --------------------
st.subheader("📊 주요 IP 포트폴리오 분석")

tab1, tab2 = st.tabs(["승리의 여신: 니케 (Nikke)", "스텔라 블레이드 (Stellar Blade)"])

with tab1:
    st.markdown("""
    ### 🔫 승리의 여신: 니케
    * **장르**: 서브컬처 건슈팅 RPG
    * **성과**: 글로벌 모바일 매출 최상위권 기록 (한국, 일본, 북미 등)
    * **특징**: 텐센트(Level Infinite) 퍼블리싱을 통한 글로벌 확장 성공, 장기 흥행 궤도 진입.
    * **매출 비중**: 현재 시프트업 매출의 가장 큰 비중을 차지하는 캐시카우.
    """)

with tab2:
    st.markdown("""
    ### 🗡️ 스텔라 블레이드
    * **장르**: 콘솔 액션 어드벤처 (PS5 독점)
    * **성과**: 소니(SIE)의 세컨드 파티 파트너십을 통한 글로벌 마케팅, 평단과 유저의 높은 평가.
    * **의의**: 모바일에 편중된 국내 게임사 한계를 넘어 **콘솔 시장(AAA급)**에서의 개발력 입증.
    """)

# --------------------
# 4. SWOT 분석 (카드 형태)
# --------------------
st.divider()
st.subheader("🔍 SWOT 분석")

swot_col1, swot_col2 = st.columns(2)

with swot_col1:
    st.info("**Strengths (강점)**")
    st.markdown("""
    - **검증된 개발력**: 김형태 대표 특유의 아트 스타일과 기술력.
    - **포트폴리오 다각화**: 모바일(니케)과 콘솔(스텔라 블레이드)의 균형.
    - **높은 이익률**: 고정비 비중이 낮은 효율적인 인력 구조.
    """)
    
    st.warning("**Weaknesses (약점)**")
    st.markdown("""
    - **특정 IP 의존도**: '니케'에 대한 매출 의존도가 여전히 높음.
    - **퍼블리셔 의존**: 텐센트, 소니 등 대형 퍼블리셔와의 계약에 따른 수수료 이슈.
    """)

with swot_col2:
    st.success("**Opportunities (기회)**")
    st.markdown("""
    - **차기작 기대감**: '프로젝트 위치스(Project Witches)' 등 신규 IP 개발.
    - **플랫폼 확장**: 스텔라 블레이드의 PC 버전 출시 가능성.
    - **서브컬처 팬덤 확대**: 글로벌 서브컬처 시장의 지속적 성장.
    """)
    
    st.error("**Threats (위협)**")
    st.markdown("""
    - **경쟁 심화**: 서브컬처 장르(호요버스 등) 및 콘솔 시장의 치열한 경쟁.
    - **규제 리스크**: 확률형 아이템 규제 등 게임 산업 내 정책 변화.
    """)

# --------------------
# 5. 재무 및 성장성 시각화 (Mock Data)
# --------------------
st.divider()
st.subheader("📈 예상 성장 추이 (시각화 예시)")

# 가상의 데이터 생성 (실제 데이터가 있다면 교체 필요)
data = {
    'Year': ['2021', '2022', '2023', '2024(E)', '2025(E)'],
    'Revenue(억 원)': [172, 660, 1686, 2500, 3200],
    'Source': ['Destiny Child', 'Nikke Launch', 'Nikke Growth', 'Nikke + Stellar Blade', 'Global Expansion']
}
df = pd.DataFrame(data)

# 차트 그리기
fig = px.bar(
    df, 
    x='Year', 
    y='Revenue(억 원)', 
    color='Source',
    title='연도별 매출 성장 추이 (추정치)',
    text_auto=True
)
fig.update_layout(xaxis_title="연도", yaxis_title="매출 (단위: 억 원)")

st.plotly_chart(fig, use_container_width=True)

# --------------------
# 사이드바
# --------------------
with st.sidebar:
    st.header("About Shift Up")
    st.markdown("시프트업은 '데스티니 차일드'로 시작해 '니케', '스텔라 블레이드'를 연이어 성공시킨 한국의 대표 게임 개발사입니다.")
    st.link_button("분석 원문 보기 (Perplexity)", "https://www.perplexity.ai/search/sipeuteueob-gieobe-daehae-buns-qqqE72mpRuaK5fsknr.okQ")
    st.caption("Developed with Streamlit")
