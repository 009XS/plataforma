import requests

BASE_URL = "http://127.0.0.1:5000"

ENDPOINTS = [
    "/panel-alumno",
    "/panel-docente",
    "/panel-admin",
    "/panel-tutor",
    "/panel-orientador",
    "/api/user/me",
    "/api/flashcards",
    "/api/tasks",
    "/api/crear-usuario"
]

def verify_protection():
    print("Verifying endpoint protection...")
    issues = []
    for endpoint in ENDPOINTS:
        try:
            url = f"{BASE_URL}{endpoint}"
            # Don't follow redirects to check for 302 (redirect to login) or 401
            response = requests.get(url, allow_redirects=False)
            
            # Expecting 302 (Redirect to login) or 401 (Unauthorized)
            if response.status_code in [302, 401]:
                print(f"[OK] {endpoint} is protected (Status: {response.status_code})")
            else:
                print(f"[FAIL] {endpoint} returned {response.status_code}. Content excerpt: {response.text[:100]}")
                issues.append(endpoint)
        except Exception as e:
            print(f"[ERROR] connecting to {endpoint}: {e}")
            issues.append(endpoint)

    if not issues:
        print("\nAll endpoints appear protected.")
    else:
        print(f"\nIssues found with: {issues}")

if __name__ == "__main__":
    verify_protection()
