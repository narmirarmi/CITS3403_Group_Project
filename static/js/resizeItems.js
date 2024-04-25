// This section recalculates and sizes the numbers of images and rows to fit window
$(document).ready(function () {
  adjustItemsPerRow();

  $(window).resize(function () {
    adjustItemsPerRow();
  });

  function adjustItemsPerRow() {
    var screenWidth = $(window).width();
    var itemsPerRow;

    if (screenWidth >= 992) {
      itemsPerRow = 3; // Large screens (lg)
    } else if (screenWidth >= 768) {
      itemsPerRow = 2; // Medium screens (md)
    } else {
      itemsPerRow = 1; // Small screens (sm) and below
    }

    var $row = $("#image-row");
    var $items = $row.children(".col-lg-4");

    $items.removeClass("col-lg-4 col-md-6 col-sm-12");
    $items.addClass("col-lg-" + 12 / itemsPerRow);
    $items.addClass("col-md-" + 12 / itemsPerRow);
    $items.addClass("col-sm-12");
  }
});
