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
    
    # IP별 상세 데이터 (단위: 억원, %)
    shiftup_ip_data = [
        {'Quarter': '1Q25', 'IP': 'NIKKE', 'Revenue': 323, 'Share': 76.5},
        {'Quarter': '1Q25', 'IP': 'Stellar Blade', 'Revenue': 90, 'Share': 21.3},
        {'Quarter': '2Q25', 'IP': 'NIKKE', 'Revenue': 451, 'Share': 40.1},
        {'Quarter': '2Q25', 'IP': 'Stellar Blade', 'Revenue': 657, 'Share': 58.5},
        {'Quarter': '3Q25', 'IP': 'NIKKE', 'Revenue': 445, 'Share': 58.9},
        {'Quarter': '3Q25', 'IP': 'Stellar Blade', 'Revenue': 277, 'Share': 36.7},
    ]
    
    # [NEW] 생산성 데이터 (인당 영업이익만 포함)
    productivity_data = [
        {'Company': 'Shift Up', 'Headcount': 322, 'OP_2024': 1485, 'OP_per_Employee': 4.6, 'Dev_Ratio': 90, 'Avg_Tenure': 3.3},
        {'Company': 'Krafton', 'Headcount': 1916, 'OP_2024': 11825, 'OP_per_Employee': 6.2, 'Dev_Ratio': None, 'Avg_Tenure': 3.2},
        {'Company': 'Netmarble', 'Headcount': 749, 'OP_2024': 1581, 'OP_per_Employee': 2.1, 'Dev_Ratio': None, 'Avg_Tenure': None},
        {'Company': 'NCSoft', 'Headcount': 3269, 'OP_2024': -1092, 'OP_per_Employee': -0.33, 'Dev_Ratio': 70.8, 'Avg_Tenure': 7.8},
        {'Company': 'Pearl Abyss', 'Headcount': 724, 'OP_2024': -121, 'OP_per_Employee': -0.17, 'Dev_Ratio': 60, 'Avg_Tenure': None},
    ]

    return pd.DataFrame(quarterly_data), pd.DataFrame(annual_2024_data), pd.DataFrame(shiftup_ip_data), pd.DataFrame(productivity_data)

df_quarter, df_annual, df_shiftup_ip, df_productivity = load_data()

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
# 4. 메인 대시보드 구성
# -----------------------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(["📊 2025 분기별 마진 비교", "🚀 시프트업 심층 분석", "👥 생산성 분석", "📅 2024 연간 비교"])

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
    
    # 상단 KPI
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

    st.divider()
    
    # IP별 상세 분석 섹션
    st.subheader("💡 IP별 상세 분석: 니케(NIKKE) vs 스텔라 블레이드")
    
    col_ip_chart, col_ip_text = st.columns([1, 1])
    
    with col_ip_chart:
        # IP별 매출 기여도 Stacked Bar Chart
        chart_ip = alt.Chart(df_shiftup_ip).mark_bar().encode(
            x=alt.X('Quarter:N', title='분기'),
            y=alt.Y('Revenue:Q', title='매출 (억원)'),
            color=alt.Color('IP:N', scale=alt.Scale(domain=['NIKKE', 'Stellar Blade'], range=['#FF4B4B', '#1F77B4'])),
            tooltip=['Quarter', 'IP', 'Revenue', 'Share']
        ).properties(title='분기별 IP 매출 구성 (억원)', height=300)
        
        st.altair_chart(chart_ip, use_container_width=True)

    with col_ip_text:
        st.markdown("""
        **1. 🛡️ 승리의 여신: 니케 (Cash Cow)**
        *   **특징:** 3Q25 YoY **+29.9%** 성장하며 장기 흥행 궤도 진입.
        *   **수익 모델:** 안정적인 F2P 라이브 서비스 + 로열티 구조.
        *   **역할:** 분기별 변동성을 잡아주는 든든한 버팀목 (기여도 40~76%).
        
        **2. ⚔️ 스텔라 블레이드 (Growth Engine)**
        *   **특징:** 2Q25 **PC 출시 효과**로 분기 매출 1위(657억원) 달성.
        *   **수익 모델:** 패키지 판매 + 소니/스팀 플랫폼 로열티.
        *   **역할:** 신작 출시에 따른 폭발적인 매출 점프-업(Jump-up).
        
        **3. 📊 시너지 효과**
        *   **안정성 + 성장성:** 서로 다른 수명 주기(Lifecycle)를 가진 두 IP가 교차하며 **60%대 고마진**을 지속 견인.
        """)

    st.divider()

    # 기존 시프트업 전체 실적 차트
    st.subheader("📈 시프트업 전체 매출 및 이익률 추이")
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
        height=350
    )
    
    st.altair_chart(combined_chart, use_container_width=True)

with tab3:
    st.header("👥 기업별 생산성 분석")
    
    st.markdown("""
    각 기업의 **조직 규모, 인당 영업이익, 개발 인력 비중** 등을 비교하여 
    비즈니스 모델에 따른 생산성 차이를 분석합니다.
    """)
    
    # 상단 KPI: 인당 영업이익 비교
    st.subheader("📌 2024년 인당 영업이익 비교")
    
    # 적자 기업 제외한 차트 (양수만)
    df_prod_positive = df_productivity[df_productivity['OP_per_Employee'] > 0].copy()
    
    chart_prod = alt.Chart(df_prod_positive).mark_bar().encode(
        x=alt.X('Company:N', sort='-y', title='기업'),
        y=alt.Y('OP_per_Employee:Q', title='인당 영업이익 (억원)'),
        color=alt.Color('Company:N', scale=alt.Scale(domain=['Shift Up', 'Krafton', 'Netmarble'], 
                                                      range=['#FF4B4B', '#1F77B4', '#FF7F0E'])),
        tooltip=['Company', 'Headcount', 'OP_per_Employee']
    ).properties(height=350, title='인당 영업이익 비교 (적자 기업 제외)')
    
    st.altair_chart(chart_prod, use_container_width=True)
    
    st.divider()
    
    # 기업별 상세 정보
    col_detail1, col_detail2 = st.columns(2)
    
    with col_detail1:
        st.subheader("🏢 직원수 및 조직 특성")
        
        # 직원수 표시
        chart_headcount = alt.Chart(df_productivity).mark_bar().encode(
            x=alt.X('Company:N', sort='-y', title='기업'),
            y=alt.Y('Headcount:Q', title='직원수 (명)'),
            color='Company:N',
            tooltip=['Company', 'Headcount', 'Dev_Ratio', 'Avg_Tenure']
        ).properties(height=300)
        
        st.altair_chart(chart_headcount, use_container_width=True)
        
        st.caption("**시프트업:** 322명으로 최소 규모, 개발직 90%")
        st.caption("**크래프톤:** 1,916명, 평균 근속 3.2년")
        st.caption("**NC소프트:** 3,269명, 개발직 70.8%, 평균 근속 7.8년 (최장)")

    with col_detail2:
        st.subheader("💼 개발 인력 비중")
        
        df_dev_ratio = df_productivity.dropna(subset=['Dev_Ratio'])
        
        if not df_dev_ratio.empty:
            chart_dev = alt.Chart(df_dev_ratio).mark_bar().encode(
                x=alt.X('Company:N', title='기업'),
                y=alt.Y('Dev_Ratio:Q', title='개발직 비중 (%)'),
                color='Company:N',
                tooltip=['Company', 'Dev_Ratio']
            ).properties(height=300)
            
            st.altair_chart(chart_dev, use_container_width=True)
            
            st.caption("**시프트업 90%:** IP 개발 중심, 경영진 최소화")
            st.caption("**NC소프트 70.8%:** R&D 집중, MMORPG 개발 역량")
            st.caption("**펄어비스 60%:** 자체 퍼블리싱 병행")
    
    st.divider()
    
    # 생산성 인사이트
    st.subheader("🔍 생산성 핵심 인사이트")
    
    col_insight1, col_insight2, col_insight3 = st.columns(3)
    
    with col_insight1:
        st.info("""
        **🥇 시프트업**
        - 인당 영업이익 4.6억원
        - 로열티 기반 고마진 모델
        - 개발 인력 90% 집중
        - 파트너 레버리지 활용
        """)
    
    with col_insight2:
        st.success("""
        **🥈 크래프톤**
        - 인당 영업이익 6.2억원
        - 절대 규모 + 안정성
        - PUBG IP 집중 구조
        - 자체 퍼블리싱
        """)
    
    with col_insight3:
        st.warning("""
        **🥉 넷마블**
        - 인당 영업이익 2.1억원
        - 구조조정 후 회복 중
        - 자체 IP 비중 확대
        - 수수료율 감소 중
        """)

with tab4:
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

with st.expander("📂 생산성 데이터 보기 (2024년)"):
    st.dataframe(df_productivity.style.format({
        'Headcount': '{:,} 명',
        'OP_2024': '{:,.0f} 억원',
        'OP_per_Employee': '{:.2f} 억원',
        'Dev_Ratio': '{:.1f}%',
        'Avg_Tenure': '{:.1f}년'
    }))
