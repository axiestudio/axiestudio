# -*- coding: utf-8 -*-
"""
ENTERPRISE EMAIL TEMPLATES - PROFESSIONAL DESIGN
Clean, professional email templates without emojis or icons
"""

def get_verification_email_template(username: str, verification_code: str) -> tuple[str, str, str]:
    """Get professional verification email template"""
    
    subject = "Verify your AxieStudio account"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verify your AxieStudio account</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #1a202c;
                max-width: 600px;
                margin: 0 auto;
                padding: 0;
                background-color: #f7fafc;
            }}
            .email-container {{
                background: #ffffff;
                margin: 20px;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 40px 30px;
                text-align: center;
            }}
            .logo {{
                width: 60px;
                height: 60px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                color: white;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            .header h1 {{
                color: white;
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .header p {{
                color: rgba(255, 255, 255, 0.9);
                margin: 8px 0 0;
                font-size: 16px;
            }}
            .content {{
                padding: 40px;
            }}
            .verification-code {{
                background: #f7fafc;
                border: 2px solid #e2e8f0;
                color: #2d3748;
                font-size: 36px;
                font-weight: 700;
                text-align: center;
                padding: 24px;
                border-radius: 8px;
                letter-spacing: 6px;
                margin: 30px 0;
                font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
            }}
            .info-box {{
                background-color: #edf2f7;
                border-left: 4px solid #4299e1;
                padding: 16px;
                margin: 24px 0;
                border-radius: 4px;
            }}
            .info-box h4 {{
                margin: 0 0 8px;
                color: #2b6cb0;
                font-size: 16px;
                font-weight: 600;
            }}
            .info-box ol {{
                margin: 8px 0 0;
                padding-left: 20px;
                color: #4a5568;
            }}
            .security-notice {{
                background-color: #fef5e7;
                border-left: 4px solid #ed8936;
                padding: 16px;
                margin: 24px 0;
                border-radius: 4px;
            }}
            .security-notice p {{
                margin: 0;
                color: #744210;
                font-weight: 500;
            }}
            .features {{
                background-color: #f7fafc;
                border-radius: 8px;
                padding: 24px;
                margin: 30px 0;
            }}
            .features h3 {{
                color: #2d3748;
                margin: 0 0 16px;
                font-size: 18px;
                font-weight: 600;
            }}
            .feature-item {{
                margin: 12px 0;
                color: #4a5568;
                font-size: 15px;
                line-height: 1.5;
            }}
            .feature-item strong {{
                color: #2d3748;
            }}
            .footer {{
                background-color: #f7fafc;
                padding: 30px 40px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
                color: #718096;
                font-size: 14px;
            }}
            .footer p {{
                margin: 8px 0;
            }}
            .footer a {{
                color: #4299e1;
                text-decoration: none;
                font-weight: 500;
            }}
            .expiry-notice {{
                text-align: center;
                color: #718096;
                font-size: 14px;
                margin: 16px 0;
                font-weight: 500;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo">AX</div>
                <h1>Email Verification</h1>
                <p>Welcome to AxieStudio</p>
            </div>

            <div class="content">
                <p>Hello <strong>{username}</strong>,</p>

                <p>Thank you for signing up for AxieStudio. To complete your account setup and start building AI workflows, please use the verification code below:</p>

                <div class="verification-code">
                    {verification_code}
                </div>

                <div class="expiry-notice">
                    This code expires in 10 minutes
                </div>

                <div class="info-box">
                    <h4>How to verify your account:</h4>
                    <ol>
                        <li>Return to the AxieStudio verification page</li>
                        <li>Enter the 6-digit code above</li>
                        <li>Click "Verify Account" to complete setup</li>
                        <li>Start building your first AI workflow</li>
                    </ol>
                </div>

                <div class="security-notice">
                    <p><strong>Security Notice:</strong> Never share this code with anyone. AxieStudio will never ask for your verification code via phone or email.</p>
                </div>

                <div class="features">
                    <h3>What you'll get access to:</h3>
                    <div class="feature-item"><strong>AI Workflow Builder</strong> - Create powerful automation with drag-and-drop interface</div>
                    <div class="feature-item"><strong>Multiple AI Models</strong> - OpenAI, Anthropic, Claude, and more integrated models</div>
                    <div class="feature-item"><strong>Real-time Dashboards</strong> - Monitor and visualize your workflow results</div>
                    <div class="feature-item"><strong>1,600+ Components</strong> - Ready-to-use flows and tools from our marketplace</div>
                    <div class="feature-item"><strong>Team Collaboration</strong> - Share and work together seamlessly on projects</div>
                </div>

                <p style="color: #718096; font-size: 14px; margin-top: 30px;">
                    Didn't request this verification? You can safely ignore this email.
                </p>
            </div>

            <div class="footer">
                <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
                <p>Visit us at <a href="https://axiestudio.se">axiestudio.se</a></p>
                <p>Need help? Our support team is ready to assist you.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_body = f"""
    AxieStudio - Email Verification

    Hello {username},

    Thank you for signing up for AxieStudio. To complete your account setup, please use the verification code below:

    Verification Code: {verification_code}

    This code expires in 10 minutes.

    How to verify your account:
    1. Return to the AxieStudio verification page
    2. Enter the 6-digit code above
    3. Click "Verify Account" to complete setup
    4. Start building your first AI workflow

    Security Notice: Never share this code with anyone. AxieStudio will never ask for your verification code via phone or email.

    What you'll get access to:
    - AI Workflow Builder - Create powerful automation with drag-and-drop interface
    - Multiple AI Models - OpenAI, Anthropic, Claude, and more integrated models
    - Real-time Dashboards - Monitor and visualize your workflow results
    - 1,600+ Components - Ready-to-use flows and tools from our marketplace
    - Team Collaboration - Share and work together seamlessly on projects

    Didn't request this verification? You can safely ignore this email.

    ---
    AxieStudio - Building the future of AI workflows
    Visit us at: https://axiestudio.se
    Need help? Our support team is ready to assist you.
    """

    return subject, html_body, text_body


def get_password_reset_email_template(username: str, reset_link: str, client_ip: str = "unknown") -> tuple[str, str, str]:
    """Get professional password reset email template"""
    
    subject = "Reset your AxieStudio password"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset your AxieStudio password</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #1a202c;
                max-width: 600px;
                margin: 0 auto;
                padding: 0;
                background-color: #f7fafc;
            }}
            .email-container {{
                background: #ffffff;
                margin: 20px;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }}
            .header {{
                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                padding: 40px 40px 30px;
                text-align: center;
            }}
            .logo {{
                width: 60px;
                height: 60px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                color: white;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            .header h1 {{
                color: white;
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .header p {{
                color: rgba(255, 255, 255, 0.9);
                margin: 8px 0 0;
                font-size: 16px;
            }}
            .content {{
                padding: 40px;
            }}
            .reset-button {{
                display: inline-block;
                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                color: white;
                padding: 16px 32px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 16px;
                margin: 24px 0;
            }}
            .info-box {{
                background-color: #fef5e7;
                border-left: 4px solid #f59e0b;
                padding: 16px;
                margin: 24px 0;
                border-radius: 4px;
            }}
            .info-box p {{
                margin: 0;
                color: #92400e;
                font-weight: 500;
            }}
            .security-notice {{
                background-color: #fee2e2;
                border-left: 4px solid #dc2626;
                padding: 16px;
                margin: 24px 0;
                border-radius: 4px;
            }}
            .security-notice p {{
                margin: 0;
                color: #991b1b;
                font-weight: 500;
            }}
            .footer {{
                background-color: #f7fafc;
                padding: 30px 40px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
                color: #718096;
                font-size: 14px;
            }}
            .footer p {{
                margin: 8px 0;
            }}
            .footer a {{
                color: #4299e1;
                text-decoration: none;
                font-weight: 500;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo">AX</div>
                <h1>Password Reset</h1>
                <p>Secure password reset for your account</p>
            </div>

            <div class="content">
                <p>Hello <strong>{username}</strong>,</p>

                <p>We received a request to reset your password for your AxieStudio account. Click the button below to reset your password:</p>

                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" class="reset-button">
                        Reset Password
                    </a>
                </div>

                <div class="info-box">
                    <p><strong>Important:</strong> This password reset link will expire in 24 hours.</p>
                </div>

                <p><strong>What happens next:</strong></p>
                <ol style="color: #4a5568;">
                    <li>Click the reset button above</li>
                    <li>You'll be logged in automatically</li>
                    <li>Go to Settings to change your password</li>
                    <li>Your new password will be saved securely</li>
                </ol>

                <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #718096; background-color: #f7fafc; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 14px;">{reset_link}</p>

                <div class="security-notice">
                    <p><strong>Security Notice:</strong> If you didn't request this password reset, please ignore this email. Your account is still secure.</p>
                    <p style="margin-top: 8px; font-size: 12px;">Request originated from IP: {client_ip}</p>
                </div>
            </div>

            <div class="footer">
                <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
                <p>Visit us at <a href="https://axiestudio.se">axiestudio.se</a></p>
                <p>Need help? Our support team is ready to assist you.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_body = f"""
    AxieStudio - Password Reset

    Hello {username},

    We received a request to reset your password for your AxieStudio account.

    To reset your password, visit this link:
    {reset_link}

    IMPORTANT: This password reset link will expire in 24 hours.

    What happens next:
    1. Click the reset link above
    2. You'll be logged in automatically
    3. Go to Settings to change your password
    4. Your new password will be saved securely

    Security Notice: If you didn't request this password reset, please ignore this email. Your account is still secure.
    Request originated from IP: {client_ip}

    ---
    AxieStudio - Building the future of AI workflows
    Visit us at: https://axiestudio.se
    Need help? Our support team is ready to assist you.
    """

    return subject, html_body, text_body
