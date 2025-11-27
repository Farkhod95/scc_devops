# app_name/views.py
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from ipreport.models import IpAddress, IpAddressInfo
from ipreport.serializers import IpAddressInfoRangeSerializer


def generate_ip_range(base_ip: str, number_from: int, number_to: int) -> list[str]:
    """
    base_ip: masalan '172.24.200.1'
    number_from/to: masalan 1..200

    1) base_ip dan faqat birinchi 3 oktet prefix sifatida olinadi (172.24.200)
    2) Har subnetda hostlar 1..254 oralig'ida bo'ladi.
       254 dan oshsa, uchinchi oktet ++ bo'ladi va host yana 1 dan boshlanadi.

       Misol:
       base_ip = 172.24.200.1
       n = 1   -> 172.24.200.1
       n = 254 -> 172.24.200.254
       n = 245 -> 172.24.201.1
       n = 246 -> 172.24.201.2
       va hokazo.
    """
    parts = base_ip.split('.')
    if len(parts) != 4:
        raise ValueError("Noto'g'ri IPv4 manzil")

    try:
        a, b, c, _ = map(int, parts)
    except ValueError:
        raise ValueError("IPv4 manzil faqat raqamlardan iborat bo'lishi kerak")

    base_third = c
    result: list[str] = []

    for n in range(number_from, number_to + 1):
        offset = n - 1  # n=1 -> 0, n=254 -> 243
        third_octet = base_third + (offset // 254)
        last_octet = 1 + (offset % 254)  # har subnetda host 1..254

        ip_str = f"{a}.{b}.{third_octet}.{last_octet}"
        result.append(ip_str)

    return result


class GenerateIpAddressInfoAPIView(APIView):
    """
    POST:
    {
        "ipaddress_id": 1,
        "ipAddress": "172.24.200.1",
        "number_from": 1,
        "number_to": 200
    }

    Natija:
    - IpAddressInfo jadvaliga ko'p yozuvlar qo'shiladi
    - Har birida:
        ipaddress = IpAddress(id=ipaddress_id)
        ip_address = generatsiya qilingan ip
        status = 'inactive'
    """

    def post(self, request, *args, **kwargs):
        # Query params yoki body'dan ham o'qiy olishi uchun:
        data = {
            "ipaddress_id": request.data.get("ipaddress_id") or request.query_params.get("ipaddress_id"),
            "ipAddress": request.data.get("ipAddress") or request.query_params.get("ipAddress"),
            "number_from": request.data.get("number_from") or request.query_params.get("number_from"),
            "number_to": request.data.get("number_to") or request.query_params.get("number_to"),
        }

        serializer = IpAddressInfoRangeSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        ipaddress_obj = serializer.validated_data["ipaddress_obj"]
        base_ip = serializer.validated_data["ipAddress"]
        number_from = serializer.validated_data["number_from"]
        number_to = serializer.validated_data["number_to"]

        try:
            ip_list = generate_ip_range(base_ip, number_from, number_to)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # bulk_create uchun obyektlar ro'yxati
        objs = [
            IpAddressInfo(
                ipaddress=ipaddress_obj,
                ip_address=ip,
                status="inactive",
            )
            for ip in ip_list
        ]

        # unique constraint (ip_address) bo'lgani uchun
        # borlarini tashlab ketish uchun ignore_conflicts=True
        with transaction.atomic():
            created_objs = IpAddressInfo.objects.bulk_create(
                objs,
                ignore_conflicts=True
            )

        total_requested = len(ip_list)
        created_count = len(created_objs)
        skipped_existing = total_requested - created_count

        return Response(
            {
                "ipaddress_id": ipaddress_obj.id,
                "base_ip": base_ip,
                "number_from": number_from,
                "number_to": number_to,
                "total_requested": total_requested,
                "created_count": created_count,
                "skipped_existing": skipped_existing,
            },
            status=status.HTTP_201_CREATED
        )

