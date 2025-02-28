ymaps3.import.registerCdn('https://cdn.jsdelivr.net/npm/{package}', '@yandex/ymaps3-default-ui-theme@latest');

const SEARCH_PARAMS = [
  {text: 'сады и парки', iconName: 'park'},
  {text: 'церкви', iconName: 'catholic_church'},
  {text: 'музеи', iconName: 'museum'},
  {text: 'зоопарки', iconName: 'zoo'},
  {text: 'монументы и мемориалы', iconName: 'monument'},
  {text: 'историческая архитектура', iconName: 'building'},
  {text: 'смотровые площадки', iconName: 'viewpoint'},
  {text: 'мечети', iconName: 'mosque'},
  {text: 'театры', iconName: 'theatre'},
  {text: 'исторические объекты', iconName: 'memorable_event'}
];

let points = []


document.getElementById('map1').addEventListener("click", пetDirections);


initMap();
        
        async function initMap() {
            await ymaps3.ready;

            await ymaps3.ready;
            const {YMapDefaultMarker, YMapGeolocationControl} = await ymaps3.import('@yandex/ymaps3-default-ui-theme');
            const {YMap, YMapDefaultSchemeLayer, YMapControls, YMapListener, YMapDefaultFeaturesLayer} = ymaps3;

            const handleMapClick = async (object, event) => {
                addMarker(event.coordinates);
                points.push(event.coordinates)
                /*const places = await getNearbyPlaces(event.coordinates, map.bounds)*/
            };

            /*
            const getNearbyPlaces = async (coordinates, bounds) => {
                const searchPromises = SEARCH_PARAMS.map(parameter => ymaps3.search({text: parameter.text, bounds}));
                const destinations = searchPromises.map(destination => destination.geometry.coordinates);
                destinations.forEach(destination => addMinMarker(destination.geometry.coordinates));
            };*/


            const addMinMarker = (coordinates) => {
                console.log(YMapDefaultMarker)
                let marker = new YMapDefaultMarker({
                    coordinates,
                    size: 'small',
                    iconName: 'fallback'
                });
                map.addChild(marker); // Add the marker to the map
            };  

            const addMarker = (coordinates) => {
                let marker = new YMapDefaultMarker({
                    coordinates,
                    size: 'normal',
                    iconName: 'fallback'
                });
                map.addChild(marker); // Add the marker to the map
            };  
            const map = new YMap(
                document.getElementById('map'),
                {
                    location: {
                        center: [37.588144, 55.733842],
                        zoom: 6
                    }, mode: 'vector'
                },
                [
                    new YMapDefaultSchemeLayer(),
                new YMapDefaultFeaturesLayer(), // Add a layer for geo objects
                new YMapListener({
                onClick: handleMapClick // Set the click event handler for the map
                })
                ]
            );

            const controls = new YMapControls({position: 'top left', orientation: 'vertical'});
            controls.addChild(new YMapGeolocationControl());


            map.addChild(controls);
        }

function пetDirections() {
    let listGPX = []
    let counter = 0
    for (var i = points.length - 1; i >= 0; i--) {
        listGPX.push({
            "waypoint_id": i,
            "point": {
                "lat": points[i][0],
                "lon": points[i][1]
            }
        })
    }
    let date = {
        "agents": [
            {
                "agent_id": 0,
                "start_waypoint_id": 0
            }
        ],
        "waypoints": listGPX,
        "routing_options": {
        "type": "shortest"
    }
    };
    const action = document.getElementById("id_GPX")
    action.value = JSON.stringify(date)
    const form = document.getElementById("inputForm")
    form.submit()
    /*
    console.log(date)
    let json = JSON.stringify(date);
    let route = fetch('https://routing.api.2gis.com/logistics/vrp/1.1.0/create?key=a605f23b-4134-4fb9-b948-e9901ebe943b', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: json
        });
    let taskId = route
    console.log(taskId)*/
}

