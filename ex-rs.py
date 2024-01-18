import streamlit as st
import pandas as pd

# 고객 정보 데이터프레임 초기화
columns = ['Name', 'Gender', 'Age', 'Number_of_Children',
           'Child_1_Age', 'Child_1_Gender', 'Child_2_Age',
           'Child_2_Gender', 'Child_3_Age', 'Child_3_Gender',
           'Parenting_Concerns', 'Stress_Level']

# 스트림릿 앱 구성
st.title('간편한 고객 정보 입력')

# 앱 실행 시에 데이터 불러오기
@st.cache_data
def load_data():
    try:
        df_customers = pd.read_csv('customer_data.csv')
    except FileNotFoundError:
        df_customers = pd.DataFrame(columns=columns)
    return df_customers

df_customers = load_data()

# 기본 정보 입력
name = st.text_input('이름:')
gender_options = ['Male', 'Female']
gender = st.selectbox('성별:', gender_options)
age = st.number_input('나이:', min_value=0)

# 자녀 정보 입력
num_children = st.number_input('자녀의 수:', min_value=0, value=0)

child_ages = []
child_genders = []

if num_children > 0:
    st.subheader('자녀 정보 입력:')
    for i in range(num_children):
        child_ages.append(st.number_input(f'자녀 {i+1}의 개월수:', key=f'child_age_{i}'))
        child_genders.append(st.radio(f'자녀 {i+1}의 성별:', gender_options, key=f'child_gender_{i}'))

# 부가 정보 입력
parenting_concerns_options = ['건강', '감정표현', '양육법']
selected_parenting_concerns = st.multiselect('육아 고민 선택:', parenting_concerns_options)
stress_level = st.slider('스트레스 정도:', min_value=0, max_value=5, step=1)

# 고객 정보 저장
if st.button('고객 정보 저장'):
    new_data = [name, gender, age, num_children]

    for i in range(num_children):
        new_data.extend([child_ages[i], child_genders[i]])

    new_data.extend([None, None] * (3 - num_children))  # 남은 자녀 정보에 대해서도 None을 추가

    new_data.extend([selected_parenting_concerns, stress_level])

    # DataFrame을 가로로 생성하여 데이터를 추가
    new_data_df = pd.DataFrame([new_data], columns=columns)
    df_customers = pd.concat([df_customers, new_data_df], ignore_index=True)

    df_customers.to_csv('customer_data.csv', index=False)
    st.success('고객 정보가 성공적으로 저장되었습니다.')

# 저장된 데이터프레임 출력
st.subheader('저장된 고객 정보 데이터프레임:')
st.write(df_customers)

