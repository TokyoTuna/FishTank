import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 제목
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="2025 게임사 실적 분석 대시보드",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 2025 주요 한국 게임사 실적 및 마진 분석")
st.markdown("""
이 대시보드는 **시프트업**을 중심으로 **크래프톤, 넥슨, NC소프트, 넷마블, 펄어비스** 등 
주요 한국 게임사의 2024년 및 2025년 3분기까지의 재무 성과(매출, 영업이익, 마진율)를 비교 분석합니다.
(Plotly 미사용 버전)
""")

# -----------------------------------------------------------------------------
# 2. 데이터 준비
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # 2025년 분기별 데이터 (단위: 억원, %)
    quarterly_data = [
        # 시프트업
        {'Company': 'Shift Up', 'Quarter': '1Q25', 'Revenue': 422, 'OP': 262, 'OPM': 62.1, 'EBITDA_Margin': 63.7},
        {'Company': 'Shift Up', 'Quarter': '2Q25', 'Revenue': 1124, 'OP': 682, 'OPM': 60.7, 'EBITDA_Margin': 62.1},
        {'Company': 'Shift Up', 'Quarter': '3Q25', 'Revenue': 755, 'OP': 495, 'OPM': 65.6, 'EBITDA_Margin': 67.4},
        # 크래프톤
        {'Company': 'Krafton', 'Quarter': '1Q25', 'Revenue': 7630, 'OP': 3444, 'OPM': 45.1, 'EBITDA_Margin': 47.9},
        {'Company': 'Krafton', 'Quarter': '2Q25', 'Revenue': 6733, 'OP': 2460, 'OPM': 36.5, 'EBITDA_Margin': 41.0},
        {'Company': 'Krafton', 'Quarter': '3Q25', 'Revenue': 8706, 'OP': 3486, 'OPM': 40.0, 'EBITDA_Margin': 44.2},
        # 넥슨 (엔화 -> 원화 환산 대략치)
        {'Company': 'Nexon', 'Quarter': '1Q25', 'Revenue': 1270, 'OP': 408, 'OPM': 32.1, 'EBITDA_Margin': None},
        {'Company': 'Nexon', 'Quarter': '2Q25', 'Revenue': 1150, 'OP': 424, 'OPM': 36.9, 'EBITDA_Margin': None},
        {'Company': 'Nexon', 'Quarter': '3Q25', 'Revenue': 1115, 'OP': 352, 'OPM': 31.6, 'EBITDA_Margin': None},
        # 넷마블
        {'Company': 'Netmarble', 'Quarter': '1Q25', 'Revenue': 6480, 'OP': 654, 'OPM': 10.1, 'EBITDA_Margin': 15.9},
        {'Company': 'Netmarble', 'Quarter': '2Q25', 'Revenue': 7174, 'OP': 1010, 'OPM': 14.1, 'EBITDA_Margin': 18.3},
        {'Company': 'Netmarble', 'Quarter': '3Q25', 'Revenue': 6960, 'OP': 909, 'OPM': 13.1, 'EBITDA_Margin': 17.6},
        # 펄어비스
        {'Company': 'Pearl Abyss', 'Quarter': '1Q25', 'Revenue': 897, 'OP': -24, 'OPM': -2.7, 'EBITDA_Margin': None},
        {'Company': 'Pearl Abyss', 'Quarter': '2Q25', 'Revenue': 796, 'OP': -116, 'OPM': -14.6, 'EBITDA_Margin': None},
        {'Company': 'Pearl Abyss', 'Quarter': '3Q25', 'Revenue': 1068, 'OP': 106, 'OPM': 9.9, 'EBITDA_Margin': None},
        # NC소프트
        {'Company': 'NCSoft', 'Quarter': '1Q25', 'Revenue': 3603, 'OP': 52, 'OPM': 1.4, 'EBITDA_Margin': None},
        {'Company': 'NCSoft', 'Quarter': '2Q25', 'Revenue': 3824, 'OP': 151, 'OPM': 3.9, 'EBITDA_Margin': None},
        {'Company': 'NCSoft', 'Quarter': '3Q25', 'Revenue': 3600, 'OP': -75, 'OPM': -2.1, 'EBITDA_Margin': None},
    ]
    
    # 2024년 연간 데이터 (단위: %)
    annual_2024_data = [
        {'Company': 'Shift Up', 'Metric': 'OP Margin', 'Value': 68.3},
        {'Company': 'Shift Up', 'Metric': 'EBITDA Margin', 'Value': 70.1},
        {'Company': 'Krafton', 'Metric': 'OP Margin', 'Value': 43.5},
        {'Company': 'Krafton', 'Metric': 'EBITDA Margin', 'Value': 46.0},
        {'Company': 'Nexon', 'Metric': 'OP Margin', 'Value': 27.8},
        {'Company': 'Nexon', 'Metric': 'EBITDA Margin', 'Value': 38.0},
        {'Company': 'Netmarble', 'Metric': 'OP Margin', 'Value': 8.1},
        {'Company': 'Netmarble', 'Metric': 'EBITDA Margin', 'Value': 13.9},
        {'Company': 'NCSoft', 'Metric': 'OP Margin', 'Value': -6.9},
        {'Company': 'NCSoft', 'Metric': 'EBITDA Margin', 'Value': 9.2},
        {'Company': 'Pearl Abyss', 'Metric': 'OP Margin', 'Value': -3.5},
        {'Company': 'Pearl Abyss', 'Metric': 'EBITDA Margin', 'Value': 4.9},
    ]

    return pd.DataFrame(quarterly_data), pd.DataFrame(annual_2024_data)

df_quarter, df_annual = load_data()

# -----------------------------------------------------------------------------
# 3. 사이드바 옵션
# -----------------------------------------------------------------------------
st.sidebar.header("설정 및 필터")
selected_companies = st.sidebar.multiselect(
    "비교할 기업 선택",
    options=df_quarter['Company'].unique(),
    default=['Shift Up', 'Krafton', 'Netmarble', 'Nexon', 'Pearl Abyss', 'NCSoft']
)

# 데이터 필터링
filtered_df = df_quarter[df_quarter['Company'].isin(selected_companies)]

# -----------------------------------------------------------------------------
# 4. 메인 대시보드 구성 (Altair 활용)
# -----------------------------------------------------------------------------

tab1, tab2, tab3 = st.tabs(["📊 2025 분기별 마진 비교", "🚀 시프트업 심층 분석", "📅 2024 연간 비교"])

with tab1:
    st.subheader("2025년 1Q ~ 3Q 영업이익률(OPM) 추이")
    
    # Altair Line Chart
    chart_opm = alt.Chart(filtered_df).mark_line(point=True).encode(
        x='Quarter:N',
        y=alt.Y('OPM:Q', title='영업이익률 (%)'),
        color='Company:N',
        tooltip=['Company', 'Quarter', 'OPM']
    ).properties(height=400).interactive()
    
    st.altair_chart(chart_opm, use_container_width=True)

    col1, col2 = st.columns(2)
    
    # 3Q25 데이터만 추출
    df_3q = filtered_df[filtered_df['Quarter'] == '3Q25']

    with col1:
        st.subheader("3Q25 매출액 (억원)")
        if not df_3q.empty:
            chart_rev = alt.Chart(df_3q).mark_bar().encode(
                x=alt.X('Company:N', sort='-y'),
                y=alt.Y('Revenue:Q', title='매출 (억원)'),
                color='Company:N',
                tooltip=['Company', 'Revenue']
            ).properties(height=300)
            st.altair_chart(chart_rev, use_container_width=True)
        else:
            st.write("데이터 없음")

    with col2:
        st.subheader("3Q25 영업이익 (억원)")
        if not df_3q.empty:
            chart_op = alt.Chart(df_3q).mark_bar().encode(
                x=alt.X('Company:N', sort='-y'),
                y=alt.Y('OP:Q', title='영업이익 (억원)'),
                color='Company:N',
                tooltip=['Company', 'OP']
            ).properties(height=300)
            st.altair_chart(chart_op, use_container_width=True)
        else:
            st.write("데이터 없음")
            
    st.subheader("EBITDA 마진 비교 (데이터 가용 기업)")
    df_ebitda = filtered_df.dropna(subset=['EBITDA_Margin'])
    
    if not df_ebitda.empty:
        chart_ebitda = alt.Chart(df_ebitda).mark_bar().encode(
            x=alt.X('Quarter:N', title=None),
            y=alt.Y('EBITDA_Margin:Q', title='EBITDA 마진 (%)'),
            color='Company:N',
            column=alt.Column('Company:N', header=alt.Header(title=None)),
            tooltip=['Company', 'Quarter', 'EBITDA_Margin']
        ).properties(width=100)
        st.altair_chart(chart_ebitda, use_container_width=False)

with tab2:
    st.header("🚀 Shift Up: 압도적 수익성의 비밀")
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    su_data = df_quarter[df_quarter['Company'] == 'Shift Up']
    
    if not su_data.empty:
        su_3q = su_data[su_data['Quarter'] == '3Q25'].iloc[0]
        
        with col_kpi1:
            st.metric(label="3Q25 영업이익률", value=f"{su_3q['OPM']}%", delta="4.9%p (vs 2Q25)")
        with col_kpi2:
            st.metric(label="3Q25 EBITDA 마진", value=f"{su_3q['EBITDA_Margin']}%", delta="5.3%p (vs 2Q25)")
        with col_kpi3:
            st.metric(label="2024 직원수 (약)", value="322명", delta="인당 생산성 최상위")

        st.markdown("---")
        
        # 시프트업 복합 차트 (Altair)
        base = alt.Chart(su_data).encode(x='Quarter:N')
        
        bar = base.mark_bar(color='#FF9F9F').encode(
            y=alt.Y('Revenue:Q', axis=alt.Axis(title='금액 (억원)', titleColor='#FF9F9F')),
            tooltip=['Quarter', 'Revenue']
        )
        
        line = base.mark_line(color='red', point=True).encode(
            y=alt.Y('OPM:Q', axis=alt.Axis(title='영업이익률 (%)', titleColor='red')),
            tooltip=['Quarter', 'OPM']
        )
        
        combined_chart = alt.layer(bar, line).resolve_scale(y='independent').properties(
            title='시프트업 매출 및 이익률 추이'
        )
        
        st.altair_chart(combined_chart, use_container_width=True)

with tab3:
    st.subheader("2024년 연간 마진 랭킹 Comparison")
    
    # 2024년 데이터 시각화
    chart_annual = alt.Chart(df_annual).mark_bar().encode(
        x=alt.X('Company:N', sort='-y', title='기업'),
        y=alt.Y('Value:Q', title='마진 (%)'),
        color='Metric:N',
        xOffset='Metric:N', # Grouped Bar 효과
        tooltip=['Company', 'Metric', 'Value']
    ).properties(height=400)
    
    st.altair_chart(chart_annual, use_container_width=True)
    
    st.markdown("""
    *   **Tier 1 (초고수익성):** 시프트업 (약 70%)
    *   **Tier 2 (고수익성):** 크래프톤 (약 45%)
    *   **Tier 3 (안정권):** 넥슨 (약 30%)
    *   **Tier 4 (개선중/적자):** 넷마블, 펄어비스, NC소프트
    """)

# -----------------------------------------------------------------------------
# 5. Raw Data 보기
# -----------------------------------------------------------------------------
with st.expander("📂 원본 데이터 보기 (2025 분기별)"):
    st.dataframe(filtered_df.style.format({
        'Revenue': '{:,.0f} 억원',
        'OP': '{:,.0f} 억원',
        'OPM': '{:.1f}%',
        'EBITDA_Margin': '{:.1f}%'
    }))
