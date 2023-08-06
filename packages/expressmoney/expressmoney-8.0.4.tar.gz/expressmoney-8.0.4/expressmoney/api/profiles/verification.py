__all__ = ('RequestPhotoVerificationPoint', 'RequestVideoVerificationPoint',
           'AutoVerificationProcessPoint', 'VideoVerificationProcessPoint', 'PhotoVerificationProcessPoint',
           )

from expressmoney.api import *
from expressmoney.viewflow import status

SERVICE = 'profiles'


class RequestPhotoVerificationCreateContract(Contract):
    file = serializers.CharField(max_length=256)


class RequestVideoVerificationCreateContract(Contract):
    TELEGRAM = 'TELEGRAM'
    WHATSAPP = 'WHATSAPP'

    MESSENGER_CHOICE = (
        (TELEGRAM, 'Telegram'),
        (WHATSAPP, 'WhatsApp'),
    )
    user_message = serializers.CharField(max_length=256, allow_blank=True)
    messenger = serializers.ChoiceField(choices=MESSENGER_CHOICE)


class AutoVerificationProcessReadContract(Contract):
    RESULT_CHOICES = (
        (status.ERROR, 'System error'),
        (status.FAILURE, 'Decline'),
        (status.SUCCESS, 'Verified'),
    )
    id = serializers.IntegerField(min_value=1)
    status = serializers.CharField(max_length=50)
    profile = serializers.IntegerField(min_value=1)
    result = serializers.ChoiceField(choices=RESULT_CHOICES)


class VideoVerificationProcessReadContract(Contract):
    RESULT_CHOICES = (
        (status.ERROR, 'Incorrect phonenumber'),
        (status.IN_PROCESS, 'Recall'),
        (status.FAILURE, 'Decline'),
        (status.SUCCESS, 'Approved'),
    )

    WAIT_10M = 'WAIT_10M'
    WAIT_30M = 'WAIT_30M'
    WAIT_1H = 'WAIT_1H'
    WAIT_1D = 'WAIT_1D'

    RECALL_CHOICES = (
        (WAIT_10M, '10 minutes'),
        (WAIT_30M, '30 minutes'),
        (WAIT_1H, '1 hour'),
        (WAIT_1D, 'Tomorrow'),
    )

    id = serializers.IntegerField(min_value=1)
    status = serializers.CharField(max_length=50)
    user_id = serializers.IntegerField(min_value=1)
    profile = serializers.IntegerField(min_value=1)
    result = serializers.ChoiceField(choices=RESULT_CHOICES)
    recall = serializers.ChoiceField(choices=RECALL_CHOICES, allow_blank=True)
    attempts = serializers.IntegerField(min_value=0)
    message = serializers.CharField(max_length=64, allow_blank=True)
    messenger = serializers.CharField(max_length=16, allow_blank=True)
    user_message = serializers.CharField(max_length=256, allow_blank=True)


class PhotoVerificationProcessReadContract(Contract):
    RESULT_CHOICES = (
        (status.IN_PROCESS, status.IN_PROCESS),
        (status.FAILURE, status.FAILURE),
        (status.SUCCESS, status.SUCCESS),
    )

    id = serializers.IntegerField(min_value=1)
    status = serializers.CharField(max_length=50)

    user_id = serializers.IntegerField(min_value=1)
    profile = serializers.IntegerField(min_value=1)
    result = serializers.ChoiceField(choices=RESULT_CHOICES)
    file = serializers.CharField(max_length=256)
    message = serializers.CharField(max_length=64, allow_blank=True)


class RequestPhotoVerificationID(ID):
    _service = SERVICE
    _app = 'verification'
    _view_set = 'request_photo_verification'


class RequestVideoVerificationID(ID):
    _service = SERVICE
    _app = 'verification'
    _view_set = 'request_video_verification'


class AutoVerificationProcessID(ID):
    _service = SERVICE
    _app = 'verification'
    _view_set = 'auto_verification_process'


class VideoVerificationProcessID(ID):
    _service = SERVICE
    _app = 'verification'
    _view_set = 'video_verification_process'


class PhotoVerificationProcessID(ID):
    _service = SERVICE
    _app = 'verification'
    _view_set = 'photo_verification_process'


class RequestPhotoVerificationPoint(CreatePointMixin, ContractPoint):
    _point_id = RequestPhotoVerificationID()
    _create_contract = RequestPhotoVerificationCreateContract


class RequestVideoVerificationPoint(CreatePointMixin, ContractPoint):
    _point_id = RequestVideoVerificationID()
    _create_contract = RequestVideoVerificationCreateContract


class AutoVerificationProcessPoint(ListPointMixin, ContractPoint):
    _point_id = AutoVerificationProcessID()
    _read_contract = AutoVerificationProcessReadContract


class VideoVerificationProcessPoint(ListPointMixin, ContractPoint):
    _point_id = VideoVerificationProcessID()
    _read_contract = VideoVerificationProcessReadContract


class PhotoVerificationProcessPoint(ListPointMixin, ContractPoint):
    _point_id = PhotoVerificationProcessID()
    _read_contract = PhotoVerificationProcessReadContract
