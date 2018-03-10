TESTS = test/funcs/*
.PHONY: test
test:
	py.test -v $(TESTS)
