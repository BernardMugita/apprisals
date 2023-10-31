import models
from user_funcs import user_parser

def task_parser(task, many=False):
    if many:
        return [task_parser(item) for item in task]
    else:
        return {
            'id': task.id,
            'assigned_to': user_parser(task.assigned_to),
            'assigned_by': user_parser(task.assigned_by),
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'task_type': task.task_type,
            'rating': task.rating,
            'feedback': task.feedback,
            'due_date': task.due_date,
        }

def create_task(title, description, status, assigned_to_id, assigned_by_id, task_type, rating, feedback, due_date, company_name):
    try:
        models.Base.metadata.clear()
        user_table = models.create_users_table(company_name)
        company_table = models.create_companies_table(user_table)
        task_table = models.create_tasks_table(company_name)
        task = task_table(
            title=title,
            description=description,
            status=status,
            assigned_to_id=assigned_to_id,
            assigned_by_id=assigned_by_id,
            task_type=task_type,
            rating=rating,
            feedback=feedback,
            due_date=due_date,
        )
        models.session.add(task)
        models.session.commit()
        return "Success"
    except Exception as e:
        print(e)
        return f"Error: {e}"
    
def get_tasks(company_name):
    try:
        models.Base.metadata.clear()
        task_table = models.create_tasks_table(company_name)
        usr_table = models.create_users_table(company_name)
        company_table = models.create_companies_table(usr_table)
        tasks = models.session.query(task_table).all()
        res = task_parser(tasks, many=True)
        return res
    except Exception as e:
        print(e)
        return f"Error: {e}"
    
def get_task_by_id(task_id, company_name):
    try:
        models.Base.metadata.clear()
        task_table = models.create_tasks_table(company_name)
        usr_table = models.create_users_table(company_name)
        company_table = models.create_companies_table(usr_table)
        task = models.session.query(task_table).filter_by(id=task_id).first()
        obj = task_parser(task)
        return obj
    except Exception as e:
        print(e)
        return f"Error: {e}"
    
def edit_task(title, description, status, assigned_to_id, assigned_by_id, task_type, rating, feedback, due_date, company_name):
    try:
        models.Base.metadata.clear()
        task_table = models.create_tasks_table(company_name)
        usr_table = models.create_users_table(company_name)
        company_table = models.create_companies_table(usr_table)
        task = models.session.query(task_table).filter_by(title=title).first()
        task.description = description
        task.status = status
        task.assigned_to_id = assigned_to_id
        task.assigned_by_id = assigned_by_id
        task.task_type = task_type
        task.rating = rating
        task.feedback = feedback
        task.due_date = due_date
        models.session.commit()
        return "Success"
    except Exception as e:
        print(e)
        return f"Error: {e}"
    
def delete_task(task_id, company_name):
    try:
        models.Base.metadata.clear()
        task_table = models.create_tasks_table(company_name)
        usr_table = models.create_users_table(company_name)
        company_table = models.create_companies_table(usr_table)
        task = models.session.query(task_table).filter_by(id=task_id).first()
        models.session.delete(task)
        models.session.commit()
        return "Success"
    except Exception as e:
        print(e)
        return f"Error: {e}"
    
def mark_done(task_id, company_name):
    try:
        models.Base.metadata.clear()
        task_table = models.create_tasks_table(company_name)
        usr_table = models.create_users_table(company_name)
        company_table = models.create_companies_table(usr_table)
        task = models.session.query(task_table).filter_by(id=task_id).first()
        task.status = "Done"
        models.session.commit()
        return "Success"
    except Exception as e:
        print(e)
        return f"Error: {e}"
    
def mark_dispute(task_id, company_name):
    try:
        models.Base.metadata.clear()
        task_table = models.create_tasks_table(company_name)
        usr_table = models.create_users_table(company_name)
        company_table = models.create_companies_table(usr_table)
        task = models.session.query(task_table).filter_by(id=task_id).first()
        task.status = "Disputed"
        models.session.commit()
        return "Success"
    except Exception as e:
        print(e)
        return f"Error: {e}"