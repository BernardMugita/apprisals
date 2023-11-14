from fastapi import APIRouter
from fastapi import Request

import pslips_funcs
import user_funcs

router = APIRouter()

@router.post("/payslips/create_payslip")
async def create_payslip(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            employee_id = data["employee_id"]
            prepared_by_id = data["prepared_by_id"]
            date = data["date"]
            period = data["period"]
            amount = data["amount"]
            status = data["status"]
            deductions = data["deductions"]
            additions = data["additions"]
            company_name = usr["organization"]
            ans = pslips_funcs.create_payslip(employee_id, prepared_by_id, date, period, amount, status, deductions, additions, company_name)
            return ans        
    else:
        return "Invalid Token"
    
@router.post("/payslips/get_all_payslips")
async def get_all_payslips(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            # data = await request.json()
            company_name = usr["organization"]
            ans = pslips_funcs.get_payslips(company_name)
            return ans        
    else:
        return "Invalid Token"
    
@router.post("/payslips/get_employee_payslips")
async def get_employee_payslips(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            employee_id = data["employee_id"]
            company_name = usr["organization"]
            ans = pslips_funcs.get_employee_payslips(employee_id, company_name)
            return ans        
    else:
        return "Invalid Token"
    
    
@router.post("/payslips/get_own_payslips")
def get_own_payslip(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            employee_id = usr["id"]
            company_name = usr["organization"]
            ans = pslips_funcs.get_employee_payslips(employee_id, company_name)
            return ans        
    else:
        return "Invalid Token"

@router.post("/payslips/get_payslip_by_id")
async def get_by_id(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            payslip_id = data["payslip_id"]
            company_name = usr["organization"]
            ans = pslips_funcs.get_payslip_by_id(payslip_id, company_name)
            return ans        
    else:
        return "Invalid Token"