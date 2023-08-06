from django.db import models, transaction

from nautobot.core.models import BaseModel
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import IPAddress, VLAN, VRF
from nautobot.utilities.querysets import RestrictedQuerySet


class VLANVRF(BaseModel):
    vlan = models.OneToOneField(
        VLAN,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    vrf = models.OneToOneField(
        VRF,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )


class EthernetSegment(BaseModel):
    segment_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=256)

    csv_headers = ["segment_id", "name"]

    objects = RestrictedQuerySet.as_manager()

    @property
    def members(self):
        return EthernetSegmentMembership.objects.filter(segment=self).values_list("interface", flat=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.segment_id)


class EthernetSegmentMembership(BaseModel):
    segment = models.ForeignKey(
        EthernetSegment,
        on_delete=models.CASCADE
    )
    interface = models.OneToOneField(
        Interface,
        on_delete=models.CASCADE
    )

    csv_headers = ["segment", "interface"]

    objects = RestrictedQuerySet.as_manager()


class VLANVRFList(BaseModel):
    vlan = models.OneToOneField(
        VLAN,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    vrf = models.ForeignKey(
        VRF,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )


class AnycastIP(BaseModel):
    vlan = models.ForeignKey(
        VLAN,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    ip = models.OneToOneField(
        IPAddress,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )


class AnycastDummyIP(BaseModel):
    vlan = models.ForeignKey(
        VLAN,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    ip = models.OneToOneField(
        IPAddress,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
