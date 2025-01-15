import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from wastory.main import app
from wastory.app.blog.service import BlogService

client = TestClient(app)

@pytest.fixture
def mock_login_headers():
    """Mock 헤더로 사용자 인증 정보를 생성."""
    return {
        "X-Wastory-Username": "test_user",
        "X-Wastory-Password": "test_password"
    }

@pytest.fixture
def mock_blog_service():
    """BlogService의 Mock 객체를 생성."""
    mock_service = MagicMock(spec=BlogService)
    app.dependency_overrides[BlogService] = lambda: mock_service
    return mock_service

# 1. Create Blog 테스트
def test_create_blog(mock_login_headers, mock_blog_service):
    mock_blog_service.create_blog = AsyncMock(return_value={
        "name": "test_blog",
        "owner": "test_user",
        "description": "Test description"
    })
    
    response = client.post(
        "/api/blog",
        headers=mock_login_headers,
        json={"address_name": "test_blog"}
    )
    assert response.status_code == 201
    assert response.json() == {
        "name": "test_blog",
        "owner": "test_user",
        "description": "Test description"
    }
    mock_blog_service.create_blog.assert_called_once_with(
        user=mock_login_headers,
        name="test_blog"
    )

# 2. Get My Blog 테스트
def test_get_my_blog(mock_login_headers, mock_blog_service):
    mock_blog_service.get_blog_by_user = AsyncMock(return_value={
        "name": "my_blog",
        "owner": "test_user",
        "description": "Test description"
    })
    
    response = client.get(
        "/api/blog/my_blog",
        headers=mock_login_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "my_blog",
        "owner": "test_user",
        "description": "Test description"
    }
    mock_blog_service.get_blog_by_user.assert_called_once()

# 3. Get Blog By Address Name 테스트
def test_get_blog_by_address_name(mock_blog_service):
    mock_blog_service.get_blog_by_address_name = AsyncMock(return_value={
        "name": "test_blog",
        "description": "Test description"
    })

    response = client.get("/api/blog/test_blog")
    assert response.status_code == 200
    assert response.json() == {
        "name": "test_blog",
        "description": "Test description"
    }
    mock_blog_service.get_blog_by_address_name.assert_called_once_with(
        address_name="test_blog"
    )

# 4. Update Blog 테스트
def test_update_blog(mock_login_headers, mock_blog_service):
    mock_blog_service.update_blog = AsyncMock(return_value={
        "name": "updated_blog",
        "description": "Updated description"
    })

    response = client.patch(
        "/api/blog/test_blog",
        headers=mock_login_headers,
        json={"blog_name": "updated_blog", "description": "Updated description"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "updated_blog",
        "description": "Updated description"
    }
    mock_blog_service.update_blog.assert_called_once_with(
        address_name="test_blog",
        new_blog_name="updated_blog",
        new_description="Updated description"
    )
