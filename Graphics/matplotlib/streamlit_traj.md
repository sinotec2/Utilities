---
layout: default
title: streamlit範例
parent: matplotlib Programs
grand_parent: Graphics
date: 2024-05-30
last_modified_date: 2024-05-30 09:34:02
tags: geoplot graphics streamlit
---

# streamlit範例
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景


```python
import streamlit as st
import subprocess
import time

# Create a function to run the external Python program:

def run_external_program():
    # Replace the following line with the actual command to run the program
    command = "python my_program.py"

    # Add the input arguments to the command
    command += f' "{date}" "{time}" "{region}" "{city}" "{station}" {lat_input} {long_input}'

    # Run the program and capture the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Display the progress
    for i in range(10):
        st.write(f"Progress: {i*10}%")
        time.sleep(1)

    # Display the output image
    if error is None:
        st.image(output)
    else:
        st.write(error)

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
# Create the input components:
date = st.date_input("Select a date")
time = st.time_input("Select a time")

lat, long = st.columns(2)
with lat:
    lat_input = st.number_input("Enter latitude", value=0.0)
with long:
    long_input = st.number_input("Enter longitude", value=0.0)

# Create the execute button

execute = st.button("Execute")


if execute:
    run_external_program()




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

```