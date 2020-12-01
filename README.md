# woody
USAA Bank statement extractor

It extracts and combines USAA Checking Account statement into one CSV. It helps for W2 and create easy reports afterwards.
Tested only on Windows so far (based on client request).

Make sure PyPDF2 is in the same folder.
Using python3 (make sure it is in your ENV variable), run as follow:
where PDF is a folder containing statements, easiest way is to create a new folder in woody-main and copy PDF files there.
>python  woody_pdf_v2.1.1.py -d PDF


It supports these types of transactions so far. (If you found a new one, please report it!)

    # DEPOSIT
            # "DEPOSIT @ MOBILE"
            # "INTEREST PAID"
            # "ATM DEPOSIT"
            # "ACH CREDIT"
            # "USAA CREDIT"
            # "DEBIT CARD REFUND"
            # "USAA FUNDS TRANSFER CR"
            # "ATM SURCHARGE REBATE"

    # WITHDRAWAL
            # "ACH DEBIT"
            # "POS DEBIT"
            # "USAA DEBIT"
            # "USAA FUNDS TRANSFER DB"
            # "ATM DB LOCAL"
            # "ATM DB NONLOCAL"
            # "DEBIT CARD PURCHASE"
            # "USAA CREDIT CARD PMT""
            # "ATM SERVICE FEE"

Report CSV headers:
DATE	FILENAME	TYPE	AMOUNT	DESC	DATE(IF APPICABLE)	OTHER_INFO	OTHER_INFO_2

