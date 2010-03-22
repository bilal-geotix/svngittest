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
import java.util.ArrayList;


/**
 * Class representing a collection of EEA air quality measurements.
 * Only a prototype for testing purposes but not fully functional.
 * 
 * @author katharina
 *
 */
public class MeasurementCollection implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private ArrayList<Measurement> meas;
	private int count;
	private String component;
	private String from;
	private String to;
	private Station st;
	private int nas = 0;
	
	/**
	 * @param meas
	 */
	public MeasurementCollection(ArrayList<Measurement> meas) {
		this.meas = meas;
	}
	
	/**
	 * @return
	 */
	public int getCount() {
		return this.meas.size();
	}
	
	/**
	 * @return
	 */
	public double calcMean() {
		double mean = -999;
		double sum = 0;
		int count = 0;
		for (Measurement m : this.meas) {
			if (m != null) {
				sum = sum+m.getValue();
				count++;
			} else {
				this.nas++;
			}
		}
		if (count != 0) {
		mean = sum/count;
		}
		return mean;
	}

	/**
	 * @return
	 */
	public ArrayList<Measurement> getMeas() {
		return meas;
	}

	/**
	 * @param meas
	 */
	public void setStats(ArrayList<Measurement> meas) {
		this.meas = meas;
	}
	
	/**
	 * @param time
	 * @return
	 */
	public Measurement getMeasurement(String time) {
		Measurement m = null;
		for (Measurement mea: meas) {
			if (m.getTimeFrom().equals(time)) {
				m = mea;
			}
		}
		return m;
	}
	
	/**
	 * @param m
	 * @return
	 */
	public boolean contains(Measurement m) {
		String t = m.getTimeFrom();
		boolean there = false;
		for (Measurement mea : meas) {
			if (mea.getTimeFrom().equals(t)) {
				there = true;
			}
		}
		return there;
	}
	
	/**
	 * @param m
	 */
	public void addMeasurement(Measurement m) {
		meas.add(m);
	}
	
	/**
	 * @return
	 */
	public double[] getXvalues() {
		double[] x = new double[meas.size()];
		for (int j = 0; j<meas.size(); j++) {	
			Measurement m = meas.get(j);
			if (m != null) {
				String d = m.getTimeTo();
				d.replace("-", "");
				d.replace(" ", "");
				d.replace(":", "");
				String ds = d.substring(d.length()-2);
				double v = Double.parseDouble(ds);
				x[j] = v;
			}
		}
		return x;
	}
	
	/**
	 * @return
	 */
	public double[] getYvalues() {
		double[] y = new double[meas.size()];
		for (int j = 0; j<meas.size(); j++) {	
			Measurement m = meas.get(j);
			if (m != null) {
				double v = m.getValue();
				y[j] = v;
			} 
		}
		return y;
	}	

	/**
	 * @return
	 */
	public Station getSt() {
		return st;
	}

	/**
	 * @param st
	 */
	public void setSt(Station st) {
		this.st = st;
	}
}
