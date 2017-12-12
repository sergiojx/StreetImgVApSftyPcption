var mongoose = require('mongoose');
var _ = require('underscore');

  /*
	Stablish data base connection. Optain image mongoose model, and
	this used to clean db.image. Once this is done, db.image collection
	is popullated with image information retrived from -/imagebank/- directory.
	This derectoty holds a collection of images grouped by longitud named
	directories.

  */

  var arrayOfImgDirs = [];
  mongoose.connect('mongodb://localhost:27017/test');
  var Image = mongoose.model('Image', require('./image'), 'image');


  Image.remove({}, function(err){
	   if (err)
	    {
		      return console.error(err);
	    }

      console.log("iamages  has been removed");
	    var fs = require('fs');
	    fs.readdir('./imagebank', function(err, files) {
	       if (err) return;
	       files.forEach(function(f, idx, array) {
		         //popullate array of image directories
		         arrayOfImgDirs.push(f);
		         if (idx === array.length - 1)
		         {
			            console.log("popullate array of image directories DONE");
			            _.each(arrayOfImgDirs, function(dirname){
				                var imgSetPath = './imagebank/' + dirname + '/' + dirname + '.js';
				                fs.readFile(imgSetPath, 'utf8', onFileReadClosure(dirname));
			            });
			       }
		     });
	   });
  	//fs.readFile('./logitud74_012712n/test.js', 'utf8', onFileRead);
  });




function onFileReadClosure(path) {
	return function(err, data){
		  if (err) throw err;
		  var jstr = data.split("=");
		  var jsonTxt = JSON.parse(jstr[1]);
		  //console.log(jsonTxt);
		  var entrySize = jsonTxt.length;
		  var entrySizeCtr = 0;
		  console.log("Amount of entries " + jsonTxt.length);
		  _.each(jsonTxt, function(image){
			//console.log(image.name);
			imageObj = new Object()
			imageObj.name = image.name;
			imageObj.lat = image.lat;
			imageObj.logt = image.log;
			imageObj.path = '/' + path + '/' + image.name;
			imageObj.loc = path;
			entry = new Image(imageObj);
			//console.log(imageObj)
			entry.save(function (err, entry) {
				if (err)
				{
					return console.error(err);
				}
				entrySizeCtr = entrySizeCtr + 1;
				if(entrySizeCtr >= entrySize)
				{
					Image.find({ loc: path }, function(err, collection){
						if (err)
						{
							return console.error(err);
						}
						console.log(collection)
					});
				}

			});

		  });
	}
}
function onFileRead(err, data) {
  if (err) throw err;
  var jstr = data.split("=");
  var jsonTxt = JSON.parse(jstr[1]);
  //console.log(jsonTxt);
  var entrySize = jsonTxt.length;
  var entrySizeCtr = 0;
  console.log("Amount of entries " + jsonTxt.length);
  _.each(jsonTxt, function(image){
	//console.log(image.name);
	imageObj = new Object()
	imageObj.name = image.name;
        imageObj.lat = image.lat;
        imageObj.logt = image.log;
        imageObj.path = "/home";
	imageObj.loc = 10;
	entry = new Image(imageObj);
	//console.log(imageObj)
	entry.save(function (err, entry) {
		if (err)
		{
			return console.error(err);
		}
		entrySizeCtr = entrySizeCtr + 1;
		if(entrySizeCtr >= entrySize)
		{
			Image.find({ loc: 10 }, function(err, collection){
				if (err)
				{
					return console.error(err);
				}
				console.log(collection)
			});
		}

	});

  });


}
