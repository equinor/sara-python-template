# sara-python-template

Template repository for creating new SARA Python services.

## Usage

Click **Use this template** on GitHub (or use `gh repo create <name> --template equinor/sara-python-template`) to bootstrap a new repo, then run the checklist below.

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

### 3. Optional: environment gate

If you want dev deploys to require approval via a GitHub Environment, uncomment the `environment_name: Development` line in `deploy_to_development.yml` and create the `Development` environment under **Settings → Environments** with required reviewers.

### 4. Configure GitHub secrets

The workflows expect these secrets to be present in the repository (org-level is fine):

- `ROBOTICS_ROBOTICSDEVACR_USERNAME` / `_PASSWORD`
- `ROBOTICS_ROBOTICSSTAGINGACR_USERNAME` / `_PASSWORD`
- `ROBOTICS_ROBOTICSPRODACR_USERNAME` / `_PASSWORD`
- `ANALYTICS_INFRASTRUCTURE_DEPLOY_KEY`

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
