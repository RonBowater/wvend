 
var G_vend_data;

/**************************************************************/
/* Set_vend_data called to send vend data from host initially */
/**************************************************************/

function set_vend_data(vend_data)
{
  console.log (vend_data);
  G_vend_data = vend_data;
}   

/******************/
/* Initialization */
/******************/
 
function addDays(date, days) 
{
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
} 
 
var CI = 
{
    run: function (access_code) 
    {
		CI.I_WinchWeeklySalesView = new CI.WinchWeeklySalesView();
		CI.I_WinchWeeklyPaymentsView = new CI.WinchWeeklyPaymentsView();
		
		CI.topdiv_owner = null;
		CI.middiv_owner = null;
		CI.botdiv_owner = null;
		
		/* get current date */
		CI.the_date = new Date();
		
		setTimeout(CI.I_WinchWeeklySalesView.render(), 20);
	}
} 	
 
/********************************/
/* Winchester Weekly Sales View */
/********************************/

CI.WinchWeeklySalesView = Backbone.View.extend(
{
    el: 'div.topdiv',
    
    template: _.template($('#T_WinchWeeklySalesTemplate').html()),
    
    initialize: function () 
    {
        _.bindAll(this, 'render', 'doProceed', 'doCancel', 'doFunction'); 
        this.on('doProceed', this.doProceed, this);
        this.on('doFunction', this.doFunction, this);
        this.on('doCancel', this.doCancel, this);
        this.on('escKey', this.doCancel, this);
    }, 
      
    /* Entry point for winchester weekly view */  
   	render: function () 
    {	
    	var self = this;
        
        CI.I_WinchWeeklySalesListView = new CI.WinchWeeklySalesListView();
        
      	clean_divs (this, 'C', 'C'); 
        this.$el.html(this.template());
            
        this.setdates();
    },
    
    remove: function() 
    {
        this.undelegateEvents();
        this.$el.empty();
        this.stopListening();
        return this;
    },
    
    setdates: function()
    {
    	var s = format_date_to_d_mname_y(CI.the_date);
    
    	dateFormModel.set('formDate', s); 
		this.myform = new dateForm({ el: $("#winchWeeklyForm") });
		this.myform.render();
	
		$('.datepicker').datepicker({
    	format: 'mm/dd/yyyy',
    	startDate: '-3d'
		});
	
		s1 = "<button id='button1' type='button' style='margin-bottom:10px;' class='btn btn-primary btn-sm'>Today</button>";
		s2 = "<button id='button2' type='button' style='margin-left:10px;margin-bottom:10px;' class='btn btn-primary btn-sm'>Week+</button>";
		s3 = "<button id='button3' type='button' style='margin-left:10px;margin-bottom:10px;' class='btn btn-primary btn-sm'>Week-</button>";
	
		$("label.control-label").html("<span style='padding-bottom:20px;'>" + s1 + s2 + s3 + "</span>");
	 
	 	$("div.form-group.formDate").find("input").prop('readonly', true);
	 
	 	$("#button1").click(function() 
		{ 
			CI.the_date = new Date();
    		CI.I_WinchWeeklySalesView.setdates();
		});   
		$("#button2").click(function() 
		{ 
			CI.the_date.setDate(CI.the_date.getDate()+7);
    		CI.I_WinchWeeklySalesView.setdates();
		}); 
		$("#button3").click(function() 
		{ 
			CI.the_date.setDate(CI.the_date.getDate()-7);
    		CI.I_WinchWeeklySalesView.setdates();
		});     
	 
		this.doProceed();	
    },
    
    /* Continue */
    doFunction: function (n)
    {
    	if (n=='switch')
    	{
    		$(document).unbind('change');
    		CI.I_WinchWeeklyPaymentsView.render();			
    	}
    	else if (n=='refresh')
    	{
    		$('#main_table').html ("<b style='font-size:18px'>Loading...</b>"); 
    		google.script.run
   				.withSuccessHandler(refresh_sales_success)
   				.withFailureHandler(refresh_sales_error)
   				.withUserObject(this)
   				.refresh_vend_data();    	
			
    	}
    	else
    	{
    		alert ("bad function call");
    	}
    },
        
    /* Continue */
    doProceed: function ()
    {
    	CI.the_date = new Date($('input[name=formDate]').val());
    	
		CI.I_WinchWeeklySalesListView.doLoading();
    	
    	var monday = moment(CI.the_date).startOf('isoweek').toDate();
		var sunday = moment(CI.the_date).endOf('isoweek').toDate();
    	
    	dm = monday.getFullYear() + '-' + ('0' + (monday.getMonth()+1)).slice(-2) + '-' + ('0' + monday.getDate()).slice(-2);
    	ds = sunday.getFullYear() + '-' + ('0' + (sunday.getMonth()+1)).slice(-2) + '-' + ('0' + sunday.getDate()).slice(-2);
    	
    	/* get all vend info between dates */ 
		/* mysql = "SELECT * from shop_vend WHERE  (date BETWEEN '"+ dm +" 00:00:00' AND '"+ ds +" 23:59:59') ORDER BY date ASC";*/
        
        var dm_date = new Date(dm);
        var ds_date = new Date(ds);
        
		var L_vend_data = [];
        for (i=2; i<G_vend_data.length; i++)
        {
        	var item = {};
        	
        	var a_date = new Date(G_vend_data[i][0]);
        	
        	if ((a_date>=dm_date) && (a_date<=ds_date))
        	{        	
				item['date'] = G_vend_data[i][0];
				item['day'] = G_vend_data[i][1];
				item['furn_sales'] = G_vend_data[i][2];
				item['hw_sales'] = G_vend_data[i][3];
				item['paint_sales'] = G_vend_data[i][4];
				item['discount_sales'] = G_vend_data[i][5];
				item['romsey_sales'] = G_vend_data[i][6];
				item['books_sales'] = G_vend_data[i][7];
				item['total_sales'] = G_vend_data[i][8];
				item['cash_payments'] = G_vend_data[i][9];
				item['card_payments'] = G_vend_data[i][10];
				item['cheque_payments'] = G_vend_data[i][11];
				item['bacs_payments'] = G_vend_data[i][12];
				item['internet_payments'] = G_vend_data[i][13];
				item['total_payments'] = G_vend_data[i][14];
				item['correction'] = G_vend_data[i][15];
				item['creation_date'] = G_vend_data[i][16];
				item['creation_time'] = G_vend_data[i][17];
				L_vend_data.push(item);
			}
        }
        
        CI.I_WinchWeeklySalesListView.render(L_vend_data);
    },
     
    /* Cancel button hit */  
    doCancel: function ()
    {
    	CI.I_WinchShopView.render();
        return false;
    }    
});

function refresh_sales_error ()
{
	alert ("error returned from server requesting refresh");
}

function refresh_sales_success (vend_data)
{
	G_vend_data = JSON.parse(vend_data);
	CI.I_WinchWeeklySalesView.render();			
}


/*************************************/
/* Winchester Weekly Sales List View */
/*************************************/

CI.WinchWeeklySalesListView = Backbone.View.extend(
{
    el: 'div.middiv',
    
    template: _.template($('#T_WinchWeeklySalesListTemplate').html()),
    
    initialize: function () 
    {
        _.bindAll(this, 'render', 'doProceed', 'doCancel', 'doLoading', 'doError'); 
        this.on('doProceed', this.doProceed, this);
        this.on('doCancel', this.doCancel, this);
        this.on('escKey', this.doCancel, this);
    }, 
    
    doLoading: function ()
    {
    	this.$el.html(_.template($('#T_WinchWeeklySalesListLoadingTemplate').html()));
    },
    
    doError: function (errstring)
    {
    	this.$el.html(_.template ( $('#T_WinchWeeklySalesListErrorTemplate').html())({errstring:errstring}));
    },
    
    /* Entry point for winchester weekly list view */  
   	render: function (vend_data) 
    {
    	console.log (vend_data);
    
    	self = this;
        
        furn_total = 0.00;
        hw_total = 0.00;
        paint_total = 0.00;
        discount_total = 0.00;
        romsey_total = 0.00;
        books_total = 0.00;
        total_total = 0.00;
        total_expenses = 0.00;
		last_update_date = "";
		last_update_time = "";
        
        mydata = [];
        ndays = 0;
        nlines = 0;
        for (key in vend_data)
    	{
    		myitem = [];
    		myitem['date'] = format_y_m_d_to_d_mname_y(vend_data[key].date)
    		myitem['day'] = vend_data[key].day.substr(0,3)
    		myitem['furn_sales'] = vend_data[key].furn_sales
    		furn_total = furn_total + parseFloat(vend_data[key].furn_sales)
    		myitem['hw_sales'] = vend_data[key].hw_sales
    		hw_total = hw_total + parseFloat(vend_data[key].hw_sales)
    		myitem['paint_sales'] = vend_data[key].paint_sales
    		paint_total = paint_total + parseFloat(vend_data[key].paint_sales)
    		myitem['discount'] = vend_data[key].discount_sales
    		discount_total = discount_total + parseFloat(vend_data[key].discount_sales)
    		myitem['romsey_sales'] = vend_data[key].romsey_sales
    		romsey_total = romsey_total + parseFloat(vend_data[key].romsey_sales)
    		myitem['books_sales'] = vend_data[key].books_sales
    		books_total = books_total + parseFloat(vend_data[key].books_sales)
    		myitem['total_sales'] = vend_data[key].total_sales
    		total_total = total_total + parseFloat(vend_data[key].total_sales)
        	mydata.push(myitem);
        	last_update_date = format_y_m_d_to_d_mname_y(vend_data[key].creation_date);
        	last_update_time = vend_data[key].creation_time;
        	if (vend_data[key].total_sales != 0)
        	{
        		ndays++;
        	}
        	nlines++;
    	}
        
        mytotals = [];
        mytotals['furn_total'] = furn_total.toFixed(2);
        mytotals['hw_total'] = hw_total.toFixed(2);
        mytotals['paint_total'] = paint_total.toFixed(2);
        mytotals['discount_total'] = discount_total.toFixed(2);
        mytotals['romsey_total'] = romsey_total.toFixed(2);
        mytotals['books_total'] = books_total.toFixed(2);
        mytotals['total_total'] = total_total.toFixed(2);
        
        daily_average = "N/A";
        if (ndays != 0)
        {
        	if (ndays == 1)
        	{
        		daily_average = "Daily Average (1 day) = £" + (total_total/ndays).toFixed(2);
        	}
        	else
        	{
        		daily_average = "Daily Average (" + ndays + " days) = £" + (total_total/ndays).toFixed(2);
        	}
        }
        
        if (last_update_date != "")
        {
        	update_text = "Updated " + last_update_date + " at " +  last_update_time;
        }	
        else
        {
        	update_text = "No Rpi updates for this week"
        }
        
      	clean_divs ('L', this, 'C'); 
        this.$el.html(this.template({WinchWeeklyData: mydata, WinchWeeklyTotals: mytotals, update_text: update_text, daily_average: daily_average}));  
        
        var html = "";
        html = html + '<h4 style="margin-top:0px">Week (Monday-Sunday) Sales by Vend category</h4>'; 
        html = html + '<h4 style="margin-top:0px">' + daily_average + '</h4>'; 
        html = html + '<table class="hoverTable" id="WinchWeeklyGrid" style="font-size:13px;" width="100%" border="1" cellspacing="1" cellpadding="5">';
        html = html + '<tr>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Date</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Day</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Furn Sales</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>HW Sales</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Paint Sales</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Disc.</b></td>';
    	html = html + "<td class='tablehdr' width='4%' align='center'><b>R\'sey Sales</b></td>";
    	html = html + '<td class="tablehdr" width="4%" align="center"><b>Book Sales</b></td>';
    	html = html + '<td class="tablehdr" width="4%" align="center"><b>Total Sales</b></td>';
        html = html + '</tr>';
        
        for (var i=0; i<mydata.length; i++)
        {
        	html = html + '<tr data-id=1>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['date'] + '</td>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['day'] + '</td>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['furn_sales'] + '</td>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['hw_sales'] + '</td>';  
            html = html + '<td align="center" class="tabledata">' + mydata[i]['paint_sales'] + '</td>';            
            html = html + '<td align="center" class="tabledata">' + mydata[i]['discount'] + '</td>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['romsey_sales'] + '</td>'; 
            html = html + '<td align="center" class="tabledata">' + mydata[i]['books_sales'] + '</td>';   
            html = html + '<td align="center" class="tabledata">' + mydata[i]['total_sales'] + '</td>';            
        	html = html + '</tr>';
        }
        
        html = html + '<tr>';
		html = html + '<td class="tabledata" align="center"><b>Week Mon-Sun</b></td>';
		html = html + '<td class="tabledata" align="center"><b>Totals</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['furn_total'] + '</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['hw_total'] + '</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['paint_total'] + '</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['discount_total'] + '</b></td>'; 
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['romsey_total'] + '</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['books_total'] + '</b></td>'; 
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['total_total'] + '</b></td>';
        html = html + '</tr>';
        
        html = html + '</table>';
        html = html + '<h4>' + update_text + '</h4>'; 
    
        $('#main_table').html (html); 
    },
    
    /* remove */
    remove: function() 
    {
        this.undelegateEvents();
        this.$el.empty();
        this.stopListening();
        return this;
    },
    
    /* Continue */
    doProceed: function ()
    {	
    	self = this;
    },
    
	/* Cancel button hit */  
    doCancel: function ()
    {
    	window.history.back();
        return false;
    }    
});

/***********************************/
/* Winchester Weekly Payments View */
/***********************************/

CI.WinchWeeklyPaymentsView = Backbone.View.extend(
{
    el: 'div.topdiv',
    
    template: _.template($('#T_WinchWeeklyPaymentsTemplate').html()),
    
    initialize: function () 
    {
        _.bindAll(this, 'render', 'doProceed', 'doCancel', 'doFunction'); 
        this.on('doProceed', this.doProceed, this);
        this.on('doFunction', this.doFunction, this);
        this.on('doCancel', this.doCancel, this);
        this.on('escKey', this.doCancel, this);
    }, 
      
    /* Entry point for winchester weekly view */  
   	render: function () 
    {	
    	var self = this;
        
        CI.I_WinchWeeklyPaymentsListView = new CI.WinchWeeklyPaymentsListView();
        
      	clean_divs (this, 'C', 'C'); 
        this.$el.html(this.template());
                
		$(document).on('change', "input[name=formDate]", function() 
		{ 
			self.doProceed();
		});   
            
        this.setdates();
    },
    
    remove: function() 
    {
        this.undelegateEvents();
        this.$el.empty();
        this.stopListening();
        return this;
    },
    
    setdates: function()
    {
    	dateFormModel.set('formDate',  format_date_to_d_mname_y(CI.the_date)); 
		this.myform = new dateForm({ el: $("#winchWeeklyForm") });
		this.myform.render();
		
		s1 = "<button id='button1' type='button' style='margin-bottom:10px;' class='btn btn-primary btn-sm'>Today</button>";
		s2 = "<button id='button2' type='button' style='margin-left:10px;margin-bottom:10px;' class='btn btn-primary btn-sm'>Week+</button>";
		s3 = "<button id='button3' type='button' style='margin-left:10px;margin-bottom:10px;' class='btn btn-primary btn-sm'>Week-</button>";
	
		$("label.control-label").html("<span style='padding-bottom:20px;'>" + s1 + s2 + s3 + "</span>");
		
		$("div.form-group.formDay", true);
	 
	 	$("#button1").click(function() 
		{ 
			console.log ("button 1 clicked");
			CI.the_date = new Date();
    		CI.I_WinchWeeklyPaymentsView.setdates();
		});   
		$("#button2").click(function() 
		{ 
			CI.the_date.setDate(CI.the_date.getDate()+7);
    		console.log (CI.the_date);
    		CI.I_WinchWeeklyPaymentsView.setdates();
		}); 
		$("#button3").click(function() 
		{ 
			CI.the_date.setDate(CI.the_date.getDate()-7);
    		console.log (CI.the_date);
    		CI.I_WinchWeeklyPaymentsView.setdates();
		});     
	 
		CI.I_WinchWeeklyPaymentsView.doProceed();	
    },
    
    /* Continue */ 
    doFunction: function (n)
    {
    	if (n=='switch')
    	{
    		$(document).unbind('change');
    		CI.I_WinchWeeklySalesView.render();	
    	}
    	else if (n=='refresh')
    	{
    		$('#main_table').html ("<b style='font-size:18px'>Loading...</b>"); 
    		google.script.run
   				.withSuccessHandler(refresh_payments_success)
   				.withFailureHandler(refresh_payments_error)
   				.withUserObject(this)
   				.refresh_vend_data();    	
    	}
    	else
    	{
    		alert ("bad function call");
    	}
    },
    
    
    /* Continue */
    doProceed: function ()
    {	
    	CI.the_date = new Date($('input[name=formDate]').val());
	
		CI.I_WinchWeeklyPaymentsListView.doLoading();
    	
    	var monday = moment(CI.the_date).startOf('isoweek').toDate();
		var sunday  = moment(CI.the_date).endOf('isoweek').toDate();
    	
    	dm = monday.getFullYear() + '-' + ('0' + (monday.getMonth()+1)).slice(-2) + '-' + ('0' + monday.getDate()).slice(-2);
    	ds = sunday.getFullYear() + '-' + ('0' + (sunday.getMonth()+1)).slice(-2) + '-' + ('0' + sunday.getDate()).slice(-2);
    	
    	var dm_date = new Date(dm);
        var ds_date = new Date(ds);
        
		var L_vend_data = [];
        for (i=2; i<G_vend_data.length; i++)
        {
        	var item = {};
        	
        	var a_date = new Date(G_vend_data[i][0]);
        	
        	if ((a_date>=dm_date) && (a_date<=ds_date))
        	{        	
				item['date'] = G_vend_data[i][0];
				item['day'] = G_vend_data[i][1];
				item['furn_sales'] = G_vend_data[i][2];
				item['hw_sales'] = G_vend_data[i][3];
				item['paint_sales'] = G_vend_data[i][4];
				item['discount_sales'] = G_vend_data[i][5];
				item['romsey_sales'] = G_vend_data[i][6];
				item['books_sales'] = G_vend_data[i][7];
				item['total_sales'] = G_vend_data[i][8];
				item['cash_payments'] = G_vend_data[i][9];
				item['card_payments'] = G_vend_data[i][10];
				item['cheque_payments'] = G_vend_data[i][11];
				item['bacs_payments'] = G_vend_data[i][12];
				item['internet_payments'] = G_vend_data[i][13];
				item['total_payments'] = G_vend_data[i][14];
				item['correction'] = G_vend_data[i][15];
				item['creation_date'] = G_vend_data[i][16];
				item['creation_time'] = G_vend_data[i][17];
				L_vend_data.push(item);
			}
        }
        
        CI.I_WinchWeeklyPaymentsListView.render(L_vend_data);
    },
     
    /* Cancel button hit */  
    doCancel: function ()
    {
    	CI.I_WinchShopView.render();
        return false;
    }    
});

function refresh_payments_error ()
{
	alert ("error returned from server requesting refresh");
}

function refresh_payments_success (vend_data)
{
	G_vend_data = JSON.parse(vend_data);
	CI.I_WinchWeeklyPaymentsView.render();			
}

/****************************************/
/* Winchester Weekly Payments List View */
/****************************************/

CI.WinchWeeklyPaymentsListView = Backbone.View.extend(
{
    el: 'div.middiv',
    
    template: _.template($('#T_WinchWeeklyPaymentsListTemplate').html()),
    
    initialize: function () 
    {
        _.bindAll(this, 'render', 'doProceed', 'doCancel', 'doLoading', 'doError'); 
        this.on('doProceed', this.doProceed, this);
        this.on('doCancel', this.doCancel, this);
        this.on('escKey', this.doCancel, this);
    }, 
    
    doLoading: function ()
    {
    	this.$el.html(_.template($('#T_WinchWeeklyPaymentsListLoadingTemplate').html()));
    },
    
    doError: function (errstring)
    {
    	this.$el.html(_.template ( $('#T_WinchWeeklyPaymentsListErrorTemplate').html())({errstring:errstring}));
    },
    
    /* Entry point for winchester weekly list view */  
   	render: function (vend_data) 
    {	
    	self = this;
        
        cash_total = 0.00;
        card_total = 0.00;
        cheque_total = 0.00;
        bacs_total = 0.00;
        internet_total = 0.00;
        total_total = 0.00;
		last_update_date = "";
		last_update_time = "";
        
        mydata = [];
        ndays = 0;
        for (key in vend_data)
    	{
    		myitem = [];
    		myitem['date'] = format_y_m_d_to_d_mname_y(vend_data[key].date)
    		myitem['day'] = vend_data[key].day.substr(0,3)
    		
    		myitem['cash_payments'] = vend_data[key].cash_payments
    		cash_total = cash_total + parseFloat(vend_data[key].cash_payments)
    		
    		myitem['card_payments'] = vend_data[key].card_payments
    		card_total = card_total + parseFloat(vend_data[key].card_payments)
    		
    		myitem['cheque_payments'] = vend_data[key].cheque_payments
    		cheque_total = cheque_total + parseFloat(vend_data[key].cheque_payments)
    		
    		myitem['bacs_payments'] = vend_data[key].bacs_payments
    		bacs_total = bacs_total + parseFloat(vend_data[key].bacs_payments)
    		
    		myitem['internet_payments'] = vend_data[key].internet_payments
    		internet_total = internet_total + parseFloat(vend_data[key].internet_payments)
    		
    		myitem['total_payments'] = vend_data[key].total_payments
    		total_total = total_total + parseFloat(vend_data[key].total_payments)
    		
        	mydata.push(myitem);
        	last_update_date = format_y_m_d_to_d_mname_y(vend_data[key].creation_date);
        	last_update_time = vend_data[key].creation_time;
        	if (vend_data[key].total_sales != 0)
        	{
        		ndays++;
        	}
    	}
        
        mytotals = [];
        mytotals['cash_total'] = cash_total.toFixed(2);
        mytotals['card_total'] = card_total.toFixed(2);
        mytotals['cheque_total'] = cheque_total.toFixed(2);
        mytotals['bacs_total'] = bacs_total.toFixed(2);
        mytotals['internet_total'] = internet_total.toFixed(2);
        mytotals['total_total'] = total_total.toFixed(2);
        
        daily_average = "N/A";
        if (ndays != 0)
        {
        	if (ndays == 1)
        	{
        		daily_average = "Daily Average (1 day) = £" + (total_total/ndays).toFixed(2);
        	}
        	else
        	{
        		daily_average = "Daily Average (" + ndays + " days) = £" + (total_total/ndays).toFixed(2);
        	}
        }
        
        if (last_update_date != "")
        {
        	update_text = "Updated " + last_update_date + " at " +  last_update_time;
        }	
        else
        {
        	update_text = "No Rpi updates for this week"
        }
        
      	clean_divs ('L', this, 'C'); 
        this.$el.html(this.template({WinchWeeklyData: mydata, WinchWeeklyTotals: mytotals, update_text: update_text, daily_average: daily_average}));
        
        var html = "";
        html = html + '<h4 style="margin-top:0px">Week (Monday-Sunday) Sales by Vend category</h4>'; 
        html = html + '<h4 style="margin-top:0px">' + daily_average + '</h4>'; 
        html = html + '<table class="hoverTable" id="WinchWeeklyGrid" style="font-size:13px;" width="100%" border="1" cellspacing="1" cellpadding="5">';
        html = html + '<tr>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Date</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Day</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Cash</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Card</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>Cheque</b></td>';
        html = html + '<td class="tablehdr" width="4%" align="center"><b>BACS</b></td>';
    	html = html + "<td class='tablehdr' width='4%' align='center'><b>Internet</b></td>";
    	html = html + '<td class="tablehdr" width="4%" align="center"><b>Total</b></td>';
        html = html + '</tr>';
        
        for (var i=0; i<mydata.length; i++)
        {
        	html = html + '<tr data-id=1>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['date'] + '</td>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['day'] + '</td>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['cash_payments'] + '</td>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['card_payments'] + '</td>';  
            html = html + '<td align="center" class="tabledata">' + mydata[i]['cheque_payments'] + '</td>';            
            html = html + '<td align="center" class="tabledata">' + mydata[i]['bacs_payments'] + '</td>';
            html = html + '<td align="center" class="tabledata">' + mydata[i]['internet_payments'] + '</td>'; 
            html = html + '<td align="center" class="tabledata">' + mydata[i]['total_payments'] + '</td>';            
        	html = html + '</tr>';
        }
        
        html = html + '<tr>';
		html = html + '<td class="tabledata" align="center"><b>Week Mon-Sun</b></td>';
		html = html + '<td class="tabledata" align="center"><b>Totals</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['cash_total'] + '</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['card_total'] + '</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['cheque_total'] + '</b></td>';
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['bacs_total'] + '</b></td>'; 
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['internet_total'] + '</b></td>'; 
		html = html + '<td class="tabledata" align="center"><b>' + mytotals['total_total'] + '</b></td>';
        html = html + '</tr>';
        html = html + '</table>';
    
    	html = html + '<h4>' + update_text + '</h4>'; 
    
        $('#main_table').html (html); 
    },
    
    /* remove */
    remove: function() 
    {
        this.undelegateEvents();
        this.$el.empty();
        this.stopListening();
        return this;
    },
    
    /* Continue */
    doProceed: function ()
    {	
    	self = this;
    },
    
	/* Cancel button hit */  
    doCancel: function ()
    {
    	window.history.back();
        return false;
    }    
});
