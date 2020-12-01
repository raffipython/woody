# -*- coding: utf-8 -*-
"""
@author: Raffi 
"""

import PyPDF2
import sys
import argparse
import os
import time
import re
from pprint import pprint as p


def content_processor(content, filename):
    local_main_in_data = {}
    local_main_out_data = {}
    local_main_in_line_no = 1
    local_main_out_line_no = 1
    desc_indexes = []
    counter = 0
    daoc_indexes = []
    od_indexes = []
    for i in content:
        if "DATE..........AMOUNT.TRANSACTION DESCRIPTION" in i:
            desc_indexes.append(counter)
        counter += 1
    for i in desc_indexes:
        #print(content[i-1])
        #print(content[i])
        if "DEPOSITS AND OTHER CREDITS" in content[i-1]:
            daoc_indexes.append(i+1)
        elif "OTHER DEBITS" in content[i-1]:
            od_indexes.append(i+1)

    # TYPES (lines each):
    # DEPOSIT
            # 1 : "DEPOSIT @ MOBILE"
            # 1 : "INTEREST PAID"
            # 1 : "ATM DEPOSIT"
            # 2 : "ACH CREDIT"
            # 2 : "USAA CREDIT"
            # 2 : "DEBIT CARD REFUND"
            # 3 : "USAA FUNDS TRANSFER CR"
            # 1 : "ATM SURCHARGE REBATE"

    # WITHDRAWAL
            # 2 : "ACH DEBIT"
            # 2 : "POS DEBIT"
            # 2 : "USAA DEBIT"
            # 3 : "USAA FUNDS TRANSFER DB"
            # 2 : "ATM DB LOCAL"
            # 2 : "ATM DB NONLOCAL"
            # 2 : "DEBIT CARD PURCHASE"
            # 2 : "USAA CREDIT CARD PMT""
            # 1 : "ATM SERVICE FEE"

    try:
        for item in daoc_indexes:
            section_index = item
            for line in content[item:]:
                # One liner
                if re.search("^[0-9]{2}/[0-9]{2}", line) and "DEPOSIT @ MOBILE" in line:
                    line_data = [i for i in line.split(" ") if i]
                    local_main_in_data.update({local_main_in_line_no: line_data})
                    local_main_in_line_no += 1

                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "INTEREST PAID" in line:
                    line_data = [i for i in line.split(" ") if i]
                    local_main_in_data.update({local_main_in_line_no: line_data})
                    local_main_in_line_no += 1

                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "ATM DEPOSIT" in line:
                    line_data = [i for i in line.split(" ") if i]
                    local_main_in_data.update({local_main_in_line_no: line_data})
                    local_main_in_line_no += 1

                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "ATM SURCHARGE REBATE" in line:
                    line_data = [i for i in line.split(" ") if i]
                    local_main_in_data.update({local_main_in_line_no: line_data})
                    local_main_in_line_no += 1

                # Two liner
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "ACH CREDIT" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_in_data.update({local_main_in_line_no: line_data})
                    local_main_in_line_no += 1

                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "USAA CREDIT" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_in_data.update({local_main_in_line_no: line_data})
                    local_main_in_line_no += 1

                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "DEBIT CARD REFUND" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_in_data.update({local_main_in_line_no: line_data})
                    local_main_in_line_no += 1

                # Three liner
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "USAA FUNDS TRANSFER CR" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line3 = [i for i in content[section_index+2].split(" ") if i]
                    line_data.append(line2)
                    line_data.append(line3)
                    local_main_in_data.update({local_main_in_line_no: line_data})
                    local_main_in_line_no += 1

                section_index += 1
                if not line or "OTHER DEBITS" in line:
                    break

        # process od
        # print(od_indexes)
        for item in od_indexes:
            section_index = item
            for line in content[item:]:
                # One liner
                if re.search("^[0-9]{2}/[0-9]{2}", line) and "ATM SERVICE FEE" in line:
                    line_data = [i for i in line.split(" ") if i]
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1
                # Two liner
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "ACH DEBIT" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "POS DEBIT" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "USAA DEBIT" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "ATM DB" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "DEBIT CARD PURCHASE" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "USAA CREDIT CARD PMT" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "USAA LOAN PAYMENT" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line_data.append(line2)
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1

                # Three liner
                elif re.search("^[0-9]{2}/[0-9]{2}", line) and "USAA FUNDS TRANSFER DB" in line:
                    line_data = [i for i in line.split(" ") if i]
                    line2 = [i for i in content[section_index+1].split(" ") if i]
                    line3 = [i for i in content[section_index+2].split(" ") if i]
                    line_data.append(line2)
                    line_data.append(line3)
                    local_main_out_data.update({local_main_out_line_no: line_data})
                    local_main_out_line_no += 1

                section_index += 1
                if not line:
                    break

        with open(filename + ".csv", "w") as fd:
            for i in sorted(local_main_in_data):
                line_to_print_list = local_main_in_data.get(i)
                line_to_print_list[1] = line_to_print_list[1].replace(",", "")
                if len(line_to_print_list) == 5 and line_to_print_list[2] == "DEPOSIT" and line_to_print_list[-1] == "MOBILE":
                    line_to_print = "{},{},DEPOSIT,{},DEPOSIT_MOBILE,NA".format(line_to_print_list[0], filename, line_to_print_list[1])

                elif len(line_to_print_list) == 4 and line_to_print_list[2] == "ATM" and line_to_print_list[-1] == "DEPOSIT":
                    line_to_print = "{},{},DEPOSIT,{},ATM_DEPOSIT,NA".format(line_to_print_list[0], filename, line_to_print_list[1])

                elif len(line_to_print_list) == 4 and line_to_print_list[2] == "INTEREST" and line_to_print_list[-1] == "PAID":
                    line_to_print = "{},{},DEPOSIT,{},INTEREST_PAID,NA".format(line_to_print_list[0], filename, line_to_print_list[1])

                elif line_to_print_list[2] == "ACH" and line_to_print_list[3] == "CREDIT":
                    line_to_print = "{},{},DEPOSIT,{},ACH_CREDIT,{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], line_to_print_list[4], " ".join(line_to_print_list[-1]))

                elif line_to_print_list[2] == "USAA" and line_to_print_list[3] == "CREDIT":
                    line_to_print = "{},{},DEPOSIT,{},USAA_CREDIT,NA,{}".format(line_to_print_list[0], filename, line_to_print_list[1], " ".join(line_to_print_list[4]))

                elif line_to_print_list[2] == "DEBIT" and line_to_print_list[3] == "CARD" and line_to_print_list[4] == "REFUND":
                    line_to_print = "{},{},DEPOSIT,{},DEBIT_CARD_REFUND,{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], line_to_print_list[5], line_to_print_list[6] + " " + " ".join(line_to_print_list[7]))

                elif line_to_print_list[2] == "USAA" and line_to_print_list[3] == "FUNDS" and line_to_print_list[5] == "CR":
                    line_to_print = "{},{},DEPOSIT,{},USAA_FUNDS_TRANSFER_CR,NA,{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], " ".join(line_to_print_list[6]), " ".join(line_to_print_list[7]).replace(",", " "))

                elif len(line_to_print_list) == 5 and line_to_print_list[2] == "ATM" and line_to_print_list[3] == "SURCHARGE" and line_to_print_list[4] == "REBATE":
                    line_to_print = "{},{},DEPOSIT,{},ATM_SURCHARGE_REBATE,NA".format(line_to_print_list[0], filename, line_to_print_list[1])




                else:
                    line_to_print = "UNKNOWN_TYPE_DEPOSIT, {}".format(line_to_print_list)
                    print("{},{},{}".format(filename, i, line_to_print))

                line_to_print = str(line_to_print)
                fd.write(line_to_print)
                fd.write("\n")

        with open(filename + ".csv", "a") as fd:
            for i in sorted(local_main_out_data):
                line_to_print_list = local_main_out_data.get(i)
                line_to_print_list[1] = line_to_print_list[1].replace(",", "")

                if line_to_print_list[2] == "ACH" and line_to_print_list[3] == "DEBIT":
                    line_to_print = "{},{},WITHDRAW,{},ACH_DEBIT,{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], line_to_print_list[4], " ".join(line_to_print_list[-1]))

                elif line_to_print_list[2] == "POS" and line_to_print_list[3] == "DEBIT":
                    line_to_print = "{},{},WITHDRAW,{},POS_DEBIT,{},{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], line_to_print_list[4], line_to_print_list[-2], " ".join(line_to_print_list[-1]))

                elif line_to_print_list[2] == "USAA" and line_to_print_list[3] == "DEBIT":
                    line_to_print = "{},{},WITHDRAW,{},USAA_DEBIT,,{}".format(line_to_print_list[0], filename, line_to_print_list[1], " ".join(line_to_print_list[-1]))

                elif line_to_print_list[2] == "USAA" and line_to_print_list[3] == "FUNDS":
                    line_to_print = "{},{},WITHDRAW,{},USAA_FUNDS_TRANSFER_DB,NA,{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], " ".join(line_to_print_list[-2]), " ".join(line_to_print_list[-1]).replace(",", " "))

                elif line_to_print_list[2] == "ATM" and line_to_print_list[3] == "DB" and line_to_print_list[4] == "LOCAL":
                    line_to_print = "{},{},WITHDRAW,{},ATM_DB_LOCAL,{},{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], line_to_print_list[5], line_to_print_list[-2], " ".join(line_to_print_list[-1]))

                elif line_to_print_list[2] == "ATM" and line_to_print_list[3] == "DB" and line_to_print_list[4] == "NONLOCAL":
                    line_to_print = "{},{},WITHDRAW,{},ATM_DB_NONLOCAL,{},{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], line_to_print_list[5], line_to_print_list[-2], " ".join(line_to_print_list[-1]))

                elif line_to_print_list[2] == "DEBIT" and line_to_print_list[3] == "CARD" and line_to_print_list[4] == "PURCHASE":
                    line_to_print = "{},{},WITHDRAW,{},DEBIT_CARD_PURCHASE,{},{},{}".format(line_to_print_list[0], filename, line_to_print_list[1], line_to_print_list[5], line_to_print_list[-2], " ".join(line_to_print_list[-1]))

                elif line_to_print_list[2] == "USAA" and line_to_print_list[3] == "CREDIT" and line_to_print_list[4] == "CARD" and line_to_print_list[5] == "PMT":
                    line_to_print = "{},{},WITHDRAW,{},USAA_CREDIT_CARD_PMT,,{}".format(line_to_print_list[0], filename, line_to_print_list[1], " ".join(line_to_print_list[-1]))

                elif line_to_print_list[2] == "ATM" and line_to_print_list[3] == "SERVICE" and line_to_print_list[4] == "FEE":
                    line_to_print = "{},{},WITHDRAW,{},ATM_SERVICE_FEE,NA".format(line_to_print_list[0], filename, line_to_print_list[1])

                elif line_to_print_list[2] == "USAA" and line_to_print_list[3] == "LOAN" and line_to_print_list[4] == "PAYMENT":
                    line_to_print = "{},{},WITHDRAW,{},USAA_LOAN_PAYMENT,NA".format(line_to_print_list[0], filename, line_to_print_list[1], " ".join(line_to_print_list[-1]))

                else:
                    line_to_print = "UNKNOWN_TYPE_WITHDRAWAL, {}".format(line_to_print_list)
                    print("{},{},{}".format(filename, i, line_to_print))
                line_to_print = str(line_to_print)
                fd.write(line_to_print)
                fd.write("\n")

    except:
        pass

def pdf_reader(filename):
    """ Reads a PDF file and returns the content as a list of lines """
    pdf_file = open(filename, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    content = []
    for i in range(0, number_of_pages, 1):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        for line in page_content.split("\n"):
            content.append(line)
    return content


def mobile_deposit_total(content):
    """ Return total amount of Mobile Deposits """
    total = 0
    for line in content:
        if "DEPOSIT @ MOBILE" in line:
            deposit = line.split("DEPOSIT")[0].split()[1]
            deposit = float(deposit.replace(",", ""))
            total += round(deposit, 2)
    return round(total, 2)


def atm_withdrawal_total(content):
    """ Return total amount of ATM Withdrawals """
    total = 0
    for line in content:
        # Assumes USAA ATM IS LOCAL or NONLOCAL
        if "ATM DB NONLOCAL" in line or "ATM DB LOCAL" in line:
            withdrawal = line.split("ATM DB")[0].split()[1]
            withdrawal = float(withdrawal.replace(",", ""))
            total += round(withdrawal, 2)
    return round(total, 2)


def usaa_deposit_total(content):
    """ Return total amount of USAA FUNDS TRANSFER CR Deposits """
    total = 0
    for line in content:
        if "USAA FUNDS TRANSFER CR" in line:
            withdrawal = line.split("USAA FUNDS TRANSFER CR")[0].split()[1]
            withdrawal = float(withdrawal.replace(",", ""))
            total += round(withdrawal, 2)
    return round(total, 2)


def usaa_withdrawal_total(content):
    """ Return total amount of USAA FUNDS TRANSFER DB Withdrawals """
    total = 0
    for line in content:
        if "USAA FUNDS TRANSFER DB" in line:
            withdrawal = line.split("USAA FUNDS TRANSFER DB")[0].split()[1]
            withdrawal = float(withdrawal.replace(",", ""))
            total += round(withdrawal, 2)
    return round(total, 2)


def usaa_withdrawal_total_detailed(content):
    """ Return detailed info on USAA FUNDS TRANSFER DB Withdrawals """
    _index = 0
    for line in content:
        if "USAA FUNDS TRANSFER DB" in line:
            person = content[_index + 1].split("TO ")[1]
            withdrawal = line.split("USAA FUNDS TRANSFER DB")[0].split()[1]
            withdrawal = float(withdrawal.replace(",", ""))
            amount = round(withdrawal, 2)
            if person not in withdrawal_details_main.keys():
                withdrawal_details_main.update({person: 0})
            old_amount = withdrawal_details_main.get(person)
            new_amount = old_amount + amount
            withdrawal_details_main.update({person: new_amount})
            #print(person, old_amount, amount, new_amount)
        _index += 1


def usaa_deposit_total_detailed(content):
    """ Return detailed info on USAA FUNDS TRANSFER CR Desposits """
    _index = 0
    for line in content:
        if "USAA FUNDS TRANSFER CR" in line:
            person = content[_index + 1].split("FROM ")[1]
            withdrawal = line.split("USAA FUNDS TRANSFER CR")[0].split()[1]
            withdrawal = float(withdrawal.replace(",", ""))
            amount = round(withdrawal, 2)
            if person not in withdrawal_details_main_cr.keys():
                withdrawal_details_main_cr.update({person: 0})
            old_amount = withdrawal_details_main_cr.get(person)
            new_amount = old_amount + amount
            withdrawal_details_main_cr.update({person: new_amount})
        _index += 1


def reporter(data, detailed_withdraw, detailed_deposit):
    """ Prints report and writes it to CSV file """
    print("[+] Processing Final Report")
    print("\n")
    report_filename = "REPORT_{}.csv".format(str(time.strftime('%d%m%Y_%H%M')))
    total_mdt = 0
    total_udt = 0
    total_awt = 0
    total_uwt = 0
    highest_month = ("", 0)
    lowest_month = ("", 0)

    with open(report_filename, 'w') as fd:
        fd.write("DATE, {}\n".format(str(time.strftime('%d/%m/%Y at %H:%M'))))
        fd.write("\n")
        fd.write("MONTH, Mobile Deposits, USAA Deposits, ATM Withdrawal,\
                 USAA Withdrawal\n")

        for month in data:
            if data.get(month)[4] > highest_month[1]:
                highest_month = (month, data.get(month)[4])
            if not lowest_month[0]:
                lowest_month = (month, data.get(month)[4])
            else:
                if data.get(month)[4] < lowest_month[1]:
                    lowest_month = (month, data.get(month)[4])
            total_mdt += data.get(month)[0]
            total_mdt = round(total_mdt, 2)
            total_udt += data.get(month)[3]
            total_udt = round(total_udt, 2)
            total_awt += data.get(month)[1]
            total_awt = round(total_awt, 2)
            total_uwt += data.get(month)[2]
            total_uwt = round(total_uwt, 2)
            m = data.get(month)
            fd.write("{},{},{},{},{}\n".format(month, m[0], m[3], m[1], m[2]))

banner = """
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
____    __    ____  ______     ______    _______  ____    ____
\   \  /  \  /   / /  __  \   /  __  \  |       \ \   \  /   /
 \   \/    \/   / |  |  |  | |  |  |  | |  .--.  | \   \/   /
  \            /  |  |  |  | |  |  |  | |  |  |  |  \_    _/
   \    /\    /   |  `--'  | |  `--'  | |  '--'  |    |  |
    \__/  \__/     \______/   \______/  |_______/     |__|

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

if __name__ == '__main__':
    """ Run the main program """
    print(banner)
    parser = argparse.ArgumentParser(""" Woody The PDF Reader """)
    parser.add_argument("-d", "--dirpath", type=str,
                        help="Directory path containing PDF files")
    args = parser.parse_args()

    if not args.dirpath:
        print("No directory path was provided")
        sys.exit(0)

    data_total = {}

    global withdrawal_details_main
    withdrawal_details_main = {}

    global withdrawal_details_main_cr
    withdrawal_details_main_cr = {}

    global main_in_line_no
    global main_out_line_no
    global main_data
    main_in_line_no = 1
    main_out_line_no = 1
    main_data = {}

    for root, dirs, files in os.walk(args.dirpath, topdown=False):
        print("[+] Found {} Files (Including non PDF)\n".format(len(files)))
        print("#####################################################")
        for name in files:
            if "PDF" in name or "pdf" in name and "csv" not in name:
                # print os.path.join(root, name))
                filename = os.path.join(root, name)
                content = pdf_reader(filename)
                content_processor(content, filename)
                print("[+] Processing:\t\t{}".format(name))
                month = content[content.index("       USAA CLASSIC CHECKING")
                                + 1]
                month = month.split(" -")[0]
                mdt = mobile_deposit_total(content)
                udt = usaa_deposit_total(content)
                awt = atm_withdrawal_total(content)
                uwt = usaa_withdrawal_total(content)
                usaa_withdrawal_total_detailed(content)
                usaa_deposit_total_detailed(content)

    main_report_lines = []
    for root, dirs, files in os.walk(args.dirpath, topdown=False):
        print("#####################################################")
        for name in files:
            if "csv" in name:
                filename = os.path.join(root, name)
                with open(filename, 'r') as fd:
                    for i in fd.read().split("\n"):
                        if i:
                            if "DEPOSIT" or "WITHDRAW" in i:
                                main_report_lines.append(i)

    print("[+] Processing Final Report")
    print("\n")
    report_filename = "REPORT_{}.csv".format(str(time.strftime('%d%m%Y_%H%M')))
    with open(report_filename, 'w') as fd:
        fd.write("DATE,FILENAME,TYPE,AMOUNT,DESC,DATE(IF APPICABLE),OTHER_INFO,OTHER_INFO_2")
        fd.write("\n")
        for i in main_report_lines:
            fd.write(i)
            fd.write("\n")
