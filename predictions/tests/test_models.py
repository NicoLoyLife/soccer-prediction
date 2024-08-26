# soccer_predictor/predictions/tests/test_models.py

import pytest
from django.contrib.auth.models import User
from predictions.models import YourModel  # Ersetze mit deinem Modell


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user("testuser", "test@example.com", "testpassword")
    assert user.username == "testuser"
    assert user.email == "test@example.com"


@pytest.mark.django_db
def test_your_model():
    # Beispiel-Test für dein Modell
    instance = YourModel.objects.create(field1="value1", field2="value2")
    assert instance.field1 == "value1"
    assert instance.field2 == "value2"
