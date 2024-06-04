import json
import streamlit as st

st.set_page_config(
    page_title="Air Quality Monitoring",
    page_icon=":barometer:",
    layout="wide"
)

st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        max-width: 90%;
        padding-top: 5rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


KPQvsCNT = {
    '北部空品區': ['基隆市', '台北市', '新北市', '桃園市'],
    '竹苗空品區': ['竹苗'],
    '中部空品區': ['台中市', '彰化南投'],
    '雲嘉南空品區': ['雲林縣', '嘉義縣市', '台南市'],
    '高屏空品區': ['高雄市', '原高雄縣', '屏東縣'],
    '宜蘭花東': ['宜蘭花東'],
}

CNTvsAQS = {
    '基隆市': ['基隆'],
    '台北市': ['士林', '中山', '萬華', '古亭', '松山', '大同', '陽明'],
    '新北市': ['汐止', '萬里', '新店', '土城', '板橋', '新莊', '菜寮', '林口', '淡水', '三重', '永和'],
    '桃園市': ['桃園', '大園', '觀音', '平鎮', '龍潭', '中壢'],
    '竹苗': ['湖口', '竹東', '新竹', '頭份', '苗栗', '三義'],
    '台中市': ['豐原', '沙鹿', '大里', '忠明', '西屯'],
    '彰化南投': ['彰化', '線西', '二林', '南投', '竹山', '埔里'],
    '雲林縣': ['斗六', '崙背', '台西', '麥寮'],
    '嘉義縣市': ['朴子', '新港', '嘉義'],
    '台南市': ['新營', '善化', '安南', '台南'],
    '屏東縣': ['屏東', '潮州', '恆春'],
    '宜蘭花東': ['花蓮', '宜蘭', '冬山', '關山', '臺東'],
    '高雄市': ['左營', '前金', '前鎮', '小港', '復興'],
    '原高雄縣': ['美濃', '橋頭', '仁武', '鳳山', '大寮', '林園', '楠梓']
}


selected_kpq = st.selectbox('請選擇空品區名稱', tuple(KPQvsCNT.keys()))

if selected_kpq:
    selected_cnt = st.selectbox('請選擇該空品區對應的縣市名稱序列', KPQvsCNT[selected_kpq])
    if selected_cnt:
        selected_aqs = st.selectbox('請選擇該縣市對應的空品測站名稱', CNTvsAQS[selected_cnt])

