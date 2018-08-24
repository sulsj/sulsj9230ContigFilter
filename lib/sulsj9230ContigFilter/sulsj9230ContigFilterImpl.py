# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import pprint
from Bio import SeqIO

from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from KBaseReport.KBaseReportClient import KBaseReport
from BBTools.BBToolsClient import BBTools
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
    GIT_COMMIT_HASH = "5387b551ccfd108aa28f7d0896b77ebe3f5d571e"

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
           types) -> structure: parameter "report_name" of String, parameter
           "report_ref" of String, parameter "filtered_assembly_ref" of
           String, parameter "n_total" of Long, parameter "n_remaining" of
           Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN filter_contigs
        for name in ['min_length', 'assembly_ref', 'workspace_name']:
            if name not in params:
                raise ValueError('Parameter "' + name + '" is required but missing')
        if not isinstance(params['min_length'], int) or (params['min_length'] < 0):
            raise ValueError('Min length must be a non-negative integer')
        if not isinstance(params['assembly_ref'], basestring) or not len(params['assembly_ref']):
            raise ValueError('Pass in a valid assembly reference string')

        print("params['min_length']=%s, params['assembly_ref']=%s" % (params['min_length'], params['assembly_ref']))
        print("params['params['workspace_name']=%s" % (params['workspace_name']))
        print("self.callback_url=%s" % self.callback_url)
        print("self.scratch=%s" % self.scratch)
        print "config = "
        pprint.pprint(self.config)

        ###############
        # Download ref
        ##############
        assembly_util = AssemblyUtil(self.callback_url)
        file = assembly_util.get_assembly_as_fasta({'ref': params['assembly_ref']})
        print "assembly fasta file = "
        pprint.pprint(file)

        ###################################
        # Real business - filter the contig
        ###################################
        parsed_assembly = SeqIO.parse(file['path'], 'fasta')
        min_length = params['min_length']
        # Keep a list of contigs greater than min_length
        good_contigs = []
        # total contigs regardless of length
        n_total = 0
        # total contigs over the min_length
        n_remaining = 0
        for record in parsed_assembly:
            n_total += 1
            if len(record.seq) >= min_length:
                good_contigs.append(record)
                n_remaining += 1

        # returnVal = {
        #     'n_total': n_total,
        #     'n_remaining': n_remaining
        # }

        # returnVal = {}

        ##################
        # Output
        ##################
        workspace_name = params['workspace_name']
        filtered_path = os.path.join(self.scratch, 'filtered.fasta')
        SeqIO.write(good_contigs, filtered_path, 'fasta')
        # Upload the filtered data to the workspace
        new_ref = assembly_util.save_assembly_from_fasta({
            'file': {
                'path': filtered_path
            },
            'workspace_name': workspace_name,
            'assembly_name': file['assembly_name']
        })

        # returnVal = {
        #     'n_total': n_total,
        #     'n_remaining': n_remaining,
        #     'filtered_assembly_ref': new_ref
        # }


        ################
        # Reporting
        ################
        text_message = "".join([
            'Filtered assembly to ', str(n_remaining),
            's contigs out of ', str(n_total)
        ])
        # Data for creating the report, referencing the assembly we uploaded
        report_data = {
            'objects_created': [
                {'ref': new_ref, 'description': 'Filtered contigs'}
            ],
            'text_message': text_message
        }
        # Initialize the report
        kbase_report = KBaseReport(self.callback_url)
        report = kbase_report.create({
            'report': report_data,
            'workspace_name': workspace_name
        })
        # Return the report reference and name in our results
        returnVal = {
            'report_ref': report['ref'],
            'report_name': report['name'],
            'n_total': n_total,
            'n_remaining': n_remaining,
            'filtered_assembly_ref': new_ref
        }

        ###############
        # BBtools test
        ###############
        # bbtools = BBTools(self.callback_url)
        bbtools = BBTools(self.callback_url, service_ver='beta')

        # set up input files
        print "file['path'] = "
        print file['path']
        # print new_ref['filtered_assembly_ref']
        rqc_filter_input = {
            "reads_file": file['path'] # /kb/module/work/tmp/Shewanella_oneidensis_MR-1_assembly.fa
        }
        # or, if you want to use a KBase Workspace UPA for your reads object:
        # rqc_filter_input = {
        #     "reads_library_ref": new_ref['filtered_assembly_ref']
        # }

        # set up parameters (example below, there are many more options, see BBTools.spec)
        rqc_filter_params = {
            "qtrim": "rl",
            "maxns": 3,
            "minlength": 40
        }
        #"maxmem": 5

        # run the local RQCFilter function
        result = bbtools.run_RQCFilter_local(rqc_filter_input, rqc_filter_params)
        print "result = "
        pprint.pprint(result)
        #END filter_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method filter_contigs return value returnVal is not type dict as required.')

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

