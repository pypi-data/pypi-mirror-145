import os


def test_pytest_plugin(testdir):

    # create a temporary conftest.py file
    testdir.makeconftest(
        """
        import pytest
        import os
        from _assembly.sdk.pytest_plugin.plugin import *
        from assembly_client.api.contracts import ContractRef
        

        @pytest.fixture
        def reset(network):
            network.reset(txe_protocol=13, sympl_version=9)

        @pytest.fixture
        def async_reset(async_network):
            async_network.reset(txe_protocol=13, sympl_version=9)

        @pytest.fixture
        def contracts(network, reset):
            os.environ["CONTRACT_PATH"] = "contracts"
            network.publish(
                [ContractRef("data", "1.0.0", 9)]
            )

        @pytest.fixture
        def async_contracts(async_network, async_reset):
            os.environ["CONTRACT_PATH"] = "contracts"
            async_network.publish(
                [ContractRef("data", "1.0.0", 9)]
            )

        @pytest.fixture
        def key_alias(network, reset, store):
            store["default_ka"] = network.register_key_alias()
            return network[store["default_ka"]]

        @pytest.fixture
        def async_key_alias(async_network, async_reset, store):
            store["default_ka"] = async_network.register_key_alias()
            return async_network[store["default_ka"]]
        """
    )

    testdir.makepyfile(
        """
        import pytest
        from assembly_client.api.types.error_types import ContractError
        def test_network(network, reset):
            assert network is not None

        def test_async_network(async_contracts, async_network, async_reset, async_key_alias):
            assert async_network is not None
            assert len(async_network.list_key_aliases()) == 1
            job = async_key_alias.data["9-1.0.0"].run_executable().start_waiting().sync_with()
            assert "foo" == job.result["result"]


        def test_list_contracts(network, reset):
            assert [] == network.list_contracts()

        def test_list_ka(network, reset):
            assert [] == network.list_key_aliases()

        def test_create_ka(network, reset):
            network.register_key_alias()
            assert len(network.list_key_aliases()) == 1

        def test_publish(contracts, network):
            assert 1 == len(network.list_contracts())

        def test_executable_return_value(contracts, network, key_alias):
            assert len(network.list_key_aliases()) == 1
            assert "foo" == key_alias.data["9-1.0.0"].run_executable()

        def test_clientside_return_value(contracts, network, key_alias):
            assert len(network.list_key_aliases()) == 1
            assert "bar" == key_alias.data["9-1.0.0"].run_clientside()

        def test_clientside_error(contracts, network, key_alias):
            with pytest.raises(ContractError, match="This is a clientside error"):
                key_alias.data["9-1.0.0"].run_clientside_error()

        def test_executable_error(contracts, network, key_alias):
            with pytest.raises(ContractError, match="This is an executable error"):
                key_alias.data["9-1.0.0"].run_executable_error()
        """
    )

    # run all tests with pytest
    result = testdir.runpytest(
        f"--contract-path={os.path.dirname(os.path.realpath(__file__)) + '/contracts'}",
    )
    result.assert_outcomes(passed=10)
