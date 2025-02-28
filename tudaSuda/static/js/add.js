ymaps3.import.registerCdn('https://cdn.jsdelivr.net/npm/{package}', '@yandex/ymaps3-default-ui-theme@latest');
const pkg = await ymaps3.import('@yandex/ymaps3-default-ui-theme');
const { YMapGeolocationControl} = pkg;
initMap();


async function initMap() {
    await ymaps3.ready;
    const {YMap, YMapDefaultSchemeLayer, YMapControls} = ymaps3;
    const map = new YMap(
        document.getElementById('map'),
        {
            location: {
                center: [37.588144, 55.733842],
                zoom: 6
            }
        }
    );


    const clickHandler = (event) => {
            // Выводим координаты в консоль
            console.log('Координаты клика:', event);
    };



    YMap.events.add(['click'], (event) => {
        let eCoords = event.get('coords');
        console.log(eCoords)
});
    const controls = new YMapControls({position: 'top left', orientation: 'vertical'});
    controls.addChild(new YMapGeolocationControl());
    map.addChild(controls);
    map.addChild(mapListener);
}