
import os
import unittest
import numpy as np
import coffea.hist as hist
from uhepp import from_yaml, from_yamls, from_json, from_jsons, from_coffea
from uhepp import from_file, UHeppHist
import uhepp

class FromTestCase(unittest.TestCase):
    """Base class to test from_XXX methods"""
    @staticmethod
    def rel_path(filename):
        """Convert a filename to a file-relative path"""
        return os.path.join(os.path.dirname(__file__), filename)

    def assertTrivialHist(self, hist, **kwds):
        """Assert the argument is the trivial toy histogram"""
        self.assertEqual(hist.version, "0.1")
        self.assertEqual(hist.date, "2020-11-10T23:39:00+01:00")
        self.assertEqual(hist.filename, "hello")
        self.assertEqual(hist.symbol, "x")
        self.assertEqual(hist.bin_edges, list(range(6)))
        self.assertEqual(hist.stacks, [])
        self.assertEqual(hist.ratio, [])
        self.assertEqual(hist.yields, {})

        self.assertIsNone(hist.author)
        self.assertIsNone(hist.lumi)
        self.assertIsNone(hist.ratio_max)

    def assertBasicHist(self, hist, **kwds):
        """Assert the argument is the basic toy histogram"""
        self.assertEqual(hist.version, "0.1")
        self.assertEqual(hist.date, "2020-11-10T23:39:00+01:00")
        self.assertEqual(hist.filename, "hello")
        self.assertEqual(hist.author, "Frank Sauerburger")
        self.assertEqual(hist.symbol, "x")
        self.assertEqual(hist.bin_edges, list(range(6)))

        stack, = hist.stacks
        self.assertEqual(stack.bartype, "points")
        content, = stack.content
        self.assertEqual(content.yield_names, ["data"])
        self.assertEqual(content.label, "Data")

        data_yield = hist.yields["data"]
        self.assertEqual(data_yield.base, [1.1, 1.9, 2.8, 4.2, 5, 6, 7])

        self.assertEqual(len(hist.yields), 1)

class FromYamlTestCase(FromTestCase):
    """Check that importing from yaml works"""

    def test_trivial_hist_string(self):
        """Check that the trivial hist is restores from a string"""
        with open(self.rel_path("trivial_hist.yaml")) as yaml_file:
            yaml_string = yaml_file.read()

        hist = from_yamls(yaml_string)
        self.assertTrivialHist(hist)

    def test_trivial_hist(self):
        """Check that importing a trivial hist restores all values"""
        hist = from_yaml(self.rel_path("trivial_hist.yaml"))
        self.assertTrivialHist(hist)

    def test_trivial_hist_render(self):
        """Check that rendering a trivial hist succeeds"""
        hist = from_yaml(self.rel_path("trivial_hist.yaml"))
        self.assertIsNotNone(hist.render())

    def test_basic_hist(self):
        """Check that importing a basic hist restores all values"""
        hist = from_yaml(self.rel_path("basic_hist.yaml"))

    def test_basic_hist_render(self):
        """Check that rendering a basic hist succeeds"""
        hist = from_yaml(self.rel_path("basic_hist.yaml"))
        self.assertIsNotNone(hist.render())

class FromFileTestCase(FromTestCase):
    """Test the auto-switching function from_file()"""

    def test_yaml_extension(self):
        """Check that a yaml file is accepted"""
        hist = from_file(self.rel_path("basic_hist.yaml"))
        self.assertIsInstance(hist, UHeppHist)

    def test_json_extension(self):
        """Check that a yaml file is accepted"""
        hist = from_file(self.rel_path("basic_hist.json"))
        self.assertIsInstance(hist, UHeppHist)

    def test_invalid_extension(self):
        """Check that a python file raises an exception"""
        self.assertRaises(ValueError, from_file, __file__)

class FromJsonTestCase(FromTestCase):
    """Check that importing from json works"""

    def test_trivial_hist_string(self):
        """Check that the trivial hist is restores from a string"""
        with open(self.rel_path("trivial_hist.json")) as json_file:
            json_string = json_file.read()

        hist = from_jsons(json_string)
        self.assertTrivialHist(hist)

    def test_trivial_hist(self):
        """Check that importing a trivial hist restores all values"""
        hist = from_json(self.rel_path("trivial_hist.json"))
        self.assertTrivialHist(hist)

    def test_trivial_hist_render(self):
        """Check that rendering a trivial hist succeeds"""
        hist = from_json(self.rel_path("trivial_hist.json"))
        self.assertIsNotNone(hist.render())

    def test_basic_hist(self):
        """Check that importing a basic hist restores all values"""
        hist = from_json(self.rel_path("basic_hist.json"))

    def test_basic_hist_render(self):
        """Check that rendering a basic hist succeeds"""
        hist = from_json(self.rel_path("basic_hist.json"))
        self.assertIsNotNone(hist.render())

class CloneTestCase(unittest.TestCase):
    """Test the implementation of clone() using to_json and from_json"""

    def test_indepenent(self):
        """Check that cloning produces an independent object"""
        hist = uhepp.UHeppHist("m", [0, 100, 200, 300])
        hist.ratio = [uhepp.RatioItem([], [])]

        new_hist = hist.clone()
        hist.ratio = []
        self.assertEqual(len(new_hist.ratio), 1)

class FromCoffeaTestCase(unittest.TestCase):
    """Test the implementation of from_coffea()"""

    @staticmethod
    def toy_coffea_hist():
        """Create and return a toy histogram  in coffea"""

        seed = int.from_bytes(b"uhepp", "big") % 2**31
        np.random.seed(seed)

        # Copy-paste example from 
        # https://coffeateam.github.io/coffea/notebooks/histograms.html

        histo = hist.Hist("Counts",
                          hist.Cat("sample", "sample name"),
                          hist.Bin("x", "x value", 20, -10, 10),
                          hist.Bin("y", "y value", 20, -10, 10),
                          hist.Bin("z", "z value", 20, -10, 10),
        )
        
        xyz = np.random.multivariate_normal(mean=[1, 3, 7], cov=np.eye(3), size=10000)
        xyz_sample2 = np.random.multivariate_normal(mean=[1, 3, 7], cov=np.eye(3), size=10000)
        weight = np.arctan(np.sqrt(np.power(xyz_sample2, 2).sum(axis=1)))

        histo.fill(sample="sample 1", x=xyz[:,0], y=xyz[:,1], z=xyz[:,2])
        histo.fill(sample="sample 2", x=xyz_sample2[:,0], y=xyz_sample2[:,1], z=xyz_sample2[:,2], weight=weight)
        
        return histo

    def test_samples(self):
        """Check that the samples are listed in the dataset return values"""
        coffea_hist = self.toy_coffea_hist()
        hists, datasets = from_coffea(coffea_hist)

        self.assertEqual(datasets, ["sample 1", "sample 2"])


    def test_yields(self):
        """Check that the yields are filled correctly"""
        coffea_hist = self.toy_coffea_hist()
        hists, datasets = from_coffea(coffea_hist)

        self.assertEqual(len(hists), 3)
        hx, hy, hz = hists

        # x projection
        self.assertEqual(hx.yields.keys(), {"sample 1", "sample 2"})
        self.assertEqual(len(hx.yields["sample 1"]), 22)
        self.assertEqual(len(hx.yields["sample 2"]), 22)

        self.assertAlmostEqual(hx.yields["sample 1"].base[9], 213)
        self.assertAlmostEqual(hx.yields["sample 1"].stat[9], np.sqrt(213))

        self.assertAlmostEqual(hx.yields["sample 2"].base[9], 324.06700678071786)
        self.assertAlmostEqual(hx.yields["sample 2"].stat[9], 21.606056455946145)

        # y projection
        self.assertEqual(hy.yields.keys(), {"sample 1", "sample 2"})
        self.assertEqual(len(hy.yields["sample 1"]), 22)
        self.assertEqual(len(hy.yields["sample 2"]), 22)

        self.assertAlmostEqual(hy.yields["sample 1"].base[12], 1377)
        self.assertAlmostEqual(hy.yields["sample 1"].stat[12], np.sqrt(1377))

        self.assertAlmostEqual(hy.yields["sample 2"].base[12], 1983.3727966421063)
        self.assertAlmostEqual(hy.yields["sample 2"].stat[12], 53.298922844614914)

        # z projection
        self.assertEqual(hz.yields.keys(), {"sample 1", "sample 2"})
        self.assertEqual(len(hz.yields["sample 1"]), 22)
        self.assertEqual(len(hz.yields["sample 2"]), 22)

        self.assertAlmostEqual(hz.yields["sample 1"].base[15], 261)
        self.assertAlmostEqual(hz.yields["sample 1"].stat[15], np.sqrt(261))

        self.assertAlmostEqual(hz.yields["sample 2"].base[15], 310.407073027837)
        self.assertAlmostEqual(hz.yields["sample 2"].stat[15], 20.834936855091176)


    def test_init_props(self):
        """Check that bins and variable are set correctly"""
        coffea_hist = self.toy_coffea_hist()
        hists, datasets = from_coffea(coffea_hist)

        self.assertEqual(len(hists), 3)
        hx, hy, hz = hists

        self.assertEqual(len(hx.bin_edges), 21)
        self.assertEqual(hx.bin_edges[0], -10)
        self.assertEqual(hx.bin_edges[-1], 10)
        self.assertEqual(hx.symbol, "x")

        self.assertEqual(len(hy.bin_edges), 21)
        self.assertEqual(hy.bin_edges[0], -10)
        self.assertEqual(hy.bin_edges[-1], 10)
        self.assertEqual(hy.symbol, "y")

        self.assertEqual(len(hz.bin_edges), 21)
        self.assertEqual(hz.bin_edges[0], -10)
        self.assertEqual(hz.bin_edges[-1], 10)
        self.assertEqual(hz.symbol, "z")

    def test_stacks(self):
        """Check that the optional stacks argument populates the stacks"""
        coffea_hist = self.toy_coffea_hist()
        hists, datasets = from_coffea(coffea_hist, stacks=True)

        self.assertEqual(len(hists), 3)
        hx, hy, hz = hists

        self.assertEqual(len(hx.stacks), 1)
        self.assertEqual(len(hx.stacks[0].content), 2)

        self.assertEqual(len(hy.stacks), 1)
        self.assertEqual(len(hy.stacks[0].content), 2)

        self.assertEqual(len(hz.stacks), 1)
        self.assertEqual(len(hz.stacks[0].content), 2)
