import boto3

from .resource import Resource


class Route53(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_hosted_zone_name = kwargs["list_hosted_zones"]
        self.record_name = kwargs["show_record_for"]
        self.zone_name = kwargs["zone_name"]
        if self.zone_name and not self.zone_name.endswith("."):
            self.zone_name += "."

        self.client = boto3.client("route53")

    def run(self):
        if self.record_name and self.zone_name:
            self.show_records_for(self.record_name, self.zone_name)
        if self.list_hosted_zone_name:
            self.list_hosted_zones(self.list_hosted_zone_name)

    def get_hosted_zones_by_name(self, zone_name=None):
        """Return all hosted zones if no zone name is provided."""
        hosted_zones = []

        paginator = self.client.get_paginator("list_hosted_zones")
        pagination_config = {
            "MaxItems": 100,
            "PageSize": 100,  # PageSize should never be greater than MaxItems.
        }

        while True:
            for res in paginator.paginate(PaginationConfig=pagination_config):
                if zone_name:
                    hosted_zones += [
                        zone for zone in res["HostedZones"] if zone_name in zone["Name"]
                    ]
                else:
                    hosted_zones += res["HostedZones"]
            if res.get("NextToken"):
                pagination_config["StartingToken"] = res["NextToken"]
            else:
                break

        return hosted_zones

    def list_hosted_zones(self, zone_name):
        if zone_name == "all":
            zone_name = None

        for zone in self.get_hosted_zones_by_name(zone_name):
            print(f'{zone["Name"]}: {zone["Id"]}')

    def get_zone_id_by_name(self, zone_name):
        zone_id = None

        paginator = self.client.get_paginator("list_hosted_zones")
        pagination_config = {
            "MaxItems": 100,
            "PageSize": 100,  # PageSize should never be greater than MaxItems.
        }

        while True:
            for res in paginator.paginate(PaginationConfig=pagination_config):
                for zone in res["HostedZones"]:
                    if zone_name == zone["Name"]:
                        zone_id = zone["Id"]
                        break
            if res.get("NextToken"):
                pagination_config["StartingToken"] = res["NextToken"]
            else:
                break

        return zone_id

    def show_records_for(self, record_name, zone_name):
        records = []

        paginator = self.client.get_paginator("list_resource_record_sets")
        pagination_config = {
            "MaxItems": 100,
            "PageSize": 100,  # PageSize should never be greater than MaxItems.
        }

        zone_id = self.get_zone_id_by_name(zone_name)
        while True:
            for res in paginator.paginate(
                HostedZoneId=zone_id,
                PaginationConfig=pagination_config,
            ):
                records += [
                    record
                    for record in res["ResourceRecordSets"]
                    if record_name in record["Name"]
                ]
            if res.get("NextToken"):
                pagination_config["StartingToken"] = res["NextToken"]
            else:
                break

        for record in records:
            print(
                f'{record["Name"]} {record["Type"]} {record["Weight"]} {[ item["Value"] for item in record["ResourceRecords"] ]}'
            )
