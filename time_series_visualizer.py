import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Importar datos y establecer el índice de la columna date
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2. Limpiar los datos filtrando el 2.5% superior e inferior
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


# 3. Dibujar el gráfico de líneas
def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Guardar e imagen y retornar la figura
    fig.savefig('line_plot.png')
    return fig


# 4. Dibujar el gráfico de barras
def draw_bar_plot():
    df_bar = df.copy()

    # Extraer año y mes
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Definir el orden de los meses
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months, ordered=True)

    # Agrupar por año y mes calculando el promedio
    df_pivot = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Graficar
    fig = df_pivot.plot(kind='bar', figsize=(10, 8)).get_figure()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    # Guardar imagen y retornar la figura
    fig.savefig('bar_plot.png')
    return fig


# 5. Dibujar los diagramas de caja (Box Plots)
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Ordenar los meses de Enero a Diciembre
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 7))

    # Diagrama de caja por Año (Tendencia)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    # Diagrama de caja por Mes (Estacionalidad)
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    # Guardar imagen y retornar la figura
    fig.savefig('box_plot.png')
    return fig
