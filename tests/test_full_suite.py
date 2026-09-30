"""Comprehensive Test Suite for PocketSmart AI."""
import os
import io
import sys
from pathlib import Path
from PIL import Image

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models.user import User

client = TestClient(app)

def setup_module():
    """Ensure clean test database."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Clean test users
    db.query(User).filter(User.email.like("%test%@example.com")).delete(synchronize_session=False)
    db.commit()
    db.close()

def test_landing_page():
    res = client.get("/")
    assert res.status_code == 200
    assert "PocketSmart" in res.text
    assert "Plan smarter" in res.text

def test_user_registration_and_validation():
    # Valid registration
    reg_data = {
        "full_name": "Test User",
        "email": "testuser@example.com",
        "password": "Password123",
        "confirm_password": "Password123"
    }
    res = client.post("/api/register", json=reg_data)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "testuser@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data

    # Duplicate registration should fail
    dup_res = client.post("/api/register", json=reg_data)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

    # Password mismatch should fail
    mismatch_data = {
        "full_name": "Mismatch User",
        "email": "mismatch@example.com",
        "password": "Password123",
        "confirm_password": "DifferentPassword"
    }
    res_mismatch = client.post("/api/register", json=mismatch_data)
    assert res_mismatch.status_code == 422

def test_login_and_token():
    login_data = {
        "email": "testuser@example.com",
        "password": "Password123"
    }
    res = client.post("/api/login", json=login_data)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    token = data["access_token"]

    # Test invalid password
    bad_login = {
        "email": "testuser@example.com",
        "password": "WrongPassword"
    }
    res_bad = client.post("/api/login", json=bad_login)
    assert res_bad.status_code == 401

    # Test session-info with token header
    headers = {"Authorization": f"Bearer {token}"}
    sess_res = client.get("/api/session-info", headers=headers)
    assert sess_res.status_code == 200
    assert sess_res.json()["authenticated"] is True
    assert sess_res.json()["user"]["email"] == "testuser@example.com"

def test_home_planner_flow():
    # Login first
    login_res = client.post("/api/login", json={"email": "testuser@example.com", "password": "Password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    home_payload = {
        "total_budget": 60000,
        "currency": "₹",
        "home_type": "2BHK",
        "number_of_rooms": 2,
        "selected_rooms": ["Living Room", "Bedroom"],
        "quantities": {
            "lights": 4,
            "ceiling_fans": 2,
            "sofa": 1,
            "dining_table": 1,
            "chairs": 4,
            "bed": 1,
            "wardrobe": 1,
            "curtains": 2,
            "rugs": 1,
            "wall_art": 2,
            "storage": 1,
            "decorative_items": 3
        },
        "preferred_style": "Modern",
        "preferred_colors": "Warm beige, navy blue",
        "brand_preferences": "IKEA, Amazon"
    }

    res = client.post("/api/generate-home", json=home_payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "plan_id" in data
    assert data["budget"] == 60000
    assert len(data["budget_allocation"]) > 0
    assert len(data["recommendations"]) > 0
    assert data["total_estimated_cost"] > 0
    assert data["remaining_budget"] >= 0

    plan_id = data["plan_id"]

    # Verify viewing results HTML page
    res_html = client.get(f"/home-planner/results/{plan_id}", headers=headers)
    assert res_html.status_code == 200
    assert "Home Interior Plan Generated" in res_html.text

def test_party_planner_flow():
    login_res = client.post("/api/login", json={"email": "testuser@example.com", "password": "Password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    party_payload = {
        "total_budget": 45000,
        "currency": "₹",
        "event_type": "Birthday",
        "number_of_guests": 25,
        "location": "Central Delhi",
        "indoor_outdoor": "Indoor",
        "event_duration": "4 hours",
        "food_preference": "Both",
        "decoration_style": "Fairy Lights",
        "entertainment_preference": "DJ & Sound System",
        "accommodation_required": False
    }

    res = client.post("/api/generate-party", json=party_payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "plan_id" in data
    assert data["number_of_guests"] == 25
    assert data["cost_per_guest"] > 0
    assert len(data["budget_allocation"]) > 0
    assert len(data["recommendations"]) > 0

    plan_id = data["plan_id"]
    res_html = client.get(f"/party-planner/results/{plan_id}", headers=headers)
    assert res_html.status_code == 200
    assert "Event Budget Plan Generated" in res_html.text

def test_jewelry_planner_with_image_upload():
    login_res = client.post("/api/login", json={"email": "testuser@example.com", "password": "Password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Generate a dummy image in memory
    img_byte_arr = io.BytesIO()
    img = Image.new("RGB", (100, 100), color=(73, 109, 137))
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    files = {
        "outfit_image": ("outfit.png", img_byte_arr, "image/png")
    }
    data = {
        "total_budget": 20000,
        "currency": "₹",
        "occasion": "Wedding",
        "jewelry_type": "Jewelry Set",
        "preferred_style": "Traditional",
        "metal_preference": "Gold Plated",
        "color_preference": "Emerald green and pearls",
        "outfit_description": "Navy blue lehenga with gold zari work"
    }

    res = client.post("/api/generate-jewelry", data=data, files=files, headers=headers)
    assert res.status_code == 200
    resp_data = res.json()
    assert "plan_id" in resp_data
    assert resp_data["occasion"] == "Wedding"
    assert resp_data["jewelry_type"] == "Jewelry Set"
    assert len(resp_data["recommendations"]) > 0
    assert resp_data["image_url"] is not None

    plan_id = resp_data["plan_id"]
    res_html = client.get(f"/jewelry-planner/results/{plan_id}", headers=headers)
    assert res_html.status_code == 200
    assert "Jewelry Plan Generated" in res_html.text

def test_recommendation_save_and_history():
    login_res = client.post("/api/login", json={"email": "testuser@example.com", "password": "Password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch history
    res_hist = client.get("/api/history", headers=headers)
    assert res_hist.status_code == 200
    plans = res_hist.json()
    assert len(plans) >= 3

    first_plan_id = plans[0]["id"]

    # Toggle save
    res_save = client.post(f"/api/recommendations/{first_plan_id}/save", headers=headers)
    assert res_save.status_code == 200
    assert res_save.json()["is_saved"] is True

    # Check history HTML page
    res_page = client.get("/history", headers=headers)
    assert res_page.status_code == 200
    assert "Plan Archives" in res_page.text

    # Delete plan
    res_del = client.delete(f"/api/history/{first_plan_id}", headers=headers)
    assert res_del.status_code == 200
    assert res_del.json()["success"] is True

def test_dashboard():
    login_res = client.post("/api/login", json={"email": "testuser@example.com", "password": "Password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/dashboard", headers=headers)
    assert res.status_code == 200
    assert "Welcome" in res.text
    assert "Dashboard" in res.text

if __name__ == "__main__":
    setup_module()
    test_landing_page()
    test_user_registration_and_validation()
    test_login_and_token()
    test_home_planner_flow()
    test_party_planner_flow()
    test_jewelry_planner_with_image_upload()
    test_recommendation_save_and_history()
    test_dashboard()
    print("ALL TESTS PASSED SUCCESSFULLY!")
