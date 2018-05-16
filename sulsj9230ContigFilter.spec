/*
A KBase module: sulsj9230ContigFilter
*/

module sulsj9230ContigFilter {
    /*
        Insert your typespec information here.
    */

    /* Input parameter types */
    typedef structure {
        string workspace_name;
        string assembly_ref;
        int min_length;
    } ContigFilterParams;
    
    /* Output result types */
    typedef structure {
    } ContigFilterResults;
    
    /* Main method */
    funcdef filter_contigs(ContigFilterParams params)
        returns (ContigFilterResults) authentication required;
};
