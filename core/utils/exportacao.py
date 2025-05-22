"""
Utilitários para exportação de dados em diferentes formatos.
"""

import csv
import io
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def exportar_para_csv(queryset, campos, nomes_campos, nome_arquivo="exportacao.csv"):
    """
    Exporta um queryset para um arquivo CSV.
    
    Args:
        queryset: QuerySet com os dados a serem exportados
        campos: Lista de nomes dos campos a serem exportados
        nomes_campos: Lista de nomes amigáveis para os cabeçalhos
        nome_arquivo: Nome do arquivo CSV a ser gerado
        
    Returns:
        HttpResponse: Resposta HTTP com o arquivo CSV
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    
    # Criar o escritor CSV
    writer = csv.writer(response)
    
    # Escrever cabeçalho
    writer.writerow(nomes_campos)
    
    # Escrever dados
    for obj in queryset:
        row = []
        for campo in campos:
            # Lidar com campos aninhados (usando __)
            if '__' in campo:
                partes = campo.split('__')
                valor = obj
                for parte in partes:
                    if hasattr(valor, parte):
                        valor = getattr(valor, parte)
                    else:
                        valor = ''
                        break
            else:
                # Verificar se é um método
                if hasattr(obj, campo) and callable(getattr(obj, campo)):
                    valor = getattr(obj, campo)()
                else:
                    valor = getattr(obj, campo, '')
            
            # Converter booleanos para Sim/Não
            if isinstance(valor, bool):
                valor = 'Sim' if valor else 'Não'
                
            row.append(valor)
        
        writer.writerow(row)
    
    return response

def exportar_para_pdf(queryset, campos, nomes_campos, titulo, nome_arquivo="exportacao.pdf", orientacao='retrato'):
    """
    Exporta um queryset para um arquivo PDF.
    
    Args:
        queryset: QuerySet com os dados a serem exportados
        campos: Lista de nomes dos campos a serem exportados
        nomes_campos: Lista de nomes amigáveis para os cabeçalhos
        titulo: Título do documento PDF
        nome_arquivo: Nome do arquivo PDF a ser gerado
        orientacao: Orientação do documento ('retrato' ou 'paisagem')
        
    Returns:
        HttpResponse: Resposta HTTP com o arquivo PDF
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    
    # Criar buffer para o PDF
    buffer = io.BytesIO()
    
    # Definir tamanho da página
    pagesize = landscape(letter) if orientacao == 'paisagem' else letter
    
    # Criar documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=pagesize, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = 1  # Centralizado
    
    # Título
    elements.append(Paragraph(titulo, title_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Preparar dados para a tabela
    data = [nomes_campos]  # Cabeçalho
    
    # Adicionar dados
    for obj in queryset:
        row = []
        for campo in campos:
            # Lidar com campos aninhados (usando __)
            if '__' in campo:
                partes = campo.split('__')
                valor = obj
                for parte in partes:
                    if hasattr(valor, parte):
                        valor = getattr(valor, parte)
                    else:
                        valor = ''
                        break
            else:
                # Verificar se é um método
                if hasattr(obj, campo) and callable(getattr(obj, campo)):
                    valor = getattr(obj, campo)()
                else:
                    valor = getattr(obj, campo, '')
            
            # Converter booleanos para Sim/Não
            if isinstance(valor, bool):
                valor = 'Sim' if valor else 'Não'
                
            row.append(valor)
        
        data.append(row)
    
    # Criar tabela
    table = Table(data)
    
    # Estilo da tabela
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    table.setStyle(style)
    elements.append(table)
    
    # Construir PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
