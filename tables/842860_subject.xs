// Stores academic subjects owned by individual users
table subject {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int owner_id {
      table = "user"
    }
  
    text name filters=trim
    text? code filters=trim
    text? description filters=trim
    text? semester filters=trim
    text? status filters=trim
    bool deleted? {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "owner_id", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
}