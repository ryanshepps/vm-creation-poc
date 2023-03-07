from azure.identity import AzureCliCredential
from azure.mgmt.resource import SubscriptionClient


class Subscription:

    def __new__(cls):
        credential = AzureCliCredential()
        subscription_client = SubscriptionClient(credential)
        subscriptions = subscription_client.subscriptions

        return list(subscriptions.list())[0]
