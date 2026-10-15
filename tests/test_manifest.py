from inneros_act3.manifest import capability_manifest


def test_manifest_is_local_first_and_auditable():
    manifest = capability_manifest()
    assert manifest["schema"] == "inneros.act3.capability-manifest.v1"
    assert manifest["local_first"] is True
    names = {item["name"] for item in manifest["capabilities"]}
    assert {"local_inference", "skills", "mcp_tools", "a2a_agents", "execution_evidence"} <= names
    assert all(item["evidence_required"] for item in manifest["capabilities"])
