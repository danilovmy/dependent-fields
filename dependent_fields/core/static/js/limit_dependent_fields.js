'use strict'

function limitDependentFields (obj) {
    // element = dependent field. Dependent on obj
    const elementIds = obj.dataset.dependentFields.split(',');
    elementIds.forEach(elem_id => {
        const elem = document.getElementById(elem_id);
        setQueryString(elem, obj)
    })
};

function setQueryString(elem, obj) {
    if (elem) {
        const limitChoicesTo = JSON.parse(elem.dataset.limitChoicesTo || '{}');
        if (!django.jQuery.isEmptyObject(limitChoicesTo) && limitChoicesTo[obj.name] != obj.value) {
            // set elem empty
            django.jQuery(elem).val(null).trigger('change');
        };
        if (obj.value) {
            limitChoicesTo[obj.name] = obj.value;
        } else {
            if (!django.jQuery.isEmptyObject(limitChoicesTo)) {
                // delete element out of limitCoicesTo - prevent passing empty str
                delete limitChoicesTo[obj.name];
            }
        }
        elem.dataset.limitChoicesTo = JSON.stringify(limitChoicesTo);
        patchUrl(elem)
    }
};

function patchUrl(elem) {
    django.jQuery.each(Object.keys(elem), function (idx, key) {
        if (elem[key].select2) {
            elem[key].select2.dataAdapter.ajaxOptions.url = elem.dataset['ajax-Url'] + ((elem.dataset['ajax-Url'].search('\\?') >= 0) ? '&limit_choices_to=' : '?limit_choices_to=') + encodeURI(elem.dataset.limitChoicesTo);
            return false
        }
    })
}

// addEventListener
// document.addEventListener('DOMContentLoaded', function () {
    // document.querySelectorAll('select[id^="id_productattributes"][id$="attribute"]').forEach(item => item.onchange())
// });
