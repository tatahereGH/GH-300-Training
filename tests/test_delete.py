"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint using Arrange-Act-Assert pattern.
"""
import pytest


def test_delete_participant_success(client):
    """Test successful deletion removes participant from activity."""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    initial_response = client.get("/activities")
    assert email in initial_response.json()[activity]["participants"]
    
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    
    # Verify participant was removed
    updated_response = client.get("/activities")
    assert email not in updated_response.json()[activity]["participants"]


def test_delete_participant_not_found(client):
    """Test delete fails with 404 when participant not in activity."""
    # Arrange
    email = "nonexistent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_delete_activity_not_found(client):
    """Test delete fails with 404 when activity doesn't exist."""
    # Arrange
    email = "student@mergington.edu"
    activity = "FakeActivity"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_reduces_participant_count(client):
    """Test that participant count decreases after deletion."""
    # Arrange
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Act
    client.delete(f"/activities/{activity}/participants/{email}")
    
    # Assert
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity]["participants"])
    assert updated_count == initial_count - 1


def test_delete_preserves_other_participants(client):
    """Test that deleting one participant doesn't affect others."""
    # Arrange
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    activity = "Chess Club"
    
    # Act
    client.delete(f"/activities/{activity}/participants/{email_to_remove}")
    
    # Assert
    activities_data = client.get("/activities").json()
    assert email_to_remove not in activities_data[activity]["participants"]
    assert email_to_keep in activities_data[activity]["participants"]


def test_delete_participant_then_signup_again(client):
    """Test that a participant can re-signup after being deleted."""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act & Assert - Delete
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    
    # Act & Assert - Verify removal
    activities_before = client.get("/activities").json()
    assert email not in activities_before[activity]["participants"]
    
    # Act & Assert - Re-signup
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # Act & Assert - Verify re-added
    activities_after = client.get("/activities").json()
    assert email in activities_after[activity]["participants"]


def test_delete_from_different_activities(client):
    """Test deleting participant from one activity doesn't affect others."""
    # Arrange
    email = "emma@mergington.edu"
    activity_to_delete_from = "Programming Class"
    other_activity = "Gym Class"
    
    # First, sign up for the other activity
    client.post(f"/activities/{other_activity}/signup?email={email}")
    
    # Act - Delete from Programming Class
    response = client.delete(f"/activities/{activity_to_delete_from}/participants/{email}")
    
    # Assert
    assert response.status_code == 200
    
    activities_data = client.get("/activities").json()
    assert email not in activities_data[activity_to_delete_from]["participants"]
    assert email in activities_data[other_activity]["participants"]
