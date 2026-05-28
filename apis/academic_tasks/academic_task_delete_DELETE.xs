query "academic_task/delete" verb=DELETE {
  api_group = "AcademicTasks"
  auth = "user"

  input {
    int task_id
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.task_id
    } as $task
  
    precondition ($task != null) {
      error_type = "notfound"
      error = "Task not found."
    }
  
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to delete this task."
    }
  
    db.del academic_tasks {
      field_name = "id"
      field_value = $task.id
    }
  }

  response = $task
  tags = ["xano:quick-start"]
}