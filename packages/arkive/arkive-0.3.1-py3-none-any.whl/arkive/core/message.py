import json
from dataclasses import dataclass, field
from posixpath import join as urljoin
from typing import Dict, List, Any
from urllib.parse import urlencode


@dataclass
class RestMessage:
    host: str = ""
    scope: List[str] = field(default_factory=list)
    params: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    method: str = "GET"

    def encode_url(self):
        sanitized_scope = [item.strip("/") for item in self.scope]
        path = urljoin(self.host, *sanitized_scope)
        query = urlencode(self.params)
        return f"{path}?{query}"

    def encode_data(self):
        json_data = json.dumps(self.data)
        return json_data.encode()
