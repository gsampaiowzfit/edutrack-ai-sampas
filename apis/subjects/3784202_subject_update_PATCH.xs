// Update an academic subject owned by the authenticated user
query "subject/update" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
    text? name
    text? code
    text? status
    text? teacher
    int? workload
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
  
    var $new_name {
      value = $input.name != null && $input.name != "" ? $input.name : $subject.name
    }
  
    var $new_teacher {
      value = $input.teacher != null && $input.teacher != "" ? $input.teacher : $subject.teacher
    }
  
    db.query subject {
      where = $db.subject.owner_id == $auth.id && $db.subject.name == $new_name && $db.subject.teacher == $new_teacher && $db.subject.id != $subject.id && $db.subject.deleted == false
      return = {type: "single"}
    } as $existing_duplicate
  
    precondition ($existing_duplicate == null) {
      error_type = "badrequest"
      error = "Já existe outra disciplina cadastrada com este mesmo nome e professor."
    }
  
    db.patch subject {
      field_name = "id"
      field_value = $subject.id
      data = {
        name       : $input.name
        code       : $input.code
        status     : $input.status
        teacher    : $input.teacher
        workload   : $input.workload
      }|filter_empty_text:""
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["xano:quick-start"]
}