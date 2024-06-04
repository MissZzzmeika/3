import pandas as pd
import matplotlib.pyplot as plt
import io
import streamlit as st

# Загрузка данных
@st.cache
def load_data():
    df = pd.read_csv('Products.csv')
    df.Weight.fillna(df.Weight.mean(), inplace=True)
    df.OutletSize.fillna('Средний', inplace=True)
    return df

df = load_data()

# Заголовок приложения
st.title('Анализ торгового предприятия')

    # Информация о данных
    st.write("### Информация о данных")
    buffer = st.empty()
    df_info = df.info(buf=buffer)
    st.text(buffer)

# Информация о данных
"""**Для удобства пометим название столбцов и их типовое назначение в датасете**
*   **ProductID** : уникальный идентификатор товара
*   **Weight** : вес продуктов
*  **FatContent** : указывает, содержит ли продукт мало жира или нет
*   **Visibility** : процент от общей площади витрины всех товаров в магазине, отведенный для конкретного продукта
*   **ProductType** : категория, к которой относится товар
*   **MRP** : Максимальная розничная цена (указанная цена) на продукты
*   **OutletID**: уникальный идентификатор магазина
*   **EstablishmentYear** : год основания торговых точек
*   **OutletSize** : размер магазина с точки зрения занимаемой площади
*   **LocationType** : тип города, в котором расположен магазин
*   **OutletType** : указывает, является ли торговая точка просто продуктовым магазином или каким-то супермаркетом
*   **OutletSales** : (целевая переменная) продажи товара в конкретном магазине
    
    # Анализ продаж по годам основания
    st.write("### Анализ продаж по годам основания")
    st.write(df['EstablishmentYear'].value_counts())
    st.write(df.groupby('EstablishmentYear')['OutletSales'].sum().astype(int))

    # Анализ самого прибыльного магазина по году основания
    st.write("### Анализ самого прибыльного магазина по году основания")
    st.write(df.groupby('OutletID')['OutletSales'].sum().astype(int))

    st.write(df[df['EstablishmentYear'] == 1985].groupby('ProductType')['OutletSales'].sum().astype(int))

    # Построение графика объема выручки
    product_sales1985 = df[df['EstablishmentYear'] == 1985].groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
    fig, ax = plt.subplots()
    ax.barh(product_sales1985.index, product_sales1985.values, color='grey')
    ax.set_title('Объем выручки')
    ax.set_xlabel('Сумма продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_sales1985.values)):
        ax.text(product_sales1985.values[i], i, round(product_sales1985.values[i]), ha='left', va='center')
    st.pyplot(fig)

    # Построение круговой диаграммы
    fig, ax = plt.subplots()
    ax.pie(product_sales1985.values, labels=product_sales1985.index, autopct='%.0f%%')
    st.pyplot(fig)

    # Анализ по категориям продуктов
    st.write("### Анализ по категориям продуктов")
    df_product = pd.DataFrame({
        'Категория товара': ['Фрукты и овощи', 'Закуски', 'Товары для дома', 'Замороженные продукты', 'Молочные продукты', 'Консервы', 'Выпечка', 'Здоровье и гигиена', 'Безалкогольные напитки', 'Мясо', 'Хлеб', 'Крепкие напитки', 'Другое', 'Бакалея', 'Завтрак', 'Морепродукты'], 
        'Количество': [1232, 1200, 910, 856, 682, 649, 648, 520, 445, 425, 251, 214, 169, 148, 110, 64]
    })
    st.write(df_product)

    # Гистограмма количества продаж по категориям товаров
    fig, ax = plt.subplots()
    df_product.groupby('Категория товара')['Количество'].mean().plot(ax=ax, kind='bar', rot=45, fontsize=10, figsize=(16, 10), color='purple', title='Количество продаж товара по категориям')
    st.pyplot(fig)

    # Самые продаваемые категории товаров
    st.write("### Самые продаваемые категории товаров")
    product_counts = df['ProductType'].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.barh(product_counts.index, product_counts.values, color='red')
    ax.set_title('Самые продаваемые категории товаров')
    ax.set_xlabel('Количество продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_counts.values)):
        ax.text(product_counts.values[i], i, str(product_counts.values[i]), ha='left', va='center')
    st.pyplot(fig)

    # Анализ объема выручки по категориям товаров
    st.write("### Анализ объема выручки по категориям товаров")
    product_sales = df.groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
    fig, ax = plt.subplots()
    ax.barh(product_sales.index, product_sales.values, color='green')
    ax.set_title('Объем выручки')
    ax.set_xlabel('Сумма продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_sales.values)):
        ax.text(product_sales.values[i], i, round(product_sales.values[i]), ha='left', va='center')
    st.pyplot(fig)

    # Локация магазина с самыми большими продажами
    st.write("### Локация магазина с самыми большими продажами")
    st.write(df['LocationType'].value_counts())

    df_location = pd.DataFrame({'Магазин': ['Локация 1', 'Локация 2', 'Локация 3'], 'Количество продаж': [2388, 2785, 3350]})
    st.write(df_location)

    ilocation = df.groupby('LocationType')['OutletSales'].sum().index
    vlocation = df.groupby('LocationType')['OutletSales'].sum().values
    fig, ax = plt.subplots()
    ax.pie(vlocation, labels=ilocation, autopct='%.0f%%')
    st.pyplot(fig)

    st.write("На диаграмме так же видно, что самые высокие продажи в 'Локация 3'.")
