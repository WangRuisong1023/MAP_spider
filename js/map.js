var map;
var result = true;
var marklist = [];
window.onload = function () {
    mapCreat();

    createMap();

    document.querySelector('#trans-map').onclick = transMap;
    map.add(marklist);
    
   
    
}
//2D地图
function mapCreat() {
    map = new AMap.Map('container', {
        resizeEnable: true, //是否监控地图容器尺寸变化
        zoom: 11, //初始化地图层级
        center: [116.397428, 39.90923] //初始化地图中心点
    });
}

//3D地图
function mapInit() {
    map = new AMap.Map('container', {
        viewMode: '3D',
        defaultCursor: 'pointer',
        expandZoomRange: true,
        zooms: [3, 20],
        pitch: 50,
        zoom: 11,
        center: [116.320492,39.927071],
        buildingAnimation: true, //楼块出现是否带动画
    });
}

//2-3
function transMap() {
    destroyMap();
    if (result) {
        mapInit();
    } else {
        map = new AMap.Map('container');
    }
    result = !result;
    createMap();

    map.add(marklist);

}

//销毁地图
function destroyMap() {
    map && map.destroy();
    log.info("地图已销毁");
}

//初始化地图
function createMap() {
    //提示地图加载
    map.on("complete", function () {
        log.success("地图加载完成！");
    });
    //绑定地图移动与缩放事件
    map.on('moveend', logMapinfo);
    map.on('zoomend', logMapinfo);
    //为地图注册click事件获取鼠标点击出的经纬度坐标
    map.on('click', function (e) {
        document.getElementById("lnglat").value = e.lnglat.getLng() + ',' + e.lnglat.getLat();
        addMark(e.lnglat.lng, e.lnglat.lat);
    });
    //绑定查询、回车查询事件
    document.querySelector('#query').onclick = gotoCity;
    document.querySelector('#city-name').onkeydown = function (e) {
        if (e.keyCode === 13) {
            gotoCity();
            return false;
        }
        return true;
    };
}

//显示地图层级与中心点信息
function logMapinfo() {
    var zoom = map.getZoom(); //获取当前地图级别
    var center = map.getCenter(); //获取当前地图中心位置

    document.querySelector("#map-zoom").innerText = zoom;
    document.querySelector("#map-center").innerText = center.toString();
}
//根据cityname、adcode、citycode设置地图位置
function gotoCity() {
    var val = document.querySelector('#city-name').value; //可以是cityname、adcode、citycode
    if (!val) {
        val = "北京市";
    }

    map.setCity(val);
    log.info(`已跳转至${val}`);
}
//添加地图选点
function addMark(lng, lat) {
    console.log(lng + "|||||" + typeof lng);
    console.log(lat + "|||||" + typeof lat);
    var position = new AMap.LngLat(lng, lat); //标准写法
    // 构造点标记
    var marker = new AMap.Marker({
        icon: "https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
        position: position
    });
    map.add(marker);
}

//回调
function train(data) {
    var marker = null;
    var length = data.length;
    for (var i = 0; i < length; i++) {
        var position = new AMap.LngLat(data[i].lng, data[i].lat);
        var title = data[i].title;
        marker = new AMap.Marker({
            position: position,
            title: title,
            icon: "https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png"
        });
        marklist.push(marker);
    }
    
}

