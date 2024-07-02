import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

# Заголовок приложения
st.title('Анализ торгового предприятия')

# Загрузка данных
df = pd.read_csv('Products.csv')

# Создаем selectbox для выбора раздела
section = st.selectbox(
    'Выберите раздел для анализа:',
    ['Просмотр данных', 'Информация о данных', 'Анализ нулевых значений', 
     'Анализ продаж по годам основания', 'Анализ самого прибыльного магазина по году основания', 
     'Анализ по категориям продуктов', 'Самые продаваемые категории товаров', 
     'Объем выручки по категориям товаров', 'Локация магазина с самыми большими продажами', 
     'Выводы']
)

# Просмотр данных
if section == 'Просмотр данных':
    st.subheader('Просмотр данных')
    st.write(df.head(15))

# Описание столбцов
if section == 'Информация о данных':
    st.subheader('Информация о данных')
    st.markdown("""
    * **ProductID** : уникальный идентификатор товара
    * **Weight** : вес продуктов
    * **FatContent** : указывает, содержит ли продукт мало жира или нет
    * **Visibility** : процент от общей площади витрины всех товаров в магазине, отведенный для конкретного продукта
    * **ProductType** : категория, к которой относится товар
    * **MRP** : Максимальная розничная цена (указанная цена) на продукты
    * **OutletID**: уникальный идентификатор магазина
    * **EstablishmentYear** : год основания торговых точек
    * **OutletSize** : размер магазина с точки зрения занимаемой площади
    * **LocationType** : тип города, в котором расположен магазин
    * **OutletType** : указывает, является ли торговая точка просто продуктовым магазином или каким-то супермаркетом
    * **OutletSales** : (целевая переменная) продажи товара в конкретном магазине
    """)

    # Информация о данных
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

# Анализ нулевых значений
if section == 'Анализ нулевых значений':
    st.subheader('Нулевые значения в столбцах')
    st.write(df.isnull().sum())

    # Заполнение нулевых значений
    df['Weight'].fillna(df['Weight'].mean(), inplace=True)
    df['OutletSize'].fillna('Средний', inplace=True)

    # Проверка проделанной работы
    st.subheader('Проверка проделанной работы')
    st.write(df.isnull().sum())
    st.write(df.head(15))

    # Удаление дубликатов
    st.subheader('Проверка дубликатов')
    st.write(f"Количество дубликатов: {df.duplicated().sum()}")

# Анализ продаж по годам основания
if section == 'Анализ продаж по годам основания':
    st.subheader('Анализ продаж по годам основания')
    st.write(df['EstablishmentYear'].value_counts())
    st.write(df.groupby('EstablishmentYear')['OutletSales'].sum().astype(int))

# Анализ самого прибыльного магазина по году основания
if section == 'Анализ самого прибыльного магазина по году основания':
    st.subheader('Анализ самого прибыльного магазина по году основания')
    st.write(df[df['EstablishmentYear'] == 1985].groupby('ProductType')['OutletSales'].sum().head(16).astype(int))

    # Гистограмма объема выручки по категориям товаров для 1985 года
    st.subheader('Объем выручки по категориям товаров для 1985 года')
    product_sales1985 = df[df['EstablishmentYear'] == 1985].groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
    fig, ax = plt.subplots()
    ax.barh(product_sales1985.index, product_sales1985.values, color='grey')
    ax.set_title('Объем выручки')
    ax.set_xlabel('Сумма продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_sales1985)):
        ax.text(product_sales1985.values[i], i, round(product_sales1985.values[i]), ha='left', va='center')
    st.pyplot(fig)

    # Круговая диаграмма по категориям товаров для 1985 года
    st.subheader('Круговая диаграмма по категориям товаров для 1985 года')
    fig, ax = plt.subplots()
    ax.pie(product_sales1985.values, labels=product_sales1985.index, autopct='%.0f%%')
    st.pyplot(fig)

# Анализ по категориям продуктов
if section == 'Анализ по категориям продуктов':
    st.subheader('Анализ по категориям продуктов')
    st.write(df['ProductType'].value_counts())

    # Создание новой таблицы для работы с отдельными данными
    st.subheader('Создание новой таблицы для анализа категорий товаров')
    df_product = pd.DataFrame({
        'Категория товара': [
            'Фрукты и овощи','Закуски','Товары для дома','Замороженные продукты','Молочные продукты',
            'Консервы','Выпечка','Здоровье и гигиена','Безалкогольные напитки','Мясо','Хлеб','Крепкие напитки',
            'Другое','Бакалея','Завтрак','Морепродукты'
        ],
        'Количество': [1232,1200,910,856,682,649,648,520,445,425,251,214,169,148,110,64]
    })
    st.write(df_product)

    # Гистограмма количества продаж по категориям товаров
    st.subheader('Количество продаж товара по категориям')
    fig, ax = plt.subplots()
    df_product.groupby('Категория товара')['Количество'].mean().plot(ax=ax, kind='bar', rot=45, fontsize=10, figsize=(16, 10), color='purple')
    st.pyplot(fig)

# Самые продаваемые категории товаров
if section == 'Самые продаваемые категории товаров':
    st.subheader('Самые продаваемые категории товаров')
    product_counts = df['ProductType'].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.barh(product_counts.index, product_counts.values, color='red')
    ax.set_title('Самые продаваемые категории товаров')
    ax.set_xlabel('Количество продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_counts)):
        ax.text(product_counts.values[i], i, str(product_counts.values[i]), ha='left', va='center')
    st.pyplot(fig)

# Объем выручки по категориям товаров
if section == 'Объем выручки по категориям товаров':
    st.subheader('Объем выручки по категориям товаров')
    product_sales = df.groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
    fig, ax = plt.subplots()
    ax.barh(product_sales.index, product_sales.values, color='green')
    ax.set_title('Объем выручки')
    ax.set_xlabel('Сумма продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_sales)):
        ax.text(product_sales.values[i], i, round(product_sales.values[i]), ha='left', va='center')
    st.pyplot(fig)

# Локация магазина с самыми большими продажами
if section == 'Локация магазина с самыми большими продажами':
    st.subheader('Локация магазина с самыми большими продажами')
    st.write(df['LocationType'].value_counts())
    df_location = pd.DataFrame({'Магазин': ['Локация 1', 'Локация 2', 'Локация 3'], 'Количество продаж': [2388, 2785, 3350]})
    st.write(df_location)

    ilocation = df.groupby('LocationType')['OutletSales'].sum().index
    vlocation = df.groupby('LocationType')['OutletSales'].sum().values
    fig, ax = plt.subplots()
    ax.pie(vlocation, labels=ilocation, autopct='%.0f%%')
    st.pyplot(fig)

# Выводы
if section == 'Выводы':
    st.subheader('Выводы')
    st.markdown('''
    В ходе работы с данными торгового предприятия был проведен комплексный анализ, включающий следующие этапы:
    ''')
    st.subheader('Анализ категорий товаров') 
    st.markdown('''
Выявление самых продаваемых категорий товаров:
Проведен анализ по категориям товаров, чтобы определить, какие из них приносят наибольшую прибыль. Например, категории "Фрукты и овощи" и "Закуски" оказались лидерами по объемам продаж.
Построены графики и диаграммы, иллюстрирующие объемы продаж по различным категориям товаров. Это позволило наглядно увидеть, какие товары наиболее востребованы покупателями.
Выявление товаров с низким спросом:
Проанализированы данные по товарам, которые продаются наименее успешно. Например, категории "Морепродукты" показали низкие объемы продаж.
На основе этого анализа предложено исключить или сократить ассортимент товаров с низким спросом, чтобы оптимизировать складские запасы и повысить общую прибыльность магазина.
''')
    st.subheader('Анализ прибыльности по годам основания магазина')
    st.markdown('''
Расчет прибыли по году основания магазина:
Проведен анализ продаж по годам основания магазинов. Данные были сгруппированы по годам, чтобы определить, в какие годы основанные магазины показали наибольшую прибыль.
Выявлено, что магазины, основанные в определенные годы, например, в 1985 году, оказались наиболее прибыльными.
Анализ самых покупаемых категорий товаров в прибыльные годы:
Для самых прибыльных годов был проведен детальный анализ по категориям товаров, чтобы определить, какие товары обеспечивали наибольшие продажи.
Построены графики, показывающие распределение продаж по категориям товаров в эти годы. На основе этого анализа предложено уделить больше внимания определенным категориям товаров, которые показали высокую прибыльность, и увеличить их наличие на полках магазинов.
  ''')
    st.subheader('Анализ прибыльности по районам') 
    st.markdown('''
Выявление самого прибыльного района:
Проведен анализ данных по районам, чтобы определить, в каком районе расположены самые прибыльные магазины.
На основе данных продаж и локации магазинов была построена диаграмма, показывающая распределение прибыли по различным районам.
Выявлено, что магазины, расположенные в определенных районах, например, в "Локация 3", показывают наибольшие объемы продаж и, следовательно, являются самыми прибыльными.
Рекомендации по открытию новых торговых точек:
На основе анализа предложено рассмотреть возможность открытия новых торговых точек в самых прибыльных районах. Это позволит увеличить общую прибыльность торгового предприятия за счет эффективного использования успешных локаций.
''')
    st.subheader('Заключение')
    st.markdown('''
В результате проведенного анализа была получена важная информация, которая поможет торговому предприятию оптимизировать свою деятельность:

1.Увеличение ассортимента и наличия самых продаваемых категорий товаров.

2.Сокращение или исключение товаров с низким спросом.

3.Фокусировка на прибыльных годах и категориях товаров при планировании закупок и маркетинговых акций.

Эти рекомендации помогут улучшить финансовые показатели предприятия и увеличить его конкурентоспособность на рынке.
    ''')
