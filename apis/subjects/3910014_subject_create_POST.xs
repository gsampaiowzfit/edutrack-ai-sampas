// Create a new academic subject owned by the authenticated user
query "subject/create" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name
    text? code
    text? description
    text? semester
    text? status
  }

  stack {
    precondition ($input.name != null && $input.name != "") {
      error_type = "invalid"
      error = "Subject name is required."
    }
  
    db.add subject {
      data = {
        owner_id   : $auth.id
        name       : $input.name
        code       : $input.code
        description: $input.description
        semester   : $input.semester
        status     : $input.status
      }
    } as $subject
  }

  response = $subject
  tags = ["xano:quick-start"]
}