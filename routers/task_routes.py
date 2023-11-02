from fastapi import APIRouter
from fastapi import Request
import task_funcs
import user_funcs

router = APIRouter()

@router.post("/tasks/create_task")
async def create_task(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            title = data["title"]
            description = data["description"]
            status = data["status"]
            assigned_to_id = data["assigned_to_id"]
            assigned_by_id = data["assigned_by_id"]
            task_type = data["task_type"]
            rating = data["rating"]
            feedback = data["feedback"]
            due_date = data["due_date"]
            company_name = usr["organization"]
            ans = task_funcs.create_task(title, description, status, assigned_to_id, assigned_by_id, task_type, rating, feedback, due_date, company_name)
            return ans        
    else:
        return "Invalid Token"
    
@router.post("/tasks/get_tasks")
def get_all_tasks(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            company_name = usr["organization"]
            ans = task_funcs.get_tasks(company_name)
            return ans        
    else:
        return "Invalid Token"
    
@router.post("/tasks/get_task_by_id")
async def get_task_by_id(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            task_id = data["task_id"]
            company_name = usr["organization"]
            ans = task_funcs.get_task_by_id(task_id, company_name)
            return ans        
    else:
        return "Invalid Token"
    
@router.post("/tasks/edit_task")
async def edit_single_task(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            title = data["title"]
            description = data["description"]
            status = data["status"]
            assigned_to_id = data["assigned_to_id"]
            assigned_by_id = data["assigned_by_id"]
            task_type = data["task_type"]
            rating = data["rating"]
            feedback = data["feedback"]
            due_date = data["due_date"]
            company_name = usr["organization"]
            ans = task_funcs.edit_task(title, description, status, assigned_to_id, assigned_by_id, task_type, rating, feedback, due_date, company_name)
            return ans        
    else:
        return "Invalid Token"

@router.post("/tasks/mark_done")
async def mark_done(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            task_id = data["task_id"]
            company_name = usr["organization"]
            ans = task_funcs.mark_done(task_id, company_name)
            return ans        
    else:
        return "Invalid Token"
    
@router.post("/tasks/mark_disputed")
async def mark_disputed(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            task_id = data["task_id"]
            company_name = usr["organization"]
            ans = task_funcs.mark_disputed(task_id, company_name)
            return ans        
    else:
        return "Invalid Token"
    
@router.post("/tasks/mark_pending")
async def mark_pending(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            data = await request.json()
            task_id = data["task_id"]
            company_name = usr["organization"]
            ans = task_funcs.mark_pending(task_id, company_name)
            return ans        
    else:
        return "Invalid Token"
    
@router.post("/tasks/get_all_pending")
async def get_all_pending(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == "Invalid":
            return "Invalid Token"
        else:
            user_id = usr["id"]
            company_name = usr["organization"]
            ans = task_funcs.get_all_pending(user_id, company_name)
            return ans
    else:
        return "Invalid Token"
    
@router.post("/tasks/get_all_done")
async def get_all_done(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == "Invalid":
            return "Invalid Token"
        else:
            user_id = usr["id"]
            company_name = usr["organization"]
            ans = task_funcs.get_all_done(user_id, company_name)
            return ans
    else:
        return "Invalid Token"
    