def test_package_import():
    import botcity.plugins.aws.s3 as plugin
    assert plugin.__file__ != ""
