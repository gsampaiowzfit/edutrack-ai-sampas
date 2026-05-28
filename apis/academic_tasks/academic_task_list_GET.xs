query "academic_task/list" verb=GET {
  api_group = "AcademicTasks"
  auth = "user"

  input {
  }

  stack {
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
      output = [
        "id"
        "created_at"
        "updated_at"
        "title"
        "description"
        "due_date"
        "status"
        "subject_id"
        "user_id"
      ]
    } as $tasks
  }

  response = $tasks
  tags = ["xano:quick-start"]
}