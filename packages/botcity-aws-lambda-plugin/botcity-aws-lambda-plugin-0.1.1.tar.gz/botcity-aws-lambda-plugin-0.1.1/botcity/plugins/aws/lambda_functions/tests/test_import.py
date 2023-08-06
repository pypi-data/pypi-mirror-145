def test_package_import():
    import botcity.plugins.aws.lambda_functions as plugin
    assert plugin.__file__ != ""
