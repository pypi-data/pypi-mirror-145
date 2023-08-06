def test_package_import():
    import botcity.plugins.excel as plugin
    assert plugin.__file__ != ""
