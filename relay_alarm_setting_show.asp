<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<script type="text/javascript">
<!-- 
	var i;
	
	function TrafficRelay(i){
		i=i-1;		
		if(document.getElementsByTagName("select")[1+i*2].options[document.getElementsByTagName("select")[1+i*2].selectedIndex].value!=0){
			document.getElementsByTagName("input")[2*i].disabled=false;
			document.getElementsByTagName("input")[2*i].style.backgroundColor="#FFFFFF";
			document.getElementsByTagName("input")[2*i+1].disabled=false;
			document.getElementsByTagName("input")[2*i+1].style.backgroundColor="#FFFFFF";	
		}else{
			document.getElementsByTagName("input")[2*i].disabled=true;
			document.getElementsByTagName("input")[2*i].style.backgroundColor="#F5F5F5";
			document.getElementsByTagName("input")[2*i+1].disabled=true;					
			document.getElementsByTagName("input")[2*i+1].style.backgroundColor="#F5F5F5";
		}		
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
	function AccountDiff(){	
	
		var j;
		CheckCookie();
		for(i=0;i<(document.getElementsByTagName("select").length)/2;i++){
			j=i+1;
			TrafficRelay(j);
		}		
		
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
				document.getElementsByTagName("input")[i].style.backgroundColor="#F5F5F5";
			}
			for(i=0;i<document.getElementsByTagName("select").length;i++){
				document.getElementsByTagName("select")[i].disabled=true;
				document.getElementsByTagName("select")[i].style.backgroundColor="#F5F5F5";
			}					
		}		
			
	}		
	
//-->
</script>
</head>

<body bgcolor="#CCE6E6" text="#000000" topmargin="0" leftmargin="0" onLoad="AccountDiff()">
<form method="post" name="show_form" id="show_form" onClick="touchLasttime()" onkeypress="touchLasttime()" action="/goform/AlarmEventType" target="mid">
<div align="left">
<table width="620" border="0">	
	<tr> 
		<td width="13%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett"> 
      	</font></div></td>
      	<td width="22%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett"> 
      	</font></div></td>
      	<td width="25%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett"> 
      	</font></div></td>
      	<td width="20%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett"> 
      	</font></div></td>
      	<td width="20%"><div align="left"><font size="2" face="Arial, Helvetica, sans-serif, Marlett"> 
      	</font></div></td>	
    </tr>
    <tr bgcolor="#FFFFFF">
<td>1</td>
<td><select name="port1_link_select" size="1">
<option value="0" selected >Ignore</option>
<option value="1" >On</option>
<option value="3" >Off</option>
</select></td>
<td><select name="port1_traffic_select" size="1" onChange="TrafficRelay(1)">

<option value="0" selected >Disable</option>
<option value="1" >Enable</option>
</select></td>
<td><input type="text" name="traffic_value1" size="3" maxlength="3" value="1">
</td>
<td><input type="text" name="traffic_duration1" size="3" maxlength="3" value="1">
</td>
</tr>
<tr bgcolor="#FFFFFF">
<td>2</td>
<td><select name="port2_link_select" size="1">
<option value="0" >Ignore</option>
<option value="1" >On</option>
<option value="3" selected >Off</option>
</select></td>
<td><select name="port2_traffic_select" size="1" onChange="TrafficRelay(2)">

<option value="0" selected >Disable</option>
<option value="1" >Enable</option>
</select></td>
<td><input type="text" name="traffic_value2" size="3" maxlength="3" value="1">
</td>
<td><input type="text" name="traffic_duration2" size="3" maxlength="3" value="1">
</td>
</tr>
<tr bgcolor="#FFFFFF">
<td>3</td>
<td><select name="port3_link_select" size="1">
<option value="0" selected >Ignore</option>
<option value="1" >On</option>
<option value="3" >Off</option>
</select></td>
<td><select name="port3_traffic_select" size="1" onChange="TrafficRelay(3)">

<option value="0" selected >Disable</option>
<option value="1" >Enable</option>
</select></td>
<td><input type="text" name="traffic_value3" size="3" maxlength="3" value="1">
</td>
<td><input type="text" name="traffic_duration3" size="3" maxlength="3" value="1">
</td>
</tr>
<tr bgcolor="#FFFFFF">
<td>4</td>
<td><select name="port4_link_select" size="1">
<option value="0" selected >Ignore</option>
<option value="1" >On</option>
<option value="3" >Off</option>
</select></td>
<td><select name="port4_traffic_select" size="1" onChange="TrafficRelay(4)">

<option value="0" selected >Disable</option>
<option value="1" >Enable</option>
</select></td>
<td><input type="text" name="traffic_value4" size="3" maxlength="3" value="1">
</td>
<td><input type="text" name="traffic_duration4" size="3" maxlength="3" value="1">
</td>
</tr>
<tr bgcolor="#FFFFFF">
<td>5</td>
<td><select name="port5_link_select" size="1">
<option value="0" selected >Ignore</option>
<option value="1" >On</option>
<option value="3" >Off</option>
</select></td>
<td><select name="port5_traffic_select" size="1" onChange="TrafficRelay(5)">

<option value="0" selected >Disable</option>
<option value="1" >Enable</option>
</select></td>
<td><input type="text" name="traffic_value5" size="3" maxlength="3" value="1">
</td>
<td><input type="text" name="traffic_duration5" size="3" maxlength="3" value="1">
</td>
</tr>
<tr bgcolor="#FFFFFF">
<td>6</td>
<td><select name="port6_link_select" size="1">
<option value="0" selected >Ignore</option>
<option value="1" >On</option>
<option value="3" >Off</option>
</select></td>
<td><select name="port6_traffic_select" size="1" onChange="TrafficRelay(6)">

<option value="0" selected >Disable</option>
<option value="1" >Enable</option>
</select></td>
<td><input type="text" name="traffic_value6" size="3" maxlength="3" value="1">
</td>
<td><input type="text" name="traffic_duration6" size="3" maxlength="3" value="1">
</td>
</tr>
<tr bgcolor="#FFFFFF">
<td>7</td>
<td><select name="port7_link_select" size="1">
<option value="0" >Ignore</option>
<option value="1" >On</option>
<option value="3" selected >Off</option>
</select></td>
<td><select name="port7_traffic_select" size="1" onChange="TrafficRelay(7)">

<option value="0" selected >Disable</option>
<option value="1" >Enable</option>
</select></td>
<td><input type="text" name="traffic_value7" size="3" maxlength="3" value="1">
</td>
<td><input type="text" name="traffic_duration7" size="3" maxlength="3" value="1">
</td>
</tr>
<tr bgcolor="#FFFFFF">
<td>8</td>
<td><select name="port8_link_select" size="1">
<option value="0" >Ignore</option>
<option value="1" >On</option>
<option value="3" selected >Off</option>
</select></td>
<td><select name="port8_traffic_select" size="1" onChange="TrafficRelay(8)">

<option value="0" selected >Disable</option>
<option value="1" >Enable</option>
</select></td>
<td><input type="text" name="traffic_value8" size="3" maxlength="3" value="1">
</td>
<td><input type="text" name="traffic_duration8" size="3" maxlength="3" value="1">
</td>
</tr>
  		  		
</table>
<input type="hidden" name="relay1_enable" id="relay1_enable" value="">
<input type="hidden" name="relay2_enable" id="relay2_enable" value="">
<input type="hidden" name="power1_select" id="power1_select" value="">
<input type="hidden" name="power2_select" id="power2_select" value="">
<input type="hidden" name="di1onoff_select" id="di1onoff_select" value="">
<input type="hidden" name="di1offon_select" id="di1offon_select" value="">
<input type="hidden" name="di2onoff_select" id="di2onoff_select" value="">
<input type="hidden" name="di2offon_select" id="di2offon_select" value="">
<input type="hidden" name="ringrelay_select" id="ringrelay_select" value=""><!-- For Turbo Ring broken relay warning -->
</div>
</form>
</body>
</html>

