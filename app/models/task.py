from app import db
# name - The name of the task
# description - A text description of the task
# completed_at - The date, saved as text, in which the task was completed.


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime,default=None)
    # is_complete=db.Column(db.String,default=False)


# nullable=True