PY := .venv/bin/python
CACHE := web/public/cache

.PHONY: setup test demo-synthetic validate clean-cache

setup:
	uv venv --python 3.11 .venv
	uv pip install --python $(PY) -e ".[dev]"

test:
	$(PY) -m pytest

# Runs the whole pipeline on the synthetic fallback. Every output is labelled SYNTHETIC.
demo-synthetic:
	$(PY) scripts/build_demo_cache.py --synthetic --out $(CACHE)
	$(PY) scripts/validate_contract.py $(CACHE)

validate:
	$(PY) scripts/validate_contract.py $(CACHE)

clean-cache:
	rm -f $(CACHE)/*.json
