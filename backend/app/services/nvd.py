from typing import Any

import httpx

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


class NVDService:
    """Client for the NVD CVE API 2.0."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def get_cve(self, cve_id: str) -> dict[str, Any] | None:
        headers = {
            "Accept": "application/json",
            "User-Agent": "security-dashboard/0.1",
        }

        if self.api_key:
            headers["apiKey"] = self.api_key

        response = httpx.get(
            NVD_API_URL,
            params={"cveId": cve_id},
            headers=headers,
            timeout=15.0,
        )

        response.raise_for_status()

        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])

        if not vulnerabilities:
            return None

        return vulnerabilities[0]["cve"]
