import ipaddress
import socket
from urllib.parse import urlparse

BLOCKED_NETS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]


class URLExtractor:
    def _validate_host(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only http/https URLs are allowed")
        if not parsed.hostname:
            raise ValueError("URL hostname is required")

        for family, _, _, _, sockaddr in socket.getaddrinfo(parsed.hostname, None):
            ip = ipaddress.ip_address(sockaddr[0])
            if any(ip in blocked for blocked in BLOCKED_NETS):
                raise ValueError("Blocked URL target")
            if ip.is_loopback or ip.is_private or ip.is_link_local:
                raise ValueError("Blocked URL target")
            if family not in (socket.AF_INET, socket.AF_INET6):
                raise ValueError("Unsupported address family")

    def extract(self, url: str) -> str:
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError as exc:
            raise RuntimeError("URL extraction dependencies not installed: requests/bs4") from exc

        self._validate_host(url)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer", "noscript"]):
            tag.decompose()
        return " ".join(soup.stripped_strings)
