Repository with a POC for a bug report

To illustrate the bug with some comments, see the tests in [poc/poc_models/tests.py](poc/poc_models/tests.py)

```
pip install django
```

```bash
cd poc
python manage.py test
```

The test `test_remote_object_does_not_exist_object_with_select_related_should_be_found` contains the failing behaviour.
