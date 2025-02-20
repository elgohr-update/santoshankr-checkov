import unittest
import os
import json
import jsonschema
import urllib.request

from checkov.common.models.enums import CheckResult
from checkov.common.output.report import Report
from checkov.common.output.record import Record


class TestSarifReport(unittest.TestCase):
    def test_valid_passing_valid_testcases(self):
        record1 = Record(
            check_id="CKV_AWS_21",
            check_name="Some Check",
            check_result={"result": CheckResult.FAILED},
            code_block=None,
            file_path="./s3.tf",
            file_line_range="1:3",
            resource="aws_s3_bucket.operations",
            evaluations=None,
            check_class=None,
            file_abs_path=",.",
            entity_tags={"tag1": "value1"},
        )

        record2 = Record(
            check_id="CKV_AWS_3",
            check_name="Ensure all data stored in the EBS is securely encrypted",
            check_result={"result": CheckResult.FAILED},
            code_block=None,
            file_path="./ec2.tf",
            file_line_range="1:3",
            resource="aws_ebs_volume.web_host_storage",
            evaluations=None,
            check_class=None,
            file_abs_path=",.",
            entity_tags={"tag1": "value1"},
        )

        r = Report("terraform")
        r.add_record(record=record1)
        r.add_record(record=record2)
        ts = r.get_test_suites()
        json_structure = r.get_sarif_json()
        print(json.dumps(json_structure))
        self.assertEqual(
            None,
            jsonschema.validate(instance=json_structure, schema=get_sarif_schema()),
        )


def get_sarif_schema():
    file_name, headers = urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"
    )
    with open(file_name, "r") as file:
        schema = json.load(file)
    return schema


if __name__ == "__main__":
    unittest.main()
