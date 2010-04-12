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

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Serializable;
import java.util.ArrayList;

/**
 * Class representing a collection of Airbase monitoring stations.
 * Only a prototype for testing purposes but not fully functional.
 * 
 * @author katharina
 *
 */
public class StationCollection implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private ArrayList<String> timeStamps;
	private ArrayList<Station> stats;
	private String datasetid;

	/**
	 * @param stats
	 */
	public StationCollection(ArrayList<Station> stats) {
		this.stats = stats;
	}

	/**
	 * @return
	 */
	public ArrayList<Station> getStats() {
		return stats;
	}

	/**
	 * @param stats
	 */
	public void setStats(ArrayList<Station> stats) {
		this.stats = stats;
	}
	
	/**
	 * @param code
	 * @return
	 */
	public Station getStation(String code) {
		Station stat = null;
		for (Station s: stats) {
			if (s.getCode().equals(code)) {
				stat = s;
			}
		}
		return stat;
	}
	
	/**
	 * @param stat
	 * @return
	 */
	public boolean contains(Station stat) {
		String code = stat.getCode();
		boolean there = false;
		for (Station s: stats) {
			if (s.getCode().equals(code)) {
				there = true;
			}
		}
		return there;
	}
	
	/**
	 * @param stat
	 */
	public void addStation(Station stat) {
		stats.add(stat);
	}
	
	/**
	 * @param path
	 * @throws IOException
	 */
	public void toCsv(String path) throws IOException {
		BufferedWriter out = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(new File(path))));
		out.write("code, x, y"+timeStampsToString());
		out.newLine();
		for (Station st : this.stats) {
			 String s = ""+st.toString();
			 out.write(s);
			 out.newLine();
		 }
		 out.close();		
	}

	/**
	 * @return
	 */
	public ArrayList<String> getTimeStamps() {
		return timeStamps;
	}

	/**
	 * @param timeStamps
	 */
	public void setTimeStamps(ArrayList<String> timeStamps) {
		this.timeStamps = timeStamps;
	}

	/**
	 * @return
	 */
	private String timeStampsToString() {
		String s = "";
		for (String t: this.timeStamps) {
			s = s+ ", "+t;
		}
		s = s.substring(0,s.length()-1);
		return s;
	}
}
