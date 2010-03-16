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

import java.awt.Point;
import java.awt.geom.Point2D;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;

/**
 * Class representing an Airbase monitoring station.
 * Only a prototype for testing purposes but not fully functional.
 * 
 * @author katharina
 *
 */
public class Station implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String code;
	private String name;
	private String type;
	private String area;
	private Point2D.Double p;
	private MeasurementCollection obs = new MeasurementCollection(new ArrayList<Measurement>());
	private String beginTimeDay;
	private String beginTimeHour;
	private String endTimeDay;
	private String endTimeHour;

	private String component;
	private boolean pm10 = false;
	private boolean oz = false;
	private boolean no = false;
	
	/**
	 * @param name
	 * @param code
	 * @param type
	 * @param area
	 * @param p
	 */
	public Station(String name, String code, String type, String area, Point2D.Double p) {
		this.area = area;
		this.code = code;
		this.name = name;
		this.type = type;
		this.p = p;
	}
	
	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	public String toString() {
		String s = "EoI: "+this.code+", Lat: "+this.p.x+", Lon: "+this.p.y +", Type: "+this.type+", Area: "+this.area+", "+this.measToString();
		return s;
	}
	
	/**
	 * @return
	 */
	public int getCountMeas() {
		return this.obs.getCount();
	}
	
	/**
	 * @return
	 */
	private String measToString() {
		String s = "[";
		ArrayList<Measurement> meas = this.obs.getMeas();
		for (Measurement m:meas){
			if (m != null)
			s = s + m.getComponent()+", "+m.getTimeTo()+", "+ m.getValue() +", ";
			else 
				s = s + ", ";
		}
		s = s.substring(0, s.length()-1);
		s.concat("]");
		return s;
	}
	
	/**
	 * @param m
	 */
	public void addMeasurement(Measurement m) {
		this.obs.addMeasurement(m);
	}
	
	/**
	 * @return
	 */
	public Point2D.Double getP() {
		return p;
	}

	/**
	 * @param p
	 */
	public void setP(Point2D.Double p) {
		this.p = p;
	}

	/**
	 * @return
	 */
	public MeasurementCollection getObs() {
		return obs;
	}

	/**
	 * @param meas
	 */
	public void setObs (MeasurementCollection meas) {
		this.obs = meas;
	}
	
	/**
	 * @return
	 */
	public double getLon() {
		return this.p.x;
	}
	
	/**
	 * @return
	 */
	public double getLat() {
		return this.p.y;
	}
	
	/**
	 * @return
	 */
	public String sensorToSql() {
		return "INSERT INTO feature_of_interest (feature_of_interest_id, feature_of_interest_name, feature_of_interest_description, geom, feature_type) VALUES ('"+this.code+"', '"+this.code+"', '"+this.name+"', GeometryFromText('POINT("+this.p.getX()+" "+this.p.getY()+")', 4326),'sa:SamplingPoint');";
	}
	
	/**
	 * @return
	 */
	public String getCode() {
		return code;
	}
	/**
	 * @param code
	 */
	public void setCode(String code) {
		this.code = code;
	}
	/**
	 * @return
	 */
	public Point.Double getSp() {
		return p;
	}
	/**
	 * @param sp
	 */
	public void setSp(Point.Double sp) {
		this.p = p;
	}
	/**
	 * @return
	 */
	public String getName() {
		return name;
	}
	/**
	 * @param name
	 */
	public void setName(String name) {
		this.name = name;
	}
	/**
	 * @return
	 */
	public String getType() {
		return type;
	}
	/**
	 * @param type
	 */
	public void setType(String type) {
		this.type = type;
	}
	/**
	 * @return
	 */
	public String getArea() {
		return area;
	}
	/**
	 * @param area
	 */
	public void setArea(String area) {
		this.area = area;
	}

	/**
	 * @return
	 */
	public boolean isPm10() {
		return pm10;
	}

	/**
	 * @param pm10
	 */
	public void setPm10(boolean pm10) {
		this.pm10 = pm10;
	}

	/**
	 * @return
	 */
	public boolean isOz() {
		return oz;
	}

	/**
	 * @param oz
	 */
	public void setOz(boolean oz) {
		this.oz = oz;
	}

	/**
	 * @return
	 */
	public boolean isNo() {
		return no;
	}

	/**
	 * @param no
	 */
	public void setNo(boolean no) {
		this.no = no;
	}

	/**
	 * @return
	 */
	public String getComponent() {
		return component;
	}

	/**
	 * @param component
	 */
	public void setComponent(String component) {
		this.component = component;
	}

	/**
	 * @return
	 */
	public String getBeginTimeDay() {
		return beginTimeDay;
	}

	/**
	 * @param beginTimeDay
	 */
	public void setBeginTimeDay(String beginTimeDay) {
		this.beginTimeDay = beginTimeDay;
	}

	/**
	 * @return
	 */
	public String getBeginTimeHour() {
		return beginTimeHour;
	}

	/**
	 * @param beginTimeHour
	 */
	public void setBeginTimeHour(String beginTimeHour) {
		this.beginTimeHour = beginTimeHour;
	}

	/**
	 * @return
	 */
	public String getEndTimeDay() {
		return endTimeDay;
	}

	/**
	 * @param endTimeDay
	 */
	public void setEndTimeDay(String endTimeDay) {
		this.endTimeDay = endTimeDay;
	}

	/**
	 * @return
	 */
	public String getEndTimeHour() {
		return endTimeHour;
	}

	/**
	 * @param endTimeHour
	 */
	public void setEndTimeHour(String endTimeHour) {
		this.endTimeHour = endTimeHour;
	}
}
