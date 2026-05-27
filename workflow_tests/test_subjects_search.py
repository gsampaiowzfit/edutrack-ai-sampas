def _read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def test_search_endpoint_exists():
    content = _read('apis/subjects/search_GET.xs')
    assert 'query "subject/search_v2"' in content or 'subject/search_v2' in content


def test_search_checks_auth_and_filters():
    content = _read('apis/subjects/search_GET.xs')
    assert 'auth = "user"' in content
    assert 'due_date' in content or 'overdue' in content
    assert '$auth.id' in content


def test_search_returns_overdue_count():
    content = _read('apis/subjects/search_GET.xs')
    assert 'overdue_tasks_count' in content
