import streamlit as st
import pandas as pd

# Configuración
st.set_page_config(page_title="Calculadora Rentabilidad", layout="wide")
st.markdown("""
<style>
    .main { padding: 20px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 45px; font-size: 16px; }
    .result-positive { color: green; font-weight: bold; font-size: 18px; }
    .result-negative { color: red; font-weight: bold; font-size: 18px; }
    .product-box { background: #f0f8ff; padding: 15px; border-radius: 10px; margin: 10px 0; }
    .total-box { background: #007bff; color: white; padding: 20px; border-radius: 10px; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# Base de datos de productos COMPLETA
PRODUCTOS = {
    1: {'nombre': 'Tomate', 'costo': 3.00, 'precio': 4.50},
    2: {'nombre': 'Papa', 'costo': 2.50, 'precio': 4.00},
    3: {'nombre': 'Zanahoria', 'costo': 2.00, 'precio': 3.50},
    4: {'nombre': 'Cebolla', 'costo': 2.80, 'precio': 4.20},
    5: {'nombre': 'Lechuga', 'costo': 1.50, 'precio': 2.50},
    6: {'nombre': 'Espinaca', 'costo': 1.80, 'precio': 3.00},
    7: {'nombre': 'Pimiento', 'costo': 3.20, 'precio': 5.00},
    8: {'nombre': 'Ajo', 'costo': 1.20, 'precio': 2.50},
    9: {'nombre': 'Maíz', 'costo': 2.00, 'precio': 3.20},
    10: {'nombre': 'Frijol', 'costo': 3.50, 'precio': 5.50},
    11: {'nombre': 'Lenteja', 'costo': 4.00, 'precio': 6.50},
    12: {'nombre': 'Arroz', 'costo': 2.70, 'precio': 4.00},
    13: {'nombre': 'Trigo', 'costo': 2.40, 'precio': 3.80},
    14: {'nombre': 'Soya', 'costo': 3.00, 'precio': 4.80},
    15: {'nombre': 'Calabaza', 'costo': 2.10, 'precio': 3.50},
    16: {'nombre': 'Pepino', 'costo': 1.90, 'precio': 3.00},
    17: {'nombre': 'Sandía', 'costo': 5.00, 'precio': 7.50},
    18: {'nombre': 'Melón', 'costo': 4.50, 'precio': 7.00},
    19: {'nombre': 'Fresa', 'costo': 6.00, 'precio': 9.00},
    20: {'nombre': 'Plátano', 'costo': 2.60, 'precio': 4.00},
    21: {'nombre': 'Banano', 'costo': 2.80, 'precio': 4.20},
    22: {'nombre': 'Mango', 'costo': 3.50, 'precio': 5.50},
    23: {'nombre': 'Piña', 'costo': 4.20, 'precio': 6.50},
    24: {'nombre': 'Aguacate', 'costo': 5.00, 'precio': 8.00},
    25: {'nombre': 'Naranja', 'costo': 3.00, 'precio': 4.80},
    26: {'nombre': 'Limón', 'costo': 2.00, 'precio': 3.50},
    27: {'nombre': 'Mandarina', 'costo': 2.80, 'precio': 4.50},
    28: {'nombre': 'Uva', 'costo': 6.00, 'precio': 9.50},
    29: {'nombre': 'Manzana', 'costo': 4.00, 'precio': 6.50},
    30: {'nombre': 'Pera', 'costo': 3.80, 'precio': 6.00},
    31: {'nombre': 'Durazno', 'costo': 4.50, 'precio': 7.00},
    32: {'nombre': 'Ciruela', 'costo': 4.20, 'precio': 6.80},
    33: {'nombre': 'Higo', 'costo': 5.50, 'precio': 8.50},
    34: {'nombre': 'Cereza', 'costo': 7.00, 'precio': 10.50},
    35: {'nombre': 'Coco', 'costo': 3.50, 'precio': 5.50},
    36: {'nombre': 'Caña de Azúcar', 'costo': 2.20, 'precio': 3.80},
    37: {'nombre': 'Café Verde', 'costo': 6.00, 'precio': 9.00},
    38: {'nombre': 'Cacao', 'costo': 6.50, 'precio': 10.00},
    39: {'nombre': 'Alcachofa', 'costo': 3.00, 'precio': 4.80},
    40: {'nombre': 'Brócoli', 'costo': 2.80, 'precio': 4.40},
    41: {'nombre': 'Coliflor', 'costo': 3.00, 'precio': 4.50},
    42: {'nombre': 'Berenjena', 'costo': 2.90, 'precio': 4.60},
    43: {'nombre': 'Rábano', 'costo': 1.60, 'precio': 2.50},
    44: {'nombre': 'Apio', 'costo': 2.10, 'precio': 3.40},
    45: {'nombre': 'Nopal', 'costo': 1.50, 'precio': 2.50},
    46: {'nombre': 'Chayote', 'costo': 2.20, 'precio': 3.60},
    47: {'nombre': 'Betabel', 'costo': 2.00, 'precio': 3.20},
    48: {'nombre': 'Jengibre', 'costo': 5.00, 'precio': 8.00},
    49: {'nombre': 'Yerbabuena', 'costo': 1.00, 'precio': 2.00},
    50: {'nombre': 'Romero', 'costo': 1.20, 'precio': 2.20}
}

# Inicializar lista de venta
if 'venta_actual' not in st.session_state:
    st.session_state.venta_actual = []

# Interfaz
st.title("🛒 Calculadora de Rentabilidad")
st.write("Sistema interno para cálculo de ganancias")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📦 Seleccionar Producto")
    producto_option = st.selectbox(
        "Producto:",
        options=list(PRODUCTOS.keys()),
        format_func=lambda x: f"{PRODUCTOS[x]['nombre']} - ${PRODUCTOS[x]['precio']}",
        key="producto_select"
    )
    
    cantidad = st.slider("Cantidad:", 1, 100, 1, key="cantidad_slider")
    descuento = st.slider("Descuento (%):", 0, 100, 0, key="descuento_slider")
    
    if st.button("➕ Agregar a Venta", type="primary", key="agregar_btn"):
        producto = PRODUCTOS[producto_option]
        precio_final = producto['precio'] * (1 - descuento/100)
        ganancia = (precio_final - producto['costo']) * cantidad
        
        st.session_state.venta_actual.append({
            'producto': producto['nombre'],
            'cantidad': cantidad,
            'descuento': descuento,
            'precio_final': precio_final,
            'ganancia': ganancia
        })
        
        st.success(f"✅ {producto['nombre']} agregado!")

with col2:
    st.markdown("### 📊 Resultados")
    
    if st.session_state.venta_actual:
        st.markdown("#### 📋 Productos en Venta:")
        for i, item in enumerate(st.session_state.venta_actual, 1):
            st.markdown(f"""
            <div class='product-box'>
                <b>{i}. {item['producto']} x{item['cantidad']}</b><br>
                Descuento: {item['descuento']}% | Ganancia: 
                <span class='{'result-positive' if item['ganancia'] >= 0 else 'result-negative'}'>
                    ${item['ganancia']:,.2f}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Calcular totales
        total_ganancia = sum(item['ganancia'] for item in st.session_state.venta_actual)
        total_ingresos = sum(item['precio_final'] * item['cantidad'] for item in st.session_state.venta_actual)
        
        st.markdown(f"""
        <div class='total-box'>
            <h3>💰 TOTALES</h3>
            <p>Ingresos: <b>${total_ingresos:,.2f}</b></p>
            <p>Ganancia: <span class='{'result-positive' if total_ganancia >= 0 else 'result-negative'}'><b>${total_ganancia:,.2f}</b></span></p>
            <p>Margen: <b>{(total_ganancia/total_ingresos*100 if total_ingresos > 0 else 0):.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Nueva Venta", key="nueva_venta_btn"):
            st.session_state.venta_actual = []
            st.rerun()
    else:
        st.info("👆 Agrega productos para ver resultados")

st.markdown("---")
st.markdown("**© 2024 - Sistema interno de rentabilidad**")
