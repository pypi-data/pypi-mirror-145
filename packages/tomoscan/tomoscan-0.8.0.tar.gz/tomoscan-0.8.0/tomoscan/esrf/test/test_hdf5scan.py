# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""Unit test for the scan defined at the hdf5 format"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "26/03/2021"

import unittest
import shutil
import os
import tempfile

from silx.io.url import DataUrl
from tomoscan.io import HDF5File
from tomoscan.test.utils import UtilsTest
from tomoscan.esrf.hdf5scan import (
    HDF5TomoScan,
    ImageKey,
    TomoFrame,
)
from tomoscan.unitsystem import metricsystem
from silx.io.utils import get_data
from tomoscan.test.utils import HDF5MockContext
import numpy
import h5py
import pytest
from tomoscan.nexus.paths.nxtomo import nx_tomo_path_v_1_0, nx_tomo_path_latest


class HDF5TestBaseClass(unittest.TestCase):
    """base class for hdf5 unit test"""

    def get_dataset(self, hdf5_dataset_name):
        dataset_file = os.path.join(self.test_dir, hdf5_dataset_name)
        o_dataset_file = UtilsTest.getH5Dataset(folderID=hdf5_dataset_name)
        shutil.copy(src=o_dataset_file, dst=dataset_file)
        return dataset_file

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)


class TestHDF5Scan(HDF5TestBaseClass):
    """Basic test for the hdf5 scan"""

    def setUp(self) -> None:
        super(TestHDF5Scan, self).setUp()
        self.dataset_file = self.get_dataset("frm_edftomomill_twoentries.nx")
        self.scan = HDF5TomoScan(scan=self.dataset_file)
        self.scan.nexus_version = 1.0

    def testGeneral(self):
        """some general on the HDF5Scan"""
        self.assertEqual(self.scan.master_file, self.dataset_file)
        self.assertEqual(self.scan.path, os.path.dirname(self.dataset_file))
        self.assertEqual(self.scan.type, "hdf5")
        self.assertEqual(self.scan.entry, "entry0000")
        self.assertEqual(len(self.scan.flats), 42)
        self.assertEqual(len(self.scan.darks), 1)
        self.assertEqual(len(self.scan.return_projs), 3)
        self.assertEqual(self.scan.tomo_n, None)
        self.assertEqual(self.scan.start_time, None)
        self.assertEqual(self.scan.end_time, None)
        self.assertEqual(self.scan.energy, 17.05)
        self.assertEqual(self.scan.field_of_view, None)
        self.assertEqual(self.scan.estimated_cor_frm_motor, None)
        self.assertEqual(len(self.scan.x_translation), 1546)
        self.assertEqual(len(self.scan.y_translation), 1546)
        self.assertEqual(len(self.scan.z_translation), 1546)

        proj_angles = self.scan.get_proj_angle_url()
        self.assertEqual(len(proj_angles), 1500 + 3)
        self.assertTrue(90 in proj_angles)
        self.assertTrue(24.0 in proj_angles)
        self.assertTrue("90.0(1)" in proj_angles)
        self.assertTrue("180.0(1)" in proj_angles)
        self.assertTrue(179.88 not in proj_angles)

        url_1 = proj_angles[0]
        self.assertTrue(url_1.is_valid())
        self.assertTrue(url_1.is_absolute())
        self.assertEqual(url_1.scheme(), "silx")
        # check conversion to dict
        _dict = self.scan.to_dict()
        scan2 = HDF5TomoScan.from_dict(_dict)
        self.assertEqual(scan2.master_file, self.scan.master_file)
        self.assertEqual(scan2.entry, self.scan.entry)

    def testFrames(self):
        """Check the `frames` property which is massively used under the
        HDF5TomoScan class"""
        frames = self.scan.frames
        # check some projections
        proj_2 = frames[24]
        self.assertTrue(isinstance(proj_2, TomoFrame))
        self.assertEqual(proj_2.index, 24)
        numpy.isclose(proj_2.rotation_angle, 0.24)
        self.assertFalse(proj_2.is_control)
        self.assertEqual(proj_2.url.file_path(), self.scan.master_file)
        self.assertEqual(proj_2.url.data_path(), "entry0000/instrument/detector/data")
        self.assertEqual(proj_2.url.data_slice(), 24)
        self.assertEqual(proj_2.image_key, ImageKey.PROJECTION)
        self.assertEqual(get_data(proj_2.url).shape, (20, 20))
        # check last two non-return projection
        for frame_index in (1520, 1542):
            with self.subTest(frame_index=frame_index):
                frame = frames[frame_index]
                self.assertTrue(frame.image_key, ImageKey.PROJECTION)
                self.assertFalse(frame.is_control)

        # check some darks
        dark_0 = frames[0]
        self.assertEqual(dark_0.index, 0)
        numpy.isclose(dark_0.rotation_angle, 0.0)
        self.assertFalse(dark_0.is_control)
        self.assertEqual(dark_0.url.file_path(), self.scan.master_file)
        self.assertEqual(dark_0.url.data_path(), "entry0000/instrument/detector/data")
        self.assertEqual(dark_0.url.data_slice(), 0)
        self.assertEqual(dark_0.image_key, ImageKey.DARK_FIELD)
        self.assertEqual(get_data(dark_0.url).shape, (20, 20))

        # check some flats
        flat_1 = frames[2]
        self.assertEqual(flat_1.index, 2)
        numpy.isclose(flat_1.rotation_angle, 0.0)
        self.assertFalse(flat_1.is_control)
        self.assertEqual(flat_1.url.file_path(), self.scan.master_file)
        self.assertEqual(flat_1.url.data_path(), "entry0000/instrument/detector/data")
        self.assertEqual(flat_1.url.data_slice(), 2)
        self.assertEqual(flat_1.image_key, ImageKey.FLAT_FIELD)
        self.assertEqual(get_data(flat_1.url).shape, (20, 20))

        # check some return projections
        r_proj_0 = frames[1543]
        self.assertTrue(isinstance(r_proj_0, TomoFrame))
        self.assertEqual(r_proj_0.index, 1543)
        numpy.isclose(r_proj_0.rotation_angle, 180)
        self.assertTrue(r_proj_0.is_control)
        self.assertEqual(r_proj_0.url.file_path(), self.scan.master_file)
        self.assertEqual(r_proj_0.url.data_path(), "entry0000/instrument/detector/data")
        self.assertEqual(r_proj_0.url.data_slice(), 1543)
        self.assertEqual(r_proj_0.image_key, ImageKey.PROJECTION)
        self.assertEqual(get_data(r_proj_0.url).shape, (20, 20))

    def testProjections(self):
        """Make sure projections are valid"""
        projections = self.scan.projections
        self.assertEqual(len(self.scan.projections), 1500)
        url_0 = projections[list(projections.keys())[0]]
        self.assertEqual(url_0.file_path(), os.path.join(self.scan.master_file))
        self.assertEqual(url_0.data_slice(), 22)
        # should be 4 but angles are truely missleading: 179.88, 180.0, 90, 0.
        # in this case we are not using any information from image_key_control
        # and we wait deduce 'return mode' from angles.
        self.assertEqual(len(self.scan.alignment_projections), 3)

    def testDark(self):
        """Make sure darks are valid"""
        n_dark = 1
        self.assertEqual(self.scan.dark_n, n_dark)
        darks = self.scan.darks
        self.assertEqual(len(darks), 1)
        # TODO check accumulation time

    def testFlats(self):
        """Make sure flats are valid"""
        n_flats = 42
        flats = self.scan.flats
        self.assertEqual(len(flats), n_flats)
        self.assertEqual(self.scan.flat_n, n_flats)
        with self.assertRaises(NotImplementedError):
            self.scan.ff_interval

    def testDims(self):
        self.assertEqual(self.scan.dim_1, 20)
        self.assertEqual(self.scan.dim_2, 20)

    def testAxisUtils(self):
        self.assertEqual(self.scan.scan_range, 180)
        self.assertEqual(len(self.scan.projections), 1500)

        radios_urls_evolution = self.scan.get_proj_angle_url()
        self.assertEqual(len(radios_urls_evolution), 1503)
        self.assertEqual(radios_urls_evolution[0].file_path(), self.scan.master_file)
        self.assertEqual(radios_urls_evolution[0].data_slice(), 22)
        self.assertEqual(
            radios_urls_evolution[0].data_path(), "entry0000/instrument/detector/data"
        )

    def testDarkRefUtils(self):
        self.assertEqual(len(self.scan.projections), 1500)
        pixel_size = self.scan.pixel_size
        self.assertTrue(pixel_size is not None)
        self.assertTrue(
            numpy.isclose(
                self.scan.pixel_size, 0.05 * metricsystem.MetricSystem.MILLIMETER.value
            )
        )
        self.assertTrue(numpy.isclose(self.scan.get_pixel_size(unit="micrometer"), 50))
        self.assertTrue(
            numpy.isclose(
                self.scan.x_pixel_size,
                0.05 * metricsystem.MetricSystem.MILLIMETER.value,
            )
        )
        self.assertTrue(
            numpy.isclose(
                self.scan.y_pixel_size,
                0.05 * metricsystem.MetricSystem.MILLIMETER.value,
            )
        )

    def testNabuUtil(self):
        self.assertTrue(numpy.isclose(self.scan.distance, -19.9735))
        self.assertTrue(numpy.isclose(self.scan.get_distance(unit="cm"), -1997.35))

    def testCompactedProjs(self):
        projs_compacted = self.scan.projections_compacted
        self.assertEqual(projs_compacted.keys(), self.scan.projections.keys())
        for i in range(22, 1520 + 1):
            self.assertEqual(projs_compacted[i].data_slice(), slice(22, 1521, None))
        for i in range(1542, 1543):
            self.assertEqual(projs_compacted[i].data_slice(), slice(1542, 1543, None))


class TestFlatFieldCorrection(HDF5TestBaseClass):
    """Test the flat field correction"""

    def setUp(self) -> None:
        super(TestFlatFieldCorrection, self).setUp()
        self.dataset_file = self.get_dataset("frm_edftomomill_twoentries.nx")
        self.scan = HDF5TomoScan(scan=self.dataset_file)

    def testFlatAndDarksSet(self):
        self.scan.set_normed_flats(
            {
                21: numpy.random.random(20 * 20).reshape((20, 20)),
                1520: numpy.random.random(20 * 20).reshape((20, 20)),
            }
        )
        self.scan.set_normed_darks({0: numpy.random.random(20 * 20).reshape((20, 20))})

        projs = []
        proj_indexes = []
        for proj_index, proj in self.scan.projections.items():
            projs.append(proj)
            proj_indexes.append(proj_index)
        normed_proj = self.scan.flat_field_correction(
            projs=projs, proj_indexes=proj_indexes
        )
        self.assertEqual(len(normed_proj), len(self.scan.projections))
        raw_data = get_data(projs[50])
        self.assertFalse(numpy.array_equal(raw_data, normed_proj[50]))

    def testNoFlatOrDarkSet(self):
        projs = []
        proj_indexes = []
        for proj_index, proj in self.scan.projections.items():
            projs.append(proj)
            proj_indexes.append(proj_index)
        with self.assertLogs("tomoscan", level="ERROR"):
            normed_proj = self.scan.flat_field_correction(
                projs=projs, proj_indexes=proj_indexes
            )
        self.assertEqual(len(normed_proj), len(self.scan.projections))
        raw_data = get_data(projs[50])
        self.assertTrue(numpy.array_equal(raw_data, normed_proj[50]))


class TestGetSinogram(HDF5TestBaseClass):
    """Test the get_sinogram function"""

    def setUp(self) -> None:
        super(TestGetSinogram, self).setUp()
        self.dataset_file = self.get_dataset("frm_edftomomill_twoentries.nx")
        self.scan = HDF5TomoScan(scan=self.dataset_file)
        # set some random dark and flats
        self.scan.set_normed_flats(
            {
                21: numpy.random.random(20 * 20).reshape((20, 20)),
                1520: numpy.random.random(20 * 20).reshape((20, 20)),
            }
        )
        dark = numpy.random.random(20 * 20).reshape((20, 20))
        self.scan.set_normed_darks({0: dark})
        self.scan._flats_weights = self.scan._get_flats_weights()
        self._raw_frame = []
        for index, url in self.scan.projections.items():
            self._raw_frame.append(get_data(url))
        self._raw_frame = numpy.asarray(self._raw_frame)

        assert self._raw_frame.ndim == 3

        normed_frames = []
        for proj_i, z_frame in enumerate(self._raw_frame):
            normed_frames.append(
                self.scan._frame_flat_field_correction(
                    data=z_frame,
                    dark=dark,
                    flat_weights=self.scan._flats_weights[proj_i]
                    if proj_i in self.scan._flats_weights
                    else None,
                )
            )
        self._normed_volume = numpy.array(normed_frames)
        assert self._normed_volume.ndim == 3
        self._normed_sinogram_12 = self._normed_volume[:, 12, :]
        assert self._normed_sinogram_12.ndim == 2
        assert self._normed_sinogram_12.shape == (1500, 20)

    def testGetSinogram1(self):
        sinogram = self.scan.get_sinogram(line=12, subsampling=1)
        self.assertEqual(sinogram.shape, (1500, 20))

    def testGetSinogram2(self):
        """Test if subsampling is negative"""
        with self.assertRaises(ValueError):
            self.scan.get_sinogram(line=0, subsampling=-1)

    def testGetSinogram3(self):
        sinogram = self.scan.get_sinogram(line=0, subsampling=3)
        self.assertEqual(sinogram.shape, (500, 20))

    def testGetSinogram4(self):
        """Test if line is not in the projection"""
        with self.assertRaises(ValueError):
            self.scan.get_sinogram(line=-1, subsampling=1)

    def testGetSinogram5(self):
        """Test if line is not in the projection"""
        with self.assertRaises(ValueError):
            self.scan.get_sinogram(line=25, subsampling=1)

    def testGetSinogram6(self):
        """Test if line is not in the projection"""
        with self.assertRaises(TypeError):
            self.scan.get_sinogram(line=0, subsampling="tata")


class TestIgnoredProjections(HDF5TestBaseClass):
    """Test the ignore_projections parameter"""

    def setUp(self) -> None:
        super(TestIgnoredProjections, self).setUp()
        self.dataset_file = self.get_dataset("frm_edftomomill_oneentry.nx")
        self.ignored_projs = [387, 388, 389, 390, 391, 392, 393, 394, 395, 396]

    def testIgnoreProjections(self):
        self.scan = HDF5TomoScan(
            scan=self.dataset_file, ignore_projections=self.ignored_projs
        )
        self.scan._projections = None
        for idx in self.ignored_projs:
            self.assertFalse(
                idx in self.scan.projections,
                "Projection index %d is supposed to be ignored" % idx,
            )


class TestGetSinogramLegacy(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

        self.proj_data = numpy.arange(1000, 1000 + 10 * 20 * 30).reshape(30, 10, 20)
        self.proj_angle = numpy.linspace(0, 180, 30)
        self.dark_value = 0.5
        self.flat_value = 1
        self.dark_data = numpy.ones((10, 20)) * self.dark_value
        self.dark_angle = numpy.array(
            [
                0,
            ]
        )
        self.flat_data_1 = numpy.ones((10, 20)) * self.flat_value
        self.flat_angle_1 = numpy.array(
            [
                0,
            ]
        )

        self.flat_data_2 = numpy.ones((10, 20)) * self.flat_value
        self.flat_angle_2 = numpy.array(
            [
                90,
            ]
        )
        self.flat_data_3 = numpy.ones((10, 20)) * self.flat_value
        self.flat_angle_3 = numpy.array(
            [
                180,
            ]
        )

        # data dataset
        self.data = numpy.empty((34, 10, 20))
        self.data[0] = self.dark_data
        self.data[1] = self.flat_data_1
        self.data[2:17] = self.proj_data[:15]
        self.data[17] = self.flat_data_2
        self.data[18:33] = self.proj_data[15:]
        self.data[33] = self.flat_data_3

        self.file_path = os.path.join(self.test_dir, "test.h5")
        self.create_arange_dataset(self.file_path)

    def create_arange_dataset(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

        with h5py.File(file_path, mode="a") as h5f:
            entry = h5f.require_group("entry0000")

            # rotation angle
            entry["instrument/detector/data"] = self.data
            rotation_angle = numpy.empty(34)
            rotation_angle[0] = self.dark_angle
            rotation_angle[1] = self.flat_angle_1
            rotation_angle[2:17] = self.proj_angle[:15]
            rotation_angle[17] = self.flat_angle_2
            rotation_angle[18:33] = self.proj_angle[15:]
            rotation_angle[33] = self.flat_angle_3

            entry["sample/rotation_angle"] = rotation_angle

            # image key / images keys
            image_keys = []
            image_keys.append(ImageKey.DARK_FIELD.value)
            image_keys.append(ImageKey.FLAT_FIELD.value)
            image_keys.extend([ImageKey.PROJECTION.value] * 15)
            image_keys.append(ImageKey.FLAT_FIELD.value)
            image_keys.extend([ImageKey.PROJECTION.value] * 15)
            image_keys.append(ImageKey.FLAT_FIELD.value)
            entry["instrument/detector/image_key"] = numpy.array(image_keys)
            entry["instrument/detector/image_key_control"] = numpy.array(image_keys)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def testImplementations(self):
        scan = HDF5TomoScan(self.file_path, "entry0000")
        assert len(scan.projections) == 30
        assert len(scan.flats) == 3
        assert len(scan.darks) == 1

        scan.set_normed_darks(
            {
                0: self.dark_data,
            }
        )

        scan.set_normed_flats(
            {
                1: self.flat_data_1,
                17: self.flat_data_2,
                33: self.flat_data_3,
            }
        )

        scan._flats_weights = scan._get_flats_weights()
        sinogram_old = scan._get_sinogram_ref_imp(line=5)
        sinogram_new = scan.get_sinogram(line=5)
        raw_sinogram = self.proj_data[:, 5, :]
        corrected = (raw_sinogram - self.dark_value) / (
            self.flat_value - self.dark_value
        )
        numpy.testing.assert_array_equal(corrected, sinogram_new)
        numpy.testing.assert_array_equal(sinogram_old, sinogram_new)


def test_HDF5TomoScan_API():
    """several minor test of the HDF5TomoScan API"""
    with HDF5MockContext(
        scan_path=os.path.join(tempfile.mkdtemp(), "scan_test"),
        n_proj=10,
        n_ini_proj=10,
        distance=1.0,
        energy=1.0,
    ) as scan:
        scan.clear_caches()
        scan.is_abort()
        scan.nexus_version = 1.1
        scan.sequence_name
        scan.sample_name
        scan.group_size
        scan.exposure_time
        with pytest.raises(NotImplementedError):
            scan.ff_interval


def test_HDF5TomoScan_source_API():
    """test dedicated API for Source"""
    with HDF5MockContext(
        scan_path=os.path.join(tempfile.mkdtemp(), "scan_test"),
        n_proj=10,
        n_ini_proj=10,
        distance=1.0,
        energy=1.0,
    ) as scan:
        scan.source
        scan.source_name
        scan.source_type
        scan.instrument_name
        with h5py.File(scan.master_file, mode="a") as h5f:
            h5f[scan.entry]["instrument/detector/field_of_view"] = "Full"
        assert scan.field_of_view.value == "Full"
        scan.x_magnified_pixel_size
        scan.y_magnified_pixel_size


def test_TomoFrame_API():
    """Test TomoFrame API"""
    frame = TomoFrame(index=0)
    frame.image_key = ImageKey.PROJECTION
    with pytest.raises(TypeError):
        frame.image_key = "projection"
    frame.rotation_angle = 12.0
    frame.x_translation
    frame.y_translation
    frame.z_translation
    frame.is_control


def test_HDF5TomoScan_nxversion():
    """test various NX versions"""
    with HDF5MockContext(
        scan_path=os.path.join(tempfile.mkdtemp(), "scan_test"),
        n_proj=10,
        n_ini_proj=10,
        distance=1.0,
        energy=1.0,
    ) as scan:

        hdf5scan = HDF5TomoScan(scan.master_file)
        # The default behavior is to take NX 1.1 if not present in file metadata
        # This is not future-proof, perhaps do a _NEXUS_PATHS_LATEST class ?
        assert hdf5scan.nexus_path is nx_tomo_path_latest
        energy_path_11 = hdf5scan.nexus_path.ENERGY_PATH

        hdf5scan = HDF5TomoScan(scan.master_file, nx_version=1.0)
        # Parse with a different NX version.
        # This Mock will provide energy at two different locations (instrument/beam/energy and beam/energy)
        # so we cannot test directly the "legacy files" behavior.
        # Instead we just check that the energy path is different in NX 1.0 and NX 1.1.
        assert hdf5scan.nexus_path is nx_tomo_path_v_1_0
        energy_path_10 = hdf5scan.nexus_path.ENERGY_PATH
        assert energy_path_10 != energy_path_11


def test_get_relative_file(tmpdir):
    """Test that get_relative_file function is working correctly for HDFScan"""
    folder_path = os.path.join(tmpdir, "scan_test")
    with HDF5MockContext(
        scan_path=folder_path,
        n_proj=10,
        n_ini_proj=10,
        distance=1.0,
        energy=1.0,
    ) as scan:
        expected_f1 = os.path.join(folder_path, "scan_test_nabu_processes.h5")
        assert (
            scan.get_relative_file("nabu_processes.h5", with_dataset_prefix=True)
            == expected_f1
        )

        expected_f2 = os.path.join(folder_path, "nabu_processes.h5")
        assert (
            scan.get_relative_file("nabu_processes.h5", with_dataset_prefix=False)
            == expected_f2
        )


def test_save_and_load_dark(tmp_path):
    """test saving and loading of the dark is workinf for HDF5"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    with HDF5MockContext(
        scan_path=str(test_dir),
        n_proj=10,
        n_ini_proj=10,
        distance=1.0,
        energy=1.0,
    ) as scan:
        assert scan.load_reduced_darks() == {}
        assert scan.load_reduced_flats() == {}
        dark_frame = numpy.ones((100, 100))
        scan.save_reduced_darks(
            {
                0: dark_frame,
            }
        )
        assert scan.load_reduced_flats() == {}
        loaded_darks = scan.load_reduced_darks()
        assert len(loaded_darks) == 1
        assert 0 in loaded_darks
        numpy.testing.assert_array_equal(loaded_darks[0], dark_frame)


def test_save_and_load_flats(tmp_path):
    """test saving and loading of the flats is workinf for HDF5"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    with HDF5MockContext(
        scan_path=str(test_dir),
        n_proj=10,
        n_ini_proj=10,
        distance=1.0,
        energy=1.0,
    ) as scan:
        assert scan.load_reduced_darks() == {}
        assert scan.load_reduced_flats() == {}

        flat_frame_1 = numpy.ones((100, 100))
        flat_frame_222 = numpy.zeros((100, 100))
        scan.save_reduced_flats(
            {
                1: flat_frame_1,
                222: flat_frame_222,
            }
        )
        loaded_flats = scan.load_reduced_flats()
        assert len(loaded_flats) == 2
        assert 1 in loaded_flats
        assert 222 in loaded_flats
        numpy.testing.assert_array_equal(loaded_flats[1], flat_frame_1)
        numpy.testing.assert_array_equal(loaded_flats[222], flat_frame_222)
        assert scan.load_reduced_darks() == {}

        # test to save other flats to insure older one are removed
        flat_frame_333 = numpy.ones((100, 100)) * 3.2
        flat_frame_1 = numpy.ones((100, 100)) * 2.1
        scan.save_reduced_flats(
            {
                1: flat_frame_1,
                333: flat_frame_333,
            }
        )
        loaded_flats = scan.load_reduced_flats()
        assert len(loaded_flats) == 2
        assert 1 in loaded_flats
        assert 333 in loaded_flats
        numpy.testing.assert_array_equal(loaded_flats[1], flat_frame_1)
        numpy.testing.assert_array_equal(loaded_flats[333], flat_frame_333)


def test_save_dark_flat_reduced_several_urls(tmp_path):
    """test saving and loading dark and flat providing several urls"""
    test_dir = tmp_path / "test_dir"
    os.makedirs(test_dir)
    with HDF5MockContext(
        scan_path=str(test_dir),
        n_proj=10,
        n_ini_proj=10,
        distance=1.0,
        energy=1.0,
    ) as scan:
        assert scan.load_reduced_darks() == {}
        assert scan.load_reduced_flats() == {}

        url_flats_edf = HDF5TomoScan.REDUCED_FLATS_DATAURLS[0]
        url_flats_processes = DataUrl(
            file_path=scan.get_relative_file(
                file_name="my_processes.h5", with_dataset_prefix=False
            ),
            data_path="/{entry}/process_1/results/flats/{index}",
            scheme="hdf5",
        )
        url_darks_edf = HDF5TomoScan.REDUCED_DARKS_DATAURLS[0]
        url_darks_processes = DataUrl(
            file_path=scan.get_relative_file(
                file_name="my_processes.h5", with_dataset_prefix=False
            ),
            data_path="/{entry}/process_1/results/darks/{index}",
            scheme="silx",
        )

        flat_frame_1 = numpy.ones((100, 100))
        flat_frame_222 = numpy.zeros((100, 100))
        scan.save_reduced_flats(
            {
                1: flat_frame_1,
                222: flat_frame_222,
            }
        )
        assert scan.load_reduced_darks() == {}
        flat_frame_1 = numpy.ones((100, 100))
        flat_frame_1000 = numpy.ones((100, 100)) * 1.2
        dark_frame = numpy.zeros((100, 100))
        scan.save_reduced_flats(
            flats={
                1: flat_frame_1,
                1000: flat_frame_1000,
            },
            output_urls=(
                url_flats_edf,
                url_flats_processes,
            ),
        )
        # test raise a type error if frame is not a numpy array
        with pytest.raises(TypeError):
            scan.save_reduced_darks(
                darks={
                    0: "test",
                },
                output_urls=(
                    url_darks_edf,
                    url_darks_processes,
                ),
            )

        # test raise a type error if frame is not a 2D numpy array
        with pytest.raises(ValueError):
            scan.save_reduced_darks(
                darks={
                    0: numpy.asarray([12, 13]),
                },
                output_urls=(
                    url_darks_edf,
                    url_darks_processes,
                ),
            )

        scan.save_reduced_darks(
            darks={
                0: dark_frame,
            },
            output_urls=(
                url_darks_edf,
                url_darks_processes,
            ),
        )
        assert len(scan.load_reduced_flats()) == 2
        assert len(scan.load_reduced_darks()) == 1
        processes_file = os.path.join(scan.path, "my_processes.h5")
        assert os.path.exists(processes_file)

        with HDF5File(processes_file, mode="r") as h5s:
            assert "/entry/process_1/results/darks" in h5s
            darks_grp = h5s["/entry/process_1/results/darks"]
            assert "0" in darks_grp
            numpy.testing.assert_array_equal(darks_grp["0"][()], dark_frame)
            assert "/entry/process_1/results/flats" in h5s
            flats_grp = h5s["/entry/process_1/results/flats"]
            assert "1" in flats_grp
            assert "1000" in flats_grp
            numpy.testing.assert_array_equal(flats_grp["1"], flat_frame_1)
            numpy.testing.assert_array_equal(flats_grp["1000"], flat_frame_1000)

        assert len(scan.load_reduced_flats((url_flats_processes,))) == 2
        assert len(scan.load_reduced_darks((url_darks_processes,))) == 1
        loaded_reduced_darks = scan.load_reduced_darks(
            (url_darks_processes,), return_as_url=True
        )
        assert isinstance(loaded_reduced_darks[0], DataUrl)
        assert loaded_reduced_darks[0].file_path() == processes_file
        assert loaded_reduced_darks[0].data_path() == "/entry/process_1/results/darks/0"
        assert loaded_reduced_darks[0].scheme() == "silx"
