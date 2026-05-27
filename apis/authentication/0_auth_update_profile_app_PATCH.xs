query "auth/update_profile_app" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    text? name
    email? email filters=trim|lower
  }

  stack {
    db.query user {
      where = $db.user.email == $input.email && $db.user.id != $auth.id
      return = {type: "single"}
    } as $existing_user
  
    precondition ($existing_user == null) {
      error_type = "accessdenied"
      error = "This email is already in use by another user."
    }
  
    db.patch user {
      field_name = "id"
      field_value = $auth.id
      data = {
        name : $input.name
        email: $input.email
      }|filter_empty_text:""
    } as $updated_user
  }

  response = $updated_user
}