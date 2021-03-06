import unittest
import os
import shutil
from Filter import Filter 
from heppy.framework.event import Event
import heppy.framework.config as cfg

class FilterTestCase(unittest.TestCase):

    def setUp(self):
        os.mkdir('looper')
    
    def tearDown(self):
        shutil.rmtree('looper')
    
    def test_list(self):
        event = Event(0)
        event.the_list = range(10)
        cfg_ana = cfg.Analyzer(
            Filter,
            output = 'filtered',
            input_objects = 'the_list',
            filter_func = lambda x : x%2 == 0
            )
        cfg_comp = cfg.Component(
            'test',
            files = []
            )
        filter = Filter(cfg_ana, cfg_comp, 'looper')
        filter.process(event)
        self.assertItemsEqual(event.filtered, [0,2,4,6,8])
    
    def test_dict(self):
        event = Event(0)
        event.the_dict = dict( [ (x, x**2) for x in range(10) ] )
        cfg_ana = cfg.Analyzer(
            Filter,
            output = 'filtered',
            input_objects = 'the_dict',
            filter_func = lambda x : x == 9
            )
        cfg_comp = cfg.Component(
            'test',
            files = []
            )
        filter = Filter(cfg_ana, cfg_comp, 'looper')
        filter.process(event)
        self.assertDictEqual(event.filtered, {3:9})
        
if __name__ == '__main__':
    unittest.main()
