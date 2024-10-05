# tgcalls-gate


# План:
- расставить дописать обработку всех ошибок в tgcalls
- расставить логи
- поправить автотесты для api
- поправить автотесты для tgcalls
- интеграционный тест api?
- реализация cleanUp
- добавить версию проекта

- рефакторинг конфигурации
- тестирование сервиса
- оптимизация docker образа
- документация кода
- коммит mvp
- добавить ci/dc 
- добавить документацию

## Development
### Run project
```
docker build -t tgcalls-gate-dev -f docker/dev/Dockerfile .
docker run -i -t --rm -p 80:80 -v //$(PWD):/tgcalls-gate tgcalls-gate-dev python src/main.py
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