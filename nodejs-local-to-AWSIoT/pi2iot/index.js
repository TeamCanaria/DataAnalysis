var awsIot = require('aws-iot-device-sdk');

//
// Replace the values of '<YourUniqueClientIdentifier>' and '<YourCustomEndpoint>'
// with a unique client identifier and custom host endpoint provided in AWS IoT.
// NOTE: client identifiers must be unique within your AWS account; if a client attempts 
// to connect with a client identifier which is already in use, the existing 
// connection will be terminated.
//
var device = awsIot.device({
   keyPath: './certs/ae9e7302df-private.pem.key',
  certPath: './certs/ae9e7302df-certificate.pem.crt',
    caPath: './certs/root-CA.crt',
  clientId: 'testpi',
      host: 'a1v1jv75i1h0ox.iot.ap-southeast-2.amazonaws.com'
});

//
// Device is an instance returned by mqtt.Client(), see mqtt.js for full
// documentation.
//

device
  .on('connect', function() {
    console.log('connect');
    device.subscribe('client-sub/test-client-1');
    device.publish('client/test-client-1', JSON.stringify(
		{
			message: 'Hello from node JS client'
		}
	));
	console.log('Message sent successfully ...');
  });
  
device
  .on('message', function(topic, payload) {
    console.log('message', topic, payload.toString());
  });

/* Read or write from Serial */
/*
var serialport = require("serialport");
var SerialPort = serialport.SerialPort;

var sp = new SerialPort("/dev/ttyACM0", {
  baudrate: 9600,
  parser: serialport.parsers.readline("\n")
});

function write() //for writing
{
    sp.on('data', function (data) 
    {
        sp.write("Write your data here");
    });
}

function read () // for reading
{
    sp.on('data', function(data)
    {
        console.log(data); 
    });
}

sp.on('open', function() 
{
    // execute your functions
    write(); 
    read(); 
});
*/


/* Append or create JSON to CSV */
/*
var fs = require('fs');
var json2csv = require('json2csv');
var newLine= "\r\n";

var fields = ['Total', 'Name'];

var appendThis = [
    {
        'Total': '100',
        'Name': 'myName1'
    },
    {
        'Total': '200',
        'Name': 'myName2'
    }
];

var toCsv = {
    data: appendThis,
    fields: fields,
    hasCSVColumnTitle: false
};

fs.stat('file.csv', function (err, stat) {
    if (err == null) {
        console.log('File exists');

        //write the actual data and end with newline
        var csv = json2csv(toCsv) + newLine;

        fs.appendFile('file.csv', csv, function (err) {
            if (err) throw err;
            console.log('The "data to append" was appended to file!');
        });
    }
    else {
        //write the headers and newline
        console.log('New file, just writing headers');
        fields= (fields + newLine);

        fs.writeFile('file.csv', fields, function (err, stat) {
            if (err) throw err;
            console.log('file saved');
        });
    }
});
*/
