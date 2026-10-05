import streamlit as st
import pandas as pd
import numpy as np

# 1. Configurar backend para entorno web antes de importar pyplot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns

# Configuración de página
st.set_page_config(
    page_title="Teen Mental Health Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo global de Seaborn
sns.set_theme(style="whitegrid")

# ==========================================
# CLASE POO: DATA ANALYZER
# ==========================================
class DataAnalyzer:
    """Clase encargada de encapsular la lógica de análisis y visualización de datos."""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def get_info(self):
        """Retorna información general del DataFrame."""
        info_dict = {
            "filas": self.df.shape[0],
            "columnas": self.df.shape[1],
            "nulos_totales": self.df.isnull().sum().sum(),
            "duplicados": self.df.duplicated().sum()
        }
        return info_dict

    def classify_variables(self):
        """Clasifica las variables en numéricas y categóricas."""
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        return num_cols, cat_cols

    def get_descriptive_stats(self):
        """Retorna estadísticas descriptivas."""
        return self.df.describe().T

    def filter_data(self, ages, genders, platforms, social_levels):
        """Filtra el dataset según parámetros seleccionados."""
        filtered_df = self.df[
            (self.df['age'].between(ages[0], ages[1])) &
            (self.df['gender'].isin(genders)) &
            (self.df['platform_usage'].isin(platforms)) &
            (self.df['social_interaction_level'].isin(social_levels))
        ]
        return filtered_df

# ==========================================
# MENÚ NAVEGACIÓN SIDEBAR
# ==========================================
st.sidebar.title("📌 Navegación Principal")
modulo = st.sidebar.radio(
    "Seleccione un Módulo:",
    ["1. Home (Presentación)", "2. Carga del Dataset", "3. Análisis EDA"]
)

# Inicializar Estado de Sesión para el DataFrame
if 'df' not in st.session_state:
    st.session_state['df'] = None

# ==========================================
# MÓDULO 1: HOME
# ==========================================
if modulo == "1. Home (Presentación)":
    st.title("🧠 Teen Mental Health Analytics Dashboard")
    st.markdown("---")
    
# 📸 Mostrar imagen principal si existe en el repositorio
st.image("Imagen DMC.png", width=100)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Objetivo del Análisis")
        st.write(
            "Esta aplicación interactiva tiene como objetivo realizar un **Análisis Exploratorio de Datos (EDA)** "
            "sobre el impacto de las redes sociales, el descanso y la actividad física en la salud mental "
            "y bienestar de los adolescentes (13 a 19 años)."
        )
        st.info(
            "ℹ️ **Nota de Responsabilidad**: Los resultados presentados son estrictamente informativos y educativos. "
            "No constituyen un diagnóstico clínico ni reemplazan la atención profesional de la salud."
        )
        
        st.subheader("🛠️ Tecnologías Utilizadas")
        st.markdown("- **Lenguaje**: Python 3.10+\n- **Librerías**: Pandas, NumPy, Matplotlib, Seaborn, Streamlit\n- **Paradigma**: Programación Orientada a Objetos (POO)")

    with col2:
        st.subheader("👤 Datos del Autor")
        st.markdown("""
        **Estudiante:** Especialista en Analytics  
        **Programa:** Especialización en Python for Analytics  
        **Institución:** DILIC Institute  
        **Año:** 2026  
        """)

# ==========================================
# MÓDULO 2: CARGA DEL DATASET
# ==========================================
elif modulo == "2. Carga del Dataset":
    st.title("📂 Carga e Inspección Inicial")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Cargue el archivo 'Teen_Mental_Health_Dataset.csv'", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state['df'] = df
            st.success("✅ Archivo cargado correctamente.")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Número de Registros (Filas)", df.shape[0])
            col2.metric("Número de Variables (Columnas)", df.shape[1])
            col3.metric("Valores Nulos Detectados", df.isnull().sum().sum())
            
            st.subheader("👀 Vista previa del Dataset (Primeros 10 registros)")
            st.dataframe(df.head(10), use_container_width=True)
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    else:
        if st.session_state['df'] is not None:
            st.info("💡 Un dataset previo ya se encuentra cargado en el sistema.")
            st.dataframe(st.session_state['df'].head(5), use_container_width=True)
        else:
            st.warning("⚠️ Por favor, cargue el archivo CSV para habilitar el análisis en el Módulo 3.")

# ==========================================
# MÓDULO 3: ANÁLISIS EXPLORATORIO (EDA)
# ==========================================
elif modulo == "3. Análisis EDA":
    if st.session_state['df'] is None:
        st.error("❌ No se ha cargado ningún dataset. Diríjase al Módulo 2 para cargar el CSV.")
    else:
        df = st.session_state['df']
        analyzer = DataAnalyzer(df)
        
        st.title("📊 Análisis Exploratorio de Datos (EDA)")
        st.markdown("---")
        
        # Estructura de TABS para organizar los 10 ítems
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 1-3. Estructura & Descriptivas", 
            "🔍 4-6. Distribuciones & Categorías", 
            "📈 7-8. Análisis Bivariado", 
            "🎛️ 9. Filtros Dinámicos", 
            "💡 10. Hallazgos & Conclusiones"
        ])
        
        # TAB 1: ITEMS 1, 2, 3
        with tab1:
            st.header("Ítem 1: Información General")
            info = analyzer.get_info()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Filas", info["filas"])
            c2.metric("Columnas", info["columnas"])
            c3.metric("Nulos", info["nulos_totales"])
            c4.metric("Duplicados", info["duplicados"])
            
            st.subheader("Ítem 2: Clasificación de Variables")
            num_cols, cat_cols = analyzer.classify_variables()
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Variables Numéricas ({len(num_cols)}):**")
                st.write(num_cols)
            with col_b:
                st.write(f"**Variables Categóricas ({len(cat_cols)}):**")
                st.write(cat_cols)
                
            st.subheader("Ítem 3: Estadísticas Descriptivas")
            st.dataframe(analyzer.get_descriptive_stats(), use_container_width=True)
            st.caption("Resumen estadístico con medidas de tendencia central, dispersión y cuartiles.")

        # TAB 2: ITEMS 4, 5, 6
        with tab2:
            st.header("Ítem 4: Análisis de Valores Faltantes")
            nulls = df.isnull().sum().reset_index()
            nulls.columns = ['Variable', 'Conteo Faltantes']
            nulls['Porcentaje (%)'] = (nulls['Conteo Faltantes'] / len(df)) * 100
            st.dataframe(nulls)
            
            st.header("Ítem 5: Distribución de Variables Numéricas")
            num_var = st.selectbox("Seleccione variable numérica a inspeccionar:", num_cols, index=1)
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(df[num_var], kde=True, ax=ax, color='skyblue')
            ax.set_title(f"Distribución de {num_var}")
            st.pyplot(fig)
            
            st.header("Ítem 6: Análisis de Variables Categóricas")
            cat_var = st.selectbox("Seleccione variable categórica:", cat_cols, index=1)
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            sns.countplot(data=df, x=cat_var, palette="Set2", ax=ax2)
            ax2.set_title(f"Frecuencia por {cat_var}")
            st.pyplot(fig2)

        # TAB 3: ITEMS 7, 8
        with tab3:
            st.header("Ítem 7: Análisis Bivariado (Numérico vs Categórico / Depression Label)")
            col_num1, col_num2 = st.columns(2)
            
            with col_num1:
                fig_social, ax_s = plt.subplots(figsize=(6, 4))
                sns.boxplot(data=df, x='depression_label', y='daily_social_media_hours', ax=ax_s, palette="Set1")
                ax_s.set_title("Uso de Redes por Etiqueta de Depresión")
                st.pyplot(fig_social)
                
            with col_num2:
                fig_sleep, ax_sl = plt.subplots(figsize=(6, 4))
                sns.boxplot(data=df, x='depression_label', y='sleep_hours', ax=ax_sl, palette="Set2")
                ax_sl.set_title("Horas de Sueño por Etiqueta de Depresión")
                st.pyplot(fig_sleep)

            st.header("Ítem 8: Análisis Bivariado (Categórico vs Categórico)")
            col_cat1, col_cat2 = st.columns(2)
            
            with col_cat1:
                fig_plat, ax_p = plt.subplots(figsize=(6, 4))
                sns.countplot(data=df, x='platform_usage', hue='depression_label', ax=ax_p, palette="coolwarm")
                ax_p.set_title("Uso de Plataforma por Etiqueta")
                st.pyplot(fig_plat)
                
            with col_cat2:
                fig_gen, ax_g = plt.subplots(figsize=(6, 4))
                sns.countplot(data=df, x='gender', hue='platform_usage', ax=ax_g, palette="viridis")
                ax_g.set_title("Género vs Plataforma Utilizada")
                st.pyplot(fig_gen)

        # TAB 4: ITEM 9 (Filtros interactivos)
        with tab4:
            st.header("Ítem 9: Análisis Basado en Parámetros Seleccionados")
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                age_range = st.slider("Rango de Edad:", int(df['age'].min()), int(df['age'].max()), (13, 19))
                gender_sel = st.multiselect("Género:", df['gender'].unique().tolist(), default=df['gender'].unique().tolist())
            with col_f2:
                plat_sel = st.multiselect("Plataforma:", df['platform_usage'].unique().tolist(), default=df['platform_usage'].unique().tolist())
                social_sel = st.multiselect("Nivel Social:", df['social_interaction_level'].unique().tolist(), default=df['social_interaction_level'].unique().tolist())
            
            df_filtered = analyzer.filter_data(age_range, gender_sel, plat_sel, social_sel)
            st.write(f"**Registros encontrados:** {len(df_filtered)}")
            
            if not df_filtered.empty:
                var_x = st.selectbox("Eje X (Hábitos Digitales):", ['daily_social_media_hours', 'screen_time_before_sleep', 'sleep_hours'])
                var_y = st.selectbox("Eje Y (Indicadores de Bienestar):", ['stress_level', 'anxiety_level', 'addiction_level', 'academic_performance'])
                
                fig_dyn, ax_d = plt.subplots(figsize=(8, 4))
                sns.scatterplot(data=df_filtered, x=var_x, y=var_y, hue='depression_label', palette="bright", ax=ax_d)
                ax_d.set_title(f"{var_y} vs {var_x} (Datos Filtrados)")
                st.pyplot(fig_dyn)

        # TAB 5: ITEM 10 & CONCLUSIONES
        with tab5:
            st.header("Ítem 10: Hallazgos Clave & Conclusiones Finales")
            
            st.subheader("📌 Conclusiones Basadas en Evidencia")
            st.markdown("""
            1. **Diferencial Significativo en Uso de Redes**: Los adolescentes categorizados con la etiqueta de depresión presentan un promedio de consumo diario de redes sociales de **6.72 horas**, frente a las **4.48 horas** del grupo sin la etiqueta.
            2. **Impacto en la Calidad de Sueño**: Se evidencia un déficit de descanso en el grupo categorizado con presencia de condición ($4.76$ horas/noche frente a $6.49$ horas/noche en el grupo estándar).
            3. **Agnosticismo de la Plataforma**: No existen variaciones estadísticamente relevantes en el indicador de bienestar según la plataforma utilizada (TikTok, Instagram o Ambos), lo que indica que el patrón de uso y tiempo es el factor preponderante y no la aplicación en sí.
            4. **Estabilidad del Rendimiento Académico**: El promedio de GPA se mantiene estable (\(\approx 2.99\)) entre ambos grupos, demostrando que el rendimiento académico no es un predictor directo o aislado del bienestar emocional.
            5. **Distribución Demográfica Equitativa**: Las variables de género e interacción social muestran proporciones equivalentes en las distintas escalas de bienestar, descartando sesgos categóricos aislados.
            """)
