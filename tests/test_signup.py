def test_signup_adds_participant_successfully(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "new.student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_only_increments_participants_on_success(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "count.check@mergington.edu"
    before_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act
    success_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    duplicate_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    after_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Assert
    assert success_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert after_count == before_count + 1
