$(document).ready(function(){

    loadGallery(true, 'a.ssviewer');

    function disableButtons(counter_max, counter_current){
        $('#show-previous-image, #show-next-image').show();
        if(counter_max == counter_current){
            $('#show-next-image').hide();
        } else if (counter_current == 1){
            $('#show-previous-image').hide();
        }
		if(location.pathname == '/ss/banned/'){
			$('#ban-player').hide();
		}
    }

    function loadGallery(setIDs, setClickAttr){
        var current_image,
            selector,
			ssid,
            counter = 0;
		var banned = [];

        $('#show-next-image, #show-previous-image').click(function(){
            if($(this).attr('id') == 'show-previous-image'){
				if (banned.indexOf(current_image-1) == -1){
					current_image--;
				}
				else{
					current_image = current_image-2;
				}
            } else {
				if (banned.indexOf(current_image+1) == -1){
					current_image++;
				}
				else{
					current_image = current_image+2;
				}
            }
            selector = $('[data-image-id="' + current_image + '"]');
            updateGallery(selector);
        });
				
		
        function updateGallery(selector) {
            var $sel = selector;
            current_image = $sel.data('image-id');
            $('#ss-view-title').text($sel.data('title'));
			ssid = $sel.data('ss-id');
						
            $('#ss-view-image').attr('src', $sel.data('image'));
            disableButtons(counter, $sel.data('image-id'));
        }

        if(setIDs == true){
            $('[data-image-id]').each(function(){
                counter++;
                $(this).attr('data-image-id',counter);
            });
        }
        $(setClickAttr).on('click',function(){
            updateGallery($(this));
        });
		
		$('#fb-share-now').click(function(){
			var url="blackassassins.tk/ss/viewss/?ssid="+ssid;
			window.open ('//www.facebook.com/sharer/sharer.php?u='+url,'','width=250, height=250, scrollbars=yes');
        });

		$('#ban-player').click(function(){
				window.location.href = "/ss/ban/?ssid="+ssid;
        });
    }

});

$(document).ready(function(){

    reportView(true, 'a.reportaction');	
    function reportView(setIDs, setClickAttr){
        var row,adminid,reportID,selector;
			
		
        function updateModal(selector) {
            var $sel = selector;
            $('#report-admin-title').text($sel.data('title'));
			reportID = $sel.data('report-id');
			row = $sel.data('row');
			adminid = $sel.data('adminid');
			//$('#report-admin-submit').attr("href", "/report/admin/?");
        }
		$(setClickAttr).on('click',function(){
            updateModal($(this));
        });
		$('#report-admin-submit').click(function(){
				var reason = document.getElementById("report-admin-comment").value;
				var params = "data="+row+"&adminid="+adminid+"&reason="+reason;
				
				window.location.href = "/report/admin/?"+params;

        });
		
    }

});

function getsongpreview() {
   var x = document.getElementById("requestsong");
   var ytid = x.elements[4].value;
   var stime = x.elements[5].value;
   var etime = (parseInt(x.elements[5].value)+10).toString();
   document.getElementById('youtubeembed').src = url = "https://www.youtube.com/embed/"+ytid+"?start="+stime+"&end="+etime;
   $('#request-music').removeAttr('disabled');
   
}
$(document).ready(function() {
	$('#penalties').dataTable( {
	  "pageLength": 10,
	  "order": [[ 0, "desc" ]]
	} );
} );

$(document).ready(function() {
	$('#sstable').DataTable( {
		"pageLength": 10,
		"order": [[ 0, "desc" ]]
	} );
} );
function recaptcha_callback(){
  $('#request-preview').removeAttr('disabled');
}
function recaptcha_callback(){
  $('#report-admin-submit').removeAttr('disabled');
  $('#report-admin-submit2').removeAttr('disabled');
}

$(function() {
$('.scroll-down').click (function() {
  $('html, body').animate({scrollTop: $('section.bg-primary').offset().top }, 'slow');
  return false;
});
});

(adsbygoogle = window.adsbygoogle || []).push({
google_ad_client: "ca-pub-5797834730464175",
enable_page_level_ads: true
});

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'UA-109345139-1');
if(document.getElementById('zfJKmUvQEqhV')){
	 zfJKmUvQEqhV='No';
} 
else {
  window.location.href = '/ads_blocker';
  zfJKmUvQEqhV='Yes';
}

if(typeof ga !=='undefined'){
  ga('send','event','Blocking Ads',zfJKmUvQEqhV,{'nonInteraction':1});
} else if(typeof _gaq !=='undefined'){
  _gaq.push(['_trackEvent','Blocking Ads',zfJKmUvQEqhV,undefined,undefined,true]);
}
