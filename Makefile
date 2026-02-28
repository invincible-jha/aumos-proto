.PHONY: generate check-generated clean lint test install buf-lint buf-breaking

generate:  ## Generate Python, Go, and TypeScript stubs from .proto files
	buf generate
	@echo "Generated files updated in src/, gen/go/, gen/ts/"

check-generated:  ## Fail if generated files are out of date with .proto sources
	@echo "Checking if generated files are up to date..."
	buf build --error-format json > /dev/null
	@echo "Proto files are valid. Run 'make generate' to regenerate stubs."

buf-lint:  ## Run buf lint against all proto files
	buf lint

buf-breaking:  ## Check for breaking changes against main branch
	buf breaking --against '.git#branch=main,subdir=proto'

clean:  ## Remove generated Python stub files
	find . -name "*_pb2.py" -not -path "./.git/*" -delete
	find . -name "*_pb2_grpc.py" -not -path "./.git/*" -delete
	rm -rf gen/go gen/ts

lint:  ## Run buf lint + ruff
	buf lint
	ruff check src/ tests/

test:  ## Run test suite
	pytest tests/ -v

install:  ## Install package with dev dependencies
	pip install -e ".[dev]"
