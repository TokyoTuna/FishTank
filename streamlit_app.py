import streamlit as st
import pandas as pd


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
""")

# -----------------------------------------------------------------------------
# 2. 데이터 준비 (하드코딩된 데이터 사용)
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
# 4. 메인 대시보드 구성
# -----------------------------------------------------------------------------

# Tab 구성
tab1, tab2, tab3 = st.tabs(["📊 2025 분기별 마진 비교", "🚀 시프트업 심층 분석", "📅 2024 연간 비교"])

with tab1:
    st.subheader("2025년 1Q ~ 3Q 영업이익률(OPM) 추이")
    st.markdown("시프트업은 3분기 내내 **60% 이상의 영업이익률**을 유지하며 압도적인 수익성을 보여줍니다.")
    
    # Line Chart: 영업이익률 추이
    fig_opm = px.line(filtered_df, x='Quarter', y='OPM', color='Company', markers=True,
                      title='분기별 영업이익률(%) 추이',
                      color_discrete_map={
                          'Shift Up': '#FF4B4B', 'Krafton': '#1F77B4', 'Nexon': '#2CA02C',
                          'Netmarble': '#FF7F0E', 'NCSoft': '#9467BD', 'Pearl Abyss': '#8C564B'
                      })
    fig_opm.update_traces(line=dict(width=3), marker=dict(size=8))
    fig_opm.update_layout(yaxis_title="영업이익률 (%)", hovermode="x unified")
    st.plotly_chart(fig_opm, use_container_width=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("3Q25 매출액 비교 (억원)")
        df_3q = filtered_df[filtered_df['Quarter'] == '3Q25'].sort_values('Revenue', ascending=False)
        fig_rev = px.bar(df_3q, x='Company', y='Revenue', color='Company', text_auto=True,
                         color_discrete_map={
                          'Shift Up': '#FF4B4B', 'Krafton': '#1F77B4', 'Nexon': '#2CA02C',
                          'Netmarble': '#FF7F0E', 'NCSoft': '#9467BD', 'Pearl Abyss': '#8C564B'
                      })
        fig_rev.update_layout(showlegend=False)
        st.plotly_chart(fig_rev, use_container_width=True)
        st.caption("매출 규모는 크래프톤, 넷마블, 넥슨이 압도적입니다.")

    with col2:
        st.subheader("3Q25 영업이익 비교 (억원)")
        df_3q_op = filtered_df[filtered_df['Quarter'] == '3Q25'].sort_values('OP', ascending=False)
        fig_op = px.bar(df_3q_op, x='Company', y='OP', color='Company', text_auto=True,
                        color_discrete_map={
                          'Shift Up': '#FF4B4B', 'Krafton': '#1F77B4', 'Nexon': '#2CA02C',
                          'Netmarble': '#FF7F0E', 'NCSoft': '#9467BD', 'Pearl Abyss': '#8C564B'
                      })
        fig_op.update_layout(showlegend=False)
        st.plotly_chart(fig_op, use_container_width=True)
        st.caption("시프트업은 매출 대비 영업이익 규모가 매우 큽니다.")

    st.subheader("EBITDA 마진 비교 (데이터 가용 기업)")
    # EBITDA 데이터가 있는 기업만 필터링
    df_ebitda = filtered_df.dropna(subset=['EBITDA_Margin'])
    fig_ebitda = px.bar(df_ebitda, x='Company', y='EBITDA_Margin', color='Quarter', barmode='group',
                        text_auto=True, title='분기별 EBITDA 마진 (%)',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_ebitda, use_container_width=True)

with tab2:
    st.header("🚀 Shift Up: 압도적 수익성의 비밀")
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    # 시프트업 3Q25 주요 지표
    su_3q = df_quarter[(df_quarter['Company'] == 'Shift Up') & (df_quarter['Quarter'] == '3Q25')].iloc[0]
    
    with col_kpi1:
        st.metric(label="3Q25 영업이익률", value=f"{su_3q['OPM']}%", delta="4.9%p (vs 2Q25)")
    with col_kpi2:
        st.metric(label="3Q25 EBITDA 마진", value=f"{su_3q['EBITDA_Margin']}%", delta="5.3%p (vs 2Q25)")
    with col_kpi3:
        st.metric(label="2024 직원수 (약)", value="322명", delta="인당 생산성 최상위")

    st.markdown("---")
    
    st.markdown("""
    ### 💡 핵심 분석 포인트
    1.  **변동비 구조의 강점**: 3Q25 매출이 2Q25(스텔라 블레이드 출시 효과) 대비 감소했음에도, 마케팅비/수수료 등 변동비가 더 크게 감소하여 마진율은 오히려 상승(60.7% → 65.6%)했습니다.
    2.  **IP 포트폴리오**: 
        *   **승리의 여신: 니케**: 안정적인 현금 창출원 (Cash Cow)
        *   **스텔라 블레이드**: 고마진 콘솔/PC 패키지 + 로열티 매출
    3.  **생산성**: 약 300명대의 인력으로 연간 1,500억 원 이상의 영업이익을 창출하는 구조는 타 대형 게임사(수천 명 인력)와 차별화됩니다.
    """)
    
    # 시프트업 전용 차트
    su_data = df_quarter[df_quarter['Company'] == 'Shift Up']
    
    fig_su = go.Figure()
    fig_su.add_trace(go.Bar(x=su_data['Quarter'], y=su_data['Revenue'], name='매출(억원)', marker_color='#FF9F9F'))
    fig_su.add_trace(go.Bar(x=su_data['Quarter'], y=su_data['OP'], name='영업이익(억원)', marker_color='#FF4B4B'))
    fig_su.add_trace(go.Scatter(x=su_data['Quarter'], y=su_data['OPM'], name='영업이익률(%)', yaxis='y2', mode='lines+markers', line=dict(color='black', width=3)))
    
    fig_su.update_layout(
        title='시프트업 2025 분기별 실적 및 이익률',
        yaxis=dict(title='금액 (억원)'),
        yaxis2=dict(title='이익률 (%)', overlaying='y', side='right', range=[0, 100]),
        legend=dict(x=0.1, y=1.1, orientation='h')
    )
    st.plotly_chart(fig_su, use_container_width=True)

with tab3:
    st.subheader("2024년 연간 마진 랭킹 Comparison")
    st.markdown("2024년 전체 실적 기준으로도 시프트업은 **가장 높은 수익성**을 기록했습니다.")

    # 영업이익률 vs EBITDA 마진 비교 차트
    fig_annual = px.bar(df_annual, x='Company', y='Value', color='Metric', barmode='group',
                        text_auto=True,
                        category_orders={"Company": ["Shift Up", "Krafton", "Nexon", "Netmarble", "Pearl Abyss", "NCSoft"]},
                        color_discrete_map={'OP Margin': '#1f77b4', 'EBITDA Margin': '#2ca02c'})
    
    fig_annual.update_layout(yaxis_title="마진 (%)", xaxis_title="기업")
    st.plotly_chart(fig_annual, use_container_width=True)

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
