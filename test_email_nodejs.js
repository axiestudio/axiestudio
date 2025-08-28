#!/usr/bin/env node
/**
 * 📧 AXIESTUDIO EMAIL TEST USING NODE.JS
 * Tests Resend SMTP configuration using standalone Node.js binary
 */

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

// Load environment variables from .env file
function loadEnvFile() {
    const envPath = path.join(__dirname, '.env');
    
    if (!fs.existsSync(envPath)) {
        console.log('❌ .env file not found!');
        return false;
    }
    
    const envContent = fs.readFileSync(envPath, 'utf8');
    const envVars = {};
    
    envContent.split('\n').forEach(line => {
        line = line.trim();
        if (line && !line.startsWith('#') && line.includes('=')) {
            const [key, ...valueParts] = line.split('=');
            const value = valueParts.join('=').replace(/^["']|["']$/g, ''); // Remove quotes
            envVars[key] = value;
            process.env[key] = value;
        }
    });
    
    console.log('✅ Environment variables loaded from .env');
    return envVars;
}

// Test email configuration
async function testEmailConfiguration() {
    console.log('🔍 AXIESTUDIO EMAIL TEST WITH NODE.JS');
    console.log('=' * 60);
    
    // Load environment
    const envVars = loadEnvFile();
    if (!envVars) {
        return false;
    }
    
    // Get SMTP configuration
    const smtpConfig = {
        host: process.env.AXIESTUDIO_EMAIL_SMTP_HOST,
        port: parseInt(process.env.AXIESTUDIO_EMAIL_SMTP_PORT || '587'),
        user: process.env.AXIESTUDIO_EMAIL_SMTP_USER,
        password: process.env.AXIESTUDIO_EMAIL_SMTP_PASSWORD,
        fromEmail: process.env.AXIESTUDIO_EMAIL_FROM_EMAIL,
        fromName: process.env.AXIESTUDIO_EMAIL_FROM_NAME || 'Axie Studio'
    };
    
    console.log('\n📧 SMTP Configuration:');
    console.log(`  Host: ${smtpConfig.host}`);
    console.log(`  Port: ${smtpConfig.port}`);
    console.log(`  User: ${smtpConfig.user}`);
    console.log(`  Password: ${'*'.repeat(smtpConfig.password?.length || 0)}`);
    console.log(`  From: ${smtpConfig.fromEmail}`);
    console.log(`  From Name: ${smtpConfig.fromName}`);
    
    // Validate configuration
    if (!smtpConfig.host || !smtpConfig.user || !smtpConfig.password || !smtpConfig.fromEmail) {
        console.log('\n❌ Missing SMTP configuration!');
        console.log('Required: SMTP_HOST, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL');
        return false;
    }
    
    // Validate Resend specific configuration
    if (smtpConfig.host === 'smtp.resend.com') {
        if (smtpConfig.user !== 'resend') {
            console.log(`\n❌ For Resend, SMTP_USER must be 'resend', got: ${smtpConfig.user}`);
            return false;
        }
        if (!smtpConfig.password.startsWith('re_')) {
            console.log('\n❌ For Resend, SMTP_PASSWORD must start with "re_" (API key)');
            return false;
        }
    }
    
    console.log('\n✅ Configuration validation passed!');
    
    // Create transporter
    console.log('\n🔧 Creating SMTP transporter...');
    const transporter = nodemailer.createTransport({
        host: smtpConfig.host,
        port: smtpConfig.port,
        secure: false, // Use STARTTLS
        auth: {
            user: smtpConfig.user,
            pass: smtpConfig.password
        },
        debug: true, // Enable debug logging
        logger: true // Enable logging
    });
    
    // Test connection
    console.log('\n🔌 Testing SMTP connection...');
    try {
        await transporter.verify();
        console.log('✅ SMTP connection successful!');
    } catch (error) {
        console.log('❌ SMTP connection failed:');
        console.log(`   Error: ${error.message}`);
        console.log(`   Code: ${error.code}`);
        return false;
    }
    
    // Send test email
    const testEmail = 'stefanjohnmiranda5@gmail.com';
    console.log(`\n📤 Sending test email to ${testEmail}...`);
    
    const mailOptions = {
        from: `"${smtpConfig.fromName}" <${smtpConfig.fromEmail}>`,
        to: testEmail,
        subject: '🎉 AxieStudio Email Test - Node.js Binary',
        html: `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AxieStudio Email Test</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">🎉 Email Test Successful!</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0;">AxieStudio Email System</p>
    </div>
    
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: #28a745; margin-top: 0;">✅ Test Results</h3>
        <ul style="color: #333;">
            <li>✅ SMTP Configuration: Working</li>
            <li>✅ Resend Integration: Connected</li>
            <li>✅ Node.js Binary: Functional</li>
            <li>✅ Email Delivery: Successful</li>
        </ul>
    </div>
    
    <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: #1976d2; margin-top: 0;">📧 Configuration Details</h3>
        <p><strong>SMTP Host:</strong> ${smtpConfig.host}</p>
        <p><strong>SMTP Port:</strong> ${smtpConfig.port}</p>
        <p><strong>From Address:</strong> ${smtpConfig.fromEmail}</p>
        <p><strong>Test Time:</strong> ${new Date().toISOString()}</p>
    </div>
    
    <div style="text-align: center; color: #666; font-size: 14px;">
        <p>This email was sent using Node.js binary to test AxieStudio's email system.</p>
        <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
    </div>
</body>
</html>
        `,
        text: `
🎉 AXIESTUDIO EMAIL TEST SUCCESSFUL!

✅ Test Results:
- SMTP Configuration: Working
- Resend Integration: Connected  
- Node.js Binary: Functional
- Email Delivery: Successful

📧 Configuration Details:
SMTP Host: ${smtpConfig.host}
SMTP Port: ${smtpConfig.port}
From Address: ${smtpConfig.fromEmail}
Test Time: ${new Date().toISOString()}

This email was sent using Node.js binary to test AxieStudio's email system.

AxieStudio - Building the future of AI workflows
        `
    };
    
    try {
        const info = await transporter.sendMail(mailOptions);
        console.log('✅ Email sent successfully!');
        console.log(`   Message ID: ${info.messageId}`);
        console.log(`   Response: ${info.response}`);
        console.log(`\n📬 Check ${testEmail} for the test email!`);
        return true;
    } catch (error) {
        console.log('❌ Failed to send email:');
        console.log(`   Error: ${error.message}`);
        console.log(`   Code: ${error.code}`);
        return false;
    }
}

// Main execution
async function main() {
    console.log('🚀 Starting AxieStudio Email Test...\n');
    
    const success = await testEmailConfiguration();
    
    console.log('\n' + '='.repeat(60));
    if (success) {
        console.log('🎉 EMAIL TEST COMPLETED SUCCESSFULLY!');
        console.log('✅ Your Resend configuration is working perfectly!');
        console.log('✅ AxieStudio email system should work now!');
    } else {
        console.log('💥 EMAIL TEST FAILED!');
        console.log('🔧 Please check the errors above and fix the configuration.');
    }
    console.log('='.repeat(60));
}

// Run the test
main().catch(console.error);
