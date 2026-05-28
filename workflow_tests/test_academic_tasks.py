def _read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def test_create_task_endpoint():
    content = _read('apis/academic_tasks/academic_task_create_POST.xs')
    assert 'query "academic_task/create"' in content
    assert 'auth = "user"' in content
    assert 'db.get subject' in content
    assert 'db.add academic_tasks' in content
    assert '$auth.id' in content


def test_list_tasks_endpoint():
    content = _read('apis/academic_tasks/academic_task_list_GET.xs')
    assert 'query "academic_task/list"' in content
    assert 'auth = "user"' in content
    assert 'db.query academic_tasks' in content
    assert '$db.academic_tasks.user_id == $auth.id' in content


def test_update_task_endpoint():
    content = _read('apis/academic_tasks/academic_task_update_PATCH.xs')
    assert 'query "academic_task/update"' in content
    assert 'auth = "user"' in content
    assert 'db.get academic_tasks' in content
    assert 'db.patch academic_tasks' in content
    assert 'filter_empty_text' in content


def test_delete_task_endpoint():
    content = _read('apis/academic_tasks/academic_task_delete_DELETE.xs')
    assert 'query "academic_task/delete"' in content
    assert 'auth = "user"' in content
    assert 'db.get academic_tasks' in content
    assert 'db.del academic_tasks' in content
