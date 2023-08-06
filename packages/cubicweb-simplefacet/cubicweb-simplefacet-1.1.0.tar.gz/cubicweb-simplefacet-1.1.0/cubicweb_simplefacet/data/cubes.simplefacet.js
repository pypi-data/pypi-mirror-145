$.format = function(str, sub) { // found on stackoverflow, use http://archive.plugins.jquery.com/node/14683/release ? or http://code.google.com/p/jquery-utils/wiki/StringF#Formatting
    return str.replace(/\{(.+?)\}/g, function($0, $1) {
        return $1 in sub ? sub[$1] : $0;
    });
}

cw.cubes.simplefacet = new Namespace('cw.cubes.simplefacet');

$.extend(cw.cubes.simplefacet, {
  finalizeRangeFacet: function($form, facetid) {
    var $mininput = $form.find('#' + facetid + '-fromdate'),
        $maxinput = $form.find('#' + facetid + '-todate');
        $mininput.removeClass('error');
        $maxinput.removeClass('error');
        var minvalue = $mininput.val().strip(),
            maxvalue = $maxinput.val().strip(),
            title='',
            value = minvalue + '-' + maxvalue;

       var errors = false;
       if (isNaN(parseInt(minvalue)) && minvalue.length){
            errors = true;
           $mininput.addClass('error');
        };
       if (isNaN(parseInt(maxvalue)) && maxvalue.length){
            $maxinput.addClass('error');
            errors = true;
        };
       if (errors){  return false; };

       if (minvalue && maxvalue) {
             title = 'Entre ' + minvalue + ' et ' + maxvalue;
        } else {
            if (minvalue) {
                title = 'Apres ' + minvalue;
            } else if (maxvalue) {
                title = 'Avant ' + maxvalue;
            }
        }
        $form.append($($.format('<input type="hidden" name="_facet" value="{facetid}:{value}" />',
                                {facetid: facetid,
                                 value: value
                                 })));
        return true;
    },

    finalizeFtiSearch: function($form, facetid) {
        var text = $form.find('input:text').val(); // only 1 input
        if (text.length){
          $form.append($($.format('<input type="hidden" name="_facet" value="{facetid}:{value}" />',
                                {facetid: facetid,
                                 value: text
                                 })));
        };
        return true;
    }

 });

function initFacetBoxEvents(root) {
    // override default behaviour: simply don't do anything
}
