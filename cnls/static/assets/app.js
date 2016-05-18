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
                if (feature.properties.classe == featureFilters[k]) {
                    return true ;
                }
            }
            return false;
        } else {
            var featureFiltered = feature.properties[filter.field][0];
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
        var featureFilteredStart = feature.properties.date_debut;
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
// toggle()
//////////
function toggleAll(source, filterName) {
    var filterCheckboxes = $('.js-filter-checkboxes');
    filterCheckboxes.each(function(index, el) {
//    alert($(el).data().filterCheckboxesField +" - "+ filterName);
        if ($(el).data().filterCheckboxesField == filterName) {
            $(el).find('input').each(function(inputIndex, inputEl) {
                $(inputEl).prop('checked', source.checked)
            })
        }
            
    })
 
//    var checkboxes = document.getElementsByName(filterName);
//    for(var i=0 ; i < checkboxes.length; i++) {
//      checkboxes[i].checked = source.checked;
//    }
    updateFilters();
    filterMarkers(getFilters());
}

//////////
// countMarkers()
//////////
function countMarkers() {
    var count = 0;
    markerClusters.eachLayer(function() {
        count++;
    });
    return count;
}

//////////
// exportCSV()
//////////
function exportCSV() {
    if (countMarkers() !== 0) {
        var lien = './actions?' ;
        var checkedFilters = getFilters();
        for (var i in checkedFilters[0].values) {
            lien += 'e=' + checkedFilters[0].values[i] + "&"; 
        }
        for (var i in checkedFilters[1].values) {
            lien += 't=' + checkedFilters[1].values[i] + "&";
        }
        for (var i in checkedFilters[2].values) {
            lien += 'c=' + checkedFilters[2].values[i] + "&";
        }
        var checkedDebut = checkedFilters[3].start.toString();
        lien += 'd=' + checkedDebut + "&";
        var checkedFin = checkedFilters[3].end.toString();
        lien += 'f=' + checkedFin ;
// TODO test        location.href = encodeURIComponent(lien);
        location.href = lien;
    } else {
        alert("Il n'y a pas d'actions à exporter");
    }

}


//////////
// buildFeatures()
//////////
//function buildFeatures(data) {
    function colorMarkers(cluster) {
        return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'marker-cluster marker-cluster-small-green', iconSize: new L.Point(40, 40) });

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
            markerClusters.addLayer(ilayer);
        } else {
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
//              alert($(inputEl).next().text());
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
    L.tileLayer('http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {attribution: "Map data &copy; <a href='https://www.openstreetmap.org/' target='_blank'>OpenStreetMap</a> contributors (<a href='http://www.opendatacommons.org/licenses/odbl' target='_blank'>ODbL</a>).<br/>Tiles by the <a href='https://hotosm.org/ target='_blank''>Humanitarian OSM Team</a> (<a href='https://creativecommons.org/publicdomain/zero/1.0/' target='_blank''>CC0</a>)."} ).addTo(map);


    regionsListContainer = $('.js-regions');
//    regionListItemTpl = _.template('<li><a href="#" data-latlon="<%= center %>"><%= name %></a></li>');
    regionListItemTpl = _.template('<option value="<%= center %>"><%= name %></option>');
    datePickerItemTpl = _.template('<li><a href="#" data-date="<%= date %>"><%= dateFormatted %></a></li>');
    datePickerStatusTpl = _.template('<%= startMonth %> <%= startYear %> → <%= endMonth %> <%= endYear %>');

    moment.locale(window.appConfig.locale);
    if ($('.js-filter-dates').length) initDatePicker();

    // initialize filters count without actually filtering (geoJSON no there yet)
    updateFilters();

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

    $('.js-filter-dates').on('click', function(e) {
        updateFilters($(e.target));
        filterMarkers(getFilters());
    })

    markerClusters = L.markerClusterGroup({
        showCoverageOnHover: false,
        maxClusterRadius: 40,
        spiderfyDistanceMultiplier: 2,
        singleMarkerMode: true,
//        iconCreateFunction: colorMarkers,
    });
    
    geojsonLayer = L.geoJson(toutesActions, {
        onEachFeature: function (feature, layer) {
            var data = feature.properties;
            var html = '';
            html += '<div class="popup-title">'+ data.titre ;
            if (typeof data.avancement !== 'undefined') {
                html += '<span class="label label-default">'+ data.avancement + '</span>'; 
            }
            html += '</div>' ;
            if (data.description !== data.titre) {
                html += '<div class="popup-description">'+ data.description +'</div>';
            }
            html += '<table class="popup-table">';
            html += '<tr><td>ONG sur le terrain</td><td>'+ data.organisme[0];
            if (typeof data.organisme[1] !== 'undefined') {
                html += '<img src='+ data.organisme[1] +' height="50">';
            }
            html += '</td></tr>';
            if (data.bailleur !== null) {
                html += '<tr><td>Bailleur de fonds</td><td>'+ data.bailleur +'</td></tr>';
            }
            if (typeof data.region !== 'undefined') {
                html += '<tr><td>&Eacute;chelle</td><td>pr&eacute;fectorale</td></tr>';                
                html += '<tr><td>Pr&eacute;fecture(s)</td><td>'+ data.region.join(', ') + '</td></tr>';
            } else if (typeof data.fokontany !== 'undefined') {
                html += '<tr><td>&Eacute;chelle</td><td>Tananarive</td></tr>';                
                html += '<tr><td>Fokontany(s)</td><td>'+ data.fokontany.join(', ') + '</td></tr>';
            } else if (typeof data.commune !== 'undefined') {
                html += '<tr><td>&Eacute;chelle</td><td>communale</td></tr>';
                html += '<tr><td>Commune(s)</td><td>'+ data.commune.join(', ') + '</td></tr>';
            } else {
                html += '<tr><td>&Eacute;chelle</td><td>Madagascar</td></tr>';
            }
            if (typeof data.typeintervention[0] !== 'undefined') {
                html += '<tr><td>Type(s) d\'actions</td><td>' + data.typeintervention[0][1];
                for (var i=1; i < data.typeintervention.length; i++) {
                        html += ", "+ data.typeintervention[i][1]; 
                    }
                html += '</td></tr>';
            }
            if (typeof data.cible[0] !== 'undefined') {
                html += '<tr><td>Population(s)</td><td>' + data.cible[0][1];
                for (var i=1; i < data.cible.length; i++) {
                        html += ", "+ data.cible[i][1]; 
                    }
                html += '</td></tr>';
            }
            html += '</table>';
            html += '<div class="popup-link">';
            html += '<a href=\"'+ data.classe +'/'+ data.id +'/'+ data.slug +'\" target="_blank">Ouvrir la fen&ecirc;tre d&eacute;taill&eacute;e (nouvel onglet)</a>';
            html += '</div>';

            layer.show = true;
            layer.on('click', function (e) {
                e.layer.bindPopup(L.popup({maxWidth: Math.min(400, map.getSize().x - 20), maxHeight: map.getSize().y - 20}).setContent(html), {offset: [0, 0]}).openPopup();
            });
            markerClusters.addLayer(layer);
        }
    });
    ilayers = geojsonLayer.getLayers();
    map.addLayer(markerClusters);
  
  // mise à jour des markers dès le chargement du geoJson si des checkboxes sont déjà décochées  
    updateFilters();
    filterMarkers(getFilters());


       
    $.getJSON( window.appConfig.faritraGeoJsonPath, function(geojson) {
        regionsGeoJson = geojson;
        // regionsShapes défini deux fois ?
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