# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import pprint
#END_HEADER


class sulsj9230ContigFilter:
    '''
    Module Name:
    sulsj9230ContigFilter

    Module Description:
    A KBase module: sulsj9230ContigFilter
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/sulsj/sulsj9230ContigFilter.git"
    GIT_COMMIT_HASH = "3996a30e1f7c2353ebf03aa947c5e69c78e8f621"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        self.config = config
        #END_CONSTRUCTOR
        pass

    def filter_contigs(self, ctx, params):
        """
        Main method
        :param params: instance of type "ContigFilterParams" (Input parameter
           types) -> structure: parameter "workspace_name" of String,
           parameter "assembly_ref" of String, parameter "min_length" of Long
        :returns: instance of type "ContigFilterResults" (Output result
           types) -> structure:
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN filter_contigs
        print("params['min_length']=%s, params['assembly_ref']=%s" % (params['min_length'], params['assembly_ref']))
        print("self.callback_url=%s" % self.callback_url)
        print("self.scratch=%s" % self.scratch)
        pprint.pprint(self.config)
        returnVal = {}
        #END filter_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method filter_contigs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
