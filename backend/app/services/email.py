import emails
from emails.template import JinjaTemplate
from typing import Optional, Dict, Any
from ..core.config import settings
import structlog

logger = structlog.get_logger(__name__)


class EmailService:
    """Email service using SMTP"""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email via SMTP"""
        if not self.smtp_password:
            logger.warning("SMTP password not configured, skipping email send")
            return False
            
        try:
            message = emails.html(
                html=html_content,
                text=text_content,
                subject=subject,
                mail_from=(self.smtp_username, "pgpyfatovutwls"),
                mail_to=to_email
            )
            
            response = message.send(
                smtp={
                    "host": self.smtp_server,
                    "port": self.smtp_port,
                    "tls": True,
                    "user": self.smtp_username,
                    "password": self.smtp_password,
                }
            )
            
            if response.status_code == 250:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    async def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new user"""
        html_template = """
        <h1>Benvenuto in pgpyfatovutwls!</h1>
        <p>Ciao {{ user_name }},</p>
        <p>Grazie per esserti registrato. Il tuo account è ora attivo.</p>
        <p>Buona giornata!</p>
        <p>Il team di pgpyfatovutwls</p>
        """
        
        template = JinjaTemplate(html_template)
        html_content = template.render(user_name=user_name)
        
        return await self.send_email(
            to_email=user_email,
            subject="Benvenuto in pgpyfatovutwls!",
            html_content=html_content
        )
    
    async def send_subscription_confirmation(
        self, 
        user_email: str, 
        user_name: str, 
        plan_name: str
    ) -> bool:
        """Send subscription confirmation email"""
        html_template = """
        <h1>Abbonamento Confermato!</h1>
        <p>Ciao {{ user_name }},</p>
        <p>Il tuo abbonamento a <strong>{{ plan_name }}</strong> è stato confermato.</p>
        <p>Ora puoi accedere a tutte le funzionalità premium.</p>
        <p>Grazie per il tuo supporto!</p>
        <p>Il team di pgpyfatovutwls</p>
        """
        
        template = JinjaTemplate(html_template)
        html_content = template.render(user_name=user_name, plan_name=plan_name)
        
        return await self.send_email(
            to_email=user_email,
            subject="Abbonamento Confermato - pgpyfatovutwls",
            html_content=html_content
        )


email_service = EmailService()