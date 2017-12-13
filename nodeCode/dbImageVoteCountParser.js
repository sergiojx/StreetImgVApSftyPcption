var mongoose = require('mongoose');
var _ = require('underscore');
var distance = require('gps-distance');

  /*
  */

  var arrayOfImgDirs = [];
  mongoose.connect('mongodb://localhost:27017/test');
  var Image = mongoose.model('Image', require('./image'), 'image');
  var Vote = mongoose.model('Vote', require('./vote'), 'vote');

  var imgStatistics = {};
  var imgRepeatedVotes = {};
  var repeatedVotesCnt = 0;
  var equalVotes = 0;
  var chargedVote = 0;
  var maxDistance = -1;
  var minDistance = -1;

  Vote.find({}, function(err, votes) {
    if (err) throw err;

    votes.forEach(function(v,i){
        //Repeated votes tracking logic
        if(imgRepeatedVotes[v.image0 + v.image1] == undefined && imgRepeatedVotes[v.image1 + v.image0] == undefined)
        {
          imgRepeatedVotes[v.image0 + v.image1] = 1;
        }
        else {
            repeatedVotesCnt = repeatedVotesCnt + 1;
            if(imgRepeatedVotes[v.image0 + v.image1] == undefined)
            {
              imgRepeatedVotes[v.image1 + v.image0] = imgRepeatedVotes[v.image1 + v.image0] + 1;
            }
            else {
              imgRepeatedVotes[v.image0 + v.image1] = imgRepeatedVotes[v.image0 + v.image1] + 1;
            }
        }

      	// Image distance
        //Image cordinates are extracted from image name
      	// https://www.npmjs.com/package/gps-distance
      	var img0Coo = v.image0.replace(/.jpg/gi, '').split("_");
      	var img1Coo = v.image1.replace(/.jpg/gi, '').split("_");
      	var dist = distance(parseFloat(img0Coo[0]), parseFloat(img0Coo[1]), parseFloat(img1Coo[0]), parseFloat(img1Coo[1]));
      	if(maxDistance == -1 || dist > maxDistance){maxDistance = dist;}
      	if(minDistance == -1 || dist < minDistance){minDistance = dist;}
        if(dist == 0){ console.log(v._id + ' Distance 0!!!: image0->' + v.image0 + " " + 'image1->' + v.image1);}

	      //Vote statistics
        if(imgStatistics[v.image0] == undefined){imgStatistics[v.image0] = {'pv':0,'nv':0,'zv':0};}
        if(imgStatistics[v.image1] == undefined){imgStatistics[v.image1] = {'pv':0,'nv':0,'zv':0};}
        if(v.vote == 1){
            imgStatistics[v.image0].pv = imgStatistics[v.image0].pv + 1;
            imgStatistics[v.image1].nv = imgStatistics[v.image1].nv + 1;
	          chargedVote = chargedVote + 1;
        }
        else if(v.vote == 2){
            imgStatistics[v.image1].pv = imgStatistics[v.image1].pv + 1;
            imgStatistics[v.image0].nv = imgStatistics[v.image0].nv + 1;
	          chargedVote = chargedVote + 1;
        }
        else {
            imgStatistics[v.image1].zv = imgStatistics[v.image1].zv + 1;
            imgStatistics[v.image0].zv = imgStatistics[v.image0].zv + 1;
	          equalVotes = equalVotes + 1;
        }
        //console.log(v.vote);

    });
    //console.log(imgStatistics);
    //console.log(imgRepeatedVotes);
    //Just print repeated votes
    console.log("Repeated votes")
    for(key in imgRepeatedVotes)
    {
      if(imgRepeatedVotes[key]>1)
      {
        console.log(key + ' ' + imgRepeatedVotes[key]);
        //compensate initialization count
        repeatedVotesCnt = repeatedVotesCnt + 1;
      }
    }
    console.log('Repetitions: ' + repeatedVotesCnt);
    /*
    for(key in imgStatistics)
    {
      if(imgStatistics[key].zv > 3)
      {
        console.log(key + ' ' + imgStatistics[key].zv);

      }
    }
    */
    console.log("Charged votes: " + chargedVote);
    console.log("Equal votes: " + equalVotes);
    console.log("Max. distance: " + maxDistance);
    console.log("Min. distance: " + minDistance);
})
/*
db.image.find({"name":"4.64325149801_-74.0656709126_135.jpg"}).forEach(function(item){db.image.update({_id : item._id},{$set:{vcnt : (item.vcnt-27)}})})
db.vote.find({ $and: [ { "image0":"4.6794205_-74.0584418_180.jpg" } , { "image1":"4.6528265304_-74.0539190259_180.jpg" } ] })
db.vote.find({ $and: [ { "image0":"4.63132993388_-74.06619847_0.jpg" } , { "image1":"4.65924216364_-74.0536616347_180.jpg" } ] })
*/
