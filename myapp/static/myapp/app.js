const image_id = JSON.parse(document.getElementById("image_id").textContent);
const exp_stage = JSON.parse(document.getElementById("exp_stage").textContent);
const exp_aipresence = JSON.parse(document.getElementById("exp_aipresence").textContent);
const default_airec = JSON.parse(document.getElementById("default_airec").textContent);
const default_aiconf = JSON.parse(document.getElementById("default_aiconf").textContent);
const default_aieof = JSON.parse(document.getElementById("default_aieof").textContent);


function get_xcoord_4img() {
  return (document.getElementById('img-container').offsetWidth / 2) - (document.getElementById('img').offsetWidth / 2)
}

function parse(str) {
  var args = [].slice.call(arguments, 1),
    i = 0;

  return str.replace(/%s/g, () => args[i++]);
}

// switch icons in navbar
function switch_icon_grouping(grouping) {

  if (document.getElementById("minus-icon-" + grouping).style.display == 'none') {
    document.getElementById("plus-icon-" + grouping).style.display = 'none'
    document.getElementById("minus-icon-" + grouping).style.display = 'inline-block'
  } else {
    document.getElementById("plus-icon-" + grouping).style.display = 'inline-block'
    document.getElementById("minus-icon-" + grouping).style.display = 'none'
  }
}

// from https://github.com/lalwanivikas/image-editor/blob/master/js/main.js
// Editing image via css properties
function editImage() {
  var brightness = $("#br").val(); // brightness
  var contrast = $("#ct").val(); // contrast

  var filter = 'brightness(' + brightness +
    '%) contrast(' + contrast +
    '%)';
  $("#img").css("filter", filter);
  $("#img").css("-webkit-filter", filter);
}

function back_to_original_image(image_id, grouping) {
  if ($("#img").attr('src') != "/static/myapp/images/task-images/" + image_id + "/" + image_id + ".jpg") {
    $("#img").attr("src", "/static/myapp/images/task-images/" + image_id + "/" + image_id + ".jpg");
    $("#img-modal").attr("src", "/static/myapp/images/task-images/" + image_id + "/" + image_id + ".jpg");
    document.getElementById("imagetype").innerHTML = "Original image";
    var xcoord_img = get_xcoord_4img()
    panZoomInstance.moveTo(xcoord_img, 0);
    panZoomInstance.zoomAbs(xcoord_img, 0, 1);
  }
  grouping = grouping.replace(/\s/g, '');
  if (grouping != 'no-group') {
    switch_icon_grouping(grouping)
  }
}

function editImage_modal() {
  var brightness = $("#br-modal").val(); // brightness
  var contrast = $("#ct-modal").val(); // contrast

  var filter = 'brightness(' + brightness +
    '%) contrast(' + contrast +
    '%)';
  $("#img-modal").css("filter", filter);
  $("#img-modal").css("-webkit-filter", filter);
}
// When sliders change, image will be
// updated via the editImage() function     
$('#br').change(editImage).mousemove(editImage);
$('#ct').change(editImage).mousemove(editImage);
$("#br-modal").change(editImage_modal).mousemove(editImage_modal);
$("#ct-modal").change(editImage_modal).mousemove(editImage_modal);
// Reset sliders back to their original values on press of 'reset'
$('#imageEditor').on('reset', editImage());
$('#imageEditor-modal').on('reset-modal', editImage());


// color/add icon to conditions based on confidence values of the AI
var valuesaiconf = [...document.getElementsByClassName('aiconf')].map(function (x) {
  return parseInt(x.innerHTML.match(/\d+/));
});
var navitems = $('[id^=navitem]');


activate_group_headers = function (index) {
  var grouping_icons = $('[id^=aibinrec-icon-grouping]');
  if (index < 8) {
    grouping_icons[0].style.display = 'inline'
  } else if (index < 19) {
    grouping_icons[1].style.display = 'inline'
  } else if (index < 24) {
    grouping_icons[2].style.display = 'inline'
  } else if (index < 27) {
    grouping_icons[3].style.display = 'inline'
  } else {
    grouping_icons[4].style.display = 'inline'
  }
}
var grouping_icons = $('[id^=aibinrec-icon-grouping]')
var condition_icons = $('[id^=aibinrec-icon-condition]')
var aifocus_divs = $('[id^=aifocusdiv]')
var cards_airec = $('[id^=card-airec-for')
if (exp_stage <= 8) {
  for (index = 0; index < valuesaiconf.length; index++) {
    if (valuesaiconf[index] > 59) {
      condition_icons[index].style.display = 'inline'
      activate_group_headers(index)
    }
  };
} else if (exp_stage >= 9 && exp_aipresence == 1) {
  var imgactivatebinrec = document.getElementById('imgactivate-aibinrec')
  // when toggle switch is used
  imgactivatebinrec.addEventListener('change', function () {
    if (this.checked) {
      document.getElementById('airec-timestamp').value = Date.now()
      for (index = 0; index < valuesaiconf.length; index++) {
        if (valuesaiconf[index] > 59) {
          condition_icons[index].style.display = 'inline'
          activate_group_headers(index)
        }
        // aifocus_divs[index].style.display = 'block'
        cards_airec[index].style.display = 'block'
        cards_airec[index].style.height = null
      };
    }
    if (!this.checked) {
      Array.from(document.getElementsByClassName("fa-exclamation-triangle")).forEach(function (item) {
        item.style.display = 'none'
      });
    }
  })
  if (default_airec == 1) {
    imgactivatebinrec.click()
  }
}

var condpresent_radiobtns_yes = document.querySelectorAll('.condpresent-yes');
var human_icons = $('[id^=human-icon-condition]')
for (let index = 0; index < condpresent_radiobtns_yes.length; index++) {
  // elem =  document.querySelectorAll('.show-grad-img')[index]
  condpresent_radiobtns_yes[index].addEventListener("click", function () {
    human_icons[index].style.display = 'inline'
  });
};
// when it's uploaded as "yes" (but not clicked)
for (index = 0; index < condpresent_radiobtns_yes.length; index++) {
  if (condpresent_radiobtns_yes[index].checked) {
    human_icons[index].style.display = 'inline'
  }
};
var condpresent_radiobtns_no = document.querySelectorAll('.condpresent-no');
for (let index = 0; index < condpresent_radiobtns_no.length; index++) {
  // elem =  document.querySelectorAll('.show-grad-img')[index]
  condpresent_radiobtns_no[index].addEventListener("click", function () {
    human_icons[index].style.display = 'none'
  });
};

// // panzoom for main image
var panZoomInstance = document.getElementById('img')
panZoomInstance = panzoom(panZoomInstance)
var rstpnz = document.getElementById("reset-image");
$('#img-container').imagesLoaded(function () {
  panZoomInstance.moveTo(get_xcoord_4img(), 0);
  panZoomInstance.zoomAbs(get_xcoord_4img(), 0, 1);
});
rstpnz.onclick = function () {
  panZoomInstance.moveTo(get_xcoord_4img(), 0);
  panZoomInstance.zoomAbs(get_xcoord_4img(), 0, 1);
};


// // panzoom for modal image
var panZoomInstance_modal = document.getElementById('img-modal')
panZoomInstance_modal = panzoom(panZoomInstance_modal)
var rstpnz_modal = document.getElementById("reset-image-modal");
rstpnz_modal.onclick = function () {
  panZoomInstance_modal.moveTo(0, 0);
  panZoomInstance_modal.zoomAbs(0, 0, 1);
};


// when click AI focus, change image that gets uploaded
// this part should be partially rewritten if we decide to sort the conditions
var conditions = [...document.getElementsByClassName('cond-title')].map(function (x) {
  return x.textContent;
});
var conditions_short = [...document.getElementsByClassName('cond-title')].map(function (x) {
  return x.id.replace('cond-title-', '');
});
var show_saliency_buttons = document.querySelectorAll('.show-grad-img')
if (show_saliency_buttons.length > 0) {
  for (let index = 0; index < valuesaiconf.length; index++) {
    show_saliency_buttons[index].addEventListener("click", function () {
      $("#img").attr("src", "/static/myapp/images/task-images/" + image_id + "/gradcam_" + conditions[index] + ".png").one('load',
        function () {
          panZoomInstance.moveTo(get_xcoord_4img(), 0);
          panZoomInstance.zoomAbs(get_xcoord_4img(), 0, 1)
        });
      // update also the image in the modal
      $("#img-modal").attr("src", "/static/myapp/images/task-images/" + image_id + "/gradcam_" + conditions[index] + ".png");
      document.getElementById('imagetype').innerHTML = 'AI focus for ' + conditions[index]
      // show the additional questions
      document.getElementById('qaifocus-' + conditions_short[index]).style['display'] = 'block'
      // create and submit timestamp Date.now()
      document.getElementById('aifocus-' + conditions_short[index] + '-timestamp').value = Date.now()
    });
  };

  var hide_grad_btns = document.querySelectorAll('.hide-grad-img');
  for (let index = 0; index < valuesaiconf.length; index++) {
    hide_grad_btns[index].addEventListener("click", function () {
      $("#img").attr("src", "/static/myapp/images/task-images/" + image_id + "/" + image_id + ".jpg").one('load',
        function () {
          panZoomInstance.moveTo(get_xcoord_4img(), 0);
          panZoomInstance.zoomAbs(get_xcoord_4img(), 0, 1)
        });
      $("#img-modal").attr("src", "/static/myapp/images/task-images/" + image_id + "/" + image_id + ".jpg");
      document.getElementById('imagetype').innerHTML = 'Original image'
    });
  };
}

if (exp_stage >= 9) {
  var ai_conf_btns = $('[id^=aiconf-activate]')
  for (let index = 0; index < valuesaiconf.length; index++) {
    ai_conf_btns[index].addEventListener('click', function () {
      document.getElementById('aiconf-sentence-' + conditions_short[index]).style.visibility = 'visible'
      document.getElementById('aiconf-sentence-' + conditions_short[index]).style.height = null
      document.getElementById('aiconf-' + conditions_short[index] + '-timestamp').value = Date.now()
    })
    if (default_aiconf == 1) {
      ai_conf_btns[index].click()
    }
  }
  var ai_eof_btns = $('[id^=aieof-activate]')
  for (let index = 0; index < valuesaiconf.length; index++) {
    ai_eof_btns[index].addEventListener('click', function () {
      document.getElementById('aieof-sentence-' + conditions_short[index]).style.display = 'block'
      document.getElementById('aieof-sentence-' + conditions_short[index]).style.height = null
      document.getElementById('aieof-' + conditions_short[index] + '-timestamp').value = Date.now()
    })
    if (default_aieof == 1) {
      ai_eof_btns[index].click()
    }
  }
}