/***************************************************************
 This program is free software; you can redistribute and/or modify it under 
 the terms of the GNU General Public License version 2 as published by the 
 Free Software Foundation.

 This program is distributed WITHOUT ANY WARRANTY; even without the implied
 WARRANTY OF MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public License along with
 this program. If not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA or
 visit the Free Software Foundation web page, http://www.fsf.org.
***************************************************************/

package de.ifgi.airquality.eea;

import java.io.File;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

import javax.xml.stream.XMLStreamException;

import de.ifgi.airquality.eea.datamodel.Measurement;
import de.ifgi.airquality.eea.datamodel.Station;
import de.ifgi.airquality.eea.datamodel.StationCollection;
import de.ifgi.airquality.eea.db.DatabaseAccess;
import de.ifgi.airquality.eea.io.WoodstoxParser;

/**
 * Class to parse insert EEA xml files into a PostGIS database.
 * Only a prototype for testing purposes but not fully functional.
 * 
 * @author katharina
 *
 */
public class EeaDataTransfer {
	
	private DatabaseAccess dba = null;
	private EeaFileFilter eff = new EeaFileFilter("xml", "");
	private File[] transFiles;
	private String sourceDir;
	private ArrayList<String> parsedFiles = new ArrayList<String>();
	private String dburl;
	private String dbuser;
	private String dbpwd;
	
	/**
	 * Constructor
	 * 
	 * @param file
	 * @param dburl
	 * @param dbuser
	 * @param dbpwd
	 */
	public EeaDataTransfer(String file, String dburl, String dbuser, String dbpwd) {
		this.dba = new DatabaseAccess(dburl, dbuser, dbpwd);
		File dir = new File(file);
		this.transFiles = dir.listFiles(this.eff);
	}
	
	/**
	 * Method to parse xml file in EEA format 
	 * 
	 * @param file
	 * @return
	 * @throws XMLStreamException
	 * @throws IOException
	 */
	public StationCollection parseData(String file) throws XMLStreamException, IOException {
		WoodstoxParser wp = new WoodstoxParser();
		wp.parse(file);
		//wp.toConsole();
		StationCollection stats = wp.getStats();
		this.parsedFiles.add(wp.getParsedDatei());
		System.out.println("Successfully parsed: "+wp.getParsedDatei());
		return stats;		
	}
	
	/**
	 * Method to insert the features of interest into the database
	 * 
	 * @param stats
	 * @throws ClassNotFoundException
	 * @throws IOException
	 */
	public void initializeDatabase(ArrayList<Station> stats) throws ClassNotFoundException, IOException {
		dba.connect();
		try {
			//INSERT INTO phenomenon VALUES ('urn:ogc:def:phenomenon:OGC:1.0.30:pm10', 'pm10 concentration', 'mmm','numericType');
			dba.insertPhenomenon("pm10", "PM10 concentration", "µg/m^3");
			//INSERT INTO offering VALUES ('PM_10','pm10 concentration',null,null);
			dba.insertOffering("AIR", "air quality");
			//INSERT INTO phen_off VALUES ('urn:ogc:def:phenomenon:OGC:1.0.30:pm10','PM_10');
			dba.relationPhenOff("pm10", "AIR");
			dba.insertPhenomenon("no2", "NO2 concentration", "µg/m^3");
			dba.relationPhenOff("no2", "AIR");
			//Please check if all monitoring station types are listed!
			dba.insertProc("Industrial_rural");
			dba.relationProcOff("Industrial_rural", "AIR");
			dba.relationProcPhen("Industrial_rural", "pm10");
			dba.relationProcPhen("Industrial_rural", "no2");
			dba.insertProc("Traffic_urban");
			dba.relationProcOff("Traffic_urban", "AIR");
			dba.relationProcPhen("Traffic_urban", "pm10");
			dba.relationProcPhen("Traffic_urban", "no2");
			dba.insertProc("Background_rural");
			dba.relationProcOff("Background_rural", "AIR");
			dba.relationProcPhen("Background_rural", "pm10");
			dba.relationProcPhen("Background_rural", "no2");
			dba.insertProc("Background_suburban");
			dba.relationProcOff("Background_suburban", "AIR");
			dba.relationProcPhen("Background_suburban", "pm10");
			dba.relationProcPhen("Background_suburban", "no2");
			dba.insertProc("Background_urban");
			dba.relationProcOff("Background_urban", "AIR");
			dba.relationProcPhen("Background_urban", "pm10");
			dba.relationProcPhen("Background_urban", "no2");
			dba.insertProc("Industrial_suburban");
			dba.relationProcOff("Industrial_suburban", "AIR");
			dba.relationProcPhen("Industrial_suburban", "pm10");
			dba.relationProcPhen("Industrial_suburban", "no2");
			dba.insertProc("Traffic_suburban");
			dba.relationProcOff("Traffic_suburban", "AIR");
			dba.relationProcPhen("Traffic_suburban", "pm10");
			dba.relationProcPhen("Traffic_suburban", "no2");
			dba.insertProc("Industrial_urban");
			dba.relationProcOff("Industrial_urban", "AIR");
			dba.relationProcPhen("Industrial_urban", "pm10");
			dba.relationProcPhen("Industrial_urban", "no2");
			dba.insertProc("Traffic_rural");
			dba.relationProcOff("Traffic_rural", "AIR");
			dba.relationProcPhen("Traffic_rural", "pm10");
			dba.relationProcPhen("Traffic_rural", "no2");
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
		}
			for (int j = 0; j<stats.size();j++) {
			    Station st = stats.get(j);
			    
				try {
					//each monitoring station represents a feature of interest
					dba.insertFoi(st.getCode(), st.getName(), st.getLon(), st.getLat());
					dba.relationProcFoi(st.getType()+"_"+st.getArea(), st.getCode());
					dba.relationFoiOff(st.getCode(), "AIR");
				} catch (SQLException e) {
					// TODO Auto-generated catch block
				}
			}
		try {
			dba.getDbConn().commit();
			dba.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
		}
	}
	
	/**
	 * Method to insert the measurements into the database
	 * 
	 * @param stats
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 */
	public void insertObservations(StationCollection stats) throws ClassNotFoundException, SQLException {
		dba.connect();
		ArrayList<Station> statis = stats.getStats();
			for (int j = 0; j<statis.size();j++) {
			    Station st = statis.get(j);
			    ArrayList<Measurement>  meas = st.getObs().getMeas();
				for (int k = 0; k<meas.size();k++) {
					Measurement m = meas.get(k);
					String time = m.getTimeTo();
					String phen = "";
					String off = "";
					if (m.getComponent().equals("PM10")) {
						phen = "pm10";
						off = "AIR";
					}
//					if (m.getComponent().equals("Ozone")) {
//						phen = "ozone";
//						off = "AIR";
//					}
					if (m.getComponent().equals("NO2")) {
						phen = "no2";
						off = "AIR";
					}
					//INSERT INTO observation (time_stamp, procedure_id, feature_of_interest_id,phenomenon_id,offering_id,numeric_value) values ('"+time+"', 'urn:ogc:object:feature:Sensor:EEA:eea-sensor-"+code+"', '"+code+"','urn:ogc:def:phenomenon:OGC:1.0.30:"+phen+"','"+off+"','"+value+"');
					dba.insertObservation(st.getType()+"_"+st.getArea(), time, st.getCode(), off, phen, m.getValue());
					//}
				}
			}
		dba.getDbConn().commit();
		dba.close();		
	}
	
	/**
	 * Parse and initialize the database
	 * 
	 * @param file
	 * @throws XMLStreamException
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	public void parseAndInitialize(String file) throws XMLStreamException, IOException, ClassNotFoundException {
		ArrayList<Station> stats = this.parseData(file).getStats();
		this.initializeDatabase(stats);
	}
	
	/**
	 * Parse and insert the measurements 
	 * 
	 * @param file
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws XMLStreamException
	 * @throws IOException
	 */
	public void parseAndObservations(String file) throws ClassNotFoundException, SQLException, XMLStreamException, IOException {
		this.insertObservations(this.parseData(file));
	}
	
	/**
	 * Send RefreshMetadata request to SOS
	 * 
	 * @param urls
	 * @throws IOException
	 */
	public void refreshSOS(String urls) throws IOException {
		URL url = new URL(urls);
        HttpURLConnection urlCon = (HttpURLConnection) url.openConnection();
        urlCon.setRequestMethod("GET");
        urlCon.getInputStream();        
        System.out.println("SOS updated: " + urls + ", " + urlCon.getDate());
	}
	
	/**
	 * 
	 */
	private void delParsedFiles() {
		for (int i = 0; i<this.transFiles.length;i++) {
			this.transFiles[i].delete();
		}
	}
	
	/**
	 * 
	 * @param srcDir
	 * @param destDir
	 * @param count
	 */
	public void moveParsedFiles(String srcDir, String destDir, int count) {
		for (int j = 0; j<count;j++) {
			File oldFile = new File(srcDir+this.transFiles[j].getName());		
			String f = destDir+this.transFiles[j].getName();
			File n = new File(f);
			boolean success = oldFile.renameTo(new File (f));
			if (!success) {
				System.out.println("Fehler beim Verschieben von " + this.transFiles[j].getName());
			}
		}
	}
	
	/**
	 * Method to parse files from directory and insert observations into the database
	 * @param file
	 * @param count
	 */
	public void piFromDir(String file, int count) {
		
		if (count == 0) {
			count = this.transFiles.length;
		}

		Arrays.sort(this.transFiles, new Comparator()
		{
			public int compare(Object o1, Object o2) {
			
				if (((File)o1).lastModified() < ((File)o2).lastModified()) {
					return -1;
				} else if (((File)o1).lastModified() > ((File)o2).lastModified()) {
					return +1;
				} else {
					return 0;
				}
			}

		}); 
		
		
		for (int i = 0; i<count;i++) {
			File f = this.transFiles[i];
			try {
				this.parseAndInitialize(f.getAbsolutePath());
			} catch (XMLStreamException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (ClassNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	/**
	 * Parses EEA xml files from directory file. If count is 0 all EEA xml files will be parsed.
	 * po indicates that only observations will be inserted into the database.
	 * @param file directory
	 * @param count number of files to be parsed, 0 means all files in directory file will be parsed.
	 */
	public void poFromDir(String file, int count) {
		
		if (count == 0) {
			count = this.transFiles.length;
		}
		
		Arrays.sort(this.transFiles, new Comparator()
		{
			public int compare(Object o1, Object o2) {
			
				if (((File)o1).lastModified() < ((File)o2).lastModified()) {
					return -1;
				} else if (((File)o1).lastModified() > ((File)o2).lastModified()) {
					return +1;
				} else {
					return 0;
				}
			}

		}); 
		
		for (int i = 0; i<count;i++) {
			File f = this.transFiles[i];
			try {
				this.parseAndObservations(f.getAbsolutePath());
			} catch (XMLStreamException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (ClassNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	/**
	 * Parses EEA xml files from directory file. If count is 0 all EEA xml files will be parsed.
	 * pio indicates that monitoring stations and observations will be inserted into the database.
	 * @param file
	 * @param count
	 */
	public void pioFromDir(String file, int count) {
		
		if (count == 0) {
			count = this.transFiles.length;
		}
		
		Arrays.sort(this.transFiles, new Comparator()
		{
			public int compare(Object o1, Object o2) {
			
				if (((File)o1).lastModified() < ((File)o2).lastModified()) {
					return -1;
				} else if (((File)o1).lastModified() > ((File)o2).lastModified()) {
					return +1;
				} else {
					return 0;
				}
			}

		}); 
		
		for (int i = 0; i<count;i++) {
			File f = this.transFiles[i];
			try {
				this.parseAndInitialize(f.getAbsolutePath());
				this.parseAndObservations(f.getAbsolutePath());
			} catch (XMLStreamException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (ClassNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}		
	}
	
	/**
	 * Main class.
	 * @param args
	 * @throws SQLException
	 * @throws IOException
	 */
	public static void main (String[] args) throws SQLException, IOException {
		//empty EeaDataTransfer object
		EeaDataTransfer edt = null;
		if (args.length == 0) {				
			edt = new EeaDataTransfer("Y:/sos_testdata", "jdbc:postgresql://hare:5432/SosDatabase", "postgres", "Anders1and");
			System.out.println("Specify file name or directory");
			String d = "Y:/sos_testdata";
			System.out.println("Try to parse from default directory: " + d);
			edt.pioFromDir(d, 0);
		} else {
			edt = new EeaDataTransfer(args[0], args[1], args[2], args[3]);
			if (args[4].equals("pi")) {
					edt.piFromDir(args[1], Integer.parseInt(args[5]));
				}
				else if (args[4].equals("po")) {
					edt.poFromDir(args[1], Integer.parseInt(args[5]));
				}
				else if (args[4].equals("pio")) {
					edt.pioFromDir(args[1], Integer.parseInt(args[5]));
				}
			}
		edt.refreshSOS("http://hare:8080/52nSOSv3/sos?REQUEST=RefreshMetadata");

		//edt.refreshSOS(args[6]);
		System.out.println("Successfully parsed "+edt.transFiles.length+" EEA files.");
	}
	
}
