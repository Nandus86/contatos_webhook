from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_text = fields.Text(
        string='Texto Padrão',
        config_parameter='contatos_webhook.default_text'
    )
    default_text_2 = fields.Text(
        string='Texto Padrão 2',
        config_parameter='contatos_webhook.default_text_2'
    )
    default_text_3 = fields.Text(
        string='Texto Padrão 3',
        config_parameter='contatos_webhook.default_text_3'
    )
    default_text_4 = fields.Text(
        string='Texto Padrão 4',
        config_parameter='contatos_webhook.default_text_4'
    )
    use_default_text_2 = fields.Boolean(
        string='Ativar Texto 2',
        config_parameter='contatos_webhook.use_default_text_2'
    )
    use_default_text_3 = fields.Boolean(
        string='Ativar Texto 3',
        config_parameter='contatos_webhook.use_default_text_3'
    )
    use_default_text_4 = fields.Boolean(
        string='Ativar Texto 4',
        config_parameter='contatos_webhook.use_default_text_4'
    )
    webhook_url = fields.Char(
        string='URL do Webhook',
        config_parameter='contatos_webhook.webhook_url'
    )