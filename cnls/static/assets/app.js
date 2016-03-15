/*eslint-globals L*/
/*eslint-env browser*/

'use strict';

//////////
// à enlever en production
//////////
function printObject(obj)
{
    if(obj==null)
    {
        alert("obj==null");
        return;
    }
    Object.getOwnPropertyNames(obj).forEach(function(val, idx, array)
    {
        alert(val + " -> " + obj[val]);
    });
}
//////////
//variables
//////////
var regionsGeoJson;
var regionsShapes;

var map, popupTpl, modalTpl, regionsListContainer, regionListItemTpl, datePickerItemTpl, datePickerStatusTpl, datePickerContainers;
var markerClusters, geojsonLayer;

var ilayers = [];


//////////
// filterFunctions
//////////
var filterFunctions = {
    checkboxes: function(filter, feature) {
        var featureFilters = filter.values;
        
        if (filter.field == 'echelle') {
            for (var k in featureFilters) {
                echelle = featureFilters[k]; // toStr?
                if (typeof feature.properties[echelle] !== 'undefined') {
                    return true ;
                }
            }
            return false;
        } else {
            var featureFiltered = feature.properties[filter.field];
            for (var k in featureFilters) {
                for (var l in featureFiltered) {
                    if (featureFilters[k] == featureFiltered[l]) {
                        return true ;
                    }
                }
            }
        }
        return false ;
    },
    date: function(filter, feature) {
//        console.log(filter)
//        var featureFilteredStart = feature.properties[filter.field_start];
        var featureFilteredStart = feature.properties.date_debut;
//        var featureFilteredEnd = feature.properties[filter.field_end];
        var featureFilteredEnd = feature.properties.date_fin;
        var featureFiltersStart = filter.start;
        var featureFiltersEnd = filter.end;
        if (typeof featureFilteredStart === 'undefined' || typeof featureFilteredEnd === 'undefined') {
            return true ;
        }
        // affiche toutes les actions qui se déroulent même en partie sur la période choisie
        var borne1 = !moment(featureFilteredStart, filter.format).isAfter(moment(featureFiltersEnd, filter.format), 'month');
        var borne2 = !moment(featureFiltersStart, filter.format).isAfter(moment(featureFilteredEnd, filter.format), 'month');
        return borne1 && borne2;
//        var isAfterStart = !featureFilteredStart || moment(featureFilteredStart, filter.format).isAfter( moment(featureFiltersStart, filter.format) );
//        var isBeforeEnd = !featureFilteredEnd || moment(featureFilteredEnd, filter.format).isBefore( moment(featureFiltersEnd, filter.format) );
//        return isAfterStart && isBeforeEnd;
    },
}

//////////
// buildFeatures()
//////////
//function buildFeatures(data) {
    function colorMarkers(cluster) {
/*        var markers = cluster.getAllChildMarkers();
        var color = 'marker-cluster-small-';
//        printObject(feature);
        if (typeof markers[0].fokontany !== 'undefined') { 
            color += 'brown';
            nextMarker('fokontany');
        } else if (typeof markers[0].region !== 'undefined') {
            color += 'green';
            nextMarker('region');
        } else if (typeof markers[0].commune !== 'undefined') {
            color += 'purple';
            nextMarker('commune');
        } else if (typeof markers[0].pays !== 'undefined') {
            color += 'blue';
            nextMarker('pays');
        } else {
            color += 'grey';
//            alert('aucune echelle trouvée ?')
        }
        var html = '<div><span>' + cluster.getChildCount() + '</span></div>'
        return new L.divIcon({ html: html, className: color, iconSize: new L.point(40, 40) });
*/
        return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'marker-cluster marker-cluster-small-brown', iconSize: new L.Point(40, 40) });
/*
        function nextMarker(echelle) {
            for (var i = 1; i < markers.length; i++) {
                if (typeof markers[i].echelle !== 'undefined') {
                    color = 'marker-cluster-small-grey'
                    return color
                } else {
                    pass
                }
            }
        }*/
    }
//}

//////////
// filterMarkers()
//////////
function filterMarkers(filters) {
    ilayers.forEach(function(ilayer) {
        // flag feature for show/hide in later renderMarkers
        ilayer.show = filters.every(function(filter) {
            return filterFunctions[filter.type](filter, ilayer.feature);
        })
        if (ilayer.show) {
//        alert('ilayer.show = true');
            markerClusters.addLayer(ilayer);
        } else {
//                alert('ilayer.show = false');
            markerClusters.removeLayer(ilayer);
        }
    })
}

//////////
// updateFilters()
//////////
function updateFilters(newDate) {
    function updateCheckboxList(name) {
        var values = _.map( $('#' + name + ' input'), function(el) {return el.checked; });
//        $('[data-countof=' + name + ']').text( _.contains(values, false) ? _.compact(values).length + '/' + values.length : 'toutes' );
    }
    updateCheckboxList('actionType');
    updateCheckboxList('population');
    updateCheckboxList('echelle');

    if (newDate) {
        newDate.parents('.dropdown-menu').data('date', newDate.data().date);
        newDate.parents('.dropdown-menu').data('dateFormatted', newDate.html());
    }

    $('.js-filter-dates-start-month .js-lbl').html( datePickerContainers.startMonth.data('dateFormatted') )
    $('.js-filter-dates-start-year .js-lbl').html( datePickerContainers.startYear.data('dateFormatted') )
    $('.js-filter-dates-end-month .js-lbl').html( datePickerContainers.endMonth.data('dateFormatted') )
    $('.js-filter-dates-end-year .js-lbl').html( datePickerContainers.endYear.data('dateFormatted') )

    $('.js-filter-dates-status').html(datePickerStatusTpl({
        startMonth: moment.monthsShort()[datePickerContainers.startMonth.data('date')],
        endMonth: moment.monthsShort()[datePickerContainers.endMonth.data('date')],
        startYear: datePickerContainers.startYear.data('date'),
        endYear: datePickerContainers.endYear.data('date')
    }));
}

//////////
// getFilters()
//////////
function getFilters() {
    // build a list of filters activated in the panels
    var filters = [];
    var filterCheckboxes = $('.js-filter-checkboxes');
    filterCheckboxes.each(function(index, el) {
        var field = $(el).data().filterCheckboxesField;
        var filter = {
            type: 'checkboxes',
            field: field,
            values: []
        }
        $(el).find('input').each(function(inputIndex, inputEl) {
            if ($(inputEl).is(':checked')) {
                filter.values.push($(inputEl).data().filterCheckboxValue);
            }
        })
        filters.push(filter);
        
    });

    var dateFormat = $('.js-filter-dates').data().filterDatesFormat;
    var dateFilter = {
        type: 'date',
        field_start: $('.js-filter-dates').data().filterDatesFieldStart,
        field_end: $('.js-filter-dates').data().filterDatesFieldEnd,
        format: dateFormat,
        start: moment({
            month:  datePickerContainers.startMonth.data('date'),
            year:  datePickerContainers.startYear.data('date')
        }).format(dateFormat),
        end: moment({
            month:  datePickerContainers.endMonth.data('date'),
            year:  datePickerContainers.endYear.data('date')
        }).format(dateFormat)
    }
    filters.push(dateFilter);

    return filters;
}

//////////
// initRegionsListEvents()
//////////
function initRegionsListEvents() {
    regionsListContainer.find('a').on('click', function (e) {
        var latlonStr = $(e.currentTarget).data('latlon');
        var latlon = latlonStr.split(',');

        //shift a bit to the west to compensate space taken by right controls
        //TODO : only desktop
        latlon[1] = parseFloat(latlon[1]) + 1;
        map.setView(latlon, 7);

        if (regionsShapes) {
            map.removeLayer(regionsShapes);
        }

        regionsShapes = L.geoJson(regionsGeoJson, {
            filter: function(feature) {
                return feature.properties.NAME_2 === $(this).html();
            }.bind(this)
        }).addTo(map);
    });
}

function initRegionsListEvents2(selection) {
    var latlonStr = selection.value;
    var latlon = latlonStr.split(',');
    latlon[1] = parseFloat(latlon[1]) + 1;
    map.setView(latlon, 7);

    if (regionsShapes) {
        map.removeLayer(regionsShapes);
    }

    regionsShapes = L.geoJson(regionsGeoJson, {
        filter: function(feature) {
            return feature.properties.NAME_2 === selection.text;
        }.bind(this)
    }).addTo(map);

}

//////////
// initDatePicker()
//////////
function initDatePicker() {
    datePickerContainers = {
        startMonth: $('.js-filter-dates-start-month .dropdown-menu'),
        startYear: $('.js-filter-dates-start-year .dropdown-menu'),
        endMonth: $('.js-filter-dates-end-month .dropdown-menu'),
        endYear: $('.js-filter-dates-end-year .dropdown-menu')
    }

    var initialDate = moment('2010-01-01');
    var today = moment();
    var current = initialDate.clone();

    moment.months().forEach(function(month, index) {
        var d = {
            dateFormatted: month,
            date: index
        };
        datePickerContainers.startMonth.append(datePickerItemTpl(d));
        datePickerContainers.endMonth.append(datePickerItemTpl(d));

        if (index === initialDate.month()) datePickerContainers.startMonth.data(d);
        if (index === today.month()) datePickerContainers.endMonth.data(d);
    });

    while(current.isBefore(today)) {
        var d = {
            dateFormatted: current.year(),
            date: current.year()
        };
        datePickerContainers.startYear.append(datePickerItemTpl(d));
        datePickerContainers.endYear.append(datePickerItemTpl(d));

        if (current.year() === initialDate.year()) datePickerContainers.startYear.data(d);
        if (current.year() === today.year()) datePickerContainers.endYear.data(d);

        current.add(1, 'years');
    }
}

//////////
// openModal()
//////////
// TODO transformer en un nouvel onglet avec url partageable
//function openModal(link) {
//    var index = $(link).parents('.js-popup').data().index;
//    var data = features[index].properties;
//    var modalDom = modalTpl({data: data});
//
//    $(modalDom).modal();
//}

/////////////////////////////////////////////////////////////

//////////
// init()
//////////
function init() {
    map = L.map('map', {
        center: [-18.766947, 49],
        zoom: 6,
        minZoom: 4,
        maxZoom: 10
    });
    // TODO check tile server's terms of use
    L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {attribution: "Tiles courtesy of <a href='http://www.mapquest.com/'>MapQuest</a>, &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='http://www.opendatacommons.org/licenses/odbl'>ODbL</a>"} ).addTo(map);


    popupTpl = _.template( $('.js-tpl-popup').html() );
//    modalTpl = _.template( $('.js-tpl-modal').html() );

    regionsListContainer = $('.js-regions');
//    regionListItemTpl = _.template('<li><a href="#" data-latlon="<%= center %>"><%= name %></a></li>');
    regionListItemTpl = _.template('<option value="<%= center %>"><%= name %></option>');
    datePickerItemTpl = _.template('<li><a href="#" data-date="<%= date %>"><%= dateFormatted %></a></li>');
    datePickerStatusTpl = _.template('<%= startMonth %> <%= startYear %> → <%= endMonth %> <%= endYear %>');

    moment.locale(window.appConfig.locale);
    if ($('.js-filter-dates').length) initDatePicker();

    // initialize filters count without actually filtering (geoJSON no there yet)
    updateFilters();

    //move that to a sass loop later :)
//    _.each($('#actionType .checkboxList input'), function(el, index) {
//        $('<span class="icon"></span>').insertBefore(el).css('background-position', '-' + index * 30 + 'px' + ' 0');
//    });

//    _.each($('#population .checkboxList input'), function(el, index) {
//          $('<span class="icon"></span>').insertBefore(el).css('background-position', '-' + index * 30 + 'px' + ' 0');
//    });

    $('.js-showfilters').on('click', function () {
        $('.js-filters').addClass('opened');
    });

    $('.js-closeFilters').on('click', function() {
        $('.js-filters').removeClass('opened');
    });

    $('.js-filter-checkboxes input').on('change', function () {
        updateFilters();
        filterMarkers(getFilters());
    });

    $('.js-filter-dates li').on('click', function(e) {
        updateFilters($(e.target));
        filterMarkers(getFilters());
    })

//    $.ajax(window.appConfig.testDataPath).done( buildFeatures );
//    buildFeatures(toutesActions);
    markerClusters = L.markerClusterGroup({
        showCoverageOnHover: false,
        maxClusterRadius: 40,
        spiderfyDistanceMultiplier: 2,
        singleMarkerMode: true,
        zoomToBoundsOnClick: false,
//        iconCreateFunction: colorMarkers,
    });
    markerClusters.on('clusterclick', function (a) {
 //       map.zoomIn(); // TODO pourquoi referme le cluster avant la fin du chargement du nouveau niveau de zoom ?
        a.layer.spiderfy();
    });
    
    geojsonLayer = L.geoJson(toutesActions, {
        onEachFeature: function (feature, layer) {
            var popupData = feature.properties;
            var popup = L.popup().setContent( popupTpl( {data: popupData, internalIndex: ilayers.length }) );
            layer.bindPopup(popup);
//            feature.layer = layer;
            layer.show = true;
//            features.push(feature);
            markerClusters.addLayer(layer);
        }
    });
    ilayers = geojsonLayer.getLayers();
//    alert(actionsTananarive);
    map.addLayer(markerClusters);
       
    $.getJSON( window.appConfig.faritraGeoJsonPath, function(geojson) {
        regionsGeoJson = geojson;
        // regionsShapes défini deux fois ??
        regionsShapes = L.geoJson(geojson, {
            onEachFeature: function(feature, layer) {
                var center = layer.getBounds().getCenter();
                var regionListItem = regionListItemTpl({
                    name: feature.properties.NAME_2,
                    center: center.lat + ',' + center.lng
                });
                $(regionListItem).appendTo(regionsListContainer);
            }
        });

//        initRegionsListEvents(); besoin de l'appeler ici ??
    } );

    $('#map').on('click', '.js-openContentModal', function(e) {
        e.preventDefault();
        openModal(e.target);
    });

}