# Dashboard de Ventas Interactivo - Streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ CONFIGURACIÓN GENERAL ------------------
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
st.title("📊 Dashboard Interactivo - Cadena de Tiendas de Conveniencia")
st.markdown("Este dashboard permite analizar las ventas, preferencias y comportamiento de clientes en distintas categorías de productos.")

# ------------------ CARGA DE DATOS ------------------
df = pd.read_csv("data.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Mes'] = df['Date'].dt.to_period('M').astype(str)

# ------------------ SIDEBAR: FILTROS ------------------
st.sidebar.title("🔎 Filtros")
st.sidebar.markdown("Ajusta los filtros para personalizar las visualizaciones.")

# Rango de meses con validación de tipo
meses_unicos = sorted(df['Mes'].unique())
seleccion_meses = st.sidebar.select_slider(
    "🗓 Rango de meses",
    options=meses_unicos,
    value=(meses_unicos[0], meses_unicos[-1])
)

# Validar si seleccionaron un solo mes o un rango
if not isinstance(seleccion_meses, tuple):
    rango_meses = (seleccion_meses, seleccion_meses)
else:
    rango_meses = tuple(sorted(seleccion_meses))

# Tipo de cliente
tipo_cliente = st.sidebar.multiselect(
    "👥 Tipo de Cliente",
    options=df['Customer type'].unique(),
    default=df['Customer type'].unique()
)

# ------------------ APLICACIÓN DE FILTROS ------------------
df_filtrado = df[
    (df['Mes'] >= rango_meses[0]) &
    (df['Mes'] <= rango_meses[1]) &
    (df['Customer type'].isin(tipo_cliente))
]

# ------------------ VALIDACIÓN ------------------
if df_filtrado.empty:
    st.warning("⚠️ No hay datos para mostrar con los filtros seleccionados. Ajusta el rango de meses o el tipo de cliente.")
else:
    # ------------------ VISUALIZACIONES ------------------
    st.markdown("---")

    # 1. Evolución de las Ventas Totales (por Mes)
    st.subheader("1️⃣ Evolución de las Ventas Totales (por Mes)")
    st.markdown("Visualiza cómo han variado las ventas mensualmente.")
    ventas_mensual = df_filtrado.groupby('Mes')['Total'].sum().reset_index()

    fig1, ax1 = plt.subplots()
    ax1.plot(ventas_mensual['Mes'], ventas_mensual['Total'], marker='o', color='steelblue')
    ax1.set_title("Ventas Totales por Mes")
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Total ($)")
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig1)

    st.markdown("---")

    # 2. Ingresos por Línea de Producto
    st.subheader("2️⃣ Ingresos por Línea de Producto")
    st.markdown("Comparación de ingresos generados por cada categoría de producto.")
    ingresos = df_filtrado.groupby('Product line')['Total'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots()
    ingresos.plot(kind='bar', ax=ax2, color='darkorange')
    ax2.set_title("Ingresos por Línea de Producto")
    ax2.set_xlabel("Línea de Producto")
    ax2.set_ylabel("Total ($)")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

    st.markdown("---")

    # 3. Métodos de Pago Preferidos
    st.subheader("3️⃣ Métodos de Pago Preferidos")
    st.markdown("Frecuencia de uso de cada método de pago.")
    pagos = df_filtrado['Payment'].value_counts()
    fig3, ax3 = plt.subplots()
    pagos.plot(kind='bar', ax=ax3, color='seagreen')
    ax3.set_title("Frecuencia de Métodos de Pago")
    ax3.set_xlabel("Método de Pago")
    ax3.set_ylabel("Cantidad de Transacciones")
    st.pyplot(fig3)

# ------------------ PIE DE PÁGINA ------------------
st.markdown("---")
st.markdown("🔍 **Este dashboard fue desarrollado como parte del análisis de ventas para una cadena de tiendas de conveniencia.**")
