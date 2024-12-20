{
    'name': 'Contatos Webhook',
    'version': '1.0',
    'summary': 'Módulo para receber contatos via webhook e gerenciar envios.',
    'description': 'Este módulo recebe dados de contatos via webhook, permite o gerenciamento dos envios e oferece uma interface para personalização das mensagens.',
    'category': 'Tools',
    'author': 'Fernando Dias - v.1.7',
    'depends': ['web','base_setup'],
    'data': [
        'security/ir.model.access.xml',
        'views/contatos_webhook_view.xml',
        'views/config_settings_view.xml',
        'data/config_settings_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}