import json
import models
from user_funcs import user_parser

sample_payslip = {
            "employee_id": "dd42783b-0e77-4832-a1b5-f86d300f7b2e",
            "prepared_by_id": "fbd08ed9-41a0-4f46-b096-5939e5b5780d",
            "date": "2022-01-01",
            "period": "January 2022",
            "amount": 5000,
            "status": "Pending",
            "deductions": [
                {
                    "name": "Tax",
                    "amount": 500
                },
                {
                    "name": "NHIF",
                    "amount": 200
                }
            ],
            "additions": [
                {
                    "name": "Bonus",
                    "amount": 1000
                }
            ]
        }

def payslip_parser(payslip, many=False):
    if many:
        return [payslip_parser(item) for item in payslip]
    else:
        total_deductions = 0
        total_additions = 0
        to_deduct = json.loads(payslip.deductions)
        to_add = json.loads(payslip.additions)
        if to_deduct:
            for x in to_deduct:
                total_deductions = total_deductions + x["amount"]
        if to_add:
            for x in to_add:
                total_additions = total_additions + x["amount"]
        net_pay = (payslip.amount + total_additions) - total_deductions
        print(net_pay, payslip.amount, total_additions, total_deductions)
        return {
            'id': payslip.id,
            'employee': user_parser(payslip.employee),
            'prepared_by': user_parser(payslip.prepared_by),
            'date': payslip.date,
            'period': payslip.period,
            'amount': payslip.amount,
            'status': payslip.status,
            'deductions': to_deduct,
            'additions': to_add,
            'net_pay': net_pay,
        }

def create_payslip(employee_id, prepared_by_id, date, period, amount, status, deductions, additions, company_name):
    try:
        User, Company, Tasks, Payslips, Messages = models.create_model_tables(company_name)
        deductions = json.dumps(deductions)
        additions = json.dumps(additions)
        payslip = Payslips(
            employee_id=employee_id,
            prepared_by_id=prepared_by_id,
            date=date,
            period=period,
            amount=amount,
            status=status,
            deductions=deductions,
            additions=additions,
        )
        models.session.add(payslip)
        models.session.commit()
        return {
            "success": True,
            "payslip": payslip_parser(payslip),
            "error": None,
        }
    except Exception as e:
        print(e)
        return {
            "success": False,
            "payslip": None,
            "error": e,
        }
    
def get_payslips(company_name):
    try:
        User, Company, Tasks, Payslips, Messages = models.create_model_tables(company_name)
        payslips = models.session.query(Payslips).all()
        res = payslip_parser(payslips, many=True)
        return {
            "success": True,
            "payslips": res,
            "error": None,
        }
    except Exception as e:
        print(e)
        return {
            "success": False,
            "payslips": None,
            "error": e,
        }
    
def get_payslip_by_id(payslip_id, company_name):
    try:
        User, Company, Task, Payslip, Messages = models.create_model_tables(company_name)
        payslip = models.session.query(Payslip).filter_by(id=payslip_id).first()
        obj = payslip_parser(payslip)
        return {
            "success": True,
            "payslip": obj,
            "error": None,
        }
    except Exception as e:
        print(e)
        return {
            "success": False,
            "payslip": None,
            "error": e,
        }
    
def get_employee_payslips(employee_id, company_name):
    try:
        User, Company, Task, Payslip, Messages = models.create_model_tables(company_name)
        payslips = models.session.query(Payslip).filter_by(employee_id=employee_id).all()
        res = payslip_parser(payslips, many=True)
        return {
            "success": True,
            "payslips": res,
            "error": None,
        }
    except Exception as e:
        print(e)
        return {
            "success": False,
            "payslips": None,
            "error": e,
        }

def edit_payslip(payslip_id, employee_id, prepared_by_id, date, period, amount, status, deductions, additions, company_name):
    try:
        User, Company, Task, Payslip, Messages = models.create_model_tables(company_name)
        payslip = models.session.query(Payslip).filter_by(id=payslip_id).first()
        payslip.employee_id = employee_id
        payslip.prepared_by_id = prepared_by_id
        payslip.date = date
        payslip.period = period
        payslip.amount = amount
        payslip.status = status
        payslip.deductions = deductions
        payslip.additions = additions
        models.session.commit()
        return {
            "success": True,
            "payslip": payslip_parser(payslip),
            "error": None,
        }
    except Exception as e:
        print(e)
        return {
            "success": False,
            "payslip": None,
            "error": e,
        }