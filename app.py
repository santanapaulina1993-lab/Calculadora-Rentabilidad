import streamlit as st
import pandas as pd

# Configuración
st.set_page_config(page_title="Calculadora Rentabilidad Inteligente", layout="wide")
st.markdown("""
<style>
    .main { padding: 20px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 45px; font-size: 16px; }
    .result-positive { color: green; font-weight: bold; font-size: 18px; }
    .result-negative { color: red; font-weight: bold; font-size: 18px; }
    .product-box { background: #f0f8ff; padding: 15px; border-radius: 10px; margin: 10px 0; }
    .total-box { background: #007bff; color: white; padding: 20px; border-radius: 10px; margin: 20px 0; }
    .warning-box { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 10px; }
    .edit-box { background: #e8f5e8; padding: 10px; border-radius: 8px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# Base de datos de productos COMPLETA
PRODUCTOS = {
    1: {'nombre': 'Tomate', 'costo': 3.00, 'precio': 4.50},
    2: {'nombre': 'Papa', 'costo': 2.50, 'precio': 4.00},
    3: {'nombre': 'Zanahoria', 'costo': 2.00, 'precio': 3.50},
    # ... (todos tus 50 productos aquí)
    50: {'nombre': 'Romero', 'costo': 1.20, 'precio': 2.20}
}

# Inicializar lista de venta
if 'venta_actual' not in st.session_state:
    st.session_state.venta_actual = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# Función para calcular ganancia
def calcular_ganancia(producto_id, cantidad, descuento):
    producto = PRODUCTOS[producto_id]
    precio_final = producto['precio'] * (1 - descuento/100)
    ganancia = (precio_final - producto['costo']) * cantidad
    return ganancia, precio_final

# Interfaz
st.title("📊 Calculadora de Rentabilidad Inteligente")
st.write("Sistema para optimizar ganancias en tiempo real")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📦 Agregar/Editar Producto")
    
    # Si estamos editando, mostrar datos actuales
    if st.session_state.edit_index is not None:
        item = st.session_state.venta_actual[st.session_state.edit_index]
        st.info(f"✏️ Editando: {item['producto']}")
    
    producto_option = st.selectbox(
        "Seleccionar Producto:",
        options=list(PRODUCTOS.keys()),
        format_func=lambda x: f"{PRODUCTOS[x]['nombre']} - ${PRODUCTOS[x]['precio']}",
        key="producto_select"
    )
    
    cantidad = st.slider("Cantidad:", 1, 100, 
                        value=st.session_state.venta_actual[st.session_state.edit_index]['cantidad'] 
                        if st.session_state.edit_index is not None else 1,
                        key="cantidad_slider")
    
    descuento = st.slider("Descuento (%):", 0, 100, 
                         value=st.session_state.venta_actual[st.session_state.edit_index]['descuento'] 
                         if st.session_state.edit_index is not None else 0,
                         key="descuento_slider")
    
    # Botones para agregar o actualizar
    if st.session_state.edit_index is not None:
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💾 Guardar Cambios", type="primary"):
                ganancia, precio_final = calcular_ganancia(producto_option, cantidad, descuento)
                st.session_state.venta_actual[st.session_state.edit_index] = {
                    'producto': PRODUCTOS[producto_option]['nombre'],
                    'producto_id': producto_option,
                    'cantidad': cantidad,
                    'descuento': descuento,
                    'precio_final': precio_final,
                    'ganancia': ganancia
                }
                st.session_state.edit_index = None
                st.success("✅ Cambios guardados!")
                st.rerun()
        with col_btn2:
            if st.button("❌ Cancelar"):
                st.session_state.edit_index = None
                st.rerun()
    else:
        if st.button("➕ Agregar a Venta", type="primary"):
            ganancia, precio_final = calcular_ganancia(producto_option, cantidad, descuento)
            st.session_state.venta_actual.append({
                'producto': PRODUCTOS[producto_option]['nombre'],
                'producto_id': producto_option,
                'cantidad': cantidad,
                'descuento': descuento,
                'precio_final': precio_final,
                'ganancia': ganancia
            })
            st.success(f"✅ {PRODUCTOS[producto_option]['nombre']} agregado!")

with col2:
    st.markdown("### 📋 Venta Actual - Editable")
    
    if st.session_state.venta_actual:
        total_ganancia = sum(item['ganancia'] for item in st.session_state.venta_actual)
        
        # Advertencia si hay pérdida
        if total_ganancia < 0:
            st.markdown("""
            <div class='warning-box'>
                ⚠️ <b>ESTÁS PERDIENDO DINERO!</b><br>
                Ganancia total negativa: <span class='result-negative'>${:,.2f}</span>
            </div>
            """.format(total_ganancia), unsafe_allow_html=True)
        
        # Mostrar productos con botones de edición
        for i, item in enumerate(st.session_state.venta_actual):
            col_info, col_action = st.columns([3, 1])
            
            with col_info:
                ganancia_class = "result-positive" if item['ganancia'] >= 0 else "result-negative"
                st.markdown(f"""
                <div class='product-box'>
                    <b>{i+1}. {item['producto']} x{item['cantidad']}</b><br>
                    Descuento: {item['descuento']}% | 
                    Ganancia: <span class='{ganancia_class}'>${item['ganancia']:,.2f}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_action:
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.rerun()
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.venta_actual.pop(i)
                    st.success("Producto eliminado!")
                    st.rerun()
        
        # Calcular totales
        total_ingresos = sum(item['precio_final'] * item['cantidad'] for item in st.session_state.venta_actual)
        total_costos = sum(PRODUCTOS[item['producto_id']]['costo'] * item['cantidad'] for item in st.session_state.venta_actual)
        
        st.markdown(f"""
        <div class='total-box'>
            <h3>💰 TOTALES DE VENTA</h3>
            <p>Ingresos: <b>${total_ingresos:,.2f}</b></p>
            <p>Costos: <b>${total_costos:,.2f}</b></p>
            <p>Ganancia: <span class='{'result-positive' if total_ganancia >= 0 else 'result-negative'}'><b>${total_ganancia:,.2f}</b></span></p>
            <p>Margen: <b>{(total_ganancia/total_ingresos*100 if total_ingresos > 0 else 0):.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recomendaciones inteligentes
        if total_ganancia < 0:
            st.markdown("### 💡 Recomendaciones para Ganar:")
            productos_perdedores = [item for item in st.session_state.venta_actual if item['ganancia'] < 0]
            
            for item in productos_perdedores:
                producto_data = PRODUCTOS[item['producto_id']]
                st.write(f"**{item['producto']}**: Estás perdiendo ${abs(item['ganancia']):.2f}")
                st.write(f"   - Reduce descuento o cantidad")
                st.write(f"   - Precio mínimo para no perder: ${producto_data['costo'] / (1 - item['descuento']/100):.2f}")
        
        if st.button("🔄 Nueva Venta", key="nueva_venta_btn"):
            st.session_state.venta_actual = []
            st.session_state.edit_index = None
            st.rerun()
            
    else:
        st.info("👆 Agrega productos para comenzar")

# Panel de análisis avanzado
st.markdown("---")
st.markdown("### 📈 Análisis de Optimización")

if st.session_state.venta_actual:
    df_venta = pd.DataFrame(st.session_state.venta_actual)
    
    col_anal1, col_anal2, col_anal3 = st.columns(3)
    
    with col_anal1:
        st.metric("Productos en Venta", len(st.session_state.venta_actual))
    
    with col_anal2:
        productos_rentables = sum(1 for item in st.session_state.venta_actual if item['ganancia'] >= 0)
        st.metric("Productos Rentables", productos_rentables)
    
    with col_anal3:
        productos_perdedores = sum(1 for item in st.session_state.venta_actual if item['ganancia'] < 0)
        st.metric("Productos con Pérdida", productos_perdedores)

st.markdown("---")
st.markdown("**© 2024 - Sistema Inteligente de Rentabilidad**")
