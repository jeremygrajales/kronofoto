import HTMX from "./htmx.js"
import timeline from "./timeline.js"
import {
  installButtons,
  toggleMenu,
  markerDnD,
  toggleLogin,
  initGalleryNav,
  autoplayStart,
  autoplayStop,
  timelineForward,
  timelineBackward,
  timelineZipForward,
  timelineZipBackward,
  timelineCrawlForward,
  timelineCrawlForwardRelease,
  timelineCrawlBackward,
  timelineCrawlBackwardRelease,
  moveTimelineCoin,
  dropTimelineCoin,
  gotoTimelinePosition,
  showToast,
  initNavSearch,
  collapseNavSearch,
  expandNavSearch
}
  from "./lib.js"

window.toggleLogin = toggleLogin
window.$ = window.jQuery

const htmx = HTMX(document)
window.htmx = htmx
const _timeline = new timeline();

function showImagesBeforeSwap(target) {
  const images = target.querySelectorAll('img');

  images.forEach((img) => {
    if (!img.complete) {
      // When the image is not yet loaded, set an event listener to show it when loaded
      img.addEventListener('load', function () {
        img.style.opacity = 1; /* or use visibility: visible; */
      });
    } else {
      img.style.opacity = 1; /* or use visibility: visible; */
    }
  });
}

// After HTMX is done loading
htmx.onLoad((e) => {

  $('.photos-timeline').each(function(i,e) {
    _timeline.connect(e);
  });

  if($(e).is('body')) {
    initPopups()
  }

  // Init gallery nav buttons
  installButtons(document)

  // Init gallery thumbnails
  initDraggableThumbnails()

  initNavSearch()

  if($('#fi-preload-zone li').length) {
    let html = $('#fi-preload-zone').html()
    // let firstId = $(html).find('li:first-child span').attr('hx-get')
    $('#fi-thumbnail-carousel-images').html(html)
    // let $after = $('#fi-thumbnail-carousel-images li span[hx-get="'+firstId+'"]').nextAll()
    // $('#fi-thumbnail-carousel-images').append($after)
    $('#fi-thumbnail-carousel-images').addClass('dragging')
    $('#fi-thumbnail-carousel-images').css('left', '0px')
    setTimeout(() => {
      $('#fi-thumbnail-carousel-images').removeClass('dragging')
      if(!$('#fi-thumbnail-carousel-images [data-origin]').length) {
        $('#fi-thumbnail-carousel-images [data-active]').attr('data-origin', '')
      }
    }, 100)

    htmx.process($('#fi-thumbnail-carousel-images').get(0))
    $('#fi-preload-zone').empty()

  }

  if($('#fi-image-preload img').length && !$('#fi-image-preload img').data('loaded')) {
    $('#fi-image-preload img').data('loaded', true)
    let url = $('#fi-image-preload img').attr('src')
    const image = new Image();
    image.src = url;
    image.onload = () => {
      let html = $('#fi-image-preload').html()
      $('#fi-image').html(html)
      $('#fi-image-preload').empty()
    }
  }
})

initGalleryNav()

htmx.logger = function(elt, event, data) {
  if(console) {
    // console.log(event, elt, data);
  }
}

const initPopups = () => {
  if($('#add-to-list-popup').length) {
    window.htmx.trigger($('#add-to-list-popup').get(0), 'manual')
    window.htmx.trigger($('#download-popup').get(0), 'manual')
    window.htmx.trigger($('#share-popup').get(0), 'manual')
    $(document).foundation()
  }
}

document.addEventListener('htmx:pushedIntoHistory', initPopups)
document.addEventListener('htmx:pushedIntoHistory', initNavSearch)

document.addEventListener('htmx:afterSwap', (event) => {
  if($('[data-timeline-target=sliderYearLabel]').length && $('[data-timeline-target=sliderYearLabel]').html()) {
    let newYear = $('[data-timeline-target=sliderYearLabel]').html().trim()
    _timeline.setYear(newYear, false)
  }
})

window.setTimeout(() => { htmx.onLoad(markerDnD(document)) }, 100)
//htmx.logAll()

const initDraggableThumbnails = () => {
  if(!$('#fi-thumbnail-carousel-images [data-origin]').length) {
    $('#fi-thumbnail-carousel-images [data-active]').attr('data-origin', '')
  }
  $('#fi-thumbnail-carousel-images').draggable({
    axis: 'x',
    drag: (event, ui) => {
      moveTimelineCoin(ui.position.left, true)
    },
    stop: (event, ui) => {
      dropTimelineCoin(ui.position.left)
    }
  })
}


const init = () => {

  new window.ClipboardJS('[data-clipboard-target]');

  $(document).ready(function() {

    $(document).on('change keydown paste input', 'input', (e) => {
      if($(e.currentTarget).closest('form')) {
        $(e.currentTarget).closest('form').find('[data-enable-on-modify]').removeAttr('disabled')
      }
    })

    $(document).on('submit', '#add-to-list-popup form', function(e) {
      showToast('Updated photo lists')
    })

    $('#overlay').on('click', (e) => {
      $('#login').addClass('collapse')
      $('#hamburger-menu').addClass('collapse')
      $('#overlay').fadeOut()
    })
    $('#hamburger-menu').on('off.zf.toggler', (e) => {
      $('#login').addClass('collapse')
      $('#overlay').fadeIn()
    }).on('on.zf.toggler', (e) => {
      if($('#login').hasClass('collapse')) {
        $('#overlay').fadeOut()
      }
    })
    $('#login').on('off.zf.toggler', (e) => {
      $('#hamburger-menu').addClass('collapse')
      $('#overlay').fadeIn()
    }).on('on.zf.toggler', (e) => {
      if($('#hamburger-menu').hasClass('collapse')) {
        $('#overlay').fadeOut()
      }
    })

  })

  // initDraggableThumbnails()

  $(document).click(function(event)
  {

      //~TESTING LINE
      //console.log(event.target.className)

      var classOfThingClickedOn = event.target.className

      //~TESTING LINE
      //console.log($('.search-form').find('*'))

      //creates a jQuery collection of the components of the search menu EXCEPT for the menu itself
      var $descendantsOfSearchForm = $('.search-form').find('*')

      //---creates an array of all components of the search menu dropdown---
      //adds the search menu itself to the array
      var componentsOfSearchMenuArray = ['search-form']

      //adds the class of all the components of the search menu to the array
      $descendantsOfSearchForm.each(function(index)
      {
          //checks to make sure the class isn't already in the array
          if($.inArray(this.className, componentsOfSearchMenuArray) == -1)
          {
              //adds the class to the array
              componentsOfSearchMenuArray.push(this.className)
          }
      })

      //~TESTING LINES
      //console.log(componentsOfSearchMenuArray)
      //console.log('Class:'+'"'+classOfThingClickedOn+'"')
      //console.log(componentsOfSearchMenuArray.includes(classOfThingClickedOn))

      //if the search menu is open and the user clicks on something outside of the menu, close the menu
      if($(event.target).attr('id') != 'search-box' && $('.search-form').is(":visible") && (!(componentsOfSearchMenuArray.includes(classOfThingClickedOn))))
      {
          collapseNavSearch()
      }
      //if the user clicks on the carrot or the small invisible box behind it, toggle the menu
      else if(classOfThingClickedOn == 'search-options' || classOfThingClickedOn == 'carrot')
      {
          // $('.search-form').toggle()
      }
  })

  $('#tag-search').autocomplete({
      source: '/tags',
      minLength: 2,
  })

  $(document).on('click', '#forward-zip', timelineZipForward)
  $(document).on('click', '#forward', timelineForward)
  $(document).on('mousedown', '#forward-zip', timelineCrawlForward)
  $(document).on('mouseup', '#forward-zip', timelineCrawlForwardRelease)
  $(document).on('click', '#backward-zip', timelineZipBackward)
  $(document).on('click', '#backward', timelineBackward)
  $(document).on('mousedown', '#backward-zip', timelineCrawlBackward)
  $(document).on('mouseup', '#backward-zip', timelineCrawlBackwardRelease)
  $(document).on('click', '#fi-arrow-right', timelineForward)
  $(document).on('click', '#fi-arrow-left', timelineBackward)
  $(document).on('click', '#fi-thumbnail-carousel-images li span', function(e) {
    let num = $('#fi-thumbnail-carousel-images li').length
    let delta = $(e.currentTarget).parent().index() - ((num-1)/2)
    gotoTimelinePosition(delta)
  })

  $(document).on('keydown', function(event) {
    var keyCode = event.which || event.keyCode;

    // Handle forward arrow key (Right Arrow or Down Arrow)
    if (keyCode === 39) {
      // Perform the action for the forward arrow key
      timelineForward()
    }

    // Handle back arrow key (Left Arrow or Up Arrow)
    if (keyCode === 37) {
      // Perform the action for the back arrow key
      timelineBackward()
    }
  });

  $(document).on('click', '#auto-play-image-control-button', (e) => {
    let $btn = $('#auto-play-image-control-button')
    $btn.toggleClass('active')
    if($btn.hasClass('active')) {
      autoplayStart()
    }
    else {
      autoplayStop()
    }
  })

  $(document).on('click', '.image-control-button--toggle', (e) => {
    let $btn = $(e.currentTarget)
    $('img', $btn).toggleClass('hide')
  })
}

const ready = fn => {
    if (document.readyState !== "loading") {
        fn()
    } else {
        document.addEventListener("DOMContentLoaded", fn)
    }
}

ready(init)
