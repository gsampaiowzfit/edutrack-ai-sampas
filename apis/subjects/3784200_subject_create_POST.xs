// Create a new academic subject owned by the authenticated user
query "subject/create" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name
    text? code
    text? status
    text? teacher
    text? semester
    int? workload
  }

  stack {
    precondition ($input.name != null && $input.name != "") {
      error_type = "badrequest"
      error = "Subject name is required."
    }
  
    db.query subject {
      where = $db.subject.owner_id == $auth.id && $db.subject.name == $input.name && $db.subject.teacher == $input.teacher && $db.subject.deleted == false
      return = {type: "single"}
    } as $existing_subject
  
    precondition ($existing_subject == null) {
      error_type = "badrequest"
      error = "Já existe uma disciplina cadastrada com este mesmo nome e professor."
    }
  
    db.add subject {
      data = {
        owner_id: $auth.id
        name    : $input.name
        code    : $input.code
        status  : $input.status
        teacher : $input.teacher
        semester: $input.semester
        workload: $input.workload
      }
    } as $subject
  }

  response = $subject
  tags = ["xano:quick-start"]
}