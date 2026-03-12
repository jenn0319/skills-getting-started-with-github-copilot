def test_unregister_removes_participant_successfully(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    # Act
    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    activities_response = client.get("/activities")

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_registered_participant(client):
    # Arrange
    activity_name = "Tennis Club"
    email = "missing.student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_only_decrements_participants_on_success(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    missing_email = "not.there@mergington.edu"
    before_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act
    success_response = client.delete(f"/activities/{activity_name}/participants/{existing_email}")
    not_found_response = client.delete(f"/activities/{activity_name}/participants/{missing_email}")
    after_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Assert
    assert success_response.status_code == 200
    assert not_found_response.status_code == 404
    assert after_count == before_count - 1
