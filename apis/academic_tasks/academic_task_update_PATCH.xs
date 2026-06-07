query "academic_task/update" verb=PATCH {
  api_group = "AcademicTasks"
  auth = "user"

  input {
    int task_id
    text? title
    text? description
    date? due_date
    text? status
    text? priority
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
      error = "You do not have permission to update this task."
    }
  
    precondition ($input.status == null || $input.status == "" || $input.status == "pending" || $input.status == "in_progress" || $input.status == "completed") {
      error_type = "badrequest"
      error = "Invalid status value. Must be pending, in_progress, or completed."
    }
  
    db.patch academic_tasks {
      field_name = "id"
      field_value = $task.id
      data = {
        title: $input.title
        description: $input.description
        due_date: $input.due_date
        status: $input.status
        priority: $input.priority
        updated_at: "now"
      }|filter_empty_text:""
    } as $updated_task
  }

  response = $updated_task
  tags = ["xano:quick-start"]
}