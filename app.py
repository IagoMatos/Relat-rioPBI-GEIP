import streamlit as st
import pandas as pd
import re
import io
from google import genai
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analista IA - GEIP", page_icon="🏢", layout="wide")

def criar_pdf_buffer(texto):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    if 'Disclaimer' not in styles:
        styles.add(ParagraphStyle(
            name='Disclaimer', parent=styles['Normal'], fontSize=8,
            textColor='gray', alignment=1, fontName='Helvetica-Oblique'
        ))

    story = [
        Paragraph("<b>GEIP - Relatório Executivo Gerencial</b>", styles["Heading1"]),
        Spacer(1, 20)
    ]

    texto_tratado = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
    for linha in texto_tratado.split('\n'):
        linha = linha.strip()
        if not linha:
            story.append(Spacer(1, 10))
            continue
        estilo = styles["Heading2"] if linha.startswith('#') else styles["Normal"]
        linha = linha.replace('#', '').strip()
        story.append(Paragraph(linha, estilo))
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color="lightgrey"))
    story.append(Paragraph("Este relatório foi gerado por Inteligência Artificial e não substitui a análise humana.", styles["Disclaimer"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --- CSS REFINADO (AJUSTE DE ESPAÇAMENTO E UNIFICAÇÃO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700&display=swap');
    
    /* Remove o espaço em branco exagerado no topo do Streamlit */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }

    .stApp {
        background-color: #023440;
        font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
    }

    /* Bloco Unificado (Cabeçalho + Corpo) */
    .unified-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        max-width: 900px;
        margin: 0 auto;
        overflow: hidden; /* Garante que as bordas arredondadas cortem o conteúdo */
    }

    /* Cabeçalho Interno */
    .header-geip {
        background-color: #ffffff;
        padding: 30px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 5px solid #018DA6;
    }

    /* Área de Conteúdo */
    .content-geip {
        padding: 40px;
        color: #333333;
    }

    /* Estilização do File Uploader para não ficar cinza */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #f8f9fa;
        border: 2px dashed #018DA6;
    }

    /* Botões Padrão GEIP */
    .stButton>button {
        background-color: #018DA6;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 25px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #279eb3;
        color: white;
    }

    /* Badge IA Corporativa */
    .badge-ia {
        background-color: #018DA6;
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .highlight-blue {
        color: #bff9ff;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ESTRUTURA UNIFICADA DO APP ---
st.markdown(f"""
    <div class="unified-card">
        <div class="header-geip">
            <div>
                <h2 style="margin:0; color: #018DA6; font-size: 26px;">SISTEMA DE ANÁLISE GEIP</h2>
                <p style="margin:0; color: #666; font-size: 14px;">Gestão de Infraestrutura e Projetos - FHEMIG</p>
            </div>
            <div class="badge-ia">IA CORPORATIVA</div>
        </div>
        <div class="content-geip">
            <h3 style="margin-top:0; color: #018DA6; font-size: 20px;">📊 Gerador de Relatórios Estratégicos</h3>
            <p style="color: #555;">Faça o upload do arquivo Excel exportado do Power BI para iniciar a redação do relatório executivo.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Agora o componente de upload fica logo abaixo, mas vamos usar um container para manter a margem
with st.container():
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        # Colocamos o seletor de arquivo aqui para alinhar com o card
        api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Key", type="password")
        arquivo = st.file_uploader("", type="xlsx") # Título vazio pois já colocamos no HTML

        if arquivo and api_key:
            if st.button("🚀 INICIAR ANÁLISE DE DADOS"):
                # ... sua lógica da IA aqui ...
                pass

# --- RODAPÉ ---
st.markdown("""
    <div style="text-align: center; margin-top: 40px;">
        <p class="highlight-blue">“Transformando dados em decisões estratégicas para a infraestrutura.”</p>
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); width: 50%; margin: 20px auto;">
        <a href="https://fhemigmg.sharepoint.com/sites/GEIP" target="_blank" 
           style="background-color: #018DA6; color: white; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px;">
           Acessar Portal GEIP
        </a>
    </div>
    """, unsafe_allow_html=True)
