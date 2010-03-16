/***************************************************************
 This program is free software; you can redistribute and/or modify it under 
 the terms of the GNU General Public License version 2 as published by the 
 Free Software Foundation.

 This program is distributed WITHOUT ANY WARRANTY; even without the implied
 WARRANTY OF MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public License along with
 this program (see gnu-gpl v2.txt). If not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA or
 visit the Free Software Foundation web page, http://www.fsf.org.
***************************************************************/


package de.ifgi.airquality.eea.datamodel;

import java.io.Serializable;


/**
 * Class represnting an EEA air quality measurement.
 * Only a prototype for testing purposes but not fully functional.
 * 
 * @author katharina
 *
 */
public class Measurement implements Serializable {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String component;
	private String qualAss;
	private String qualCon;
	private double value;
	private double avTime;
	private String timeFrom;
	private String timeTo;
	private int day;
	private int hour;
	
//	<component>Ozone</component>
//	<datetime_from>2009-02-25 00:00</datetime_from>
//	<datetime_to>2009-02-25 01:00</datetime_to>
//	<averaged_time>60</averaged_time>
//	<value>15</value>
//	<quality_assurance>1</quality_assurance>
//	<quality_control>0</quality_control>
	
	public Measurement(double val, String timeTo) {
		this.value = val;
		this.timeTo = timeTo;		
	}
		
	public Measurement(String component, String timeFrom, String timeTo, double avTime, double value, String qualAss, String qualCon) {
		this.avTime = avTime;
		this.component = component;
		this.qualAss = qualAss;
		this.qualCon = qualCon;
		this.timeFrom = timeFrom;
		this.timeTo = timeTo;
		this.value = value;
	}

	public Measurement(double val, String day, String hour) {
		this.value = val;
		this.day = Integer.parseInt(day);
		this.hour = Integer.parseInt(hour);
	}

	public String getComponent() {
		return component;
	}
	
	public void setComponent(String component) {
		this.component = component;
	}
	public String isQualAss() {
		return qualAss;
	}
	public void setQualAss(String qualAss) {
		this.qualAss = qualAss;
	}
	public String isQualCon() {
		return qualCon;
	}
	public void setQualCon(String qualCon) {
		this.qualCon = qualCon;
	}
	public double getValue() {
		return value;
	}
	public void setValue(double value) {
		this.value = value;
	}
	public double getAvTime() {
		return avTime;
	}
	public void setAvTime(double avTime) {
		this.avTime = avTime;
	}
	public String getTimeFrom() {
		return timeFrom;
	}
	public void setTimeFrom(String timeFrom) {
		this.timeFrom = timeFrom;
	}
	public String getTimeTo() {
		return timeTo;
	}
	public void setTimeTo(String timeTo) {
		this.timeTo = timeTo;
	}
	
}
