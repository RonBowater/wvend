window.clickit_top_cancel = function () { if (CI.topdiv_owner != null) CI.topdiv_owner.trigger('doCancel', ""); }
window.clickit_mid_cancel = function () { if (CI.middiv_owner != null) CI.middiv_owner.trigger('doCancel', ""); }
window.clickit_bot_cancel = function () { if (CI.botdiv_owner != null) CI.botdiv_owner.trigger('doCancel', ""); }

window.clickit_top_proceed = function () { if (CI.topdiv_owner != null) CI.topdiv_owner.trigger('doProceed', ""); }
window.clickit_mid_proceed = function () { if (CI.middiv_owner != null) CI.middiv_owner.trigger('doProceed', ""); }
window.clickit_bot_proceed = function () { if (CI.botdiv_owner != null) CI.botdiv_owner.trigger('doProceed', ""); }

window.clickit_top_function = function (n) { if (CI.topdiv_owner != null) CI.topdiv_owner.trigger('doFunction', n); } 
window.clickit_mid_function = function (n) { if (CI.middiv_owner != null) CI.middiv_owner.trigger('doFunction', n); }
window.clickit_bot_function = function (n) { if (CI.botdiv_owner != null) CI.botdiv_owner.trigger('doFunction', n); }

clean_divs = function(topview, midview, botview)
{
	if (topview != 'L')
	{
		if (CI.topdiv_owner != null)
    	{
      		CI.topdiv_owner.remove();
      		CI.topdiv_owner = null;
      		$('.topdiv').html = "";
    	}
    	if (topview != 'C')
    	{
      		CI.topdiv_owner = topview;
    	}
    }	
    if (midview != 'L')
	{
		if (CI.middiv_owner != null)
    	{
      		CI.middiv_owner.remove();
      		CI.middiv_owner = null;
      		$('.middiv').html = "";
    	}
    	if (midview != 'C')
    	{
      		CI.middiv_owner = midview;
    	}
    }
    if (botview != 'L')
	{
		if (CI.botdiv_owner != null)
    	{
      		CI.botdiv_owner.remove();
      		CI.botdiv_owner = null;
      		$('.botdiv').html = "";
    	}
    	if (botview != 'C')
    	{
      		CI.botdiv_owner = botview;
    	}
    }		
} 
 
document.onkeydown = keyDown;

function keyDown(e)
{
  	var x = e || window.event;
  	var key = (x.keyCode || x.which);
  
    if(key == 13 || key == 3)
    {
    	if (CI.botdiv_owner != null)
    	{
    		CI.botdiv_owner.trigger('enterKey', "");
   		}
   		else if (CI.middiv_owner != null)
    	{
    		CI.middiv_owner.trigger('enterKey', "");
   		}
    	else if (CI.topdiv_owner != null)
    	{
    		CI.topdiv_owner.trigger('enterKey', "");
   		}
    }
    else if (key == 27)
    {
    	if (CI.botdiv_owner != null)
    	{
    		CI.botdiv_owner.trigger('escKey', "");
   		}
   		else if (CI.middiv_owner != null)
    	{
    		CI.middiv_owner.trigger('escKey', "");
   		}
    	else if (CI.topdiv_owner != null)
    	{
    		CI.topdiv_owner.trigger('escKey', "");
   		}
    }
}  
  
/****************************/  
/* Date conversion routines */
/****************************/  
 
var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/* convert e.g. 2015-8-21 to 21 Aug 2015 */
format_y_m_d_to_d_mname_y = function(d) 
{
    d = d.split('-');
    return d[2] + ' ' + monthNames[d[1]-1] + ' ' + d[0];
};

/* convert e.g. 2015-8-21 to 21/08/15 */
format_y_m_d_to_d_m_y = function(d) 
{
    d = d.split('-');
    return d[2] + '/' + d[1] + '/' + d[0];
};

/* convert e.g. 21-8-2015 to 21 Aug 2015 */
format_d_m_y_to_d_mname_y = function(d) 
{
    d = d.split('-');
    return d[0] + ' ' + monthNames[d[1]-1] + ' ' + d[2];
};

/* convert e.g. 21-8-2015 to 2015-08-21 */
format_d_m_y_to_y_m_d = function(d) 
{
    d = d.split('-');
    return d[2] + '-' + d[1] + '-' + d[0];
};

/* format javascript date object to 21 Aug 2015 */
format_date_to_d_mname_y = function(d) 
{
    return d.getDate().toString() + ' ' + monthNames[d.getMonth()] + ' ' + d.getFullYear().toString();
};

/* convert e.g. 21 Aug 2015 to 21-8-2105 */
format_d_mname_y_to_d_m_y = function(d) 
{
	MyDate = new Date(d)
	MyDateString = ('0' + MyDate.getDate()).slice(-2) + '-' + ('0' + (MyDate.getMonth()+1)).slice(-2) + '-' + MyDate.getFullYear();
    return MyDateString; 
};

/* convert e.g. 21 Aug 2015 to 2015-8-21 */
format_d_mname_y_to_y_m_d = function(d) 
{
	MyDate = new Date(d)
	
	MyDateString = MyDate.getFullYear() + '-' + ('0' + (MyDate.getMonth()+1)).slice(-2) + '-' + ('0' + MyDate.getDate()).slice(-2);
	return MyDateString; 
};
 
ensureNotUndefined = function(val)
{
	if (typeof val == "undefined") val = "";
	return val;
} 
   
/********************************/
/* remove the value of a cookie */
/********************************/  

clearCookie = function(sName)
{
    setCookie(sName,'');
}

/*******************************/
/* numeric validation function */
/*******************************/

do_validate = function(val) 
{
	neg = "";
	if (val[0] == '-')
	{
		neg = '-';
		val = val.substring(1);
	}

	value = val.replace(/\s+$/, '');
	console.log (">>" + value + "<<");
	if (value == "") return (" ");
	value = value.replace(/^\s+|\s+$/g, "");
    var regex = /^[0-9]\d*(((,\d{3}){1})?(\.\d{0,2})?)$/;
    if (regex.test(value))
    {
        //Input is valid, check the number of decimal places
        var twoDecimalPlaces = /\.\d{2}$/g;
        var oneDecimalPlace = /\.\d{1}$/g;
        var noDecimalPlacesWithDecimal = /\.\d{0}$/g;
        
        if(value.match(twoDecimalPlaces ))
        {
            //all good, return as is
            return neg + value;
        }
        if(value.match(noDecimalPlacesWithDecimal))
        {
            //add two decimal places
            return neg + value + '00';
        }
        if(value.match(oneDecimalPlace ))
        {
            //ad one decimal place
            return neg + value+'0';
        }
        //else there is no decimal places and no decimal
        return neg + value +".00";
    }
    return null;
};

/********************/
/* Simple Date Form */
/********************/

/* data form model definition*/
var d_dateFormModel = Backbone.Model.extend
({
	defaults: 
	{
    	formDate: "02-08-2015"
  	}
});

/* model instance */
var dateFormModel = new d_dateFormModel
({
	formDate: "02-08-2015"  
});
 
/* fields */
var dateFormFields = [{name: "formDate", label: "Date", control: "datepicker"}]; 
   
/* form */
var dateForm = Backform.Form.extend
({
  	model:  dateFormModel,
  	fields: dateFormFields
})