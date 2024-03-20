import unittest

from virsh_duplicate import modify_vm_xml


class MyTestCase(unittest.TestCase):
    def test_modify_vm_xml(self):
        old_xml = """
        <domain type="kvm">
          <name>old_name</name>
          <uuid>old_guid</uuid>
        </domain>
        """
        actual = modify_vm_xml(old_xml, 'new_name', 'new_uuid')

        self.assertNotIn('old_name', actual)
        self.assertNotIn('old_guid', actual)

        self.assertIn('<name>new_name</name>', actual)
        self.assertIn('<uuid>new_uuid</uuid>', actual)


if __name__ == '__main__':
    unittest.main()
