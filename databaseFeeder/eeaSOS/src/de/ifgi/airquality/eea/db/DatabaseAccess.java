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

package de.ifgi.airquality.eea.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Feeder for the SosDatabase,
 * PostgreSQL in this case.
 * Only a prototype for testing purposes but not fully functional.
 * 
 * @author katharina
 */
public class DatabaseAccess {

	// DBMS and Database-specific connection parameters
	private static final String JDBC_DRIVER = "org.postgresql.Driver";
	// You may need to change these values
	private String url = "";
	private String username = "";
	private String pwd = "";
	private Connection dbConn = null;

	public DatabaseAccess(String url, String username, String pwd) {
		this.url = url;
		this.username = username;
		this.pwd = pwd;
	}

	public void connect() throws ClassNotFoundException {

		Class.forName(JDBC_DRIVER);

		// Create a connection to the database
		try {
			dbConn = DriverManager.getConnection(this.url, this.username, this.pwd);
			System.out.println("Connected to: " + this.url);
		} catch (SQLException e) {
			System.out.println("Unable to connect to database\n"
					+ e.getMessage());
			System.exit(1);
		}
	}
	
	/**
	 * @param ogc
	 * @param name
	 * @param unit
	 * @throws SQLException
	 */
	public void insertPhenomenon(String ogc, String name, String unit) throws SQLException {
		//INSERT INTO phenomenon VALUES ('urn:ogc:def:phenomenon:OGC:1.0.30:waterlevel', 'gauge height', 'cm','numericType');
		Statement stmt;	String sqlInsert; String sqlUpdate;  int rows;
		sqlInsert = "INSERT INTO phenomenon VALUES ('urn:ogc:def:phenomenon:OGC:1.0.30:"+ogc+"', '"+name+"', '"+unit+"','numericType');";
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		rows = stmt.executeUpdate(sqlInsert); 
	}
	
	/**
	 * @param name
	 * @param description
	 * @throws SQLException
	 */
	public void insertOffering(String name, String description) throws SQLException {
		Statement stmt;	String sqlInsert; String sqlUpdate; int rows;
		sqlInsert = "INSERT INTO offering VALUES ('"+name+"','"+description+"',null,null);";
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		rows = stmt.executeUpdate(sqlInsert); 
	}
	
	/**
	 * @param code
	 * @param name
	 * @param x
	 * @param y
	 * @throws SQLException
	 */
	public void insertFoi(String code, String name, double x, double y) throws SQLException {
		Statement stmt;	String sqlInsert; String sqlUpdate; String sqlQuery; int rows;
		sqlInsert = "INSERT INTO feature_of_interest (feature_of_interest_id, feature_of_interest_name, feature_of_interest_description, geom, feature_type, schema_link) VALUES ('"+code+"', 'EEA_"+code+"', '"+name+"', GeometryFromText('POINT("+x+" "+y+")', 4326),'sa:SamplingPoint', 'http://xyz.org/url"+code.hashCode()+".html');";
		sqlQuery = "SELECT * FROM feature_of_interest WHERE feature_of_interest_id='"+code+"'"; 
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		ResultSet set = stmt.executeQuery(sqlQuery);
		boolean b = set.first();
		if (!b) {
			rows = stmt.executeUpdate(sqlInsert);
		}
	}
	
	/**
	 * @param proc
	 * @throws SQLException
	 */
	public void insertProc(String proc) throws SQLException {
		Statement stmt;	String sqlInsert; String sqlUpdate; int rows;
		sqlInsert = "INSERT INTO procedure VALUES ('urn:ogc:object:feature:Sensor:EEA:eea-sensor-"+proc+"', 'standard/eea-sensor-"+proc+".xml', 'text/xml;subtype=\"SensorML\"');";
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		rows = stmt.executeUpdate(sqlInsert); 
	}
	
	/**
	 * @param phen
	 * @param off
	 * @throws SQLException
	 */
	public void relationPhenOff(String phen, String off) throws SQLException {
		Statement stmt;	String sqlInsert; String sqlUpdate; int rows;
		sqlInsert = "INSERT INTO phen_off VALUES ('urn:ogc:def:phenomenon:OGC:1.0.30:"+phen+"','"+off+"');";
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		rows = stmt.executeUpdate(sqlInsert); 
	}
	
	/**
	 * @param code
	 * @param off
	 * @throws SQLException
	 */
	public void relationFoiOff(String code, String off) throws SQLException {
		Statement stmt;	String sqlInsert; String sqlUpdate; int rows;
		sqlInsert = "INSERT INTO foi_off VALUES ('"+code+"','"+off+"');";
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		rows = stmt.executeUpdate(sqlInsert); 
	}
	
	/**
	 * @param proc
	 * @param phen
	 * @throws SQLException
	 */
	public void relationProcPhen(String proc, String phen) throws SQLException {
		Statement stmt;	String sqlInsert; String sqlUpdate; int rows;
		sqlInsert = "INSERT INTO proc_phen VALUES ('urn:ogc:object:feature:Sensor:EEA:eea-sensor-"+proc+"','urn:ogc:def:phenomenon:OGC:1.0.30:"+phen+"');";
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		rows = stmt.executeUpdate(sqlInsert); 
	}
	
	/**
	 * @param proc
	 * @param code
	 * @throws SQLException
	 */
	public void relationProcFoi(String proc, String code) throws SQLException {
		Statement stmt;	String sqlInsert; String sqlUpdate;  int rows;
		sqlInsert = "INSERT INTO proc_foi VALUES ('urn:ogc:object:feature:Sensor:EEA:eea-sensor-"+proc+"','"+code+"');";
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		rows = stmt.executeUpdate(sqlInsert); 
	}
	
	/**
	 * @param proc
	 * @param off
	 * @throws SQLException
	 */
	public void relationProcOff(String proc, String off) throws SQLException {
		Statement stmt;	String sqlInsert; String sqlQuery; int rows;
		sqlInsert = "INSERT INTO proc_off VALUES ('urn:ogc:object:feature:Sensor:EEA:eea-sensor-"+proc+"','"+off+"');";
		stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE); 
		rows = stmt.executeUpdate(sqlInsert); 
	}
	
	/**
	 * @param proc
	 * @param time
	 * @param code
	 * @param off
	 * @param phen
	 * @param value
	 */
	public void insertObservation(String proc, String time, String code, String off, String phen, double value) {
		Statement stmt;	String sqlInsert; String sqlUpdate; String sqlQuery;int rows;
		sqlInsert = "INSERT INTO observation (time_stamp, procedure_id, feature_of_interest_id,phenomenon_id,offering_id,numeric_value) values ('"+time+"', 'urn:ogc:object:feature:Sensor:EEA:eea-sensor-"+proc+"', '"+code+"','urn:ogc:def:phenomenon:OGC:1.0.30:"+phen+"','"+off+"','"+value+"');";
		sqlQuery = "SELECT * FROM observation WHERE time_stamp='"+time+"' AND feature_of_interest_id = '"+code+"' AND phenomenon_id = 'urn:ogc:def:phenomenon:OGC:1.0.30:"+phen+"';";
		sqlUpdate = "UPDATE observation SET numeric_value = "+value+" WHERE time_stamp='"+time+"' AND feature_of_interest_id = '"+code+"' AND phenomenon_id = 'urn:ogc:def:phenomenon:OGC:1.0.30:"+phen+"';";
		try {
			stmt = dbConn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_UPDATABLE);
			ResultSet set = stmt.executeQuery(sqlQuery);
			System.out.println("set.first() " + set.first());
			boolean b = set.first();
			if (b) {
				rows = stmt.executeUpdate(sqlUpdate);
			} else
			{
				rows = stmt.executeUpdate(sqlInsert);
			}
		} catch (SQLException e) {
			System.out.println("bombed");
		} 
	}

	/**
	 * @throws SQLException
	 */
	public void close() throws SQLException {
		this.dbConn.close();
	}

	/**
	 * @return
	 */
	public Connection getDbConn() {
		return dbConn;
	}

	/**
	 * @param dbConn
	 */
	public void setDbConn(Connection dbConn) {
		this.dbConn = dbConn;
	}

	/**
	 * Method connects to the database.
	 * 
	 * @throws ClassNotFoundException
	 * @throws SQLException 
	 */
	public static void main(String[] args) throws ClassNotFoundException, SQLException {
		DatabaseAccess db = new DatabaseAccess("", "", "");
		db.connect();
		db.close();
	} 

} 
