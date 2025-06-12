from flask import request
from tasks.long_task import add_together
from celery.result import AsyncResult
from api.routes import tasks
from celery import shared_task

@tasks.route("/add",methods=["POST"])
def start_add() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
    result = add_together.delay(a,b)
    
    return {
        "result_id":result.id,
        "result": result.get(timeout=1),
        "State" : result.state 
    }

@tasks.route("/addApplyAsync",methods=["POST"])
def start_addApplyAsync() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
    result = add_together.apply_async((a,b),queue='example',countdown=10)
   
    return {
        "result_id":result.id,
        "result": result.get(timeout=1),
        "State" : result.state 
    }

@tasks.route("/addFullSignature",methods=["POST"])
def start_addFullSignature() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
    task = add_together.signature((a,b),countdown=10)
    result = task.delay()
    
    return {
        "result_id":result.id,
        "result": result.get(timeout=1),
        "State" : result.state 
    }

@tasks.route("/addImpartialSugnature",methods=["POST"])
def start_addImpartialSignature() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
    task = add_together.signature((b),countdown=10,debug=False)
    result = task.delay(a,debug=True)
    
    return {
        "result_id":result.id,
        "result": result.get(timeout=1),
        "State" : result.state 
    }


@tasks.route("/result/<id>",methods=["GET"])
def task_result(id:str) -> dict[str,object]:
    result = AsyncResult(id)
    return{
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None
    }