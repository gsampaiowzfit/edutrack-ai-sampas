// Stores academic subjects owned by individual users
table subject {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int owner_id {
      table = "user"
    }
  
    text name filters=trim
    text? code filters=trim
    text? status?=active filters=trim
    text? teacher filters=trim
    text? semester filters=trim
    int? workload
    bool deleted?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "owner_id", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
}