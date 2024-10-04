# tgcalls-gate

## Development
### Run project
```
docker build -t tgcalls-gate-dev -f docker/dev/Dockerfile .
docker run -i -t --rm -v //$(PWD):/tgcalls-gate tgcalls-gate-dev python src/main.py
```

### Run tests
```
docker build -t tgcalls-gate-dev -f docker/dev/Dockerfile .
docker run -i -t --rm -v //$(PWD):/tgcalls-gate tgcalls-gate-dev pytest tests/
```


### Run service
```
docker build -t tgcalls-gate -f docker/prod/Dockerfile .
docker run -i -t --rm -v //$(PWD)/data:/tgcalls-gate/data tgcalls-gate
```