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
package de.ifgi.airquality.eea;

import java.io.File;
import java.io.FileFilter;

/**
 * Class represents a file filteer for the EEA xml files.
 * Only a prototype for testing purposes but not fully functional.
 * 
 * @author katharina
 *
 */
public class EeaFileFilter implements FileFilter {

	private String ende;
	private String begin;
	
	public EeaFileFilter (String endung, String anfang) {
		ende = endung;begin = anfang;
	}
	
	@Override
	public boolean accept(File dat) {
		if (dat.isFile() == true && dat.getName().endsWith(ende)) 
		return true;
		else 
			return false;
	}

}
