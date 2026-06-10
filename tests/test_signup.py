"""
Tests for POST /activities/{activity_name}/signup endpoint using Arrange-Act-Assert pattern.
"""
import pytest


def test_signup_success(client):
    """Test successful signup adds email to activity participants."""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_returns_success_message(client):
    """Test that successful signup returns appropriate message."""
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Gym Class"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    result = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "message" in result
    assert email in result["message"]
    assert activity in result["message"]


def test_signup_activity_not_found(client):
    """Test signup fails with 404 when activity doesn't exist."""
    # Arrange
    email = "student@mergington.edu"
    activity = "NonexistentActivity"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email(client):
    """Test signup fails with 400 when student already registered."""
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_updates_participant_count(client):
    """Test that participant count updates after successful signup."""
    # Arrange
    email = "newuser@mergington.edu"
    activity = "Programming Class"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Act
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity]["participants"])
    assert updated_count == initial_count + 1


def test_signup_multiple_different_activities(client):
    """Test that same student can signup for different activities."""
    # Arrange
    email = "versatile@mergington.edu"
    activities_to_join = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    for activity in activities_to_join:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Assert
    activities_data = client.get("/activities").json()
    for activity in activities_to_join:
        assert email in activities_data[activity]["participants"]


def test_signup_different_students_same_activity(client):
    """Test that multiple students can signup for the same activity."""
    # Arrange
    students = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
    activity = "Gym Class"
    
    # Act
    for email in students:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Assert
    activities_data = client.get("/activities").json()
    for email in students:
        assert email in activities_data[activity]["participants"]
