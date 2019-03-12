$('.gallery__slider-main').slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: true,
  // autoplay: true,
  autoplaySpeed: 3000,
  lazyLoad: 'ondemand',
  asNavFor: '.gallery__slider-thumb',
  fade: true
});

$('.gallery__slider-thumb').slick({
  slidesToShow: 4,
  slidesToScroll: 1,
  lazyLoad: 'ondemand',
  asNavFor: '.gallery__slider-main',
  dots: false,
  centerMode: true,
  focusOnSelect: true,
  arrows: true,

  responsive: [
    {
      breakpoint: 767,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 1
      }
    },
  ]
});
