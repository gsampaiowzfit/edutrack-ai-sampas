// List academic subjects owned by the authenticated user
query "subject/list" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subject {
      where = $db.subject.owner_id == $auth.id && $db.subject.deleted == false
      return = {type: "list"}
      output = [
        "id"
        "created_at"
        "name"
        "code"
        "status"
        "owner_id"
        "teacher"
        "workload"
      ]
    } as $subjects
  }

  response = $subjects
  tags = ["xano:quick-start"]
}