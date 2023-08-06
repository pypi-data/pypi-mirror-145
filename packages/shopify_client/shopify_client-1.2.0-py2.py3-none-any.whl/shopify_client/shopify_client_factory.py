import shopify

from shopify_client.billing import BillingClient
from shopify_client.constants import SupportedClient
from shopify_client.script_tag.client import ScriptTagClient
from shopify_client.store_properties import StorePropertiesClient
from shopify_client.versions import BASE_VERSION
from shopify_client.webhooks import WebhookClient


class ShopifyClientFactory:
    CLIENT_MAPPING = {
        SupportedClient.BILLING.value: BillingClient,
        SupportedClient.WEBHOOK.value: WebhookClient,
        SupportedClient.SCRIPT_TAG.value: ScriptTagClient,
        SupportedClient.STORE_PROPERTIES.value: StorePropertiesClient
    }

    def __init__(self, shop, access_token, api_version=BASE_VERSION):
        shopify.ShopifyResource.activate_session(shopify.Session(shop, api_version, access_token))

    @property
    def billing(self) -> BillingClient:
        return self.__get_client(SupportedClient.BILLING.value)

    @property
    def webhook(self) -> WebhookClient:
        return self.__get_client(SupportedClient.WEBHOOK.value)

    @property
    def script_tag(self) -> ScriptTagClient:
        return self.__get_client(SupportedClient.SCRIPT_TAG.value)

    @property
    def store_properties(self) -> StorePropertiesClient:
        return self.__get_client(SupportedClient.STORE_PROPERTIES.value)

    def __get_client(self, client_name: str):
        return self.CLIENT_MAPPING.get(client_name)()
