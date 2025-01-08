from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    webhook_url = fields.Char(
        string='URL do Webhook',
        config_parameter='contatos_webhook.webhook_url',
        default_model='contatos_webhook.config'
    )
    
    default_text = fields.Char(
        string='Texto Padrão',
        config_parameter='contatos_webhook.default_text',
        default_model='contatos_webhook.config'
    )
    
    default_text_2 = fields.Char(
        string='Texto Padrão 2',
        config_parameter='contatos_webhook.default_text_2',
        default_model='contatos_webhook.config'
    )
    
    default_text_3 = fields.Char(
        string='Texto Padrão 3',
        config_parameter='contatos_webhook.default_text_3',
        default_model='contatos_webhook.config'
    )
    
    default_text_4 = fields.Char(
        string='Texto Padrão 4',
        config_parameter='contatos_webhook.default_text_4',
        default_model='contatos_webhook.config'
    )
    
    use_default_text_2 = fields.Boolean(
        string='Ativar Texto 2',
        config_parameter='contatos_webhook.use_default_text_2',
        default_model='contatos_webhook.config'
    )
    
    use_default_text_3 = fields.Boolean(
        string='Ativar Texto 3',
        config_parameter='contatos_webhook.use_default_text_3',
        default_model='contatos_webhook.config'
    )
    
    use_default_text_4 = fields.Boolean(
        string='Ativar Texto 4',
        config_parameter='contatos_webhook.use_default_text_4',
        default_model='contatos_webhook.config'
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        
        res.update(
            webhook_url=ICPSudo.get_param('contatos_webhook.webhook_url', default=''),
            default_text=ICPSudo.get_param('contatos_webhook.default_text', default=''),
            default_text_2=ICPSudo.get_param('contatos_webhook.default_text_2', default=''),
            default_text_3=ICPSudo.get_param('contatos_webhook.default_text_3', default=''),
            default_text_4=ICPSudo.get_param('contatos_webhook.default_text_4', default=''),
            use_default_text_2=ICPSudo.get_param('contatos_webhook.use_default_text_2', default=False),
            use_default_text_3=ICPSudo.get_param('contatos_webhook.use_default_text_3', default=False),
            use_default_text_4=ICPSudo.get_param('contatos_webhook.use_default_text_4', default=False)
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        
        ICPSudo.set_param('contatos_webhook.webhook_url', self.webhook_url or '')
        ICPSudo.set_param('contatos_webhook.default_text', self.default_text)
        ICPSudo.set_param('contatos_webhook.default_text_2', self.default_text_2)
        ICPSudo.set_param('contatos_webhook.default_text_3', self.default_text_3)
        ICPSudo.set_param('contatos_webhook.default_text_4', self.default_text_4)
        ICPSudo.set_param('contatos_webhook.use_default_text_2', self.use_default_text_2)
        ICPSudo.set_param('contatos_webhook.use_default_text_3', self.use_default_text_3)
        ICPSudo.set_param('contatos_webhook.use_default_text_4', self.use_default_text_4)