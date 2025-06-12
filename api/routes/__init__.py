from flask import Blueprint

tasks = Blueprint("tasks",__name__)
primitives = Blueprint("primitives",__name__)

from api.routes.primitives_implementation import groups,partialgroups,chains,partialchain,chords
from api.routes.calls import start_add,task_result,start_addApplyAsync,start_addFullSignature,start_addImpartialSignature