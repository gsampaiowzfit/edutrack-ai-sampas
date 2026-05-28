query "academic_task/create" verb=POST {
  api_group = "AcademicTasks"
  auth = "user"

  input {
    text title
    text description?
    date due_date
    int subject_id
  }

  stack {
    precondition ($input.title != null && $input.title != "") {
      error_type = "badrequest"
      error = "Title is required."
    }
  
    precondition ($input.due_date != null) {
      error_type = "badrequest"
      error = "Due date is required."
    }
  
    precondition ($input.subject_id != null) {
      error_type = "badrequest"
      error = "Subject ID is required."
    }
  
    db.get subject {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    precondition ($subject != null && $subject.owner_id == $auth.id && $subject.deleted == false) {
      error_type = "notfound"
      error = "Subject not found or access denied."
    }
  
    db.add academic_tasks {
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : "pending"
        subject_id : $input.subject_id
        user_id    : $auth.id
      }
    } as $task
  }

  response = $task
  tags = ["xano:quick-start"]
}