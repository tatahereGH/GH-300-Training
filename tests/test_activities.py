"""
Tests for GET /activities endpoint using Arrange-Act-Assert pattern.
"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities with correct structure."""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert isinstance(activities_data, dict)
    assert set(activities_data.keys()) == set(expected_activities)


def test_get_activities_returns_correct_fields(client):
    """Test that each activity has all required fields."""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    for activity_name, activity_details in activities_data.items():
        assert isinstance(activity_details, dict)
        assert required_fields.issubset(set(activity_details.keys()))
        assert isinstance(activity_details["participants"], list)
        assert isinstance(activity_details["max_participants"], int)


def test_get_activities_includes_initial_participants(client):
    """Test that activities include pre-populated participants."""
    # Arrange
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert "michael@mergington.edu" in activities_data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities_data["Chess Club"]["participants"]
    assert "emma@mergington.edu" in activities_data["Programming Class"]["participants"]
    assert "john@mergington.edu" in activities_data["Gym Class"]["participants"]
