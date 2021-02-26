from footil.version import GenericVersion, SemverVersion, EMPTY_VERSION

from . import common


class TestVersionCommon(common.TestFootilCommon):
    """Common class for version module tests."""

    _version_manager = None

    def get_latest_version_values_map(self):
        """Get values map for latest version check.

        Case 1: no versions (list), default empty version.
        Case 2: no versions (tuple), not a default empty version.
        """
        return [
            # Case 1.
            (([],), EMPTY_VERSION),
            # Case 2.
            (((), '0.1'), '0.1'),
        ]

    def test_01_get_latest_version(self):
        """Check latest version from version manager."""
        if not self._version_manager:
            return
        values_map = self.get_latest_version_values_map()
        for class_args, expected_version in values_map:
            VM = self._version_manager(*class_args)
            self.assertEqual(VM.get_latest_version(), expected_version)

    def get_version_values_map(self):
        """Get values map for version check."""
        return []

    def test_02_get_version(self):
        """Check latest version from version manager."""
        if not self._version_manager:
            return
        values_map = self.get_version_values_map()
        for class_args, meth_args, expected_version in values_map:
            VM = self._version_manager(*class_args)
            if expected_version == ValueError:
                self.assertRaises(ValueError, VM.get_version, *meth_args)
            else:
                try:
                    version = VM.get_version(*meth_args)
                except ValueError:
                    self.fail('Should not fail, version is as expected.')
                self.assertEqual(version, expected_version)


class TestGenericVersion(TestVersionCommon):
    """Test cases for generic version manager tests."""

    _version_manager = GenericVersion

    def get_latest_version_values_map(self):
        """Get values map for latest generic version check.

        Case 3: versions defined (list of str).
        Case 4: versions defined (list of int/str/float).
        """
        return super().get_latest_version_values_map() + [
            # Case 3.
            ((['1', '0.1', '2', '1.2'],), '2'),
            # Case 4.
            ((['1', 0.1, 2, '1.2'],), 2),
        ]

    def get_version_values_map(self):
        """Get values map for generic version check.

        Case 1: no versions, no passed version.
        Case 2: no versions, custom version passed.
        Case 3: versions, custom (existing) version passed.
        Case 4: versions, custom (not existing) version passed.
        """
        return super().get_version_values_map() + [
            # Case 1.
            (([],), ((),), ValueError),
            # Case 2.
            (([],), ('0.0.1',), '0.0.1'),
            # Case 3.
            ((['0.1', 2, '0.0.1', '1'],), ('0.1',), ValueError),
            # Case 4.
            ((['0.1', 2, '0.0.1', '1'],), ('0.0.2',), '0.0.2'),
        ]


class TestSemverVersion(TestVersionCommon):
    """Test cases for semver version manager tests."""

    _version_manager = SemverVersion

    def get_latest_version_values_map(self):
        """Get values map for latest semver version check.

        Case 3: no versions (tuple), not a default empty version (semver
            valid).
        Case 4: versions defined, but non is semver valid.
        Case 5: versions defined, some of them - semver valid.
        """
        return super().get_latest_version_values_map() + [
            # Case 3.
            (((), '0.1.0'), '0.1.0'),
            # Case 4.
            ((['1', '2.0', '0.1', '0.1', '2', '1.2'],), EMPTY_VERSION),
            # Case 5.
            ((['1', '2.0.2', '0.1', '0.0.1', '2', '1.2'],), '2.0.2'),
        ]

    def get_version_values_map(self):
        """Get values map for semver version check.

        Case 1: no versions, no passed version.
        Case 2: no versions, custom version (valid) passed.
        Case 3: no versions, custom version (invalid) passed.
        Case 4: versions, custom (existing) version passed.
        Case 5: versions, custom (not existing) version passed.
        """
        return super().get_version_values_map() + [
            # Case 1.
            (([],), ((),), '0.1.0'),
            # Case 2.
            (([],), ('0.0.1',), '0.0.1'),
            # # Case 3.
            (([],), ('0.1',), ValueError),
            (([],), ('0.0.0.1',), ValueError),
            # # Case 4.
            ((['2.0.1', '0.1.0', '0.0.1', '1.0.0'],), ('2.0.1',), ValueError),
            # # Case 5.
            ((['2.0.1', '0.1.0', '0.0.1', '1.0.0'],), ('2.1.0',), '2.1.0'),
        ]

    def test_03_generate_semver_version(self):
        """Check version generation from semver version manager.

        Case 1: no previous versions.
        Case 2: previous versions exist.
        """
        def test_version_bump(values_map):
            for part, expected_version in values_map:
                self.assertEqual(
                    SV.generate_version(part=part), expected_version)

        # Case 1.
        SV = SemverVersion([])
        test_version_bump([
            ('minor', '0.1.0'),
            ('major', '1.0.0'),
            ('patch', '0.0.1'),
            ('prerelease', '0.0.0-rc.1'),
            ('build', '0.0.0+build.1'),
            ('final', '0.0.0'),
        ])
        # Case 2.
        SV = SemverVersion(['0.0.1', '2.1.1', '0.0.3', '0.0.3-rc.1', '5.0'])
        test_version_bump([
            ('minor', '2.2.0'),
            ('major', '3.0.0'),
            ('patch', '2.1.2'),
            ('prerelease', '2.1.1-rc.1'),
            ('build', '2.1.1+build.1'),
            ('final', '2.1.1'),
        ])
