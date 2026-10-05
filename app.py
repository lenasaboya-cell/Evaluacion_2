import streamlit as st
import pandas as pd
import numpy as np

# 1. Configurar backend para entorno web antes de importar pyplot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns

# Estilo global opcional
sns.set_theme(style="whitegrid")

# Ejemplo de uso seguro en Streamlit:
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot([1, 2, 2, 3, 3, 3, 4], kde=True, ax=ax, color='skyblue')
ax.set_title("Ejemplo de Gráfico")

# Renderizar en la app de Streamlit
st.pyplot(fig)

# Limpiar la figura en memoria
plt.close(fig)
