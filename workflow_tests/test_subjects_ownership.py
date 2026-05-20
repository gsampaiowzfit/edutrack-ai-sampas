def _read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def test_create_sets_owner_id():
    content = _read('apis/subjects/3784200_subject_create_POST.xs')
    assert 'owner_id' in content and '$auth.id' in content, 'create endpoint must set owner_id from auth'


def test_list_filters_by_owner_and_not_deleted():
    content = _read('apis/subjects/3784201_subject_list_GET.xs')
    assert 'owner_id' in content and 'deleted' in content
    assert 'owner_id == $auth.id' in content or '$auth.id' in content


def test_update_checks_owner():
    content = _read('apis/subjects/3784202_subject_update_PATCH.xs')
    assert 'precondition ($subject.owner_id == $auth.id)' in content or 'owner_id == $auth.id' in content


def test_delete_checks_owner():
    content = _read('apis/subjects/3784203_subject_delete_DELETE.xs')
    assert 'precondition ($subject.owner_id == $auth.id)' in content or 'owner_id == $auth.id' in content


def test_get_endpoint_exists_and_checks_owner():
    content = _read('apis/subjects/3784204_subject_get_GET.xs')
    assert 'db.get subject' in content
    assert 'precondition ($subject.owner_id == $auth.id)' in content or 'owner_id == $auth.id' in content
