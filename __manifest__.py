# -*- coding: utf-8 -*-
{
    'name': 'Contatos Webhook',                
    'version': '1.0',                        
    'summary': 'Módulo para receber contatos via webhook e gerenciar envios.', # Resumo do módulo
    'description': 'Este módulo recebe dados de contatos via webhook, permite o gerenciamento dos envios e oferece uma interface para personalização das mensagens.', # Descrição detalhada do módulo
    'category': 'Tools',                       # Categoria do módulo
    'author': 'Fernando Dias',                    # Seu nome (ou o nome do autor do módulo)
    'depends': ['base', 'web', 'base_setup'],  # Lista de módulos dos quais este módulo depende
    'data': [                                 # Lista de arquivos de dados (XML, CSV, etc.) que este módulo usa
        'security/ir.model.access.csv',     # Permissões de acesso ao modelo
        'views/contatos_webhook_view.xml', # View do modelo de contatos
        'views/config_settings_view.xml',     # View de configurações do módulo
        'data/config_settings_data.xml',    # Dados iniciais de configuração
    ],
    'installable': True,                      # Define se o módulo pode ser instalado
    'application': True,                     # Define se o módulo é um aplicativo
    'auto_install': False,                    # Define se o módulo deve ser instalado automaticamente
}