# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from sulsj9230ContigFilter.sulsj9230ContigFilterImpl import sulsj9230ContigFilter
from sulsj9230ContigFilter.sulsj9230ContigFilterServer import MethodContext
from sulsj9230ContigFilter.authclient import KBaseAuth as _KBaseAuth


class sulsj9230ContigFilterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('sulsj9230ContigFilter'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'sulsj9230ContigFilter',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = sulsj9230ContigFilter(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_sulsj9230ContigFilter_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    
    # def test_your_method(self):
    #     # Prepare test objects in workspace if needed using
    #     # self.getWsClient().save_objects({'workspace': self.getWsName(),
    #     #                                  'objects': []})
    #     #
    #     # Run your method by
    #     # ret = self.getImpl().your_method(self.getContext(), parameters...)
    #     #
    #     # Check returned data with
    #     # self.assertEqual(ret[...], ...) or other unittest methods
    #     pass
    
    def test_filter_contigs(self):
        ref = "79/16/1"
        result = self.getImpl().filter_contigs(self.getContext(), {
            'workspace_name': self.getWsName(),
            'assembly_ref': ref,
            'min_length': 100
        })
        print result
        # TODO -- assert some things (later)
        
    def test_invalid_params(self):
        impl = self.getImpl()
        ctx = self.getContext()
        ws = self.getWsName()        
        # Missing assembly ref
        # with self.assertRaises(ValueError):
        #     impl.filter_contigs(ctx, ws, {'min_length': 100})
        # # Missing min length
        # with self.assertRaises(ValueError):
        #     impl.filter_contigs(ctx, ws, {'assembly_ref': 'x'})
        # # Min length is negative
        # with self.assertRaises(ValueError):
        #     impl.filter_contigs(ctx, ws, {'assembly_ref': 'x', 'min_length': -1})
        # # Min length is wrong type
        # with self.assertRaises(ValueError):
        #     impl.filter_contigs(ctx, ws, {'assembly_ref': 'x', 'min_length': 'x'})
        # # Assembly ref is wrong type
        # with self.assertRaises(ValueError):
        #     impl.filter_contigs(ctx, ws, {'assembly_ref': 1, 'min_length': 1})
        # with self.assertRaises(ValueError):
        #     impl.filter_contigs(ctx, {
        #         'workspace_name': ws,
        #         'assembly_ref': "79/16/1",
        #         'min_length': 1
        #     })
    
    
    def test_filter_contigs(self):
        ref = "79/16/1"
        params = {
            'workspace_name': self.getWsName(),
            'assembly_ref': ref,
            'min_length': 200000
        }
        # result = self.getImpl().filter_contigs(self.getContext(), self.getWsName(), params)
        result = self.getImpl().filter_contigs(self.getContext(), params)
        pprint(result)
                
        self.assertEqual(result[0]['n_total'], 2)
        self.assertEqual(result[0]['n_remaining'], 1)
        
        self.assertTrue(len(result[0]['filtered_assembly_ref']))
        self.assertTrue(len(result[0]['report_name']))
        self.assertTrue(len(result[0]['report_ref']))
    
    

