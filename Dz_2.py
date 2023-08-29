import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from scipy import stats
from scipy.stats import mannwhitneyu

st.title("Первая промежуточная аттестация")
uploaded_dataset = st.file_uploader("Выберите CSV или XLSX файл для загрузки", type = ['csv','xlsx'])

if uploaded_dataset is not None:
    dataset = pd.read_csv(uploaded_dataset)
    st.write(dataset)
else:
    st.warning("загрузите ваш датасет")

#Первый селектбокс для выбора столбца, по умолчанию стоит 3 столбец - "Total Fat"
FirstColumn = st.selectbox(
    "Выберите первый столбец (По умолчанию Total Fat)",
    options = dataset.columns,
    help= "Колонны должны быть одного типа и не должны быть одинаковыми (не получится сравнить две колонки Total Fat)",
    index = 3) 

#Второй селектбокс для выбора столбца, по умолчанию стоит 4 столбец - "Saturated Fat"
SecondColumn = st.selectbox(
    "Выберите второй столбец (По умолчанию Saturated Fat)",
    options = dataset.columns,
    help= "Колонны должны быть одного типа и не должны быть одинаковыми (не получится сравнить две колонки Saturated Fat)",
    index = 4) 

#Условие, когда key = False активирует доступ к кнопкам, позволяя выдавать им необходимый результат по выборке
#При key = True в проверке ниже будет выводиться ошибка, при которой кнопки станут недоступны
key = False 

#Проверка на выбор одинаковых столбцов
if FirstColumn == SecondColumn:
    st.error("Выбрали одинаковые столбики")
    key = True

#Проверка на разный тип столбцов    
elif dataset[FirstColumn].dtype != dataset[SecondColumn].dtype:
    st.error("У столбиков разные типы данных")
    key = True 



if st.button("Создать общую гистограмму", disabled = key):
   fig = go.Figure()
   fig.add_trace(go.Histogram(x = dataset[FirstColumn], name = FirstColumn))
   fig.add_trace(go.Histogram(x = dataset[SecondColumn], name = SecondColumn))
   fig.update_layout( 
       xaxis_title = "Значение",
       yaxis_title = "Общее количество жиров (гр.)",
       #barmode='overlay' #наложение гистограмм друг на друга
   )
   st.plotly_chart(fig) #создание гистограммы с 1 и 2 столбиком
   

if st.button("Отдельные гистограммы", disabled = key):
    fig_1 = go.Figure(data=[go.Histogram(x = dataset[FirstColumn], name = FirstColumn)])
    fig_1.update_layout( 
       title=f"Гистограмма распределения {FirstColumn}",
       xaxis_title = "Значение",
       yaxis_title = "Общее количество жиров (гр.)",
   )   
    st.plotly_chart(fig_1) #создание гистограммы 1 столбика
    
    fig_2 = go.Figure(data=[go.Histogram(x = dataset[SecondColumn], name = SecondColumn)])
    fig_2.update_layout( 
       title=f"Гистограмма распределения {SecondColumn}",
       xaxis_title = "Значение",
       yaxis_title = "Количество насыщенных жиров (гр.)",
   )   
    st.plotly_chart(fig_2) #создание гистограммы 1 столбика
    
algoritm = st.selectbox(
    'Выберите алгоритм теста гипотез',
    ("A/B тестирование","T-test","U-test")) #выпадающий список


if FirstColumn == SecondColumn:
    st.error("Выбрали одинаковые столбики")
elif dataset[FirstColumn].dtype != dataset[SecondColumn].dtype:
    st.error("У столбиков разные типы данных")
elif algoritm == "A/B тестирование":
    mean_stolb_1 = dataset[FirstColumn].mean()
    mean_stolb_2 = dataset[SecondColumn].mean()
    st.write(f"среднее значение {FirstColumn} = {mean_stolb_1 / 1:.4f}")
    st.write(f"среднее значение {SecondColumn} = {mean_stolb_2 / 1:.4f}")
    st.write(f"A/B-тест — это эксперимент с двумя группами для определения лучшего из двух вариантов. При сравнении двух столбцов ({FirstColumn} и {SecondColumn}) видно, что среднее значение одного столбца больше, чем среднее значение второго, а значит его выбор предпочтительнее.")

elif algoritm == "T-test":
    res = stats.ttest_ind(dataset[FirstColumn], dataset[SecondColumn], equal_var = False)
    
    st.write(f"p-value = {res.pvalue/ 1:.6}")
    st.write(f"p-value - это вероятность получить для данной вероятностной модели распределения значения случайной величины. Маленькие значения p-value показывают, что значения получены не случайно")
    
elif algoritm == "U-test":
    U_test = mannwhitneyu(dataset[FirstColumn],dataset[SecondColumn])
    st.write(f"p-value = {U_test.pvalue/ 1:.6}")
    st.write(f"Темт Манна-Уитни (U-Test), так же оценивает значимость как и t-test, только он менее чувствителен к нормальности распрежделения. Чем меньше значение p-value, тем меньше вероятность что значения получены случайно")

    

    