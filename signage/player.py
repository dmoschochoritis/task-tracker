def decide(status, body):
    if status == 404:
        return "Unknown screen"
    if body is None:
        return "No content assigned"
    return f"Playing {body['name']}: {', '.join(body['items'])}"
