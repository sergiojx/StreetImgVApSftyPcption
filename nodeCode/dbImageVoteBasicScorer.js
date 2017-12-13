var mongoose = require('mongoose');
var _ = require('underscore');
var distance = require('gps-distance');
var fs = require('fs');
var outputFile = "/home/sergio/webperception/dbpopullation/imageScore.js"
var wholeVoteTxt = ""
var txtLine = "var colorImgScore = [\n"

  var arrayOfImgDirs = [];
  mongoose.connect('mongodb://localhost:27017/test');
  var Image = mongoose.model('Image', require('./image'), 'image');
  var Vote = mongoose.model('Vote', require('./vote'), 'vote');

  var imgStatistics = {};


  Vote.find({}, function(err, votes) {
    if (err) throw err;

    votes.forEach(function(v,i){
        /*
	       Vote statistics
         pv: positive(win) vote count
         pn: negative(lose) vote count
         zv: zero(tie) vote count
         EqsumP: sumatoria of win vote count of images, image being rating got
         a zero(tie) vote with.
         EqsumN:  sumatoria of lose vote count of images, image being rating got
         a zero(tie) vote with.
         EqsumZ:  sumatoria of tie vote count of images, image being rating got
         a zero(tie) vote with.
        */
        if(imgStatistics[v.image0] == undefined){imgStatistics[v.image0] = {'pv':0,'nv':0,'zv':0,'EqsumP':0,'EqsumN':0,'EqsumZ':0};}
        if(imgStatistics[v.image1] == undefined){imgStatistics[v.image1] = {'pv':0,'nv':0,'zv':0,'EqsumP':0,'EqsumN':0,'EqsumZ':0};}
        if(v.vote == 1){
            imgStatistics[v.image0].pv = imgStatistics[v.image0].pv + 1;
            imgStatistics[v.image1].nv = imgStatistics[v.image1].nv + 1;
        }
        else if(v.vote == 2){
            imgStatistics[v.image1].pv = imgStatistics[v.image1].pv + 1;
            imgStatistics[v.image0].nv = imgStatistics[v.image0].nv + 1;
        }
        else {
            imgStatistics[v.image1].zv = imgStatistics[v.image1].zv + 1;
            imgStatistics[v.image0].zv = imgStatistics[v.image0].zv + 1;
        }
    });
    // remaining uncertainty reduction
    for(var jj = 0;jj<2;jj++)
    {
      // Go across the whole vote table in order to update EqsumP, EqsumN and EqsumZ
      votes.forEach(function(v,i){
        if(v.vote == 0){
            imgStatistics[v.image0].EqsumP = imgStatistics[v.image0].EqsumP + imgStatistics[v.image1].pv
            imgStatistics[v.image1].EqsumP = imgStatistics[v.image1].EqsumP + imgStatistics[v.image0].pv
            imgStatistics[v.image0].EqsumN = imgStatistics[v.image0].EqsumN + imgStatistics[v.image1].nv
            imgStatistics[v.image1].EqsumN = imgStatistics[v.image1].EqsumN + imgStatistics[v.image0].nv
            imgStatistics[v.image0].EqsumZ = imgStatistics[v.image0].EqsumZ + imgStatistics[v.image1].zv
            imgStatistics[v.image1].EqsumZ = imgStatistics[v.image1].EqsumZ + imgStatistics[v.image0].zv
          }
      });
      //Update image vote win and lose counts,based on tie vote counts
      for(key in imgStatistics)
      {
        var total = imgStatistics[key].EqsumP + imgStatistics[key].EqsumN + imgStatistics[key].EqsumZ
        if(total > 0)
        {
          imgStatistics[key].EqsumP = imgStatistics[key].EqsumP/total;
          imgStatistics[key].EqsumN = imgStatistics[key].EqsumN/total;
          imgStatistics[key].EqsumZ = imgStatistics[key].EqsumZ/total;
        }
        //tie vote addition
        imgStatistics[key].pv = imgStatistics[key].pv + imgStatistics[key].zv*imgStatistics[key].EqsumP
        imgStatistics[key].nv = imgStatistics[key].nv + imgStatistics[key].zv*imgStatistics[key].EqsumN
        //update remaining uncertainty
        imgStatistics[key].zv = imgStatistics[key].zv*imgStatistics[key].EqsumZ
        //
        imgStatistics[key].EqsumP = 0;
        imgStatistics[key].EqsumN = 0;
        imgStatistics[key].EqsumZ = 0;

      }
    }

    for(key in imgStatistics)
    {
      var total = imgStatistics[key].pv + imgStatistics[key].nv + imgStatistics[key].zv
      imgStatistics[key].pv = (imgStatistics[key].pv/total)*100;
      imgStatistics[key].nv = (imgStatistics[key].nv/total)*100;
      imgStatistics[key].zv = (imgStatistics[key].zv/total)*100;
    }

    wholeVoteTxt = wholeVoteTxt + txtLine;
    for(key in imgStatistics)
    {
      var img0Coo = key.replace(/.jpg/gi, '').split("_");
      var lat = img0Coo[0];
      var log = img0Coo[1];
      // {"name":"4.62424175098_-74.0575098164_180.jpg","lat":4.62424175098,"log":-74.0575098164,"heading":180},
      txtLine = "{\"lat\":" + lat + ",\"log\":" + log + ",\"pv\":" + imgStatistics[key].pv + ",\"nv\":" + imgStatistics[key].nv + ",\"zv\":" + imgStatistics[key].zv + ",\"name\":" + "\"" + key + "\"" + "},\n";
      wholeVoteTxt = wholeVoteTxt + txtLine;
      txtLine = "";
    }
    wholeVoteTxt = wholeVoteTxt + "]\n";
    //console.log(wholeVoteTxt)
    //Save outpur file
    fs.writeFile(outputFile, wholeVoteTxt, function(err) {
        if(err) {
            return console.log(err);
        }
        console.log("The descriptor indexer file was saved!");
    });

})
