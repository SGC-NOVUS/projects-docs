---
id: novus-life-user-manual
cluster: novus-life
category: novus-life-general
order: 100
status: active
version: 0.1.0
title: Novus Life — Official User Manual (From A to Z)
description: '> **Version:** 1.0.0-beta Enterprise Edition > **Applicable Platforms:**
  Web, Mobile PWA (iOS, Android), Desktop (macOS, Windows, Linux) > **Jurisdictions
  & Currencies:** Global...'
last_updated: '2026-10-27'
source_locale: en
locale: en
source_repo: SGC-NOVUS/novus-life
source_branch: main
source_path: docs/USER_MANUAL.md
managed_by: sync_private_docs
---
# Novus Life — Official User Manual (From A to Z)

> **Version:** 1.0.0-beta Enterprise Edition  
> **Applicable Platforms:** Web, Mobile PWA (iOS, Android), Desktop (macOS, Windows, Linux)  
> **Jurisdictions & Currencies:** Global (Universal Multi-Currency, ISO 4217, Custom Rates)  
> **Documentation URL:** [https://novus-life.online/docs/USER_MANUAL.md](https://novus-life.online/docs/USER_MANUAL.md)

---

## Table of Contents

1. [Introduction & Core Philosophy](#1-introduction--core-philosophy)
2. [Installation, PWA Setup & Offline Mode](#2-installation-pwa-setup--offline-mode)
3. [Property & Address Management](#3-property--address-management)
   * 3.1. Adding and Configuring Properties
   * 3.2. Rental Properties & Landlord Directory
   * 3.3. Mortgage Tracking & Loan Amortization
   * 3.4. Multi-Tenant Bill Splitting (By Headcount, Area, or Custom Percentage)
4. [Utility Resource Metering (Utilities Engine)](#4-utility-resource-metering)
   * 4.1. Supported Tariff Models (The 24 Accounting Patterns)
   * 4.2. Entering Readings & Optical Character Recognition (OCR)
   * 4.3. Social Norms, Benefits & Subsidies (e.g., UBD 75% Discount)
   * 4.4. Subscription & Distribution Fees
   * 4.5. Exporting Statements (PDF & Excel)
5. [Wealth Management & Financial Engineering](#5-wealth-management--financial-engineering)
   * 5.1. Accounts Architecture: Net Worth & Cash Flow
   * 5.2. Credit Cards, Grace Periods & Minimum Payments
   * 5.3. Financial Guard: Automated Debt Trap ("Carousel") Detection
   * 5.4. Transactions, Split Checks & Reconciliation
   * 5.5. Soft-Delete Trash Bin & Transaction Recovery
6. [Adaptive Budgeting & Savings Goals](#6-adaptive-budgeting--savings-goals)
   * 6.1. The "4 Envelopes" Weekly Budgeting Method
   * 6.2. Two-Tier Category Budgets
   * 6.3. Piggy Banks & Target Savings Goals
7. [Work Schedules, Timesheets & Payroll](#7-work-schedules-timesheets--payroll)
   * 7.1. Work Schedule Builder (Cyclic Rotations 2/2, 3/3, 1/3, Day/Night)
   * 7.2. Logging Shifts, Night Multipliers & Overtime
   * 7.3. Sick Leaves, Vacations & Business Trips with Per Diem
   * 7.4. Gross-to-Net Payroll Calculation with Tax Deductions
   * 7.5. One-Click Earnings Synchronization to Budget
8. [Data Sync, Backups & Privacy](#8-data-sync-backups--privacy)
   * 8.1. Local-First Offline Operation
   * 8.2. Cloud Synchronization (Self-Hosted PostgreSQL & Supabase)
   * 8.3. Google Drive Encrypted Vault Backup
9. [Power User Tips & Shortcuts](#9-power-user-tips--shortcuts)
10. [Troubleshooting & FAQ](#10-troubleshooting--faq)

---

## 1. Introduction & Core Philosophy

Novus Life is built on three uncompromised engineering pillars:
1. **Local-First Architecture:** Your device is the single source of truth. The application works 100% offline via modern IndexedDB (`Dexie.js v4`). You never lose access to your data during network outages.
2. **Absolute Data Privacy:** Your personal financial records, utility bills, and work hours belong exclusively to you. All sensitive calculations execute locally in your browser.
3. **Enterprise Precision:** Whether calculating tiered block electricity tariffs, mortgage amortization, or complex multi-shift payroll with progressive taxation, mathematical accuracy is strictly guaranteed.

---

## 2. Installation, PWA Setup & Offline Mode

Novus Life is distributed as a **Progressive Web App (PWA)**, meaning you do not need an app store account to install it. It provides native speed, home-screen icons, offline caching, and push notifications.

### 📱 Installing on iOS (iPhone & iPad)
1. Open **Safari** and navigate to your Novus Life instance (e.g., `https://novus-life.online`).
2. Tap the **Share** button (the square with an arrow pointing up) in the bottom toolbar.
3. Scroll down and select **"Add to Home Screen"**.
4. Confirm the application title and tap **"Add"**. Novus Life will launch as a standalone application without Safari browser chrome.

### 🤖 Installing on Android (Chrome, Brave, Samsung Internet)
1. Open **Chrome** and navigate to your Novus Life instance.
2. A banner reading **"Install Novus Life"** will automatically appear at the bottom. Tap **Install**.
3. If the banner does not appear, tap the three-dot menu `⋮` in the upper-right corner and select **"Install app"** or **"Add to Home screen"**.

### 💻 Installing on Desktop (macOS, Windows, Linux)
1. In Google Chrome, Microsoft Edge, or Brave, look at the right side of the address bar.
2. Click the **Install** icon (a monitor with a down arrow).
3. The app will launch in an isolated native desktop window and register in your operating system application launcher.

> [!TIP]
> **Offline Readiness:** Once loaded for the first time, all application assets, stylesheets, scripts, and language bundles are stored in the browser's Service Worker cache (`Workbox`). You can turn on Airplane Mode and use 100% of the application without an internet connection.

---

## 3. Property & Address Management

The **Addresses** module is the central container for your living spaces, commercial offices, rental apartments, and vacation homes.

### 3.1. Adding and Configuring Properties
1. Navigate to **Addresses** from the sidebar or bottom navigation.
2. Click **"+ Add Object"**.
3. Enter property parameters:
   - **Name:** e.g., "Main Apartment", "Suburban House", "Studio on Central Ave".
   - **Type:** Apartment, Private House, Office, Warehouse, Commercial.
   - **Primary Currency:** Select the local billing currency (e.g., USD, EUR, UAH, PLN).
   - **Total Area ($m^2$):** Used for square-meter heating, maintenance, and bill splitting calculations.
   - **Residents Count:** Used for per-capita garbage disposal and water standards.
   - **Accent Color:** Personalize cards with a custom color badge for quick visual recognition.

### 3.2. Rental Properties & Landlord Directory
If you rent an apartment or lease out property:
- Toggle **"Rental Property"** in the property settings.
- Fill in:
  - **Contract End Date:** Automatic reminders will notify you before the lease renewal deadline.
  - **Payment Day:** Monthly due date for rent transfer.
  - **Security Deposit:** Track the amount held by the landlord to guarantee return upon lease termination.
  - **Landlord Contact Details:** Full Name, Phone, Email, Passport/ID, and Registration Address for instant calling and emailing.

### 3.3. Mortgage Tracking & Loan Amortization
For mortgaged properties, activate the **Mortgage** switch:
- Specify the **Original Principal**, **Annual Interest Rate (%)**, **Term (Months)**, and **Lender Name**.
- Novus Life calculates:
  - **Monthly Annuity Payment:** Monthly breakdown of principal and interest.
  - **Principal Paid vs. Remaining Balance:** Visual progress bar tracking loan repayment.
  - **Annual Property Insurance Cost:** Automatically added to total ownership cost calculations.

### 3.4. Multi-Tenant Bill Splitting
When sharing an apartment with roommates or family members:
1. Open the property settings and enable **"Bill Splitting"**.
2. Select the distribution method:
   - **Equal Shares:** Splits total expenses equally among all roommates ($1/N$).
   - **By Room Area ($m^2$):** Each resident pays proportional to their bedroom size, while common areas are shared equally.
   - **Custom Percentages (%):** Manually assign customized percentages per resident.
3. Add participant names, phone numbers, and room areas. Novus Life will calculate each person's exact share on every utility bill.

---

## 4. Utility Resource Metering (Utilities Engine)

The **Utilities** module is powered by an industrial-grade calculation engine supporting **24 tariff models**, multi-meter configurations, and optical recognition.

### 4.1. Supported Tariff Models
Novus Life supports all standard utility billing methods worldwide:
- **Flat Single Rate:** Standard volume multiplied by a fixed rate per unit (e.g., $100\text{ kWh} \times \$0.15$).
- **Two-Zone / Day-Night:** Separate meters or split time intervals (Day rate $T_0$ + Night discount rate $T_1$, typically 50% from 23:00 to 07:00).
- **Three-Zone (Peak / Semi-Peak / Night):** Differentiated commercial and residential power tariffs.
- **Tiered Block Tariffs:** Progressive price brackets (e.g., First $100\text{ kWh}$ at $\$0.10$, volume between $101-250\text{ kWh}$ at $\$0.18$, volume above $250\text{ kWh}$ at $\$0.30$).
- **Fixed Monthly Subscription / Area-Based:** Maintenance fees based on floor area ($m^2$) or fixed service fees (Internet, security, elevator).
- **Two-Meter Configurations (Kitchen & Bathroom):** Separate readings for cold/hot water risers with unified calculation.

### 4.2. Entering Readings & Optical Character Recognition (OCR)
1. Open the **Utilities** tab and select the current billing month.
2. Click **"Enter Reading"** on the target service.
3. You have three ways to enter readings:
   - **Manual Input:** Type the new meter numbers. Consumption is calculated automatically against the previous month's final reading.
   - **Camera OCR Recognition:** Tap **"Scan with Camera"**. Point your smartphone camera at the mechanical or digital meter display. The embedded `Tesseract.js` engine extracts numerical digits directly in the browser without uploading photos to external servers.
   - **Flashlight / Torch Toggle:** If inspecting a dark electrical panel or basement, tap the **Flashlight** button to illuminate the meter.

### 4.3. Social Norms, Benefits & Subsidies
Novus Life features a universal social quota and benefit engine:
- **Combat Veteran / Service Discount (UBD 75%):** Applies a legally mandated 75% discount to consumption within normative limits.
- **Large Family / Low-Income Subsidy:** Supports fixed monetary subsidies or percentage reductions.
- **Normative Quota Caps:** Subsidized rates apply up to the normative threshold (e.g., $70\text{ kWh}$ per family member), and standard rates apply to excess volume.

### 4.4. Subscription & Distribution Fees
Certain utilities (e.g., natural gas transmission or district heating maintenance) charge a separate fixed monthly capacity fee regardless of consumption:
- Enter the **Subscription Fee** in the tariff configuration.
- The breakdown will show:
  $$\text{Total Due} = (\text{Volume} \times \text{Rate}) + \text{Distribution Fee} - \text{Benefits}$$

### 4.5. Exporting Statements (PDF & Excel)
- Click **"Export PDF"** to generate an official payment statement with barcodes, account numbers, and detailed formula breakdowns.
- Click **"Export Excel"** to download complete historical time-series datasets (`.xlsx` or `.csv`) for personal archives or tax reporting.

---

## 5. Wealth Management & Financial Engineering

The **Finances** module implements double-entry personal accounting inspired by professional wealth management standards.

### 5.1. Accounts Architecture: Net Worth & Cash Flow
Novus Life classifies all accounts into two macroeconomic categories:
- **Assets:** Cash in wallet, checking/debit accounts, savings deposits, investment accounts, and cryptocurrency wallets.
- **Liabilities:** Credit card balances, installment loans, personal debts, and mortgages.

$$\text{Net Worth} = \sum \text{Assets} - \sum \text{Liabilities}$$
$$\text{Net Cash Flow} = \text{Total Monthly Income} - \text{Total Monthly Expenses}$$

### 5.2. Credit Cards, Grace Periods & Minimum Payments
Credit cards require rigorous monitoring to avoid expensive bank penalties:
- **Grace Period (Days):** Enter your card's interest-free term (e.g., 55 or 62 days).
- **Grace Period Trigger:**
  - *From 1st of the month:* Debt incurred in April must be repaid by May 25th.
  - *From transaction date:* Each transaction has an individual countdown timer.
- **Minimum Mandatory Payment:** Configurable as a percentage of total balance (e.g., 5%) plus minimum monetary floor (e.g., $100).
- **Countdown Badges:** The Financial dashboard displays dynamic alerts showing days remaining before interest applies.

### 5.3. Financial Guard: Automated Debt Trap ("Carousel") Detection
Credit card "Carousel" (revolving borrowing from Card B to repay Card A) is the #1 cause of personal insolvency.
- **Detection Algorithm:** If you make a debt repayment into a credit card, but within 45 days spend $\ge 85\%$ of that amount from the same credit limit, Financial Guard flags a **Carousel Warning**:
  > *"Warning: Revolving Debt Carousel detected! You repaid \$5,000 but spent \$4,800 shortly after. Your net debt is not decreasing. Lock this balance with debit funds!"*

### 5.4. Transactions, Split Checks & Reconciliation
- **Quick Logging:** Record expenses and income with category tags (#groceries, #fuel, #entertainment).
- **Split Checks (Multi-Category Receipts):** When shopping at a supermarket or department store, tap **"Split Receipt"** to divide a single \$150 transaction into \$90 Groceries, \$40 Household Goods, and \$20 Clothing.
- **Reconciliation Status:** Mark transactions as *Cleared*, *Reconciled*, or *Void* when checking your physical bank statement.

### 5.5. Soft-Delete Trash Bin & Transaction Recovery
To prevent accidental data loss:
- Deleted transactions are moved to the **Financial Trash Bin** rather than being permanently destroyed.
- The account balance automatically rolls back upon deletion.
- You can restore any deleted record with one click or choose **"Empty Trash"** to purge.

---

## 6. Adaptive Budgeting & Savings Goals

### 6.1. The "4 Envelopes" Weekly Budgeting Method
The 4 Envelopes system removes the stress of detailed daily micro-budgeting:
1. Enter your **Expected Monthly Income**.
2. Subtract **Mandatory Fixed Expenses** (Rent, utilities, loan installments, insurance).
3. Subtract your **Savings Reserve** (e.g., 10% emergency cushion).
4. The remaining funds are automatically split equally into **4 Weekly Envelopes**:
   $$\text{Weekly Envelope Limit} = \frac{\text{Income} - (\text{Mandatory Expenses} + \text{Savings Reserve})}{4}$$
5. As you spend during Week 1, the envelope depletes. Any surplus on Sunday night can be rolled into your **Piggy Bank**!

### 6.2. Two-Tier Category Budgets
Organize expenses into Parent Categories (e.g., "Transportation") and Subcategories ("Fuel", "Parking", "Public Transit", "Repairs") with visual threshold progress bars (Safe $\le 75\%$, Warning $76-90\%$, Overbudget $> 90\%$).

### 6.3. Piggy Banks & Target Savings Goals
- Create targeted savings buckets (e.g., "Emergency Fund", "New Laptop", "Summer Vacation").
- Set a **Target Amount** and **Target Date**.
- Novus Life calculates required monthly contributions and displays visual progress animations.

---

## 7. Work Schedules, Timesheets & Payroll

The **Schedules & Payroll** module is tailored for shift workers, freelancers, medical staff, law enforcement, and hourly professionals.

### 7.1. Work Schedule Builder
Configure complex rotating cycles:
- **Preset Cycles:** 2/2 (2 Day shifts, 2 Off), 3/3, 1/3 (24h on, 72h off), 4/2, or standard 5/2.
- **Custom Pattern Editor:** Define any arbitrary sequence of shifts (Day, Night, Post-Night Rest, Vacation, Sick Leave, Standby).
- **Smart Shift Calendar:** Generates your working schedule for months into the future based on your first working day.

### 7.2. Logging Shifts, Night Multipliers & Overtime
- **Base Rate:** Supports hourly rate, fixed shift rate, or monthly base salary.
- **Night Work Premium (1.2x):** Legally mandated 20% or 40% surcharge for hours worked between 22:00 and 06:00.
- **Two-Tier Overtime:**
  - *Tier 1:* First 2 overtime hours paid at $1.5\times$ base rate.
  - *Tier 2:* Consecutive overtime hours paid at $2.0\times$ base rate.
- **Holiday Multiplier (2.0x):** Double pay for shifts falling on official public holidays.

### 7.3. Sick Leaves, Vacations & Business Trips
- **Sick Leave by Seniority:** Automatically adjusts sick pay percentage based on career longevity ($60\%$, $80\%$, or $100\%$).
- **Business Trips:** Automatically adds non-taxable daily subsistence allowances (Per Diem) and lodging/transportation reimbursements.

### 7.4. Gross-to-Net Payroll Calculation
Computes your net take-home salary after all deductions:
$$\text{Taxable Base} = \text{Gross Earnings} - \text{Tax Deductions}$$
$$\text{Income Tax} = \text{Taxable Base} \times \text{Tax Rate \%}$$
$$\text{Net Salary} = \text{Gross} + \text{Allowances} - \text{Taxes} - \text{Pension/Social} - \text{Advance Payments}$$

### 7.5. One-Click Earnings Synchronization to Budget
At the end of the pay cycle, click **"Sync to Finances"**. Novus Life creates an incoming income transaction in your target bank account, closing the loop between work hours and your personal budget!

---

## 8. Data Sync, Backups & Privacy

### 8.1. Local-First Offline Operation
- All operations save instantly to `IndexedDB` on your device.
- Even if offline for weeks, all calculations, graphs, and features operate at full capacity.

### 8.2. Cloud Synchronization
When connected to the internet:
- **Delta Sync:** Novus Life synchronizes only updated records (`updatedAt` timestamp comparisons) to minimize bandwidth.
- **Self-Hosted PostgreSQL & Supabase:** Connect to your private server with end-to-end Row Level Security (RLS). Each user can only read and write their own family data.

### 8.3. Google Drive Encrypted Vault Backup
- Authorize your Google account via OAuth 2.0.
- Novus Life creates an encrypted backup package inside the hidden `appDataFolder` in your personal Google Drive.
- Neither Google nor external third parties can read the contents without your master password.

---

## 9. Power User Tips & Shortcuts

- **Quick Action FAB (Floating Action Button):** The dynamic `+` button in the lower right adapts to the active tab:
  - In Utilities $\rightarrow$ Add Meter Reading.
  - In Finances $\rightarrow$ Add Expense or Income.
  - In Schedules $\rightarrow$ Log Completed Shift.
  - In Addresses $\rightarrow$ Add New Property.
- **Fast Date Shifting:** Click the month header on any screen to quickly pick another billing period without scrolling through tables.
- **Bulk Shift Assignment:** In the Schedule Calendar, switch to **"Batch Mode"** to select multiple days and assign shifts in one operation.
- **Exporting Raw Data:** Go to **Settings $\rightarrow$ Export Database** to download your complete workspace as a JSON archive.

---

## 10. Troubleshooting & FAQ

#### Q1: Will I lose my data if I clear my browser history?
**A:** Standard browser cache clearing usually preserves IndexedDB. However, selecting *"Delete all site cookies and offline data"* will erase local records. **Always enable Cloud Sync or export a JSON backup** before performing browser maintenance.

#### Q2: Can multiple family members share the same budget?
**A:** Yes! Under **Settings $\rightarrow$ Family Sharing**, create a Family Workspace. All invited accounts will see shared utility meters and pooled accounts while keeping personal debit cards private.

#### Q3: Why does OCR meter scanning give an incorrect number?
**A:** Check for glare on the glass dial or weak lighting. Turn on the built-in **Torch / Flashlight** toggle and hold your camera parallel to the meter dials. If dials are worn out, you can tap and edit any recognized digit before saving.

#### Q4: How do I switch languages?
**A:** Click your avatar or the Globe icon in the navigation bar. Novus Life supports English, Ukrainian, Polish, and Russian with instantaneous live switching without page reloads.

---

*End of User Manual. For technical architecture details, please refer to [ARCHITECTURE.md](ARCHITECTURE.md).*
