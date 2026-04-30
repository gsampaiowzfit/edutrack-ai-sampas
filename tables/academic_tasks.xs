// Stores academic tasks for students, linked to subjects and users
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    timestamp updated_at?=now {
      visibility = "private"
    }
  
    text title filters=trim
    text? description filters=trim
    date due_date
    text status filters=trim
    int subject_id {
      table = "subject"
    }
  
    int user_id {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
}