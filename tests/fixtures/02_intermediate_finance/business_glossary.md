# Retail Banking Business Glossary

This document defines the core business concepts and terminology used in the retail banking domain.

---

## Account

**Definition:** A financial arrangement between a customer and the bank that allows deposit, withdrawal, and management of funds.

**Business Context:** Accounts are the primary vehicle for customer banking relationships. They can be individual or jointly held, and may be organized into hierarchical portfolio structures for relationship management purposes.

**Key Attributes:**
- Account Number (unique identifier)
- Account Type (Checking, Savings, MoneyMarket, CD, Investment)
- Current Balance vs. Available Balance
- Interest Rate and Interest Earned
- Minimum Balance Requirements
- Monthly Fees
- Account Status (Active, Dormant, Frozen, Closed)

**Business Rules:**
- Account numbers must be unique across the system
- Parent accounts cannot reference themselves (no circular hierarchies)
- Available balance may be less than current balance due to holds or pending transactions
- Minimum balance requirements may trigger monthly fees if not met
- Dormant accounts are automatically flagged after 12 months of inactivity

**Synonyms:** Bank Account, Deposit Account, Financial Account

**Examples:**
- Checking Account CHK-001001 (Premium) with $5,240.35 current balance
- Savings Account SAV-003001 (Premium) with $48,750.50 balance earning 0.50% APY
- Certificate of Deposit CD-001001 (12-Month) with $50,000 principal at 4.50% APR
- Money Market Account MM-003001 with $25,000 balance earning 0.75% APY

---

## Customer

**Definition:** An individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification.

**Business Context:** Customers are the central entities in retail banking. Each customer undergoes KYC screening to comply with regulatory requirements and is assigned a risk profile to guide product recommendations and investment strategies.

**Key Attributes:**
- Customer ID (primary key)
- Tax ID (SSN for individuals, EIN for corporations)
- Contact Information (email, phone, address)
- KYC Status (Level1, Level2, Level3)
- Risk Profile (Conservative, Moderate, Aggressive)
- Customer Since Date
- Preferred Status (VIP flag)

**Business Rules:**
- Tax ID must be unique across all customers
- KYC Level1 is minimum requirement for account opening
- Level3 KYC required for high-value accounts and international transfers
- Risk profile determines eligibility for investment products and credit limits
- Preferred customers receive waived fees and priority service

**Synonyms:** Account Holder, Client, Banking Customer

**Examples:**
- James Wilson (ID: 10001) - Level2 KYC, Moderate risk, preferred since 2018
- Mary Johnson (ID: 10002) - Level3 KYC, Conservative risk, preferred since 2015
- Patricia Davis (ID: 10004) - Level1 KYC, Moderate risk, standard customer since 2021

---

## Transaction

**Definition:** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees.

**Business Context:** Transactions represent the operational heartbeat of banking. They flow through multiple states (Pending → Posted) and create audit trails for regulatory compliance and customer service.

**Key Attributes:**
- Transaction ID (unique identifier)
- Transaction Type (Debit, Credit, Transfer, Payment, Withdrawal, Deposit, Fee)
- Amount and Currency
- Transaction Date/Time
- Status (Pending, Posted, Failed, Cancelled, OnHold)
- Balance After Transaction
- Description and Reference Number
- Location (for POS and ATM transactions)

**Business Rules:**
- Debit transactions reduce account balance
- Credit transactions increase account balance
- Transactions must maintain sufficient funds (except for overdraft-protected accounts)
- Posted transactions are final and cannot be modified (only reversed with new transaction)
- Failed transactions are logged for audit but do not affect balance
- POS transactions include merchant location data for fraud detection

**Synonyms:** Financial Transaction, Account Activity, Bank Transaction

**Examples:**
- POS Debit: $85.50 at Whole Foods Market #1234 (New York, NY)
- ACH Credit: $2,500.00 Payroll Direct Deposit (Reference: ACH123456789)
- Online Bill Pay: $1,200.00 to Con Edison (Reference: PAY-987654321)
- ATM Withdrawal: $100.00 at ATM-0003 (456 Oak Avenue)
- Monthly Maintenance Fee: $12.00 automatically assessed

---

## Loan

**Definition:** A financial arrangement where the bank lends a principal amount to a customer, who repays with interest over a specified term according to a fixed schedule.

**Business Context:** Loans are core revenue-generating products. They range from secured mortgages to unsecured personal loans and revolving credit facilities. Each loan tracks amortization, remaining balance, and maturity dates.

**Key Attributes:**
- Loan ID (unique identifier)
- Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)
- Principal Amount
- Interest Rate (APR)
- Term (months)
- Monthly Payment Amount
- Balance Due
- Origination Date and Maturity Date
- Loan Status (Pending, Approved, Active, PaidOff, Defaulted)

**Business Rules:**
- Interest rates vary by loan type and customer creditworthiness
- Mortgages require collateral (real estate) and higher KYC levels
- HELOC (Home Equity Line of Credit) allows revolving access to equity
- Credit card loans have no fixed term (revolving credit)
- Defaulted loans trigger collections and credit reporting
- Early payoff may incur prepayment penalties depending on loan terms

**Synonyms:** Credit Facility, Debt Instrument, Borrowing Arrangement

**Examples:**
- Mortgage: $350,000 at 5.50% APR for 360 months ($1,987.57/month)
- Personal Loan: $15,000 at 8.50% APR for 48 months ($368.22/month)
- Auto Loan: $35,000 at 6.50% APR for 60 months ($684.57/month)
- HELOC: $50,000 credit line at 8.50% APR, $450/month minimum payment
- Credit Card: $10,000 limit at 18.50% APR, $250 minimum monthly payment

---

## Interest

**Definition:** The cost of borrowing money (paid by borrower) or the return on depositing money (paid by bank), expressed as an annual percentage rate.

**Business Context:** Interest is the fundamental profit mechanism in banking. Banks pay interest on deposits (lower rate) and charge interest on loans (higher rate), profiting from the spread.

**Key Attributes:**
- Interest Rate (annual percentage)
- APR (Annual Percentage Rate) - for loans
- APY (Annual Percentage Yield) - for deposits
- Compounding Frequency (daily, monthly, annually)
- Simple vs. Compound Interest
- Fixed vs. Variable Rates

**Business Rules:**
- Deposit interest is credited monthly (typically on first day of month)
- Loan interest is amortized (early payments are mostly interest, later mostly principal)
- APY accounts for compounding effects and is higher than stated rate
- Promotional rates may be temporary (e.g., 12-month CD bonus rates)
- Penalty rates may apply for rule violations (e.g., early CD withdrawal)

**Synonyms:** Finance Charge, Yield, Return

**Examples:**
- Standard Savings: 0.25% APY (0.10% stated rate with monthly compounding)
- Premium Savings: 0.50% APY (0.495% stated rate with daily compounding)
- Money Market: 0.75% APY tiered by balance
- 12-Month CD: 4.50% APR (4.60% APY with monthly compounding)
- Mortgage: 5.50% fixed APR for 360-month term
- Credit Card: 18.50% variable APR based on prime rate

---

## Branch

**Definition:** A physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financial advisory services.

**Business Context:** Branches represent the physical presence of the bank. They range from full-service headquarters with multiple staff to satellite locations with limited services and ATM-only locations with no staff.

**Key Attributes:**
- Branch ID and Code
- Branch Name
- Branch Type (FullService, Satellite, ATMOnly)
- Physical Address and Contact Information
- Operating Hours
- Teller Count and Manager Assignment
- ATM Count (on-premises)
- Branch Status (Active, TemporarilyClosed, PermanentlyClosed)

**Business Rules:**
- FullService branches offer complete banking services including loan origination
- Satellite branches have limited hours and staff (no loan officers)
- ATMOnly locations have no staff, only cash machines
- Branch codes must be unique within the bank
- Temporary closures require system status updates and customer notifications

**Synonyms:** Banking Center, Financial Center, Branch Office

**Examples:**
- Downtown Headquarters (0001): FullService, 5 tellers, 4 ATMs, Mon-Fri 9AM-5PM
- Westside Branch (0002): FullService, 3 tellers, 2 ATMs, Mon-Fri 9AM-6PM
- Northtown Satellite (0003): Satellite, 2 tellers, 1 ATM, Mon-Fri 10AM-4PM
- South Station ATM (0004): ATMOnly, 2 ATMs, 24/7 access

---

## ATM

**Definition:** Automated Teller Machine - a self-service banking terminal that allows customers to perform basic transactions without teller assistance.

**Business Context:** ATMs extend banking access beyond branch hours and locations. They can be physically attached to branches or deployed as standalone units in high-traffic areas like malls and grocery stores.

**Key Attributes:**
- ATM ID and Code
- Location (address and GPS coordinates)
- ATM Type (Standalone, Branch, DriveThrough)
- Status (Operational, OutOfService, OutOfCash)
- Cash Balance and Last Replenished Date
- Supported Features (Deposit, Cardless Withdrawal)
- Installation Date

**Business Rules:**
- Standalone ATMs are not affiliated with a branch
- Branch ATMs are located on branch premises
- DriveThrough ATMs serve vehicles only
- Cash replenishment is triggered when balance falls below threshold
- OutOfCash status prevents withdrawal attempts but allows balance inquiries
- Cardless transactions require mobile app authentication

**Synonyms:** Cash Machine, Cashpoint, Automated Banking Machine

**Examples:**
- ATM-0001: Branch ATM at 123 Main Street, $85,000 cash balance, supports deposits
- ATM-0003: Branch ATM at 456 Oak Avenue, $62,000 cash balance, cardless enabled
- STANDALONE-001: Shopping Mall ATM, $25,000 cash balance, deposit not supported
- STANDALONE-002: Grocery Store ATM, OutOfService, $15,000 cash balance

---

## Card

**Definition:** A payment card issued to a customer, linked to their bank account or credit line, enabling electronic transactions at POS terminals, ATMs, and online merchants.

**Business Context:** Cards are the primary interface for customer banking activities. They range from ATM-only cards to full-featured debit cards and revolving credit cards, each with specific security features and spending limits.

**Key Attributes:**
- Card ID and Card Number (PAN)
- Card Type (Debit, Credit, ATM)
- Card Network (Visa, Mastercard, Discover, AmericanExpress)
- Linked Account and Customer
- Cardholder Name
- Expiration Date and CVV
- Credit Limit (for credit cards)
- Daily Limits (POS and ATM)
- Security Features (Chip, Contactless, PIN)
- Card Status (Active, Frozen, Blocked, Expired)

**Business Rules:**
- Debit cards deduct directly from linked checking account
- Credit cards access revolving credit line requiring monthly payments
- ATM cards only work at ATMs (not POS terminals)
- Daily limits prevent fraud and control exposure
- Chip cards provide EMV security for in-person transactions
- Contactless (tap-to-pay) has transaction amount limits
- Lost/stolen cards must be immediately blocked to prevent fraud
- Expired cards are automatically renewed and mailed to customer

**Synonyms:** Payment Card, Bank Card, Plastic

**Examples:**
- Debit Card: ****-****-****-0366 (Visa), $3,000 daily limit, $500 ATM limit
- Credit Card: ****-****-****-0840 (Visa), $25,000 credit limit, $5,000 daily limit
- ATM Card: ****-****-****-9903, $500 ATM daily limit, no POS capability
- Premium Debit: ****-****-****-2125 (Mastercard), $5,000 daily limit, $2,000 ATM limit

---

**Document Version:** 1.0
**Last Updated:** 2024-02-15
**Domain:** Retail Banking & Finance
**Complexity Level:** Intermediate
