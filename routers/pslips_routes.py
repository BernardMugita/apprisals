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
    

