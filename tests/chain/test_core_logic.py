# def test_initiate_order(chain):
#     greeter, _ = chain.provider.get_or_deploy_contract('Greeter')

#     greeting = greeter.call().greet()
#     assert greeting == 'Hello'


# def test_custom_greeting(chain):
#     greeter, _ = chain.provider.get_or_deploy_contract('Greeter')

#     set_txn_hash = greeter.transact().setGreeting('Guten Tag')
#     chain.wait.for_receipt(set_txn_hash)

#     greeting = greeter.call().greet()
#     assert greeting == 'Guten Tag'


def test_initiate_order(btrans):
    assert False
    print("hi")
