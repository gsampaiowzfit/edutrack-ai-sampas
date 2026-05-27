query "auth/reset_password_app" verb=POST {
  api_group = "Authentication"

  input {
    email email filters=trim|lower
    text token
    text password
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    precondition ($user != null) {
      error_type = "notfound"
      error = "User not found."
    }
  
    precondition ($user.password_reset != null) {
      error_type = "accessdenied"
      error = "No password reset requested for this user."
    }
  
    precondition ($user.password_reset.used == false) {
      error_type = "accessdenied"
      error = "This token has already been used."
    }
  
    precondition ($user.password_reset.expiration > now) {
      error_type = "accessdenied"
      error = "This token has expired."
    }
  
    security.check_password {
      text_password = $input.token
      hash_password = $user.password_reset.token
    } as $token_ok
  
    precondition ($token_ok) {
      error_type = "accessdenied"
      error = "Invalid reset token."
    }
  
    db.patch user {
      field_name = "id"
      field_value = $user.id
      data = {
        password      : $input.password
        password_reset: {
          used: true
        }
      }
    } as $result
  }

  response = {
    message: "Password reset successfully. You can now login with your new credentials."
  }
}