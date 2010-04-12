package de.ifgi.airquality.eea;

import java.sql.DriverManager;
import java.sql.Connection;
import java.sql.SQLException;
 
public class JDBCtest {
  public static void main(String[] argv) {
 
	  System.out.println("-------- PostgreSQL JDBC Connection Testing ------------");
 
	  try {
	    Class.forName("org.postgresql.Driver");
 
	  } catch (ClassNotFoundException e) {
	    System.out.println("Where is your PostgreSQL JDBC Driver? Include in your library path!");
	    e.printStackTrace();
	    return;
	  }
 
	  System.out.println("PostgreSQL JDBC Driver Registered!");
 
	  Connection connection = null;
 
	  try {
 
		 connection = DriverManager.getConnection("jdbc:postgresql://hare:5432/SosDatabase","postgres", "Anders1and");
 
	  } catch (SQLException e) {
	    System.out.println("Connection Failed! Check output console");
	    e.printStackTrace();
	    return;
	  }
 
	  if (connection != null)
		  System.out.println("You made it, take control your database now!");
	  else
	          System.out.println("Failed to make connection!");
	  }
}


