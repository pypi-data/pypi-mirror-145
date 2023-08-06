
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.audit_log_api import AuditLogApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from soracom_api.api.audit_log_api import AuditLogApi
from soracom_api.api.auth_api import AuthApi
from soracom_api.api.billing_api import BillingApi
from soracom_api.api.cell_location_api import CellLocationApi
from soracom_api.api.credential_api import CredentialApi
from soracom_api.api.data_entry_api import DataEntryApi
from soracom_api.api.device_api import DeviceApi
from soracom_api.api.device_object_model_api import DeviceObjectModelApi
from soracom_api.api.diagnostic_api import DiagnosticApi
from soracom_api.api.email_api import EmailApi
from soracom_api.api.event_handler_api import EventHandlerApi
from soracom_api.api.file_entry_api import FileEntryApi
from soracom_api.api.files_api import FilesApi
from soracom_api.api.gadget_api import GadgetApi
from soracom_api.api.group_api import GroupApi
from soracom_api.api.lagoon_api import LagoonApi
from soracom_api.api.log_api import LogApi
from soracom_api.api.lora_device_api import LoraDeviceApi
from soracom_api.api.lora_gateway_api import LoraGatewayApi
from soracom_api.api.lora_network_set_api import LoraNetworkSetApi
from soracom_api.api.operator_api import OperatorApi
from soracom_api.api.order_api import OrderApi
from soracom_api.api.payment_api import PaymentApi
from soracom_api.api.port_mapping_api import PortMappingApi
from soracom_api.api.query_api import QueryApi
from soracom_api.api.role_api import RoleApi
from soracom_api.api.shipping_address_api import ShippingAddressApi
from soracom_api.api.sigfox_device_api import SigfoxDeviceApi
from soracom_api.api.sim_api import SimApi
from soracom_api.api.soralet_api import SoraletApi
from soracom_api.api.stats_api import StatsApi
from soracom_api.api.subscriber_api import SubscriberApi
from soracom_api.api.system_notification_api import SystemNotificationApi
from soracom_api.api.user_api import UserApi
from soracom_api.api.virtual_private_gateway_api import VirtualPrivateGatewayApi
