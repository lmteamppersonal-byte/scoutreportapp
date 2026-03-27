"""
Módulo de exportação para PDF
Gera relatórios profissionais em PDF
"""

import io
import base64
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from config import CATEGORY_COLORS


class ScoutReportPDFExporter:
    """Exporta relatórios de Scout em formato PDF profissional"""

    def __init__(self, largura_pagina: float = 21, altura_pagina: float = 29.7):
        """
        Inicializa o exportador
        
        Args:
            largura_pagina: Largura em cm (A4 = 21)
            altura_pagina: Altura em cm (A4 = 29.7)
        """
        self.page_width = largura_pagina * cm
        self.page_height = altura_pagina * cm
        self.styles = self._configurar_estilos()

    def _configurar_estilos(self) -> Dict:
        """
        Configura estilos personalizados para o relatório
        
        Returns:
            Dict com estilos ReportLab
        """
        default_styles = getSampleStyleSheet()
        styles = {}
        
        # Título principal
        styles['titulo_principal'] = ParagraphStyle(
            'TituloPrincipal',
            parent=default_styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1C3144'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Subtítulo
        styles['subtitulo'] = ParagraphStyle(
            'Subtitulo',
            parent=default_styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2C5282'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        # Corpo de texto
        styles['corpo'] = ParagraphStyle(
            'Corpo',
            parent=default_styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            textColor=colors.HexColor('#333333')
        )
        
        # Destaque
        styles['destaque'] = ParagraphStyle(
            'Destaque',
            parent=default_styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#E74C3C'),
            fontName='Helvetica-Bold'
        )
        
        return styles

    def _criar_cabecalho(self) -> Table:
        """
        Cria cabecalho do relatório com informações do clube
        
        Returns:
            Table com cabecalho
        """
        cabecalho_data = [[
            Paragraph("<b>⚽ SCOUT REPORT PRO</b>", self.styles['titulo_principal']),
        ]]
        
        cabecalho = Table(cabecalho_data, colWidths=[self.page_width - 2*cm])
        cabecalho.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BORDER', (0, 0), (-1, -1), 0),
        ]))
        
        return cabecalho

    def _criar_secao_info_jogador(
        self,
        nome: str,
        posicao: str,
        clube: str,
        idade: int,
        valor_mercado: str,
        pe_dominante: str,
        nacionalidade: str
    ) -> Table:
        """
        Cria secção de informação pessoal do jogador
        
        Args:
            nome, posicao, clube, idade, valor_mercado, pe_dominante, nacionalidade
            
        Returns:
            Table formatada
        """
        info_data = [
            [
                f"<b>Nome:</b> {nome}",
                f"<b>Posição:</b> {posicao}",
                f"<b>Clube:</b> {clube}"
            ],
            [
                f"<b>Idade:</b> {idade} anos",
                f"<b>Pé Dominante:</b> {pe_dominante}",
                f"<b>Nacionalidade:</b> {nacionalidade}"
            ],
            [
                f"<b>Valor de Mercado:</b> {valor_mercado}",
                "",
                ""
            ]
        ]
        
        info_table = Table(info_data, colWidths=[6*cm, 6*cm, 6*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ECEFF1')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.grey),
        ]))
        
        return info_table

    def _criar_secao_avaliacoes(
        self,
        categorias_medias: Dict[str, float]
    ) -> Table:
        """
        Cria secção com avaliações por pilares
        
        Args:
            categorias_medias: Dict {categoria: média}
            
        Returns:
            Table formatada
        """
        dados = [["Pilar", "Score", "Classificação"]]
        
        for categoria, media in categorias_medias.items():
            if media >= 80:
                classificacao = "⭐ Excelente"
                cor_fundo = colors.HexColor('#D4EDDA')
            elif media >= 65:
                classificacao = "✓ Bom"
                cor_fundo = colors.HexColor('#D1ECF1')
            elif media >= 50:
                classificacao = "→ Médio"
                cor_fundo = colors.HexColor('#FFF3CD')
            else:
                classificacao = "↓ Abaixo da Média"
                cor_fundo = colors.HexColor('#F8D7DA')
            
            dados.append([
                Paragraph(f"<b>{categoria}</b>", self.styles['corpo']),
                Paragraph(f"<b>{media:.1f}/100</b>", self.styles['corpo']),
                Paragraph(classificacao, self.styles['corpo'])
            ])
        
        table = Table(dados, colWidths=[5*cm, 4*cm, 6*cm])
        
        # Estilo com cores alternadas
        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ]
        
        # Alternância de cores nas linhas
        for i in range(1, len(dados)):
            if i % 2 == 0:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F9FA')))
            else:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#FFFFFF')))
            style_cmds.append(('TOPPADDING', (0, i), (-1, i), 8))
            style_cmds.append(('BOTTOMPADDING', (0, i), (-1, i), 8))
        
        table.setStyle(TableStyle(style_cmds))
        
        return table

    def _criar_secao_analise(
        self,
        texto_analise: str,
        forcas: List[str],
        arestas: List[str]
    ) -> List:
        """
        Cria secção de análise textual e pontos chave
        
        Args:
            texto_analise: Texto de análise descritiva
            forcas: Lista com pontos fortes
            arestas: Lista com áreas a desenvolver
            
        Returns:
            List com elementos para adicionar ao PDF
        """
        elementos = []
        
        # Análise descritiva
        elementos.append(Paragraph("<b>Análise Descritiva</b>", self.styles['subtitulo']))
        elementos.append(Paragraph(texto_analise, self.styles['corpo']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Pontos fortes
        elementos.append(Paragraph("<b>💪 Pontos Fortes</b>", self.styles['subtitulo']))
        for forca in forcas:
            elementos.append(Paragraph(f"• {forca}", self.styles['corpo']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Áreas a desenvolver
        elementos.append(Paragraph("<b>📍 Áreas a Desenvolver</b>", self.styles['subtitulo']))
        for aresta in arestas:
            elementos.append(Paragraph(f"• {aresta}", self.styles['corpo']))
        
        return elementos

    def _criar_rodape(self) -> Paragraph:
        """
        Cria rodapé com informação de data e confidencialidade
        
        Returns:
            Paragraph com rodapé
        """
        data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
        return Paragraph(
            f"<i>Relatório gerado em {data_geracao} | Scout Report Pro v1.0 | Uso Confidencial - Direção Desportiva</i>",
            self.styles['corpo']
        )

    def gerar_relatorio(
        self,
        nome: str,
        posicao: str,
        clube: str,
        idade: int,
        valor_mercado: str,
        pe_dominante: str,
        nacionalidade: str,
        categorias_medias: Dict[str, float],
        texto_analise: str,
        forcas: List[str],
        arestas: List[str],
        imagem_jogador_path: Optional[str] = None,
        imagem_radar_path: Optional[str] = None
    ) -> io.BytesIO:
        """
        Gera PDF completo do relatório
        
        Args:
            nome, posicao, clube, idade, valor_mercado, pe_dominante, nacionalidade
            categorias_medias, texto_analise, forcas, arestas
            imagem_jogador_path: Caminho para foto (opcional)
            imagem_radar_path: Caminho para gráfico radar (opcional)
            
        Returns:
            BytesIO com PDF gerado
        """
        buffer = io.BytesIO()
        
        # Cria documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm
        )
        
        elementos = []
        
        # 1. Cabeçalho
        elementos.append(self._criar_cabecalho())
        elementos.append(Spacer(1, 0.5*cm))
        
        # 2. Info do Jogador
        elementos.append(self._criar_secao_info_jogador(
            nome, posicao, clube, idade, valor_mercado, pe_dominante, nacionalidade
        ))
        elementos.append(Spacer(1, 0.5*cm))
        
        # 3. Foto (se disponível)
        if imagem_jogador_path:
            try:
                img = Image(imagem_jogador_path, width=3*cm, height=4*cm)
                elementos.append(img)
                elementos.append(Spacer(1, 0.3*cm))
            except:
                pass
        
        # 4. Avaliações
        elementos.append(Paragraph("<b>Avaliação por Pilares</b>", self.styles['subtitulo']))
        elementos.append(self._criar_secao_avaliacoes(categorias_medias))
        elementos.append(Spacer(1, 0.5*cm))
        
        # 5. Gráfico Radar (se disponível)
        if imagem_radar_path:
            try:
                img_radar = Image(imagem_radar_path, width=12*cm, height=10*cm)
                elementos.append(img_radar)
                elementos.append(Spacer(1, 0.5*cm))
            except:
                pass
        
        # 6. PageBreak para segunda página
        elementos.append(PageBreak())
        
        # 7. Análise Descritiva
        elementos.extend(self._criar_secao_analise(texto_analise, forcas, arestas))
        elementos.append(Spacer(1, 1*cm))
        
        # 8. Rodapé
        elementos.append(self._criar_rodape())
        
        # Constrói PDF
        doc.build(elementos)
        buffer.seek(0)
        
        return buffer

    @staticmethod
    def para_download_link(buffer: io.BytesIO, nome_arquivo: str) -> Tuple[bytes, str]:
        """
        Prepara dados para download
        
        Args:
            buffer: BytesIO com PDF
            nome_arquivo: Nome do arquivo para download
            
        Returns:
            Tuple (bytes, nome_arquivo)
        """
        return buffer.getvalue(), nome_arquivo


class DashboardHTMLExporter:
    """Exporta dashboard executivo em HTML"""

    @staticmethod
    def gerar_html_one_pager(
        nome: str,
        posicao: str,
        clube: str,
        idade: int,
        valor_mercado: str,
        categorias_medias: Dict[str, float],
        metricas_avancadas: Dict[str, float],
        texto_analise: str,
        imagem_radar_base64: Optional[str] = None,
        imagem_heatmap_base64: Optional[str] = None
    ) -> str:
        """
        Gera uma página HTML estilo one-pager para impressão
        
        Args:
            nome, posicao, clube, idade, valor_mercado
            categorias_medias, metricas_avancadas, texto_analise
            imagem_radar_base64, imagem_heatmap_base64
            
        Returns:
            String HTML
        """
        # Calcula score geral
        score_geral = sum(categorias_medias.values()) / len(categorias_medias) if categorias_medias else 0
        
        # Constrói cards de categorias
        categoria_cards = ""
        for cat, valor in categorias_medias.items():
            cor = CATEGORY_COLORS.get(cat, "#808080")
            categoria_cards += f"""
            <div class="card-categoria" style="border-left: 5px solid {cor};">
                <div class="cat-titulo">{cat}</div>
                <div class="cat-valor">{valor:.1f}/100</div>
            </div>
            """
        
        # Constrói cards de métricas avançadas
        metricas_cards = ""
        for metrica, valor in metricas_avancadas.items():
            metricas_cards += f"""
            <div class="metric-card">
                <div class="metric-nome">{metrica}</div>
                <div class="metric-valor">{valor:.2f}</div>
            </div>
            """
        
        # Imagens (se disponíveis)
        imagem_radar_html = f'<img src="data:image/png;base64,{imagem_radar_base64}" class="chart-img" />' if imagem_radar_base64 else ""
        imagem_heatmap_html = f'<img src="data:image/png;base64,{imagem_heatmap_base64}" class="chart-img" />' if imagem_heatmap_base64 else ""
        
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Scout Report - {nome}</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                
                .header {{
                    text-align: center;
                    border-bottom: 3px solid #E74C3C;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                
                .header h1 {{ font-size: 36px; color: #1C3144; margin-bottom: 10px; }}
                .header-info {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 14px; }}
                .header-item {{ text-align: left; }}
                .header-label {{ font-weight: bold; color: #555; }}
                .header-value {{ color: #E74C3C; font-size: 16px; }}
                
                .score-geral {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-align: center;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    font-size: 18px;
                }}
                
                .score-number {{ font-size: 48px; font-weight: bold; }}
                
                .section {{ margin-bottom: 40px; }}
                .section h2 {{ font-size: 20px; color: #1C3144; margin-bottom: 15px; border-bottom: 2px solid #3498DB; padding-bottom: 10px; }}
                
                .categorias-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 15px;
                    margin-bottom: 20px;
                }}
                
                .card-categoria {{
                    background: #F8F9FA;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    transition: transform 0.2s;
                }}
                
                .card-categoria:hover {{ transform: translateY(-5px); }}
                .cat-titulo {{ font-size: 12px; color: #666; margin-bottom: 10px; text-transform: uppercase; }}
                .cat-valor {{ font-size: 32px; font-weight: bold; color: #E74C3C; }}
                
                .metricas-grid {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                }}
                
                .metric-card {{
                    background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
                    padding: 15px;
                    border-radius: 6px;
                    border-left: 4px solid #667eea;
                }}
                
                .metric-nome {{ font-size: 12px; color: #666; margin-bottom: 8px; }}
                .metric-valor {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                
                .analysis-text {{
                    background: #ECEFF1;
                    padding: 20px;
                    border-radius: 8px;
                    line-height: 1.6;
                    text-align: justify;
                }}
                
                .charts-container {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                }}
                
                .chart-img {{
                    max-width: 100%;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #999;
                    margin-top: 40px;
                    border-top: 1px solid #DDD;
                    padding-top: 20px;
                }}
                
                @media print {{
                    body {{ margin: 0; padding: 0; }}
                    .container {{ max-width: 100%; padding: 10mm; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚽ Scout Report</h1>
                    <div class="header-info">
                        <div class="header-item">
                            <div class="header-label">Jogador</div>
                            <div class="header-value">{nome}</div>
                        </div>
                        <div class="header-item">
                            <div class="header-label">Posição</div>
                            <div class="header-value">{posicao}</div>
                        </div>
                        <div class="header-item">
                            <div class="header-label">Clube</div>
                            <div class="header-value">{clube}</div>
                        </div>
                        <div class="header-item">
                            <div class="header-label">Idade</div>
                            <div class="header-value">{idade} anos</div>
                        </div>
                    </div>
                </div>
                
                <div class="score-geral">
                    <div>SCORE GERAL</div>
                    <div class="score-number">{score_geral:.1f}</div>
                    <div>/100</div>
                </div>
                
                <div class="section">
                    <h2>📊 Avaliação por Pilares</h2>
                    <div class="categorias-grid">
                        {categoria_cards}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📈 Métricas Avançadas</h2>
                    <div class="metricas-grid">
                        {metricas_cards}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📝 Análise Descritiva</h2>
                    <div class="analysis-text">
                        {texto_analise}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📊 Visualizações</h2>
                    <div class="charts-container">
                        {imagem_radar_html}
                        {imagem_heatmap_html}
                    </div>
                </div>
                
                <div class="footer">
                    <p>Scout Report Pro v1.0 | Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")} | Uso Confidencial - Direção Desportiva</p>
                </div>
            </div>
            
            <script>
                function imprimir() {{ window.print(); }}
            </script>
        </body>
        </html>
        """
        
        return html
