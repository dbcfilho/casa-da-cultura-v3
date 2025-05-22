from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.core.paginator import Paginator
import csv
import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .models import Pessoa, MensagemPadrao, DataComemorativa, RegistroEnvioMensagem
from .forms import (
    PessoaForm, MensagemPadraoForm, DataComemorativaForm, 
    EnvioMensagemForm, PessoaFilterForm
)

# Decorador personalizado para verificar permissões
def permissao_requerida(tipo_permissao):
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            # Verificar permissões com base no tipo de usuário
            if tipo_permissao == 'consulta':
                # Todos os usuários logados podem consultar
                pass
            elif tipo_permissao == 'cadastro':
                # Apenas usuários com permissão de cadastro ou admin
                if request.user.tipo_usuario == 'consulta':
                    messages.error(request, 'Você não tem permissão para esta operação.')
                    return redirect('core:home')
            elif tipo_permissao == 'admin':
                # Apenas administradores
                if request.user.tipo_usuario != 'admin':
                    messages.error(request, 'Você não tem permissão para esta operação.')
                    return redirect('core:home')
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

@login_required
def home(request):
    """
    View da página inicial do sistema.
    """
    # Contagem de pessoas cadastradas
    total_pessoas = Pessoa.objects.count()
    
    # Aniversariantes do dia
    hoje = timezone.now().date()
    aniversariantes_hoje = Pessoa.objects.filter(
        data_nascimento__day=hoje.day,
        data_nascimento__month=hoje.month
    ).count()
    
    # Aniversariantes do mês
    aniversariantes_mes = Pessoa.objects.filter(
        data_nascimento__month=hoje.month
    ).count()
    
    # Estatísticas de ajudas
    ajuda_hospital = Pessoa.objects.filter(ajuda_hospital=True).count()
    ajuda_creche = Pessoa.objects.filter(ajuda_creche=True).count()
    cesta_basica = Pessoa.objects.filter(recebeu_cesta_basica=True).count()
    ajuda_transporte = Pessoa.objects.filter(ajuda_transporte=True).count()
    
    context = {
        'total_pessoas': total_pessoas,
        'aniversariantes_hoje': aniversariantes_hoje,
        'aniversariantes_mes': aniversariantes_mes,
        'ajuda_hospital': ajuda_hospital,
        'ajuda_creche': ajuda_creche,
        'cesta_basica': cesta_basica,
        'ajuda_transporte': ajuda_transporte,
    }
    
    return render(request, 'core/home.html', context)

@login_required
def pessoa_lista(request):
    """
    View para listar pessoas cadastradas com filtros.
    """
    pessoas = Pessoa.objects.all()
    form_filtro = PessoaFilterForm(request.GET)
    
    # Aplicar filtros se o formulário for válido
    if form_filtro.is_valid():
        if form_filtro.cleaned_data.get('nome'):
            pessoas = pessoas.filter(nome_completo__icontains=form_filtro.cleaned_data['nome'])
        
        if form_filtro.cleaned_data.get('bairro'):
            pessoas = pessoas.filter(bairro__icontains=form_filtro.cleaned_data['bairro'])
        
        # Filtros booleanos
        for campo in ['pai_ou_mae', 'ajuda_hospital', 'ajuda_creche', 'recebeu_cesta_basica',
                     'participa_oficinas', 'tem_filhos', 'ajuda_transporte']:
            if form_filtro.cleaned_data.get(campo):
                pessoas = pessoas.filter(**{campo: True})
        
        # Aniversariantes do mês
        if form_filtro.cleaned_data.get('aniversariantes_mes'):
            hoje = timezone.now().date()
            pessoas = pessoas.filter(data_nascimento__month=hoje.month)
    
    # Paginação
    paginator = Paginator(pessoas, 20)  # 20 pessoas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form_filtro': form_filtro,
        'total_resultados': pessoas.count(),
    }
    
    return render(request, 'core/pessoa_lista.html', context)

@permissao_requerida('cadastro')
def pessoa_cadastro(request):
    """
    View para cadastro de nova pessoa.
    """
    if request.method == 'POST':
        form = PessoaForm(request.POST)
        if form.is_valid():
            pessoa = form.save()
            messages.success(request, f'Pessoa "{pessoa.nome_completo}" cadastrada com sucesso!')
            return redirect('core:pessoa_detalhe', pk=pessoa.pk)
    else:
        form = PessoaForm()
    
    return render(request, 'core/pessoa_form.html', {'form': form, 'titulo': 'Cadastrar Pessoa'})

@login_required
def pessoa_detalhe(request, pk):
    """
    View para exibir detalhes de uma pessoa.
    """
    pessoa = get_object_or_404(Pessoa, pk=pk)
    return render(request, 'core/pessoa_detalhe.html', {'pessoa': pessoa})

@permissao_requerida('cadastro')
def pessoa_editar(request, pk):
    """
    View para editar uma pessoa existente.
    """
    pessoa = get_object_or_404(Pessoa, pk=pk)
    
    if request.method == 'POST':
        form = PessoaForm(request.POST, instance=pessoa)
        if form.is_valid():
            pessoa = form.save()
            messages.success(request, f'Dados de "{pessoa.nome_completo}" atualizados com sucesso!')
            return redirect('core:pessoa_detalhe', pk=pessoa.pk)
    else:
        form = PessoaForm(instance=pessoa)
    
    return render(request, 'core/pessoa_form.html', {
        'form': form, 
        'titulo': f'Editar: {pessoa.nome_completo}',
        'pessoa': pessoa
    })

@permissao_requerida('admin')
def pessoa_excluir(request, pk):
    """
    View para excluir uma pessoa.
    """
    pessoa = get_object_or_404(Pessoa, pk=pk)
    
    if request.method == 'POST':
        nome = pessoa.nome_completo
        pessoa.delete()
        messages.success(request, f'Pessoa "{nome}" excluída com sucesso!')
        return redirect('core:pessoa_lista')
    
    return render(request, 'core/pessoa_excluir.html', {'pessoa': pessoa})

@login_required
def aniversariantes(request):
    """
    View para listar aniversariantes do dia e do mês.
    """
    hoje = timezone.now().date()
    
    # Aniversariantes do dia
    aniversariantes_hoje = Pessoa.objects.filter(
        data_nascimento__day=hoje.day,
        data_nascimento__month=hoje.month
    ).order_by('nome_completo')
    
    # Aniversariantes do mês
    aniversariantes_mes = Pessoa.objects.filter(
        data_nascimento__month=hoje.month
    ).exclude(
        data_nascimento__day=hoje.day
    ).order_by('data_nascimento__day', 'nome_completo')
    
    # Mensagens padrão para aniversário
    mensagens = MensagemPadrao.objects.filter(tipo='aniversario', ativa=True)
    
    context = {
        'aniversariantes_hoje': aniversariantes_hoje,
        'aniversariantes_mes': aniversariantes_mes,
        'mensagens': mensagens,
        'hoje': hoje,
    }
    
    return render(request, 'core/aniversariantes.html', context)

@permissao_requerida('cadastro')
def enviar_mensagem_aniversario(request, pk):
    """
    View para enviar mensagem de aniversário.
    """
    pessoa = get_object_or_404(Pessoa, pk=pk)
    
    if request.method == 'POST':
        form = EnvioMensagemForm(request.POST)
        if form.is_valid():
            mensagem = form.cleaned_data['mensagem']
            personalizar = form.cleaned_data['personalizar']
            conteudo = mensagem.conteudo
            
            if personalizar:
                conteudo = form.cleaned_data['conteudo_personalizado']
            
            # Aqui implementaríamos o envio real via WhatsApp
            # Por enquanto, apenas registramos o envio
            registro = RegistroEnvioMensagem(
                pessoa=pessoa,
                mensagem=mensagem,
                sucesso=True,
                observacao=f"Mensagem de aniversário enviada {'(personalizada)' if personalizar else ''}"
            )
            registro.save()
            
            messages.success(request, f'Mensagem enviada com sucesso para {pessoa.nome_completo}!')
            return redirect('core:aniversariantes')
    else:
        form = EnvioMensagemForm()
    
    return render(request, 'core/enviar_mensagem.html', {
        'form': form,
        'pessoa': pessoa,
        'titulo': f'Enviar Mensagem de Aniversário para {pessoa.nome_completo}'
    })

@permissao_requerida('cadastro')
def mensagem_lista(request):
    """
    View para listar mensagens padrão.
    """
    mensagens = MensagemPadrao.objects.all().order_by('tipo', '-data_atualizacao')
    return render(request, 'core/mensagem_lista.html', {'mensagens': mensagens})

@permissao_requerida('cadastro')
def mensagem_cadastro(request):
    """
    View para cadastrar nova mensagem padrão.
    """
    if request.method == 'POST':
        form = MensagemPadraoForm(request.POST)
        if form.is_valid():
            mensagem = form.save()
            messages.success(request, f'Mensagem "{mensagem.titulo}" cadastrada com sucesso!')
            return redirect('core:mensagem_lista')
    else:
        form = MensagemPadraoForm()
    
    return render(request, 'core/mensagem_form.html', {'form': form, 'titulo': 'Nova Mensagem Padrão'})

@permissao_requerida('cadastro')
def mensagem_editar(request, pk):
    """
    View para editar mensagem padrão existente.
    """
    mensagem = get_object_or_404(MensagemPadrao, pk=pk)
    
    if request.method == 'POST':
        form = MensagemPadraoForm(request.POST, instance=mensagem)
        if form.is_valid():
            mensagem = form.save()
            messages.success(request, f'Mensagem "{mensagem.titulo}" atualizada com sucesso!')
            return redirect('core:mensagem_lista')
    else:
        form = MensagemPadraoForm(instance=mensagem)
    
    return render(request, 'core/mensagem_form.html', {
        'form': form, 
        'titulo': f'Editar Mensagem: {mensagem.titulo}',
        'mensagem': mensagem
    })

@permissao_requerida('cadastro')
def data_comemorativa_lista(request):
    """
    View para listar datas comemorativas.
    """
    datas = DataComemorativa.objects.all().order_by('data')
    return render(request, 'core/data_comemorativa_lista.html', {'datas': datas})

@permissao_requerida('cadastro')
def data_comemorativa_cadastro(request):
    """
    View para cadastrar nova data comemorativa.
    """
    if request.method == 'POST':
        form = DataComemorativaForm(request.POST)
        if form.is_valid():
            data = form.save()
            messages.success(request, f'Data comemorativa "{data.nome}" cadastrada com sucesso!')
            return redirect('core:data_comemorativa_lista')
    else:
        form = DataComemorativaForm()
    
    return render(request, 'core/data_comemorativa_form.html', {'form': form, 'titulo': 'Nova Data Comemorativa'})

@permissao_requerida('cadastro')
def data_comemorativa_editar(request, pk):
    """
    View para editar data comemorativa existente.
    """
    data = get_object_or_404(DataComemorativa, pk=pk)
    
    if request.method == 'POST':
        form = DataComemorativaForm(request.POST, instance=data)
        if form.is_valid():
            data = form.save()
            messages.success(request, f'Data comemorativa "{data.nome}" atualizada com sucesso!')
            return redirect('core:data_comemorativa_lista')
    else:
        form = DataComemorativaForm(instance=data)
    
    return render(request, 'core/data_comemorativa_form.html', {
        'form': form, 
        'titulo': f'Editar Data: {data.nome}',
        'data': data
    })

@login_required
def exportar_pessoas_csv(request):
    """
    View para exportar lista de pessoas em formato CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pessoas_casa_da_cultura.csv"'
    
    # Criar o escritor CSV
    writer = csv.writer(response)
    
    # Escrever cabeçalho
    writer.writerow([
        'Nome Completo', 'CPF', 'RG', 'Data de Nascimento', 'Idade',
        'Endereço', 'Bairro', 'Cidade', 'Estado', 'CEP', 'Telefone', 'Email',
        'Pai/Mãe', 'Ajuda Hospital', 'Ajuda Creche', 'Recebeu Cesta Básica',
        'Participa Oficinas', 'Interesse Novas Turmas', 'Tem Filhos', 'Ajuda Transporte',
        'Observações', 'Data de Cadastro'
    ])
    
    # Obter pessoas com base nos filtros aplicados
    pessoas = Pessoa.objects.all()
    form_filtro = PessoaFilterForm(request.GET)
    
    # Aplicar filtros se o formulário for válido
    if form_filtro.is_valid():
        if form_filtro.cleaned_data.get('nome'):
            pessoas = pessoas.filter(nome_completo__icontains=form_filtro.cleaned_data['nome'])
        
        if form_filtro.cleaned_data.get('bairro'):
            pessoas = pessoas.filter(bairro__icontains=form_filtro.cleaned_data['bairro'])
        
        # Filtros booleanos
        for campo in ['pai_ou_mae', 'ajuda_hospital', 'ajuda_creche', 'recebeu_cesta_basica',
                     'participa_oficinas', 'tem_filhos', 'ajuda_transporte']:
            if form_filtro.cleaned_data.get(campo):
                pessoas = pessoas.filter(**{campo: True})
        
        # Aniversariantes do mês
        if form_filtro.cleaned_data.get('aniversariantes_mes'):
            hoje = timezone.now().date()
            pessoas = pessoas.filter(data_nascimento__month=hoje.month)
    
    # Escrever dados
    for pessoa in pessoas:
        writer.writerow([
            pessoa.nome_completo,
            pessoa.cpf,
            pessoa.rg or '',
            pessoa.data_nascimento.strftime('%d/%m/%Y'),
            pessoa.idade(),
            pessoa.endereco,
            pessoa.bairro,
            pessoa.cidade,
            pessoa.estado,
            pessoa.cep or '',
            pessoa.telefone,
            pessoa.email or '',
            'Sim' if pessoa.pai_ou_mae else 'Não',
            'Sim' if pessoa.ajuda_hospital else 'Não',
            'Sim' if pessoa.ajuda_creche else 'Não',
            'Sim' if pessoa.recebeu_cesta_basica else 'Não',
            'Sim' if pessoa.participa_oficinas else 'Não',
            'Sim' if pessoa.interesse_novas_turmas else 'Não',
            'Sim' if pessoa.tem_filhos else 'Não',
            'Sim' if pessoa.ajuda_transporte else 'Não',
            pessoa.observacoes or '',
            pessoa.data_cadastro.strftime('%d/%m/%Y %H:%M')
        ])
    
    return response

@login_required
def exportar_pessoas_pdf(request):
    """
    View para exportar lista de pessoas em formato PDF.
    """
    # Obter pessoas com base nos filtros aplicados
    pessoas = Pessoa.objects.all()
    form_filtro = PessoaFilterForm(request.GET)
    
    # Aplicar filtros se o formulário for válido
    if form_filtro.is_valid():
        if form_filtro.cleaned_data.get('nome'):
            pessoas = pessoas.filter(nome_completo__icontains=form_filtro.cleaned_data['nome'])
        
        if form_filtro.cleaned_data.get('bairro'):
            pessoas = pessoas.filter(bairro__icontains=form_filtro.cleaned_data['bairro'])
        
        # Filtros booleanos
        for campo in ['pai_ou_mae', 'ajuda_hospital', 'ajuda_creche', 'recebeu_cesta_basica',
                     'participa_oficinas', 'tem_filhos', 'ajuda_transporte']:
            if form_filtro.cleaned_data.get(campo):
                pessoas = pessoas.filter(**{campo: True})
        
        # Aniversariantes do mês
        if form_filtro.cleaned_data.get('aniversariantes_mes'):
            hoje = timezone.now().date()
            pessoas = pessoas.filter(data_nascimento__month=hoje.month)
    
    # Criar resposta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pessoas_casa_da_cultura.pdf"'
    
    # Criar documento PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    
    # Título
    elements.append(Paragraph("Lista de Pessoas - Casa da Cultura", title_style))
    elements.append(Paragraph(f"Data de geração: {timezone.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Paragraph(f"Total de registros: {pessoas.count()}", styles['Normal']))
    elements.append(Paragraph(" ", styles['Normal']))  # Espaço em branco
    
    # Dados para a tabela
    data = [
        ['Nome', 'CPF', 'Telefone', 'Bairro', 'Data Nasc.', 'Idade']
    ]
    
    for pessoa in pessoas:
        data.append([
            pessoa.nome_completo,
            pessoa.cpf,
            pessoa.telefone,
            pessoa.bairro,
            pessoa.data_nascimento.strftime('%d/%m/%Y'),
            str(pessoa.idade())
        ])
    
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

@login_required
def dashboard(request):
    """
    View para exibir dashboard com estatísticas.
    """
    # Contagem total de pessoas
    total_pessoas = Pessoa.objects.count()
    
    # Distribuição por bairro (top 5)
    bairros = Pessoa.objects.values('bairro').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # Contagem de ajudas por tipo
    ajuda_hospital = Pessoa.objects.filter(ajuda_hospital=True).count()
    ajuda_creche = Pessoa.objects.filter(ajuda_creche=True).count()
    cesta_basica = Pessoa.objects.filter(recebeu_cesta_basica=True).count()
    ajuda_transporte = Pessoa.objects.filter(ajuda_transporte=True).count()
    
    # Aniversariantes por mês
    aniversariantes_por_mes = []
    for mes in range(1, 13):
        count = Pessoa.objects.filter(data_nascimento__month=mes).count()
        aniversariantes_por_mes.append({
            'mes': datetime.date(2000, mes, 1).strftime('%B'),
            'total': count
        })
    
    # Cadastros por mês (últimos 6 meses)
    hoje = timezone.now().date()
    cadastros_por_mes = []
    
    for i in range(5, -1, -1):
        mes_alvo = hoje.month - i
        ano_alvo = hoje.year
        
        if mes_alvo <= 0:
            mes_alvo += 12
            ano_alvo -= 1
        
        inicio_mes = datetime.date(ano_alvo, mes_alvo, 1)
        if mes_alvo == 12:
            fim_mes = datetime.date(ano_alvo + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            fim_mes = datetime.date(ano_alvo, mes_alvo + 1, 1) - datetime.timedelta(days=1)
        
        count = Pessoa.objects.filter(
            data_cadastro__date__gte=inicio_mes,
            data_cadastro__date__lte=fim_mes
        ).count()
        
        cadastros_por_mes.append({
            'mes': inicio_mes.strftime('%b/%Y'),
            'total': count
        })
    
    context = {
        'total_pessoas': total_pessoas,
        'bairros': bairros,
        'ajuda_hospital': ajuda_hospital,
        'ajuda_creche': ajuda_creche,
        'cesta_basica': cesta_basica,
        'ajuda_transporte': ajuda_transporte,
        'aniversariantes_por_mes': aniversariantes_por_mes,
        'cadastros_por_mes': cadastros_por_mes,
    }
    
    return render(request, 'core/dashboard.html', context)
