python_sources(
    name="libstorage", sources=["*.py"], dependencies=["src/python/utils:parser"]
)

pex_binary(
    name="storagemanager",
    dependencies=[":libstorage"],
    entry_point="main.py",
)
