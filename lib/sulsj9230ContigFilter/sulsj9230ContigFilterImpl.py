# -*- coding: utf-8 -*-
#BEGIN_HEADER
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
    GIT_COMMIT_HASH = "0373e44d4a4f12aa24b5d1d18f7bcf5ba0f0d3a1"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
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
