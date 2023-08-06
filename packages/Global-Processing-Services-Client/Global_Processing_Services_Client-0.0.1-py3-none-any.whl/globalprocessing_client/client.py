"""GPS client.

:copyright: (c) DiviPay 2022
"""

from datetime import datetime

import requests
import zeep
from pytz import timezone as tz
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport

from .exceptions import GPSClientConnectionException, GPSClientException


class GPSClient:
    """GPS client."""

    # Status codes:
    # https://gpsuat-developer.globalprocessing.com/webservices/Content/Reference/Status_Codes.htm
    OK = "00"
    NOT_ACTIVATED = "02"
    CAPTURE_CARD = "04"
    DO_NOT_HONOUR = "05"
    LOST_CARD = "41"
    STOLEN_CARD = "43"
    ACCOUNT_CLOSED = "46"
    TRANSACTION_NOT_PERMITTED_TO_CARDHOLDER = "57"
    SUSPECTED_FRAUD = "59"
    RESTRICTED_CARD = "62"
    SECURITY_VIOLATION = "63"
    CARDHOLDER_CONTACT_ISSUER = "70"
    ALLOWABLE_NUMBER_OF_PIN_TRIED_EXCEEDED = "75"
    CARD_DESTROYED = "83"
    REFUND_GIVEN_TO_CUSTOMER = "98"
    CARD_VOIDED = "99"
    SHORT_TERM_BLOCK = "G1"
    SHORT_TERM_FULL_BLOCK = "G2"
    LONG_TERM_BLOCK = "G3"
    LONG_TERM_FULL_BLOCK = "G4"

    def __init__(
        self, username: str, password: str, iss_code: str, wsdl: str, timezone: str
    ) -> None:
        """Initialise client.

        :param username: Username provided by GPS
        :param password: Password provided by GPS
        :param iss_code: Issuer code provided by GPS
        :param wsdl: Path to WSDL file
        :param timezone: Timezone in TZ database name format ie "Australia/Sydney"
        :raises:
            UnknownTimeZoneError - if timezone format is wrong.
            GPSClientConnectionException - if connection to GPS fails
        """
        self.timezone = tz(timezone)
        self.client = self._create_connection(username, password, wsdl)
        self.iss_code = iss_code

    def _create_connection(
        self, username: str, password: str, wsdl: str
    ) -> zeep.Client:
        """Create connection.

        :param username: Username provided by GPS
        :param password: Password provided by GPS
        :param wsdl: Path to WSDL file
        :raises:
            GPSClientConnectionException: If card cannot be connected to.
        """
        session = Session()
        session.auth = HTTPBasicAuth(username, password)
        try:
            return zeep.Client(wsdl, transport=Transport(session=session))
        except (zeep.exceptions.Fault, requests.exceptions.HTTPError):
            raise GPSClientConnectionException("Could not connect to GPS.")

    def _get_local_time(self) -> datetime:
        """Return localised datetime object."""
        now = datetime.utcnow()
        return self.timezone.fromutc(now)

    def create_card(
        self,
        card_design: str,
        **kwargs,
    ) -> dict:
        """Issue new card.

        Uses bare minimum number of fields and additional fields may need to be added depending
        on your GPS configuration.

        Defaults:
            TxnCode = 10
            LoadValue = 0
            ItemSrc = 0
            LoadFee = 0
            CreateImage = 0
            CreateType = 1
            ActivateNow = 1
            Replacement = 0

        :param card_design: Card design ID
        :param kwargs: Optional kwards that can be used to override/add fields.
        :return: Token to be used as a reference for newly issued card
        :raises:
            CardIssuerException: If cannot revoke card.

        :example:

            >>> client = GPSClient(
                    "username",
                    "password",
                    "iss-code",
                    "https://example.com/wsdl",
                    "Australia/Sydney"
                )
            >>> client.create_card(1234)
        """
        now = self._get_local_time()
        wsid = int(now.timestamp() * 1000000)
        defaults = {
            "WSID": wsid,
            "IssCode": self.iss_code,
            "TxnCode": 10,
            "CardDesign": card_design,
            "LocDate": now.strftime("%Y-%m-%d"),
            "LocTime": now.strftime("%H%M%S"),
            "LoadValue": 0,
            "ItemSrc": 0,
            "LoadFee": 0,
            "CreateImage": 0,
            "CreateType": 1,
            "ActivateNow": 1,
            "Replacement": 0,
        }
        payload = defaults | kwargs
        try:
            response = self.client.service.Ws_CreateCard(**payload)
            return response
        except zeep.exceptions.Fault as e:
            raise GPSClientException(e)

    def status_change(self, token: str, stat_code: str, **kwargs) -> None:
        """Revoke card at GPS.

        Uses bare minimum number of fields and additional fields may need to be added depending
        on your GPS configuration.

        Defaults:
            - TxnCode = 2,
            - AuthType = 1,
            - ItemSrc = 0,

        :param wsid: Unique reference for to track request and idempotency
        :param token: Card token
        :param stat_code: GPS status code to update card with
        :param kwargs: optional kwargs used to override defaults
        :raises:
            CardIssuerException: If cannot revoke card.

        :example:

            >>> client = GPSClient("username", "password", "iss-code")
            >>> client.status_change("public-token", GPSClient.ACCOUNT_CLOSED)

        """
        now = self._get_local_time()
        wsid = int(now.timestamp() * 1000000)
        defaults = {
            "WSID": wsid,
            "IssCode": self.iss_code,
            "TxnCode": 2,  # Status change code
            "AuthType": 1,  # Only require PublicToken to reference the card
            "PublicToken": token,
            "LocDate": now.strftime("%Y-%m-%d"),
            "LocTime": now.strftime("%H%M%S"),
            "NewStatCode": stat_code,
            "ItemSrc": 0,
        }
        payload = defaults | kwargs
        try:
            response = self.client.service.Ws_StatusChange(**payload)
            return response
        except zeep.exceptions.Fault as e:
            raise GPSClientException(e)
