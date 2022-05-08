
from app.models.task import Task
from app import db
from flask import Blueprint, jsonify,abort,make_response,request


task_list_bp = Blueprint("task_list", __name__,url_prefix="/tasks")


@task_list_bp.route("", methods=["post"])
def create_new_task():
    #************************
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at =request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return make_response(jsonify(f"Task {new_task.title} successfully created", 201))

@task_list_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    # sort_asc = request.args.get(Task.title.asc())
    # sort_dsc = request.args.get(Task.title.desc())

    # posts = Post.query.order_by(Post.title.asc()).all()
    if title_query: 
        task = Task.query.filter_by(title=title_query)
    if sort_query and sort_query=="asc":
        task= Task.query.order_by(Task.title.asc()).all()
    if sort_query and sort_query=="desc":
        task= Task.query.order_by(Task.title.desc()).all()

    # if sort_asc:
    #     task=Task.query.filter_by(title.asc())
    # if sort_dsc:
    #     task=Task.query.filter_by(title.desc())


        # query.order_by(SpreadsheetCells.y_index.desc()) # desc
    else:
        tasks = Task.query.all()
        
    task_response = []
    for task in tasks:
        task_response.append({
            "task_id": task.task_id,
            "name": task.title,
            "description": task.description
        })
    return jsonify(task_response)
#do we need 200 ok
# @task_list_bp.route("", methods=["GET"])
# def return_orderd():
#     ordered_task=Task.query.filter_by(title.asc())
#     return jsonify(ordered_task)


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
       #************************* ***
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

@task_list_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    return {
        "task_id": task.task_id,
        "name": task.title,
        "description": task.description}
@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(f"task #{task.task_id} successfully updated")

@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task #{task.task_id} successfully deleted") 

# @task_list_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
# def mark_complet(task_id):
#     request_body = request.get_json()
#     task.is_complete = request_body["is_complete"]

#     db.session.commit()

#     return make_response(f"task #{task.task_id} successfully updated")