from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    webhook_url = fields.Char(
        string='URL do Webhook',
        config_parameter='contatos_webhook.webhook_url'
    )
    
    use_default_text = fields.Boolean(
        string='Usar Texto Padrão',
        config_parameter='contatos_webhook.use_default_text'
    )
    
    default_text = fields.Text(
        string='Texto Padrão',
        config_parameter='contatos_webhook.default_text'
    )
    
    use_default_text_2 = fields.Boolean(
        string='Ativar Texto 2',
        config_parameter='contatos_webhook.use_default_text_2'
    )
    
    default_text_2 = fields.Text(
        string='Texto Padrão 2',
        config_parameter='contatos_webhook.default_text_2'
    )
    
    use_default_text_3 = fields.Boolean(
        string='Ativar Texto 3',
        config_parameter='contatos_webhook.use_default_text_3'
    )
    
    default_text_3 = fields.Text(
        string='Texto Padrão 3',
        config_parameter='contatos_webhook.default_text_3'
    )
    
    use_default_text_4 = fields.Boolean(
        string='Ativar Texto 4',
        config_parameter='contatos_webhook.use_default_text_4'
    )
    
    default_text_4 = fields.Text(
        string='Texto Padrão 4',
        config_parameter='contatos_webhook.default_text_4'
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        
        res.update(
            webhook_url=ICPSudo.get_param('contatos_webhook.webhook_url', default=''),
            use_default_text=ICPSudo.get_param('contatos_webhook.use_default_text', default=False),
            default_text=ICPSudo.get_param('contatos_webhook.default_text', default=''),
            use_default_text_2=ICPSudo.get_param('contatos_webhook.use_default_text_2', default=False),
            default_text_2=ICPSudo.get_param('contatos_webhook.default_text_2', default=''),
            use_default_text_3=ICPSudo.get_param('contatos_webhook.use_default_text_3', default=False),
            default_text_3=ICPSudo.get_param('contatos_webhook.default_text_3', default=''),
            use_default_text_4=ICPSudo.get_param('contatos_webhook.use_default_text_4', default=False),
            default_text_4=ICPSudo.get_param('contatos_webhook.default_text_4', default='')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        
        ICPSudo.set_param('contatos_webhook.webhook_url', self.webhook_url or '')
        ICPSudo.set_param('contatos_webhook.use_default_text', self.use_default_text)
        ICPSudo.set_param('contatos_webhook.default_text', self.default_text or '')
        ICPSudo.set_param('contatos_webhook.use_default_text_2', self.use_default_text_2)
        ICPSudo.set_param('contatos_webhook.default_text_2', self.default_text_2 or '')
        ICPSudo.set_param('contatos_webhook.use_default_text_3', self.use_default_text_3)
        ICPSudo.set_param('contatos_webhook.default_text_3', self.default_text_3 or '')
        ICPSudo.set_param('contatos_webhook.use_default_text_4', self.use_default_text_4)
        ICPSudo.set_param('contatos_webhook.default_text_4', self.default_text_4 or '')