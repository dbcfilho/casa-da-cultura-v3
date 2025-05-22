from django import forms
from .models import Pessoa, MensagemPadrao, DataComemorativa

class PessoaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de pessoas.
    """
    class Meta:
        model = Pessoa
        fields = [
            'nome_completo', 'cpf', 'rg', 'data_nascimento', 
            'endereco', 'bairro', 'cidade', 'estado', 'cep', 'telefone', 'email',
            'pai_ou_mae', 'ajuda_hospital', 'ajuda_creche', 'recebeu_cesta_basica',
            'participa_oficinas', 'interesse_novas_turmas', 'tem_filhos', 'ajuda_transporte',
            'observacoes'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalização dos campos
        self.fields['cpf'].widget.attrs.update({'class': 'cpf-mask'})
        self.fields['telefone'].widget.attrs.update({'class': 'telefone-mask'})
        self.fields['cep'].widget.attrs.update({'class': 'cep-mask'})
        
        # Campos booleanos com estilo de switch
        for field_name in ['pai_ou_mae', 'ajuda_hospital', 'ajuda_creche', 'recebeu_cesta_basica',
                          'participa_oficinas', 'interesse_novas_turmas', 'tem_filhos', 'ajuda_transporte']:
            self.fields[field_name].widget.attrs.update({'class': 'form-check-input'})


class MensagemPadraoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de mensagens padrão.
    """
    class Meta:
        model = MensagemPadrao
        fields = ['tipo', 'titulo', 'conteudo', 'ativa']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 5}),
        }


class DataComemorativaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de datas comemorativas.
    """
    class Meta:
        model = DataComemorativa
        fields = ['nome', 'data', 'mensagem', 'enviar_automaticamente']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }


class EnvioMensagemForm(forms.Form):
    """
    Formulário para envio de mensagens personalizadas.
    """
    mensagem = forms.ModelChoiceField(
        queryset=MensagemPadrao.objects.filter(ativa=True),
        label="Mensagem Padrão",
        required=True
    )
    personalizar = forms.BooleanField(
        required=False,
        label="Personalizar mensagem",
        initial=False
    )
    conteudo_personalizado = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        label="Conteúdo personalizado"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        personalizar = cleaned_data.get('personalizar')
        conteudo = cleaned_data.get('conteudo_personalizado')
        
        if personalizar and not conteudo:
            self.add_error('conteudo_personalizado', 'Este campo é obrigatório quando a opção "Personalizar mensagem" está marcada.')
        
        return cleaned_data


class PessoaFilterForm(forms.Form):
    """
    Formulário para filtrar pessoas no painel.
    """
    nome = forms.CharField(required=False, label="Nome")
    bairro = forms.CharField(required=False, label="Bairro")
    pai_ou_mae = forms.BooleanField(required=False, label="Pai ou Mãe")
    ajuda_hospital = forms.BooleanField(required=False, label="Ajuda Hospital")
    ajuda_creche = forms.BooleanField(required=False, label="Ajuda Creche")
    recebeu_cesta_basica = forms.BooleanField(required=False, label="Recebeu Cesta Básica")
    participa_oficinas = forms.BooleanField(required=False, label="Participa de Oficinas")
    tem_filhos = forms.BooleanField(required=False, label="Tem Filhos")
    ajuda_transporte = forms.BooleanField(required=False, label="Ajuda Transporte")
    aniversariantes_mes = forms.BooleanField(required=False, label="Aniversariantes do Mês")
