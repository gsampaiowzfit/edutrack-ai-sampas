// Update an academic subject owned by the authenticated user
query "subject/update" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
    text? name
    text? code
    text? description
    text? semester
    text? status
  }

  stack {
    db.get subject {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    precondition ($subject.owner_id == $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to update this subject."
    }
  
    db.patch subject {
      field_name = "id"
      field_value = $subject.id
      data = {
        name       : $input.name
        code       : $input.code
        description: $input.description
        semester   : $input.semester
        status     : $input.status
      }|filter_empty_text:""
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["xano:quick-start"]
}