import pytest


def test_lazy_load_working():
    import hydra.cloud
    plugins = hydra.cloud.registered_platforms
    assert len(plugins) > 1

def test_diable_works():
    from hydra.cloud import abstract_platform

    @abstract_platform.mark_disabled
    class DisabledPlatform(abstract_platform.AbstractPlatform):
        pass

    assert hasattr(DisabledPlatform, '__hydra_plugin_disabled__')
    assert DisabledPlatform.__hydra_plugin_disabled__() is True

def test_disable_not_inherited():
    from hydra.cloud import abstract_platform

    @abstract_platform.mark_disabled
    class DisabledPlatform(abstract_platform.AbstractPlatform):
        pass

    class EnabledPlatform(DisabledPlatform):
        pass

    assert hasattr(EnabledPlatform, '__hydra_plugin_disabled__')
    assert EnabledPlatform.__hydra_plugin_disabled__() is False
    assert DisabledPlatform.__hydra_plugin_disabled__() is True

def test_disable_not_inherited_deep():
    from hydra.cloud import abstract_platform

    @abstract_platform.mark_disabled
    class DisabledPlatform(abstract_platform.AbstractPlatform):
        pass

    class EnabledPlatform(DisabledPlatform):
        pass

    @abstract_platform.mark_disabled
    class DisabledPlatform2(EnabledPlatform):
        pass

    class EnabledPlatform2(DisabledPlatform2):
        pass

    for c in (DisabledPlatform, DisabledPlatform2, EnabledPlatform, EnabledPlatform2):
        assert hasattr(c, '__hydra_plugin_disabled__')
    
    assert EnabledPlatform.__hydra_plugin_disabled__() is False
    assert EnabledPlatform2.__hydra_plugin_disabled__() is False
    assert DisabledPlatform.__hydra_plugin_disabled__() is True
    assert DisabledPlatform2.__hydra_plugin_disabled__() is True


@pytest.mark.parametrize('decorator_name', ('mark_disabled', 'register_plugin'))
def test_disable_plugin_check_inherit_from_base_class(decorator_name):
    from hydra.cloud import abstract_platform

    decorator = getattr(abstract_platform, decorator_name)
    
    with pytest.raises(ValueError, match='AbstractPlatform'):
        @decorator
        class A():
            pass
    
    class C(abstract_platform.AbstractPlatform):
        pass

    class D(C):
        pass

    # should not raise
    @decorator
    class E(D):
        pass


def test_abstract_base_not_registered():
    import hydra.cloud
    from hydra.cloud import abstract_platform
    plugins = hydra.cloud.registered_platforms
    assert abstract_platform.AbstractPlatform not in plugins

