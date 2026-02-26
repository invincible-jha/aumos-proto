.PHONY: generate clean lint test install

generate:
	@echo "Generating Python stubs from proto files..."
	buf generate proto/

clean:
	find . -name "*_pb2.py" -delete
	find . -name "*_pb2_grpc.py" -delete

lint:
	buf lint proto/
	ruff check src/ tests/

test:
	pytest tests/ -v

install:
	pip install -e ".[dev]"
