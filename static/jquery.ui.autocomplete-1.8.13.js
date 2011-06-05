/*
 * jQuery UI Autocomplete 1.8.13
 *
 * Copyright 2011, AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * http://docs.jquery.com/UI/Autocomplete
 *
 * Depends:
 *jquery.ui.core.js
 *jquery.ui.widget.js
 *jquery.ui.position.js
 */
(function( $, undefined ) {

    // used to prevent race conditions with remote data sources
    var requestIndex = 0;

    $.widget( "ui.autocomplete", {
	    options: {
		appendTo: "body",
		    autoFocus: false,
		    delay: 300,
		    minLength: 1,
		    position: {
		    my: "left top",
			at: "left bottom",
			collision: "none"
			},
		    source: null
		    },

		pending: 0,

		_create: function() {
		var self = this,
		    doc = this.element[ 0 ].ownerDocument,
		    suppressKeyPress;

		this.element
		    .addClass( "ui-autocomplete-input" )
		    .attr( "autocomplete", "off" )
		    // TODO verify these actually work as intended
		    .attr({
			    role: "textbox",
				"aria-autocomplete": "list",
				"aria-haspopup": "true"
				})
		    .bind( "keydown.autocomplete", function( event ) {
			    if ( self.options.disabled || self.element.attr( "readonly" ) ) {
				return;
			    }

			    suppressKeyPress = false;
			    var keyCode = $.ui.keyCode;
			    switch( event.keyCode ) {
			    case keyCode.PAGE_UP:
				self._move( "previousPage", event );
				break;
			    case keyCode.PAGE_DOWN:
				self._move( "nextPage", event );
				break;
			    case keyCode.UP:
				self._move( "previous", event );
				// prevent moving cursor to beginning of text field in some browsers
				event.preventDefault();
				break;
			    case keyCode.DOWN:
				self._move( "next", event );
				// prevent moving cursor to end of text field in some browsers
				event.preventDefault();
				break;
			    case keyCode.ENTER:
			    case keyCode.NUMPAD_ENTER:
				// when menu is open and has focus
				if ( self.menu.active ) {
				    // #6055 - Opera still allows the keypress to occur
				    // which causes forms to submit
				    suppressKeyPress = true;
				    event.preventDefault();
				}
				//passthrough - ENTER and TAB both select the current element
			    case keyCode.TAB:
				if ( !self.menu.active ) {
				    return;
				}
				self.menu.select( event );
				break;
			    case keyCode.ESCAPE:
				self.element.val( self.term );
				self.close( event );
				break;
			    default:
				// keypress is triggered before the input value is changed
				clearTimeout( self.searching );
				self.searching = setTimeout(function() {
					// only search if the value has changed
					if ( self.term != self.element.val() ) {
					    self.selectedItem = null;
					    self.search( null, event );
					}
				    }, self.options.delay );
				break;
			    }
			})
		    .bind( "keypress.autocomplete", function( event ) {
			    if ( suppressKeyPress ) {
				suppressKeyPress = false;
				event.preventDefault();
			    }
			})
		    .bind( "focus.autocomplete", function() {
			    if ( self.options.disabled ) {
				return;
			    }

			    self.selectedItem = null;
			    self.previous = self.element.val();
			})
		    .bind( "blur.autocomplete", function( event ) {
			    if ( self.options.disabled ) {
				return;
			    }

			    clearTimeout( self.searching );
			    // clicks on the menu (or a button to trigger a search) will cause a blur event
			    self.closing = setTimeout(function() {
				    self.close( event );
				    self._change( event );
				}, 150 );
			});
		this._initSource();
		this.response = function() {
		    return self._response.apply( self, arguments );
		};
		this.menu = $( "<ul></ul>" )
		    .addClass( "ui-autocomplete" )
		    .appendTo( $( this.options.appendTo || "body", doc )[0] )
		    // prevent the close-on-blur in case of a "slow" click on the menu (long mousedown)
		    .mousedown(function( event ) {
			    // clicking on the scrollbar causes focus to shift to the body
			    // but we can't detect a mouseup or a click immediately afterward
			    // so we have to track the next mousedown and close the menu if
			    // the user clicks somewhere outside of the autocomplete
			    var menuElement = self.menu.element[ 0 ];
			    if ( !$( event.target ).closest( ".ui-menu-item" ).length ) {
				setTimeout(function() {
					$( document ).one( 'mousedown', function( event ) {
						if ( event.target !== self.element[ 0 ] &&
						     event.target !== menuElement &&
						     !$.ui.contains( menuElement, event.target ) ) {
						    self.close();
						}
					    });
				    }, 1 );
			    }

			    // use another timeout to make sure the blur-event-handler on the input was already triggered
			    setTimeout(function() {
				    n menu)
				if ( self.elemenn() {
					var ul = this.menu.element;
					