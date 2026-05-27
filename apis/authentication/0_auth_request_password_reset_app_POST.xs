query "auth/request_password_reset_app" verb=POST {
  api_group = "Authentication"

  input {
    email email filters=trim|lower
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    precondition ($user != null) {
      error_type = "notfound"
      error = "User not found with this email."
    }
  
    var $token {
      value = "123456"
    }
  
    var $expiration {
      value = now
        |add_secs_to_timestamp:(3600|to_int)
    }
  
    db.patch user {
      field_name = "id"
      field_value = $user.id
      data = {
        password_reset: {
          token: $token
          expiration: $expiration
          used: false
        }
      }
    } as $result
  }

  response = {
    message: "Reset token generated successfully."
    token  : "123456"
  }
}