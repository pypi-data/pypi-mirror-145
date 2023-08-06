"""
Base classes and helpers for traffic generators shells.
"""
import logging
import time
from typing import Optional

from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.logging.qs_logger import get_qs_logger
from cloudshell.shell.core.context_utils import get_resource_name
from cloudshell.shell.core.driver_context import ResourceCommandContext
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext

from .helpers import get_cs_session, get_reservation_id
from .rest_api_helpers import SandboxAttachments

TGN_CHASSIS_FAMILY = "CS_TrafficGeneratorChassis"
TGN_CONTROLLER_FAMILY = "CS_TrafficGeneratorController"
TGN_PORT_FAMILY = "CS_TrafficGeneratorPort"

BYTEBLOWER_CHASSIS_MODEL = "ByteBlower Chassis Shell 2G"
BYTEBLOWER_CONTROLLER_MODEL = "ByteBlower Controller Shell 2G"
IXIA_CHASSIS_MODEL = "Ixia Chassis Shell 2G"
IXLOAD_CONTROLLER_MODEL = "IxLoad Controller Shell 2G"
IXNETWORK_CONTROLLER_MODEL = "IxNetwork Controller Shell 2G"
PERFECT_STORM_CHASSIS_MODEL = "PerfectStorm Chassis Shell 2G"
STC_CHASSIS_MODEL = "STC Chassis Shell 2G"
STC_CONTROLLER_MODEL = "STC Controller Shell 2G"
XENA_CHASSIS_MODEL = "Xena Chassis Shell 2G"
XENA_CONTROLLER_MODEL = "Xena Controller Shell 2G"


def is_blocking(blocking: str) -> bool:
    """Returns True if the value of `blocking` parameter represents true else returns false.

    :param blocking: Value of `blocking` parameter.
    """
    return blocking.lower() == "true"


def get_reservation_ports(session, reservation_id, model_name="Generic Traffic Generator Port"):
    """Get all Generic Traffic Generator Port in reservation.

    :return: list of all Generic Traffic Generator Port resource objects in reservation
    """
    reservation_ports = []
    reservation = session.GetReservationDetails(reservation_id).ReservationDescription
    for resource in reservation.Resources:
        if resource.ResourceModelName == model_name:
            reservation_ports.append(resource)
    return reservation_ports


class TrafficDriver(ResourceDriverInterface):
    """Base class for all TG shells drivers."""

    def __init__(self) -> None:
        self.handler = None
        self.logger = None

    def initialize(self, context, log_group="traffic_shells") -> None:
        self.logger = get_qs_logger(log_group=log_group, log_file_prefix=context.resource.name)
        self.logger.setLevel(logging.DEBUG)
        self.handler.initialize(context, self.logger)

    def cleanup(self) -> None:
        pass

    def get_inventory(self, context):
        return self.handler.load_inventory(context)


class TrafficHandler:
    """Base class for all TG shell handlers."""

    def __init__(self) -> None:
        self.resource = None
        self.service = None
        self.logger = None
        self.address = None
        self.user = None
        self.password = None

    def initialize(self, resource, logger, packages_loggers: Optional[list] = None) -> None:
        self.resource = resource
        self.service = resource
        self.logger = logger

        for package_logger in packages_loggers or []:
            package_logger = logging.getLogger(package_logger)
            package_logger.setLevel(self.logger.level)
            for handler in self.logger.handlers:
                if handler not in package_logger.handlers:
                    package_logger.addHandler(handler)

    def get_connection_details(self, context):
        self.address = context.resource.address
        self.logger.debug(f"Address - {self.address}")
        self.user = self.resource.user
        self.logger.debug(f"User - {self.user}")
        self.logger.debug(f"Encrypted password - {self.resource.password}")
        self.password = CloudShellSessionContext(context).get_api().DecryptPassword(self.resource.password).Value
        self.logger.debug(f"Password - {self.password}")


class TgChassisDriver(TrafficDriver):
    def initialize(self, context, log_group="traffic_shells"):
        super().initialize(context, log_group)


class TgControllerDriver(TrafficDriver):
    def initialize(self, context, log_group="traffic_shells"):
        super().initialize(context, log_group)

    def cleanup(self) -> None:
        self.handler.cleanup()

    def keep_alive(self, context, cancellation_context):
        while not cancellation_context.is_cancelled:
            time.sleep(2)
        if cancellation_context.is_cancelled:
            self.cleanup()

    def load_config(self, context, config_file_location):
        enqueue_keep_alive(context)
        return self.handler.load_config(context, config_file_location)

    def send_arp(self, context):
        self.handler.send_arp()

    def start_protocols(self, context):
        self.handler.start_protocols()

    def stop_protocols(self, context):
        self.handler.stop_protocols()

    def start_traffic(self, context, blocking):
        self.handler.start_traffic(context, blocking)
        return f"traffic started in {blocking} mode"

    def stop_traffic(self, context):
        self.handler.stop_traffic()

    def get_statistics(self, context, view_name, output_type):
        return self.handler.get_statistics(context, view_name, output_type)


class TgChassisHandler(TrafficHandler):
    pass


class TgControllerHandler(TrafficHandler):
    """Bas class for all TG controller handlers shells."""

    def initialize(self, context, logger, service):
        super().initialize(resource=service, logger=logger)


def enqueue_keep_alive(context):
    cs_session = CloudShellAPISession(
        host=context.connectivity.server_address,
        token_id=context.connectivity.admin_auth_token,
        domain=context.reservation.domain,
    )
    resource_name = get_resource_name(context=context)
    cs_session.EnqueueCommand(
        reservationId=get_reservation_id(context), targetName=resource_name, targetType="Service", commandName="keep_alive"
    )


def attach_stats_csv(
    context: ResourceCommandContext, logger: logging.Logger, view_name: str, output: str, suffix: str = "csv"
) -> str:
    """Attach statistics CSV to reservation."""
    quali_api_helper = SandboxAttachments(context.connectivity.server_address, context.connectivity.admin_auth_token, logger)
    quali_api_helper.login()
    full_file_name = view_name.replace(" ", "_") + "_" + time.ctime().replace(" ", "_") + "." + suffix
    quali_api_helper.attach_new_file(get_reservation_id(context), file_data=output, file_name=full_file_name)
    get_cs_session(context).WriteMessageToReservationOutput(
        get_reservation_id(context), f"Statistics view saved in attached file - {full_file_name}"
    )
    return full_file_name
