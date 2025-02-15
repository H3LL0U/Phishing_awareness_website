google.charts.load('current', {packages: ['corechart']});




    
var sent_email_data;
var visit_data;

var total_users; 
var typed;
var visited ;
var not_visited;

var trafic_data;
var email_trafic_data;
async function getDataFromAPI(link) {
    try {
        const response = await fetch(link, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        
        
        
        

        return data;  
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

(async function() {
    visit_data = await getDataFromAPI("/api/visit_data");
    sent_email_data =  await getDataFromAPI("/api/email_data")
    total_users = visit_data["total_users"]; 
    typed = visit_data["typed"]
    visited = visit_data["visited"] - typed;
    not_visited = total_users - (typed + visited);
    trafic_data = visit_data["visit_trafic"]
    email_trafic_data = sent_email_data["email_trafic"]
    
    google.charts.setOnLoadCallback(drawCharts);
})();


    

function drawTraficChart(){


    //chart for user trafic
    var pieDataArray = [['Gebruiker status', 'Aantal gebruikers']];

    // Only add non-zero values to the chart
    if (visited > 0) pieDataArray.push(['Bezocht zonder typen', visited]);
    if (not_visited > 0) pieDataArray.push(['Niet Bezocht', not_visited]);
    if (typed > 0) pieDataArray.push(['Bezocht en begon te typen in het wachtwoord veld', typed]);

    var pieData = google.visualization.arrayToDataTable(pieDataArray);

    var pieOptions = {
        title: '',
        is3D: true,
        sliceVisibilityThreshold: 0
    };

    var pieChart = new google.visualization.PieChart(document.getElementById('pie_chart_visited_users'));
    pieChart.draw(pieData, pieOptions);

    
    window.pieChart = pieChart;
    window.pieData = pieData;
    window.pieOptions = pieOptions;
}
function drawTimeVisitChart(jsonData, idName, unit ) {
    // Example data (replace this with the actual data you want to use)
    var jsonData = jsonData;

    
    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Datum');
    data.addColumn('number', unit);
    data.addColumn({ type: 'string', role: 'tooltip' });

    // Loop through each redirect type in the JSON data
    Object.keys(jsonData).forEach(function(key) {
        // For each redirect type, loop through the date and value pairs
        var dataPoints = jsonData[key];
        var lineData = [];

        Object.keys(dataPoints).forEach(function(date) {
            
            var dateObj = new Date(date);
            
            var value = dataPoints[date];
            
            var tooltip = `Redirect type: ${key}, Date: ${dateObj.toLocaleString()}`;
            
            lineData.push([dateObj, value, tooltip]);
        });

        // Add the data for this line (redirect type) to the Google Charts data table
        data.addRows(lineData);
    });

    // Chart options
    var options = {
        title: '',
        curveType: 'function',
        legend: { position: 'bottom' },
        hAxis: {
            title: 'Datum en tijd',
            format: 'MMM d, HH:00', 
            gridlines: { count: -1 }  
        },
        vAxis: { title: unit },
        tooltip: { isHtml: true, trigger: 'focus' }, // Show custom tooltip
    };

    // Create and draw the chart
    var chart = new google.visualization.LineChart(document.getElementById(idName));
    chart.draw(data, options);
}




function drawCharts() {
    drawTraficChart()
    drawTimeVisitChart(jsonData=trafic_data,idName='time_visit_chart',unit = "Aantal bezocht")
    drawTimeVisitChart(jsonData=email_trafic_data,'email_by_time', unit = "Aantal verstuurde e-mails")
}



window.addEventListener('resize', function () {
    clearTimeout(window.resizedFinished);
    window.resizedFinished = setTimeout(function(){
        google.charts.setOnLoadCallback(drawCharts);
    }, 300); 
});