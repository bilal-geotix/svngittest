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

package de.ifgi.airquality.eea.io;

import java.awt.geom.Point2D;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.text.ParsePosition;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;

import de.ifgi.airquality.eea.datamodel.Measurement;
import de.ifgi.airquality.eea.datamodel.MeasurementCollection;
import de.ifgi.airquality.eea.datamodel.Station;
import de.ifgi.airquality.eea.datamodel.StationCollection;

/**
 * Parser for the EEA xml files. Parses O3 and PM10 only.
 * Only a prototype for testing purposes but not fully functional.
 * @author katharina
 *
 */
public class WoodstoxParser {

	private StationCollection stations;
	private HashMap<String, Station> hashStats = new HashMap<String, Station>();
	private HashMap<String, Date> hashOld;
	private HashMap<String, Date> hashNew;
	private String parsedDatei;

	/**
	 * 
	 */
	public WoodstoxParser() {
		stations = new StationCollection(new ArrayList<Station>());
		hashNew = hashOld;
	}

	/**
	 * @param file
	 * @throws XMLStreamException
	 * @throws IOException
	 */
	public void parse(String file) throws XMLStreamException, IOException {
		System.out.println("parse it ");
		this.parsedDatei = file;
		File parsedFile = new File(file);
		InputStream input = new FileInputStream(parsedFile);
		System.out.println("Parsing " + parsedFile.getAbsolutePath());
        Map<String,Station> map = new HashMap<String, Station>();
        XMLInputFactory inputFactory = XMLInputFactory.newInstance();
        XMLStreamReader parser = inputFactory.createXMLStreamReader(input);
        for (int event = parser.next();
        event != XMLStreamConstants.END_DOCUMENT;
        event = parser.next()) {
        switch (event) {
        case XMLStreamConstants.START_ELEMENT:
        	System.out.println(parser.getLocalName());
        if (parser.getLocalName().equals("station")) {
        	Station stat = this.parseStation(parser);
        	if (stat.getObs().getMeas().size() != 0) {
        		stations.addStation(stat);
        	}
        }
        break;
        case XMLStreamConstants.END_ELEMENT:
        break;
        case XMLStreamConstants.CHARACTERS:
        break;
        case XMLStreamConstants.CDATA:
        break;
        } // Ende switch
        } // Ende while
        
        input.close();
	}

	/**
	 * @return
	 */
	public String getParsedDatei() {
		return parsedDatei;
	}

	/**
	 * @param parsedDatei
	 */
	public void setParsedDatei(String parsedDatei) {
		this.parsedDatei = parsedDatei;
	}

	/**
	 * @param parser
	 * @return
	 * @throws XMLStreamException
	 */
	private Station parseStation(XMLStreamReader parser)
			throws XMLStreamException {
		ArrayList<String> statDet = new ArrayList<String>();
		ArrayList<String> statComp = new ArrayList<String>();
		ArrayList<Measurement> meas = new ArrayList<Measurement>();
		String e = "";
		do {
			int event = parser.next();
			switch (event) {
			case XMLStreamConstants.START_ELEMENT:
				if (parser.getLocalName().equals("measurement")) {
					Measurement m = this.parseMeasurement(parser);
					if (m.getValue() != -999 && m.getValue() != -111) {
						if (m.getComponent().equals("PM10")) {
							meas.add(m);
							statComp.add("PM10");
						}
						if (m.getComponent().equals("NO2")) {
							meas.add(m);
							statComp.add("NO2");
						}
//						if (m.getComponent().equals("Ozone")) {
//							meas.add(m);
//							statComp.add("Ozone");
//						}
					}
				}
				break;
			case XMLStreamConstants.END_ELEMENT:
				if (parser.getLocalName().equals("station")) {
					e = "rrr";
				}
				break;
			case XMLStreamConstants.CHARACTERS:
				// details of measurement station
				statDet.add(parser.getText());
				// System.out.println(parser.getText());
				break;
			} // Ende switch

		} while (e == "");// Ende while
		boolean pm10, no, oz;
		pm10 = statComp.contains("PM10");
		no = statComp.contains("NO2");
		//oz = statComp.contains("Ozone");
		Point2D.Double p = new Point2D.Double(Double
				.parseDouble(statDet.get(4)), Double
				.parseDouble(statDet.get(5)));
		Station stati = new Station(statDet.get(0), statDet.get(1), statDet
				.get(2), statDet.get(3), p);
		MeasurementCollection measures = new MeasurementCollection(meas);
		stati.setObs(measures);
		stati.setPm10(pm10);
		stati.setNo(no);
		//stati.setOz(oz);
		return stati;

	}

	/**
	 * @param parser
	 * @return
	 * @throws XMLStreamException
	 */
	private Measurement parseMeasurement(XMLStreamReader parser)
			throws XMLStreamException {
		// <component>Ozone</component>
		// <datetime_from>2009-02-25 00:00</datetime_from>
		// <datetime_to>2009-02-25 01:00</datetime_to>
		// <averaged_time>60</averaged_time>
		// <value>15</value>
		// <quality_assurance>1</quality_assurance>
		// <quality_control>0</quality_control>

		ArrayList<String> measDet = new ArrayList<String>();
		String e = "";
		do {
			int event = parser.next();
			switch (event) {
			case XMLStreamConstants.END_ELEMENT:
				if (parser.getLocalName().equals("measurement")) {
					e = "rrr";
				}
				break;
			case XMLStreamConstants.CHARACTERS:
				// details of measurement station
				measDet.add(parser.getText());
				//System.out.println(parser.getText());
				break;
			} // Ende switch

		} while (e == "");// Ende while
		String timeBegin = measDet.get(1);
		String timeEnd = measDet.get(2);
		Measurement meas = new Measurement(measDet.get(0), timeBegin, timeEnd,
				Double.parseDouble(measDet.get(3)), Double.parseDouble(measDet
						.get(4)), measDet.get(5), measDet.get(6));
		return meas;
	}

	/**
	 * @param token
	 * @return
	 */
	public Date getDate(String token) {
		Date visited;
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm");
		ParsePosition pos;
		pos = new ParsePosition(0);
		visited = sdf.parse(token, pos);
		return visited;
	}
	
	/**
	 * 
	 */
	public void toConsole() {
		for (int i = 0; i<this.stations.getStats().size(); i++) {
			String s = this.stations.getStats().get(i).toString();
			System.out.println(s);
		}
	}

	/**
	 * @return
	 */
	public StationCollection getStats() {
		return stations;
	}

	/**
	 * @param stats
	 */
	public void setStats(StationCollection stats) {
		this.stations = stats;
	}



	/**
	 * @param args
	 * @throws XMLStreamException
	 * @throws IOException
	 */
	public static void main(String args[]) throws XMLStreamException, IOException {
		WoodstoxParser wp = new WoodstoxParser();
		if (args.length == 0) {
		wp.parse("C:/diplomarbeit/sos_testdata/{5E38E187-B5B4-4DF0-B0D6-00A479B0F2B6}.xml");
		} else {
			wp.parse(args[0]);
		}
		wp.toConsole();
	}
}
