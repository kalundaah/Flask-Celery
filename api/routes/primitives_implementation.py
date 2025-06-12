from flask import request
from tasks.long_task import add_together,mul
from celery.result import AsyncResult
from api.routes import primitives
from celery import group,chain,chord

@primitives.route("/groups",methods=["POST"])
def groups() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
 
    result = group(add_together.s(a,b) for i in range(10))()
    
    return {
        "result": result.get(),
    }   
    
@primitives.route("/partialgroups",methods=["POST"])
def partialgroups() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
 
    result = group(add_together.s(b) for i in range(10))()
    
    return {
        "result": result(a).get(),
    }
    
@primitives.route("/chain",methods=["POST"])
def chains() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
 
    result = chain(add_together.s(a,b) | mul.s(a))()

    return {
        "result": result.get(),
    }   
    
@primitives.route("/partialchain",methods=["POST"])
def partialchain() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
    
    result = chain(add_together.s(b) | mul.s(a))()
    
    return {
        "result": result(a).get(),
    }
   
@primitives.route("/chords",methods=["POST"])
def chords() -> dict[str,object]:
    a = request.form.get("a",type=int)
    b = request.form.get("b",type=int)
 
    result = chord((add_together.s(a,b) for i in range(10)),mul.s(a))()
    # result = ((add_together.s(a,b) for i in range(10)) | mul.s(a))() 

    return {
        "result": result.get(),
    }   
    
