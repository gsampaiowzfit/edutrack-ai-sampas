// Search subjects by name or by overdue tasks for the authenticated user
query "subject/search" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    text? name filters=trim
    bool overdue?
    int limit?=20
    int offset?
  }

  stack {
    var $name {
      value = $input.name
    }
  
    var $limit {
      value = $input.limit
    }
  
    var $offset {
      value = $input.offset
    }
  
    var $overdue_flag {
      value = $input.overdue == true
    }
  
    conditional {
      if (($name == null || $name == "") && $overdue_flag == false) {
        db.query subject {
          where = $db.subject.owner_id == $auth.id && $db.subject.deleted == false
          return = {type: "list"}
          output = ["id", "name", "description"]
        } as $subjects
      
        foreach ($subjects) {
          each as $s {
            var.update $s {
              value = $s|set:"overdue_tasks_count":0
            }
          }
        }
      
        db.query subject {
          where = $db.subject.owner_id == $auth.id && $db.subject.deleted == false
          return = {type: "count"}
        } as $total
      
        var $paginated_subjects {
          value = $subjects|slice:$offset:$limit
        }
      
        var $result {
          value = {items: $paginated_subjects, total: $total}
        }
      }
    
      else {
        var $name_ids {
          value = []
        }
      
        var $overdue_ids {
          value = []
        }
      
        conditional {
          if ($name != null && $name != "") {
            db.query subject {
              where = $db.subject.owner_id == $auth.id && $db.subject.deleted == false && ($db.subject.name like $name)
              return = {type: "list"}
              output = ["id"]
            } as $subjects_name
          
            foreach ($subjects_name) {
              each as $n {
                var.update $name_ids {
                  value = $name_ids|push:$n.id
                }
              }
            }
          }
        }
      
        conditional {
          if ($overdue_flag) {
            var $today {
              value = "now"
            }
          
            db.query academic_tasks {
              where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.due_date < $today && $db.academic_tasks.status != "completed"
              return = {type: "list"}
              output = ["subject_id"]
            } as $overdue_tasks
          
            foreach ($overdue_tasks) {
              each as $t {
                conditional {
                  if (!($overdue_ids|in:$t.subject_id)) {
                    var.update $overdue_ids {
                      value = $overdue_ids|push:$t.subject_id
                    }
                  }
                }
              }
            }
          }
        }
      
        var $union_ids {
          value = []
        }
      
        foreach ($name_ids) {
          each as $id {
            conditional {
              if (!($union_ids|in:$id)) {
                var.update $union_ids {
                  value = $union_ids|push:$id
                }
              }
            }
          }
        }
      
        foreach ($overdue_ids) {
          each as $id {
            conditional {
              if (!($union_ids|in:$id)) {
                var.update $union_ids {
                  value = $union_ids|push:$id
                }
              }
            }
          }
        }
      
        conditional {
          if (($union_ids|count) == 0) {
            var $result {
              value = {items: [], total: 0}
            }
          }
        
          else {
            db.query subject {
              where = ($db.subject.id in $union_ids) && $db.subject.owner_id == $auth.id && $db.subject.deleted == false
              return = {type: "list"}
              output = ["id", "name", "description"]
            } as $subjects
          
            foreach ($subjects) {
              each as $s {
                var.update $s {
                  value = $s|set:"overdue_tasks_count":0
                }
              }
            }
          
            var $paginated_subjects {
              value = $subjects|slice:$offset:$limit
            }
          
            var $total {
              value = $union_ids|count
            }
          
            var $result {
              value = {items: $paginated_subjects, total: $total}
            }
          }
        }
      }
    }
  }

  response = $result
  tags = ["xano:quick-start"]
}