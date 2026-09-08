from .core import RouteRequest, route, verify_evidence


def main() -> None:
    samples = [
        ('private-workload', RouteRequest(privacy_required=True)),
        ('elastic-workload', RouteRequest(needs_elastic_capacity=True)),
        ('local-fast-path', RouteRequest(latency_sensitive=True)),
        ('local-unavailable', RouteRequest(local_available=False)),
    ]
    for name, request in samples:
        evidence = route(request)
        digest = evidence.sha256()
        assert verify_evidence(evidence, digest)
        print(f'{name}: target={evidence.target} reasons={list(evidence.reason_codes)} sha256={digest[:16]}...')


if __name__ == '__main__':
    main()
