import math
import argparse
import sys

def calculate_diff_payment(principal, months, nominal, repay_month):
    differentiated_payment = math.ceil(principal / months + nominal * (principal - ((principal * (repay_month - 1)) / months)))
    print(f"Month {repay_month}: payment is {differentiated_payment}")
    return differentiated_payment


def calculate_annuity(principal, months, nominal):
    annu = math.ceil(principal * ((nominal * (1 + nominal) ** months) / ((1 + nominal) ** months - 1)))
    print(f"Your annuity payment = {annu}")
    return annu


def calculate_loan(ann, months, nominal):
    loan = ann / ((nominal * (1 + nominal) ** months) / ((1 + nominal) ** months - 1))
    print(f"Your loan principal = {loan}")
    return loan


def calculate_number(principal, payment, nominal):
    years = 0
    months = int(math.ceil(math.log((payment / (payment - nominal * principal)), (1 + nominal))))
    while months >= 12:
        if months % 12 == 0:
            years = int(months / 12)
            break
        else:
            years += 1
            months -= 12
    if years == 0 and months != 0:
        print(f"It will take {months} months to repay this loan!")
    elif years == 1 and months != 0:
        print(f"It will take 1 year and {months} months to repay this loan!")
    elif years == 1 and months == 0:
        print("It will take 1 year to repay this loan!")
    elif years >= 2 and months == 0:
        print(f"It will take {years} years to repay this loan!")
    else:
        print(f"It will take {years} years and {months} months to repay this loan!")
    return months


parser = argparse.ArgumentParser(description="Beispieltext")
parser.add_argument("--type", choices=["annuity", "diff"], required=True)
parser.add_argument("--payment", type=int)
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)

args = parser.parse_args()
if len(sys.argv) <= 4:
    print("Incorrect parameters")
else:
    if args.interest is None:
        print("Incorrect parameters")
    else:
        for index in range(2, len(sys.argv)):
            if float(sys.argv[index].split("=")[1]) < 0.0:
                print("Incorrect parameters")
        else:
            if args.type == "annuity":
                if args.periods is None:
                    args.periods = calculate_number(args.principal, args.payment, (args.interest / (100.0 * 12)))
                    print(f"Overpayment = {(args.periods * args.payment) - args.principal}")
                elif args.principal is None:
                    args.principal = calculate_loan(args.payment, args.periods, (args.interest / (100.0 * 12)))
                    print(f"Overpayment = {(args.periods * args.payment) - args.principal}")
                elif args.payment is None:
                    args.payment = calculate_annuity(args.principal, args.periods, (args.interest / (100.0 * 12)))
                    print(f"Overpayment = {args.principal - (args.payment * args.periods)}")
            elif args.type == "diff":
                repayment_month = 1
                payment_total = 0
                while repayment_month <= args.periods:
                    payment_total += calculate_diff_payment(args.principal,
                                                            args.periods,
                                                            (args.interest / (100.0 * 12)), repayment_month)
                    repayment_month += 1
                print(f"Overpayment = {args.principal - payment_total}")

