# GHCR audit commands

These commands are for an authenticated GitHub CLI session on a trusted local machine.
Do not paste a PAT or token into chat, a workflow log, or a repository file.

## 1. Confirm current package versions, digests, and tags

```bash
gh auth status

gh api --paginate '/user/packages?package_type=container' \
  --jq '.[] | select(.name=="maximal-one") | {name,visibility,updated_at,html_url}'

gh api --paginate '/user/packages/container/maximal-one/versions' \
  --jq '.[] | {id,name,created_at,updated_at,tags:(.metadata.container.tags // [])}'
```

In this endpoint, `name` is the manifest digest (`sha256:...`); `id` is the package version ID; tags are listed in `metadata.container.tags`.

Do not delete any package version during this audit.

## 2. Inspect the current `latest` manifest from GHCR

```bash
docker buildx imagetools inspect ghcr.io/ahmedpearl/maximal-one:latest
```

Record the manifest digest, media type, platform manifests, and creation time if available. Compare the current digest to the historical digest from run 43614085900:

`sha256:5c930ed151cbba762d66ec2d0fc6e4de02637b6bc41455276e29069824899c96`

If current `latest` differs, preserve both digests and determine when/which run moved the tag.

## 3. Search accessible repositories for consumers

```bash
gh search code '"ghcr.io/ahmedpearl/maximal-one"' --owner AhmedPeaRL
```

Also inspect every repository you control for:
- `FROM ghcr.io/ahmedpearl/maximal-one`
- `image: ghcr.io/ahmedpearl/maximal-one`
- Compose, Kubernetes, devcontainer, deployment, and workflow references.

This can identify public indexed consumers, not every private/external consumer. Package access logs and external deployments may not be visible to the owner.

## 4. Evidence record

Record:
- package URL and visibility;
- each version ID;
- each digest and tag;
- which run/commit produced it;
- whether any deployment or workflow references the tag;
- whether the digest is still referenced;
- reviewer and date.

Do not delete or retag `latest` until downstream use and rollback needs are understood.
