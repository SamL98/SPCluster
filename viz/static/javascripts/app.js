function fetchGraph() {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            parseGraph(xhr.responseText);
        }
    }

    xhr.open('GET', location.href + '/connections');
    xhr.send();
}

function parseGraph(graphStr) {
    graph = {};

    graphStr.split('\n').forEach((line) => {
        var tids = line.split(',');
        var tid1 = tids[0], tid2 = tids[1];

        if (!graph.hasOwnProperty(tid1)) {
            graph[tid1] = [];
        }

        graph[tid1].push(tid2);
    });

    var checkForWSOpen = setInterval(() => {
        if (ws.readyState != WebSocket.OPEN)
            return;

        clearInterval(checkForWSOpen);
        displayGraph();
    })
}

function displayGraph() {
}

var ws;
var graph = null;
var tracks = {};

function openTrackWebSocket() {
    ws = new WebSocket('ws://' + location.host + '/tracks');

    ws.onopen = (e) => {
        console.log("Web socket opened");
    };

    ws.onmessage = (e) => {
        var trackTerms = e.data.split(":");

        tracks[trackTerms[0]] = {
            title: trackTerms[1],
            artist: trackTerms[2]
        };
    }
}

function requestTrackMetadata(tid) {
    console.log('Requesting md for ' + tid);
    ws.send(tid);
}

window.onload = () => {
    openTrackWebSocket();
    fetchGraph();
}