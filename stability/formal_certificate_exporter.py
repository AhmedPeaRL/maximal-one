import json
import hashlib

def export_certificate(P_matrix, metadata):
    data = {
        "P_matrix": P_matrix.tolist(),
        "metadata": metadata
    }

    raw = json.dumps(data, sort_keys=True).encode()
    digest = hashlib.sha256(raw).hexdigest()

    data["sha256"] = digest

    with open("lyapunov_certificate.json", "w") as f:
        json.dump(data, f, indent=4)

    return digest
