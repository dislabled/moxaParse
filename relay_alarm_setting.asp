<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<script type="text/javascript">
<!--

	function PortRelaySet(){

		if(document.relay_alarm_form.relay1_checkbox.checked==true){
			port_relay_frame.document.getElementById("relay1_enable").value=1;
		}else{
			port_relay_frame.document.getElementById("relay1_enable").value=0;
		}

		if( document.relay_alarm_form.relay2_checkbox ){
			if(document.relay_alarm_form.relay2_checkbox.checked==true){
				port_relay_frame.document.getElementById("relay2_enable").value=1;
			}else{
				port_relay_frame.document.getElementById("relay2_enable").value=0;
			}
		}
		port_relay_frame.document.getElementById("power1_select").value=document.relay_alarm_form.power1_relay_select.options[document.relay_alarm_form.power1_relay_select.selectedIndex].value;
		port_relay_frame.document.getElementById("power2_select").value=document.relay_alarm_form.power2_relay_select.options[document.relay_alarm_form.power2_relay_select.selectedIndex].value;

		if( document.relay_alarm_form.di1onoff_relay_select ){
			port_relay_frame.document.getElementById("di1onoff_select").value=document.relay_alarm_form.di1onoff_relay_select.options[document.relay_alarm_form.di1onoff_relay_select.selectedIndex].value;
		}

		if( document.relay_alarm_form.di1offon_relay_select ){
			port_relay_frame.document.getElementById("di1offon_select").value=document.relay_alarm_form.di1offon_relay_select.options[document.relay_alarm_form.di1offon_relay_select.selectedIndex].value;
		}

		if( document.relay_alarm_form.di2onoff_relay_select ){
			port_relay_frame.document.getElementById("di2onoff_select").value=document.relay_alarm_form.di2onoff_relay_select.options[document.relay_alarm_form.di2onoff_relay_select.selectedIndex].value;
		}

		if( document.relay_alarm_form.di2offon_relay_select ){
			port_relay_frame.document.getElementById("di2offon_select").value=document.relay_alarm_form.di2offon_relay_select.options[document.relay_alarm_form.di2offon_relay_select.selectedIndex].value;
		}

		/* Yenting (2007.10.01) - If the Turbo Ring is borken, relay warning is on. */
		if( document.relay_alarm_form.ring_relay_select ){
			port_relay_frame.document.getElementById("ringrelay_select").value=document.relay_alarm_form.ring_relay_select.options[document.relay_alarm_form.ring_relay_select.selectedIndex].value;
		}
		/* Yenting (2007.10.01) - End */

		port_relay_frame.document.getElementById("show_form").submit();
	}

	function AccountDiff(){
		CheckCookie();

		theData = "";
		theName = "AccountName508=";
		theCookie = document.cookie+";";
		start = theCookie.indexOf(theName);
		if(start != -1){
			end=theCookie.indexOf(";",start);
			theData = unescape(theCookie.substring(start+theName.length,end));
		}

		var i;
		if(theData=="user"){
			for(i=0;i<document.getElementsByTagName("input").length;i++){
				document.getElementsByTagName("input")[i].disabled=true;
				if(i!=0 && i!=1){
					document.getElementsByTagName("input")[i].style.backgroundColor="#F5F5F5";
				}
			}
			for(i=0;i<document.getElementsByTagName("select").length;i++){
				document.getElementsByTagName("select")[i].disabled=true;
				document.getElementsByTagName("select")[i].style.backgroundColor="#F5F5F5";
			}
		}
	}

	function stopSubmit(){
		return false;
	}
	function touchLasttime()
	{
							theName = "lasttime";
					expires = null;
					now=new Date( );
					document.cookie =theName + "=" + now.getTime() + "; path=/" + ((expires == null) ? " " : "; expires = " +expires.toGMTString());

	}
	function CheckCookie()
	{
		
	}

//-->
</script>
</head>

<body bgcolor="#CCE6E6" text="#000000" topmargin="10" leftmargin="12" onLoad="AccountDiff()">
<form method="post" name="relay_alarm_form" onClick="touchLasttime()" onkeypress="touchLasttime()" onSubmit="return stopSubmit()">
<div align="left">
	<font size="5" face="Arial, Helvetica, sans-serif, Marlett" color="#007C60">
	<!-- ---------------------------------- -->
    <b>Relay Warning Events Settings</b></font>
	<!-- ---------------------------------- -->
</div>
<div align="left">
<table width="100%" border="0">
  	<tr>
		<td width="3%"><div align="left"><font size="3" face="Arial, Helvetica, sans-serif, Marlett">
      		</font></div></td>
		<td width="97%" colspan="4"><div align="left"><font size="3" face="Arial, Helvetica, sans-serif, Marlett" color="#FF9900">
			<!-- ----------- -->
      		<b>System Events</b>
			<!-- ---------- --->
      	</font></div></td>
  	</tr>
	<tr>
		<td width="3%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
      		</font></div></td>
      	<td width="3%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
      		</font></div></td>
		<td width="94%" colspan="3"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
			<table width="100%" border="0">
				<tr>
					<td width="50%" colspan="2"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
						<!-- ---------------------------- -->
      					<input type="checkbox" name="relay1_checkbox" ><B>Override Relay Warning Settings</B>
						<!-- ---------------------------- -->
      					</font></div></td>
					<td width="50%" colspan="2"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
						<!-- ---------------------------- -->
      					
						<!-- ---------------------------- -->
      					</font></div></td>
  				</tr>
  				<tr>
   					<td width="50%" colspan="2"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
						<!-- --------------------- -->
   						Power Input 1 failure(On->Off)
						<!-- --------------------- -->
   						<select name="power1_relay_select" size="1">
							<!-- ---------------------------- -->
   							<option value="0" selected >Disable</option><option value="1" >Enable</option>
							<!-- ---------------------------- -->
   						</select>
   						</font></div></td>
   					<td width="50%" colspan="2"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
						<!-- --------------------- -->
   						Power Input 2 failure(On->Off)
						<!-- --------------------- -->
   						<select name="power2_relay_select" size="1">
							<!-- ---------------------------- -->
   							<option value="0" selected >Disable</option><option value="1" >Enable</option>
							<!-- ---------------------------- -->
   						</select>
   						</font></div></td>
  				</tr>
				<!-- ----------------------- -->
  				
				<!-- ----------------------- -->
  				<!-- Yenting (2007.10.01) - If the Turbo Ring is borken, relay warning is on. -->
  				<tr>
   					<td width="50%" colspan="2"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
						<!-- ------------------------------- -->
   						Turbo Ring Break<select name="ring_relay_select" size="1" disabled><option value="0" selected >Disable</option><option value="1">Enable</option></select>
						<!-- ------------------------------- -->
   						</font></div></td>
   					<td width="50%" colspan="2"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
   						</font></div></td>
  				</tr>
  				<!-- Yenting (2007.10.01 - End -->
			</table></font></div></td>
  	</tr>
  	<tr>
		<td width="3%"><div align="left"><font size="3" face="Arial, Helvetica, sans-serif, Marlett">
      		</font></div></td>
		<td width="97%" colspan="2"><div align="left"><font size="3" face="Arial, Helvetica, sans-serif, Marlett" color="#FF9900">
			<!-- -------- -->
      		<b>Port Events</b></font></div></td>
			<!-- -------- -->
  	</tr>
	<tr>
		<td width="3%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
      		</font></div></td>
      	<td width="3%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
      		</font></div></td>
		<td width="620"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
			<table width="620" border="0">
  				<tr bgcolor="#007C60">
					<td width="13%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett" color="#FFFFFF">
      					Port</font></div></td>
      				<td width="22%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett" color="#FFFFFF">
      					Link</font></div></td>
      				<td width="25%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett" color="#FFFFFF">
      					Traffic-Overload</font></div></td>
      				<td width="20%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett" color="#FFFFFF">
      					Rx-Threshold(%)</font></div></td>
      				<td width="20%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett" color="#FFFFFF">
      					Traffic-Duration(s)</font></div></td>
      			</tr>
  			</table>
		</font></div></td>
	</tr>
	<tr>
		<td width="3%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
      		</font></div></td>
      	<td width="3%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
      		</font></div></td>
		<td width="94%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
			<!-- --------------------------------------------------------- -->
			<iframe name="port_relay_frame" src="relay_alarm_setting_show.asp" width="637" height="229" marginHeight="0" marginWidth="0" frameBorder="0">
			<!-- --------------------------------------------------------- -->
			</iframe></font></div></td>
  	</tr>
	<tr>
		<td width="3%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
    	</font></div></td>
    	<td width="3%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
    	</font></div></td>
  		<td width="637"><div align="center"><font size="2" face="Arial, Helvetica, sans-serif, Marlett">
		<br><input type="image" src="activate_button.gif" onClick="PortRelaySet()" onMouseover="document.body.style.cursor='hand'" onMouseout="document.body.style.cursor='default'">
		</font></div></td>
	</tr>
</table>
</div>

</form>
</body>
</html>

