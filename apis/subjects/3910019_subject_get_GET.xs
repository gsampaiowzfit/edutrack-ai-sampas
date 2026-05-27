// Get a single academic subject owned by the authenticated user
query "subject/get" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
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
      error = "You do not have permission to view this subject."
    }
  }

  response = $subject
  tags = ["xano:quick-start"]
}