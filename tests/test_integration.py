def test_signup_then_unregister_updates_activity_participants(client):
    # Arrange
    activity_name = "Debate Team"
    email = "workflow.student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    after_signup = client.get("/activities").json()[activity_name]["participants"]
    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    after_unregister = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert email in after_signup
    assert unregister_response.status_code == 200
    assert email not in after_unregister
