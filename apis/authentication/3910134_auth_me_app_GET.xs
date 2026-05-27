// Get the user record belonging to the authentication token
query "auth/me_app" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    // Get the user record based on the auth ID
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "name", "email", "account_id", "role"]
    } as $user
  }

  response = $user
  tags = ["xano:quick-start"]
}