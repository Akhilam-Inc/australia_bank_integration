# Bank Integration for ERPNext

Automatically sync your bank transactions into ERPNext. Save hours of manual data entry, eliminate errors, and keep your financial records up-to-date in real-time.

## Why Choose This App?

**Stop Manual Data Entry**  
Your team spends hours copying transactions from bank statements into ERPNext. This app does it automatically—saving time and eliminating human error.

**Always Accurate, Always Current**  
Set it once and forget it. Your transactions sync automatically every hour, day, or week. No more outdated financial records or reconciliation nightmares.

**Multiple Banks, One Dashboard**  
Manage all your business bank accounts from different platforms in one place. Whether you use Airwallex for international payments or Skript for Australian banking, it's all in ERPNext.

## Supported Banking Platforms

### 🌐 Airwallex
Perfect for businesses with international operations. Handle payments in 60+ currencies from one account.
- Global payment collections
- Multi-currency transactions
- International supplier payments

### 🇦🇺 Skript  
Built for Australian businesses managing local banking operations.
- Australian dollar transactions
- Domestic payments and receipts
- Local business banking

## Who Is This For?

✅ **E-commerce Businesses** – Process hundreds of daily transactions without manual entry  
✅ **Import/Export Companies** – Handle multi-currency transactions effortlessly  
✅ **Growing Businesses** – Scale your accounting without hiring more staff  
✅ **CFOs & Finance Teams** – Get real-time financial visibility  
✅ **Accountants** – Spend less time on data entry, more on analysis


## What You Get

### Automatic Transaction Sync
Set your schedule—hourly, daily, weekly, or monthly—and let the app handle the rest. Your transactions appear in ERPNext automatically.

### Smart Transaction Matching
The app intelligently matches transactions to the correct bank accounts based on currency. No confusion, no mismatches.

### Duplicate Protection
Never worry about the same transaction appearing twice. Built-in intelligence prevents duplicates automatically.

### Historical Data Import
Need to import past transactions? Choose any date range and bring in historical data with a single click.

### Multi-Account Management
Run multiple business entities? Manage unlimited bank accounts across both platforms from one interface.

### Real-Time Progress Tracking
Watch your transactions sync in real-time. Know exactly what's happening and when it's done.

### Error Alerts & Logging
If something goes wrong, you'll know immediately. Detailed logs help you understand and resolve issues quickly.

## Real Business Impact

**Time Savings**  
"We used to spend 5 hours every week entering bank transactions. Now it takes 5 minutes to review what's already synced." – Finance Manager, Manufacturing Company

**Accuracy Improvement**  
Eliminate manual data entry errors. Every transaction is captured exactly as it appears in your bank.

**Better Cash Flow Visibility**  
Know your real-time cash position without waiting for manual updates. Make informed business decisions faster.

**Audit Ready**  
Complete transaction history with timestamps and sync logs. Your auditors will thank you.

## How It Works

**Step 1: Connect Your Bank**  
Link your Airwallex or Skript account to ERPNext in minutes. Simply enter your credentials and select which bank accounts to sync.

**Step 2: Configure Your Schedule**  
Choose how often you want transactions to sync—every hour for high-volume businesses or daily for smaller operations.

**Step 3: Let It Run**  
That's it. The app handles everything automatically. Review your transactions in ERPNext whenever you need.

## Getting Started

**Installation**  

*Option 1: From ERPNext Marketplace*  
Install directly from your ERPNext instance through the app marketplace. Search for "Bank Integration" and click install.

*Option 2: Manual Installation*  
If you have access to your server, install using:
```bash
bench get-app https://github.com/Akhilam-Inc/australia_bank_integration
bench --site your-site-name install-app bank_integration
```

**Configuration**  

Once installed, follow our step-by-step configuration guide to connect your bank accounts:

1. Open **Bank Integration Setting** in ERPNext
2. Select your banking platform (Airwallex or Skript)
3. Enter your bank credentials
4. Link to your ERPNext bank accounts
5. Set your preferred sync schedule
6. Test the connection

📖 **Detailed Setup Guide**: [Configuration Documentation](doc/02-configuration.md)  

**Support**  
Comprehensive documentation and responsive support when you need help.

## Common Questions

**Does this work with my existing bank accounts in ERPNext?**  
Yes! The app works with your existing ERPNext bank accounts. Just link them to your external banking platform.

**What happens to transactions I've already entered manually?**  
The app detects duplicates automatically and skips transactions already in your system.

**Can I sync past transactions?**  
Absolutely. Import historical transactions for any date range you need.

**Do I need technical knowledge to set this up?**  
No. If you can use ERPNext, you can set up this integration. We provide clear instructions for every step.

**What if I use multiple banking platforms?**  
Perfect! The app supports both Airwallex and Skript simultaneously. Manage all your accounts from one place.

**Is my banking data secure?**  
Yes. All credentials are encrypted and stored securely. Only authorized users can access the integration settings.

## Use Cases

### International Trade Company
Handles payments in 15 different currencies through Airwallex. Syncs 200+ transactions daily automatically, saving 10 hours per week of manual entry.

### Australian Retail Business  
Uses Skript for local operations with high transaction volumes. Hourly sync ensures real-time visibility of cash position for inventory purchasing decisions.

### Multi-Entity Corporation
Manages 5 different business entities with separate bank accounts. One integration handles all accounts with proper segregation and reporting.

### Consulting Firm
Monthly invoicing with weekly expense reconciliation. Daily sync ensures accurate cash flow forecasting for resource planning.

## Pricing & Plans

This app is available for installation on your ERPNext instance. Contact us for enterprise licensing and support packages.

## Requirements

- Active ERPNext instance (cloud or self-hosted)
- Bank account with Airwallex or Skript
- Basic ERPNext knowledge

## Support

**Need Help?**  
- Comprehensive user guides and video tutorials
- Email support for installation and configuration
- Community forum for tips and best practices

**Have Questions?**  
Visit our documentation or create a support ticket. We're here to help you succeed.

## What's Coming Next

We're constantly improving based on customer feedback:
- Additional banking platform integrations
- Enhanced transaction categorization
- Automatic reconciliation suggestions
- Advanced financial reporting
- Real-time transaction notifications
- Custom field mapping options

## Get Started Today

Stop wasting time on manual data entry. Start automating your bank transaction sync today.

**Ready to save hours every week?**  
Install now and see the difference automated banking integration makes for your business.

---

## License

## License

MIT License

Copyright (c) 2025 Akhilam Inc

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

**Made with ❤️ by [Akhilam Inc](https://github.com/Akhilam-Inc)**
*Helping businesses automate financial operations* 🚀

