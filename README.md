# sara-python-template

Template repository for creating new SARA Python services.

## Usage

Click **Use this template** on GitHub (or use `gh repo create <name> --template equinor/sara-python-template`) to bootstrap a new repo, then:

1. Work through the **Bootstrap checklist** below to rename the package and register the service.
2. Work through [`equinor/armada/docs/new_repo_checklist.md`](https://github.com/equinor/armada/blob/main/docs/new_repo_checklist.md) to configure repository settings, branch rulesets, environments, and secrets — GitHub templates only copy files, not repo configuration.

## Bootstrap checklist

After creating a new repo from this template, replace the placeholders and configure the repo:

### 1. Rename package and files

Replace every occurrence of `sara-service` (kebab-case, project name) and `sara_service` (snake_case, package name) with your service names.

```bash
NEW_KEBAB=sara-your-service
NEW_SNAKE=sara_your_service

# Rename the package directory
git mv sara_service "$NEW_SNAKE"

# Update string references in tracked files
git grep -l sara-service | xargs sed -i "s/sara-service/$NEW_KEBAB/g"
git grep -l sara_service | xargs sed -i "s/sara_service/$NEW_SNAKE/g"
```

Then edit:

- `pyproject.toml` — `[project].name`, `[project].description`, `[project.urls].repository`, `[tool.setuptools.packages.find].include`, `[tool.isort].known_first_party`.
- `catalog-info.yaml` — `metadata.name`, `github.com/project-slug`.
- `.github/workflows/deploy_to_development.yml`, `deploy_to_staging.yml`, `promote_to_production.yml` — `image_name` values.

### 2. Choose a runner size

The default `runs_on` is `ubuntu-latest` (GitHub-hosted, ~14 GB disk). If your image includes torch/ML weights and exceeds that, set `runs_on: ubuntu` in `deploy_to_development.yml` and `deploy_to_staging.yml` to use Equinor's self-hosted runner. See `sara-anonymizer` for reference.

### 3. Create the GitHub Environments

Create `Development`, `Staging` and `Production` under **Settings → Environments**. These are **required**, not optional: the federated credential that authenticates to the registry matches on the environment name, so a missing or differently-cased environment means the deploy cannot authenticate at all.

Add required reviewers on any of them you want to gate.

### 4. Set up registry access

Publishing uses a federated credential, not a registry password. There is nothing secret to request.

1. Add this repository to `automation/aks/gha-push-<env>.bicepparam` in [`equinor/robotics-infrastructure`](https://github.com/equinor/robotics-infrastructure) for each environment you publish to, and deploy `gha-push-identity.bicep` for that environment.
2. Set `ACR_PUSH_CLIENT_ID` as an **environment variable** on each GitHub Environment, to the client ID of `robotics-gha-push-<env>`.

`AZURE_TENANT_ID` and `AZURE_SUBSCRIPTION_ID` are inherited from the organisation.

The only secret the workflows need is:

- `ANALYTICS_INFRASTRUCTURE_DEPLOY_KEY`

If a deploy fails at `azure/login`, the usual causes are a missing `id-token: write` on some job in the call chain (a called workflow's token can never exceed its caller's), or an Actions allowlist that does not permit `azure/login@*` — the latter shows as `startup_failure` at 0s with no jobs, which looks like a syntax error but is not.

See [`equinor/armada/docs/new_repo_checklist.md`](https://github.com/equinor/armada/blob/main/docs/new_repo_checklist.md) for the full list of repository settings, branch rulesets, environments, and secrets used across sara-* repos.

### 5. Register the service in infrastructure

Add a new overlay entry in `equinor/analytics-infrastructure` under `k8s_kustomize/overlays/{development,staging,production}/kustomization.yaml` pointing at `robotics/sara-your-service`.

### 6. Generate `uv.lock`

The template intentionally ships without a lockfile. After renaming the package and picking your initial dependencies in `pyproject.toml`, run:

```bash
uv lock
git add uv.lock
```

### 7. Delete this section

Remove the bootstrap checklist from the README once the repo is set up.

---

# sara-service

_Short description of what the service does._

## Development

```bash
uv sync
uv run python main.py --help
uv run pytest
```

## Deployment

Deployment is fully handled by the workflows in `.github/workflows/`, which delegate to the reusable workflows in [`equinor/armada`](https://github.com/equinor/armada). See [`equinor/armada/.github/workflows/deploy_to_development.yml`](https://github.com/equinor/armada/blob/main/.github/workflows/deploy_to_development.yml) for the pipeline.
